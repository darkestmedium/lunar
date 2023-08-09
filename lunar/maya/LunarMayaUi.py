# Built-in imports
# import json
# import platform
# import subprocess
import logging
import functools
# from collections import OrderedDict

# Third-party imports
from maya import cmds
from maya import mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
from PySide2 import QtCore as qtc

# Custom imports
import lunar.maya.LunarMaya as lm
import lunar.maya.LunarMayaAnim as lma
from lunar.maya.toolset import animation

import lunar.maya.resources.retarget.lunarctrl as lmrrlc




def loadDependencies():
	"""Loads all dependencies (hik plugins and mel sources).
	"""
	mel.eval(f'source "melOverrides.mel"')
	mel.eval(f'source "dagMenuProcOverride.mel"')

	log = logging.getLogger('Lunar MayaUi')
	log.info("Successfully loaded all dependencies.")

if (om.MGlobal.mayaState() == om.MGlobal.kInteractive): loadDependencies()




class LMUi():
	"""Python wrapper / override for mel ui procedures.
	"""
	log = logging.getLogger("LMUi")

	rigComponents = {
		"head_grp": "headFkIk",
		"leg_l_grp": "leftLegFkIk",
		"arm_l_grp": "leftArmFkIk",
		"leg_r_grp": "rightLegFkIk",
		"arm_r_grp": "rightArmFkIk",
	}


	@classmethod
	def buildObjectMenuItemsNow(cls, parent:str):
		"""Python override for buildObjectMenuItemsNow from others/buildObjectMenuItemsNow.mel

		Method used to build the right click menus based on context.

		Args:
			parent (string): Name of the parent ui element ex. "MainPane|viewPanes|modelPanel4|modelPanel4|modelPanel4|modelPanel4ObjectPop"

		"""
		if mel.eval("exists DRUseModelingToolkitMM") and mel.eval(f'DRUseModelingToolkitMM("{parent}")'): 
			return

		mel.eval("global int $gIsMarkingMenuOn;")
		gIsMarkingMenuOn = int(mel.eval("$tempVar=$gIsMarkingMenuOn"))

		if cmds.popupMenu(parent, exists=True):
			cmds.popupMenu(parent, edit=True, deleteAllItems=True)
			if cmds.popupMenu(parent, query=True, markingMenu=True) != gIsMarkingMenuOn:
				cmds.popupMenu(parent, edit=True, markingMenu=gIsMarkingMenuOn)

			editMode = 0
			currentContext = cmds.currentCtx()
			if cmds.contextInfo(currentContext, exists=True):
				ctx = cmds.contextInfo(currentContext, c=True) 
				if ctx == "manipMove":
					editMode = cmds.manipMoveContext("Move", editPivotMode=True, query=True)
				elif ctx == "manipScale":
					editMode =  cmds.manipScaleContext("Scale", editPivotMode=True, query=True)
				elif ctx == "manipRotate":
					editMode =  cmds.manipRotateContext("Rotate", query=True)
				elif ctx == "sculptMeshCache":
					cmds.setParent(parent, menu=True)
					mel.eval("sculptMeshCacheOptionsPopup();")
					return
				elif ctx == "polyCutUV":
					cmds.setParent(parent, menu=True)
					mel.eval("polyCutUVOptionsPopup();")
					return
				elif mel.eval(f'contextXGenToolsMM("{parent}")'):
					return
				elif ctx == "bpDraw" and cmds.pluginInfo("bluePencil", query=True, loaded=True):
					cmds.setParent(parent, menu=True)
					mel.eval("bpDrawOptionsPopup();")
					return

			if editMode:
				cmds.setParent(parent, menu=True)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kPinComponentPivot")'),
					checkBox=cmds.manipPivot(query=True, pin=True),
					radialPosition="N",
					command=mel.eval("setTRSPinPivot #1"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kResetPivot")'),
					radialPosition="S",
					command=mel.eval("manipPivotReset true true"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kSnapPivotOrientation")'),
					checkBox=cmds.manipPivot(query=True, snapOri=True),
					radialPosition="NW",
					command=mel.eval("setTRSSnapPivotOri #1"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kSnapPivotPosition")'),
					checkBox=cmds.manipPivot(query=True, snapPos=True),
					radialPosition="NE",
					command=mel.eval("setTRSSnapPivotPos #1"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kResetPivotOrientation")'),
					radialPosition="SW",
					command=mel.eval("manipPivotReset false true"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kResetPivotPosition")'),
					radialPosition="SE",
					command=mel.eval("manipPivotReset true false"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kShowPivotOrientationHandle")'),
					checkBox=cmds.optionVar("manipShowPivotRotateHandle", query=True),
					radialPosition="W",
					command=mel.eval("setTRSPivotOriHandle #1"),
				)
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kExitPivotMode")'),
					radialPosition="E",
					command=mel.eval("ctxEditMode"),
				)
				# Lower non-gestural menu items
				cmds.menuItem(
					label=mel.eval('uiRes("m_buildObjectMenuItemsNow.kBakePivotOri")'),
					checkBox=cmds.manipPivot(quey=True, bakeOri=True),
					command=("setTRSBakePivotOri #1"),
				)
				cmds.setParent("..")
			else:
				if not cmds.dagObjectHit(menu=parent):
					# // Nothing was hit - check selection/hilight list.
					# // Include UFE objects, and ask for long names so we can properly check
					# // the type.
					leadObject = cmds.ls(selection=True, tail=1, typ="transform")
					if leadObject.__len__() == 0:
						leadObject = cmds.ls(hilite=True, tail=1, typ="transform")
					if leadObject.__len__() > 0:
						# // MAYA-67156: Something is selected/hilighted so pass
						# // an empty object to dagMenuProc to indicate nothing was
						# // under the cursor and let it decide what object(s) to use
						mel.eval(f'dagMenuProc("{parent}", "");')
					else:
						leadObject = cmds.ls(selection=True, ufe=True, long=True, tail=1, typ="transform", shapes=True)
						ufeRuntime = "Maya-DG"
						if leadObject.__len__() > 0:
							ufeRuntime = cmds.nodeType(leadObject[0], ufeRuntimeName=True)
						if "Maya-DG" != ufeRuntime:
							# // Empty string for the object name is an indication that the user did not
							# // click on an object, we looked at what was selected to decide what 
							# // script to call. Also including the ufe runtime name which the proc
							# // uses to look up a runtime-specific proc.
							mel.eval(f'ufeMenuProc("{parent}", "", "{ufeRuntime}")')
							return
						if mel.eval("modelingTookitActive()") and cmds.nexCtx(rmbComplete=True, query=True):
							cmds.ctxCompletion()
							return
						#If nothing is selected build jsut the radial menu
						cls.buildAnimationMM(parent, radialMM=True, dropdownMM=False)
		else:
			cls.log.warning(mel.eval('uiRes("m_buildObjectcmds.menuItem(sNow.kParentWarn")'))


# Animation Marking Menu
#--------------------------------------------------------------------------------------------------

	@classmethod
	def buildAnimationMM(cls, parent:str, object:str="", radialMM:bool=True, dropdownMM:bool=True):
		"""Python wrapper for building the lunar animation marking menus.
		"""
		cmds.setParent(parent, menu=True)
		if radialMM: cls.buildAnimationRadialMM(object)
		if dropdownMM: cls.buildAnimationPopupMM(object)


	@classmethod
	def buildAnimationRadialMM(cls, object:str=""):
		"""Builds the radial menu if nothing is selected and rmb is pressed.
		"""
		cmds.menuItem(
			label="Graph Editor",
			radialPosition="NW",
			command=functools.partial(cls.openGraphEditor, object),
		)
		cmds.menuItem(
			label="Studio Library",
			radialPosition="N",
			command=cls.openStudioLibrary,
		)
		cls.buildTimeEditordMM(object)

		cls.buildSceneBuildMM()
		# Bottom Three
		cls.buildImportAnimationMM()
		cls.buildExportAnimationMM()
		cls.buildBakeAnimationMM()


	@classmethod
	def buildTimeEditordMM(cls, object:str, *args):
		"""Builds the Build Scene menu item for the animation radial marking menu.
		"""
		cmds.menuItem(
			label="Time Editor",
			subMenu=True,
			radialPosition="NE",
			command=cmds.TimeEditorWindow,
		)
		cmds.menuItem(
			label="Create Clip",
			radialPosition="N",
			command=functools.partial(cls.addTimeEditorClip, object)
		)
		cmds.menuItem(
			label="Create Relocator",
			radialPosition="E",
			command=functools.partial(cls.addTimeEditorRelocator, object)
		)
		cmds.setParent("..", menu=True)


	@classmethod
	def buildSceneBuildMM(cls):
		"""Builds the Build Scene menu item for the animation radial marking menu.
		"""
		cmds.menuItem(
			label="Build Scene",
			subMenu=True,
			radialPosition="W",
			command=animation.buildNewAnimationScene,
		)
		cmds.menuItem(
			label="Build new Scene",
			radialPosition="NW",
			command=animation.buildNewAnimationScene,
		)
		cmds.menuItem(
			label="Add Character",
			radialPosition="SW",
			command=animation.loadCharacter,
		)
		cmds.setParent("..", menu=True)


	@classmethod
	def buildImportAnimationMM(cls):
		"""Builds the Import Animation menu item for the animation radial marking menu.
		"""
		cmds.menuItem(
			label="Import Animation",
			subMenu=True,
			radialPosition="SW",
			command=animation.loadMocap,
		)
		cmds.menuItem(
			label="Import MannequinUe5",
			radialPosition="NW",
			command=animation.loadMocap,
		)
		cmds.menuItem(
			label="Import MannequinUe4",
			radialPosition="W",
			command=functools.partial(animation.loadMocap, hikTemplate="MannequinUe4"),
		)
		cmds.menuItem(
			label="Import HumanIk",
			radialPosition="SW",
			command=functools.partial(animation.loadMocap, hikTemplate="HumanIk"),
		)
		cmds.menuItem(
			label="Import SinnersDev2",
			radialPosition="S",
			command=functools.partial(animation.loadMocap, hikTemplate="SinnersDev2"),
		)
		cmds.menuItem(
			label="Import SinnersDev1",
			radialPosition="SE",
			command=functools.partial(animation.loadMocap, hikTemplate="SinnersDev1"),
		)
		cmds.setParent("..", menu=True)


	@classmethod
	def buildExportAnimationMM(cls):
		"""Builds the Export Animation menu item for the animation radial marking menu.
		"""
		cmds.menuItem(
			label="Export Animation",
			subMenu=True,
			radialPosition="SE",
			command=animation.exportAnimation,
		)
		cmds.menuItem(
			label="Export Ctrls",
			radialPosition="E",
			command=functools.partial(animation.exportAnimation, bake=True),
		)
		cmds.menuItem(
			label="Export Skeleton",
			radialPosition="S",
			command=functools.partial(animation.exportAnimation, bake=False),
		)
		cmds.setParent("..", menu=True)


	@classmethod
	def buildBakeAnimationMM(cls):
		"""Builds the Bake Animation menu item for the animation radial marking menu.
		"""
		cmds.menuItem(
			label="Bake Animation",
			subMenu=True,
			radialPosition="E",
			command=animation.bakeToAnother,
		)
		cmds.menuItem(
			label="Bake Ctrls to Skeleton",
			radialPosition="NE",
			command=animation.bakeToAnother,
		)
		cmds.menuItem(
			label="Bake Skeleton to Ctrls",
			radialPosition="SE",
			command=functools.partial(animation.bakeToAnother, ctrlsToSkeleton=False, skeletonToCtrls=True),
		)
		cmds.setParent("..", menu=True)


	@classmethod
	def buildAnimationPopupMM(cls, object:str="", *args):
		"""Builds the menu for the lunar rig controller.
		"""
		cls.builAnimationSwitchToMM(object)

		cmds.menuItem(divider=True)

		cmds.menuItem(
			label="Select Main Ctrl",
			command=functools.partial(cls.selectMainCtrl, object),
		)
		cmds.menuItem(
			label="Select Component Ctrls",
			command=functools.partial(cls.selectComponentCtrls, object),
		)
		cmds.menuItem(
			label="Select All Ctrls",
			command=functools.partial(cls.selectAllCtrls, object),
		)
		cmds.menuItem(divider=True)
		cmds.menuItem(
			label="Reset Ctrl",
			command=functools.partial(cls.resetCtrl, object),
		)
		cmds.menuItem(
			label="Reset Component Ctrls",
			command=functools.partial(cls.resetComponentCtrls, object),
		)
		cmds.menuItem(
			label="Reset All Ctrls",
			command=functools.partial(cls.resetAllCtrls, object)
		)
		cmds.menuItem(divider=True)

		cls.builAnimationDisplayMM(object)

		cmds.setParent("..", menu=True)


	@classmethod
	def builAnimationSwitchToMM(cls, object:str):
		"""Builds the Animaation Display menu item for the animation popup marking menu.
		"""
		cmds.menuItem(
			label="Switch To",
			subMenu=True,
			# command=functools.partial(cls.selectMainCtrl, object),
		)
		cmds.menuItem(
			label="Fk",
			command=functools.partial(cls.switchComponentMode, object=object, mode="Fk"),
		)
		cmds.menuItem(
			label="Ik",
			command=functools.partial(cls.switchComponentMode, object=object, mode="Ik"),
		)
		cmds.setParent("..", menu=True)
		

	@classmethod
	def builAnimationDisplayMM(cls, object:str):
		"""Builds the Animaation Display menu item for the animation popup marking menu.
		"""
		cmds.menuItem(
			label="Display",
			subMenu=True,
			# command=print("Selecting all rig ctrls."),
		)
		cmds.menuItem(
			label="Toggle Bones Visibility",
			command=functools.partial(cls.toggleBonesVisbility, object),
		)
		cmds.menuItem(
			label="Toggle X-Ray Bones",
			command=LMViewport.toggleXrayJoints,
		)
		cmds.menuItem(
			label="Toggle Ctrls Visibility",
			command=functools.partial(cls.toggleCtrlsVisbility, object),
		)
		cmds.setParent("..", menu=True)


	# Temp methods - will prolly move to rig module?
	@classmethod
	def addTimeEditorClip(cls, object:str, *args):
		# namespace = lm.LMNamespace.getNamespaceFromName(object)
		try:
			name = cmds.getAttr("sceneMetaDataShape.metaData[0].text")
		except NameError:
			name = "anim_clip"
		listCtrls = cls.getAllCtrls(object)
		lma.LMTimeEditor.createClip(listCtrls, name, lma.LMAnimControl.currentTime().value())

	@classmethod
	def addTimeEditorRelocator(cls, object:str, *args):
		"""Adds a relocator to the selected clip in the Time Editor.
		"""
		listTeClipIds = cmds.timeEditor(selectedClips="")
		if listTeClipIds:
			namespace = lm.LMNamespace.getNamespaceFromName(object)
			teClipId = listTeClipIds[0]
			teClipPath = cmds.timeEditorClip(teClipId, query=True, clipPath=True)
			teClipName = cmds.timeEditorClip(teClipId, query=True, clipNode=True)
			teRelocator = cmds.listConnections(f"{teClipName}.offset.offsetMtx", source=True)
			if not teRelocator:
				cmds.timeEditorClipOffset(path=teClipPath, clipId=teClipId, offsetTransform=True, rootObj=f"{namespace}:root_ctrl")
				teClipName = cmds.timeEditorClip(teClipId, query=True, clipNode=True)
				teRelocator = cmds.listConnections(f"{teClipName}.offset.offsetMtx", source=True)[0]
				cmds.connectAttr(f"{teRelocator}.worldMatrix", f"{teClipName}.offset.offsetMtx", force=True)
				# lm.LMAttribute.copyTransformsToOPM(teRelocator)
				lm.LMAttribute.lockControlChannels(teRelocator, lm.listAttrSC)
				return teRelocator
			else:
				cls.log.warning(f"'{teClipPath}' clip alreay has relocator/s: {teRelocator}.")

		cls.log.warning("No clips selected in the Time Editor.")

	@classmethod
	def switchComponentMode(cls, *args, object:str, mode:str):
		namespace = lm.LMNamespace.getNamespaceFromName(object)
		componentNs = cmds.listConnections(f"{object}.component", destination=True)[0]
		component = lm.LMNamespace.removeNamespaceFromName(componentNs)
		
		ctrlSwitch = f"{namespace}:fkik_ctrl"
		if component in cls.rigComponents:
			attrFkIk = cls.rigComponents[component]
			if mode == "Fk": cmds.setAttr(f"{ctrlSwitch}.{attrFkIk}", 0)
			if mode == "Ik": cmds.setAttr(f"{ctrlSwitch}.{attrFkIk}", 100)

	@classmethod
	def getAllCtrls(cls, object:str, *args) -> list:
		"""Selects all the rig ctrls.
		"""
		namespace = lm.LMNamespace.getNamespaceFromName(object)
		ctrlMain = f"{namespace}:main_ctrl"
		listTransforms = cmds.listRelatives(ctrlMain, typ="transform", allDescendents=True)
		listCtrls = []
		listCtrls.append(ctrlMain)
		[listCtrls.append(ctrl) for ctrl in listTransforms if ctrl.endswith("_ctrl")]
		return listCtrls

	@classmethod
	def getComponentCtrls(cls, object:str, *args) -> list:
		"""Selects all the rig ctrls.
		"""
		listComponentCtrls = []
		if cmds.attributeQuery("component", node=object, exists=True, message=True):
			component = cmds.listConnections(f"{object}.component", destination=True)[0]
			listComponentCtrls = cmds.listConnections(f"{component}.ctrl", source=True)
		else:
			listComponentCtrls.append(object)
		
		return listComponentCtrls

	@classmethod
	def selectMainCtrl(cls, object:str, *args):
		namespace = lm.LMNamespace.getNamespaceFromName(object)
		lm.LMGlobal.selectByName(f"{namespace}:main_ctrl", lm.LMGlobal.kReplaceList)

	@classmethod
	def selectComponentCtrls(cls, object:str, *args):
		"""Selects all the components ctrls.
		"""
		# listComponentCtrls = []
		# if cmds.attributeQuery("component", node=object, exists=True, message=True):
		# 	component = cmds.listConnections(f"{object}.component", destination=True)[0]
		# 	listComponentCtrls = cmds.listConnections(f"{component}.ctrl", source=True)
		# else:
		# 	listComponentCtrls.append(object)
		cmds.select(cls.getComponentCtrls(object), replace=True)

	@classmethod
	def selectAllCtrls(cls, object:str, *args):
		"""Selects all the rig ctrls.
		"""
		cmds.select(cls.getAllCtrls(object), replace=True)

	@classmethod
	def resetCtrl(cls, object:str, *args):
		"""Resets all rig ctrls by setting the apose from retargeting setup.
		"""
		[cmds.setAttr(f"{object}.{attr}", 0) for attr in lm.listAttrTRXYZ if cmds.getAttr(f"{object}.{attr}", keyable=True)]

	@classmethod
	def resetComponentCtrls(cls, object:str, *args):
		"""Resets all rig ctrls by setting the apose from retargeting setup.
		"""
		for ctrl in cls.getComponentCtrls(object):
			for attr in lm.listAttrTRXYZ:
				attr = f"{ctrl}.{attr}"
				if cmds.getAttr(attr, keyable=True): cmds.setAttr(attr, 0)

	@classmethod
	def resetAllCtrls(cls, object:str, *args):
		"""Resets all rig ctrls by setting the apose from retargeting setup.
		"""
		# namespace = lm.LMNamespace.getNamespaceFromName(object)
		pose = lmrrlc.templateLC["aPose"]
		for node in pose:
			ctrl = lm.LMNamespace.getNameWithNamespace(node, lm.LMNamespace.getNamespaceFromName(object))
			if not cmds.objExists(ctrl): continue
			for attr in pose[node]:
				attrNs = f"{ctrl}.{attr}"
				if cmds.getAttr(attrNs, settable=True):	cmds.setAttr(attrNs, pose[node][attr])

	@classmethod
	def toggleCtrlsVisbility(cls, object:str, *args):
		namespace = lm.LMNamespace.getNamespaceFromName(object)
		attrVisibility = f"{namespace}:main_ctrl.ctrlsVisibility"
		isCtrlVisible = cmds.getAttr(attrVisibility)
		cmds.setAttr(attrVisibility, not isCtrlVisible)

	@classmethod
	def toggleBonesVisbility(cls, object:str, *args):
		namespace = lm.LMNamespace.getNamespaceFromName(object)
		attrVisibility = f"{namespace}:main_ctrl.exportSkeletonVisibility"
		isCtrlVisible = cmds.getAttr(attrVisibility)
		cmds.setAttr(attrVisibility, not isCtrlVisible)

	@classmethod
	def openGraphEditor(cls, object:str="", *args):
		"""Wrapper for opening the GraphEditor with selection of the object returned from dagObjectHit
		"""
		if object: lm.LMGlobal.selectByName(object, lm.LMGlobal.kReplaceList)
		cmds.GraphEditor()

	@classmethod
	def openStudioLibrary(cls, *args):
		"""Wrapper method for opening the studio library windows.
		"""
		try:
			import studiolibrary
			studiolibrary.main()
		# except:
			# return
		except ImportError():
			cls.log.critical("Failed to import studiolibrary.")
			return
		# studiolibrary.main()




class LMViewport():
	"""Class wrapper for the 3d viewport.
	"""
	log = logging.getLogger("LMViewport")


	@classmethod
	def getActiveViewport(cls) -> str or None:
		"""Gets the active 3d viewport.
		"""
		currentModelPanel = None
		for modelPanel in cmds.getPanel(type="modelPanel"):
			if cmds.modelEditor(modelPanel, query=True, activeView=True):
				currentModelPanel = modelPanel
				break
		if currentModelPanel: return currentModelPanel
		return False


	@classmethod
	def toggleXrayJoints(cls, *args) -> bool:
		"""Toggles the xray joints state.
		"""
		activeViewport = cls.getActiveViewport()
		if activeViewport:
			statusXrayJoints = cmds.modelEditor(activeViewport, query=True, jointXray=True)
			cmds.modelEditor(activeViewport, edit=True, jointXray=not statusXrayJoints)
			return True
		cls.log.warning("Select a 3d viewport!")
		return False
	