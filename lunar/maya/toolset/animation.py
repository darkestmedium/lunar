"""Module for handling the animation shelf.

Project folder hierarchy:
Home														( FiHome )
|---Bambaa											( FiBambaa )
	|---Content										( FiContent )
		|---Sinners									( FiSinners )
			|---Characters						( FiCharacters )
				|---Player
					|
					|---Animations
					|		|---Cover
					|		|---Crouch
					|		|---Melee
					|		|---Pickups
					|		|---Scout
					|		|---Traversal
					|
					|---AnimationKit
					|		|---Rigs
					|		|---Skeletons
					|
					|---Meshes
					|---Physics

"""

# Built-in imports

# Third-party imports
from maya import cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
from PySide2 import QtCore as qtc

# Custom imports
import lunar.maya.LunarMaya as lm
import lunar.maya.LunarMayaAnim as lma
import lunar.maya.LunarMayaRig as lmr
import lunar.maya.LunarMayaRetarget as lmrtg




# Paths Init
# Validate paths function
# Init locations - ensure path compability through qt's QFileInfo class
fiHome = qtc.QFileInfo(qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.HomeLocation))
fiBambaa = qtc.QFileInfo(f"{fiHome.filePath()}/Bambaa")
fiContent = qtc.QFileInfo(f"{fiBambaa.filePath()}/Content")
fiProject = qtc.QFileInfo(f"{fiContent.filePath()}/Sinners")
fiCharacters = qtc.QFileInfo(f"{fiProject.filePath()}/Characters")
fiPlayer = qtc.QFileInfo(f"{fiCharacters.filePath()}/Player")
fiPlayerAnimationKit = qtc.QFileInfo(f"{fiPlayer.filePath()}/AnimationKit")
fiPlayerRigs = qtc.QFileInfo(f"{fiPlayerAnimationKit.filePath()}/Rigs")
fiAnimations = qtc.QFileInfo(f"{fiPlayer.filePath()}/Animations")

fiMannyRig = qtc.QFileInfo(f"{fiPlayerRigs.filePath()}/RIG_Player.ma")


sceneMetaData = None




def wrapRetargeters(namespace) -> tuple[lmrtg.LMLunarCtrl, lmrtg.LMRetargeter]:
	"""Wraps the scene objects into HiK python objects.
	"""
	global sceneMetaData

	rtgLunarCtrl = lmrtg.LMLunarCtrl(f"{namespace}:Ctrl")
	rtgLunarExport = lmrtg.LMLunarExport(f"{namespace}:Export")

	if sceneMetaData is None: sceneMetaData = lm.LMMetaData()

	return rtgLunarCtrl, rtgLunarExport



def buildNewAnimationScene(*args) -> bool:
	"""Builds a new animation scene with a clean player rig for working with mocap.
	"""
	global sceneMetaData

	if lm.LMFile.new():
		lm.LMScene.setFramerate()
		namespace = "Player"
		lm.LMFile.load(fiMannyRig.filePath(), namespace)

		sceneMetaData = lm.LMMetaData()

		cmds.select(f"{namespace}:main_ctrl")

		return True
	return False



def selectCharacter():
	nodes = cmds.ls(selection=True)
	if nodes:
		# Check if selection has a namespace
		namespace = lm.LMNamespace.getNamespaceFromName(nodes[0])
		if namespace:
			# Yes -> check for root_node
			if lm.LMSceneObject.sceneObjectType(f"{namespace}:rig"):
				# print("is rig")
				return
			# No -> return
	else:
		# print("nothing is selected")
		# check for reference nodes
		# listReferenceNodes = cmds.ls(type="reference")
		listReferencs = []
		lm.LMFile.getReferences(listReferencs)
		if listReferencs:
			# get nodes from ref
			for reference in listReferencs:
				listReferenceNodes = []
				lm.LMFile.getReferenceNodes(reference, listReferenceNodes)
				namespace = lm.LMNamespace.getNamespaceFromName(listReferenceNodes[0])
				if namespace:
					if lm.LMSceneObject.sceneObjectType(f"{namespace}:rig"):
						cmds.select(f"{namespace}:main_ctrl")
						return
					continue

			lm.LMGlobal.displayWarning("No referenced characters found in the scene, nothing to select.")
			return



def loadCharacter(*args, characterTemplate="Manny"):
	"""Loads a character rig into the scene with the specified template and namespace.
	"""
	namespace = lm.LMFile.characterDialog()
	if not namespace: return None

	if characterTemplate == "Manny":
		lm.LMFile.reference(fiMannyRig.filePath(), namespace)
		cmds.select(f"{namespace}:main_ctrl")



def loadMocap(*args, hikTemplate="MannequinUe5") -> bool or None:
	"""Import mocap to the control rig from an fbx file.
	"""
	global fiAnimFbx
	global sceneMetaData

	selectCharacter()

	# Check if selection is valid
	namespaceRig = lm.LMNamespace.getNamespaceFromSelection()
	if not namespaceRig: return None

	strFilePath = lm.LMFile.importDialog()
	if strFilePath != None:
		listTimeRanges = []
		namespaceMocap = "Mocap"
		fiAnimFbx = qtc.QFileInfo(strFilePath[0])
		lm.LMScene.setFramerate()

		stateAutoKeyMode = lma.LMAnimControl.autoKeyMode()
		if stateAutoKeyMode: lma.LMAnimControl.setAutoKeyMode(False)

		rtgLunarCtrl, rtgLunarExport = wrapRetargeters(namespaceRig)

		# Anim load / mocap reference
		# Get the current working time range - check if a time range is selected first
		offsetAnim = False
		# timeAnimationStartEnd = lma.LMAnimControl.animationStartEndTime()
		timeSelectedStartEnd = lma.LMAnimControl.selectedStartEndTime()
		if timeSelectedStartEnd:
			useTimeSelected = True
			offsetAnim = True
			timeCurrent = timeSelectedStartEnd[0]
		else:
			useTimeSelected = False
			timeSelectedStartEnd = lma.LMAnimControl.minMaxStartEndTime()
			timeCurrent = lma.LMAnimControl.currentTime()
			# This is incorrect
			if timeCurrent != timeSelectedStartEnd[0]: 
				offsetAnim = True

		referenceNode = lm.LMFile.reference(fiAnimFbx.filePath(), namespaceMocap)
		isAnimReferenced = True
		listReferenceJoints = lm.LMFile.getReferenceNodesByType(fiAnimFbx.filePath(), "joint")
		listReferenceAnimCurves = lm.LMFile.getReferenceNodesByType(fiAnimFbx.filePath(), "animCurveTA")
		namespaceMocap = om.MNamespace.getNamespaceFromName(listReferenceJoints[0]) # Get the mocap namespace from ref + file

		# Get time of mocap after import - replace with a more reliable function later
		# timeMocapStartEnd = lma.LMAnimControl.startEndTimeFromAnimCurves(listReferenceAnimCurves)
		timeMocapStartEnd = lma.LMAnimControl.minMaxStartEndTime()
		# Time for baking with eventual offset
		timeBakeStartEnd = tuple([time for time in timeMocapStartEnd])
		if timeCurrent != timeMocapStartEnd[0]: offsetAnim = True
		if offsetAnim:
			lm.LMFile.importReference(fiAnimFbx.filePath()) # import the file in order to be able to modify keyframes
			isAnimReferenced = False
			timeOffset = timeCurrent - timeMocapStartEnd[0]
			if useTimeSelected:
				timeBakeStartEnd = tuple([time for time in timeSelectedStartEnd]) # should match selection end
			else:
				listTimeBakeStartEnd = [timeMocapStartEnd[0] + timeOffset, timeMocapStartEnd[1] + timeOffset + 1]
				timeBakeStartEnd = tuple([time for time in listTimeBakeStartEnd])

			lma.LMAnimControl.offsetKeyframes(listReferenceJoints, timeBakeStartEnd[0].value())

		# lma.LMAnimControl.setStartEndTime(timeMocapStartEnd[0], timeMocapStartEnd[1])

		# Metadata node
		if not cmds.objExists(sceneMetaData.name): sceneMetaData = lm.LMMetaData()
		sceneMetaData.setText(fiAnimFbx.baseName())
		# Temp override for array attributes
		cmds.setAttr(f"{sceneMetaData.node}.metaData[1].text", fiAnimFbx.filePath(), type="string")
		cmds.setAttr(f"{sceneMetaData.node}.metaData[0].displayInViewport", True)

		rtgMocap = lmrtg.LMRetargeter.getFromHikTemplate(f"{namespaceMocap}:Skeleton", hikTemplate)

		rtgLunarCtrl.setSourceAndBake(rtgMocap, timeBakeStartEnd[0].value(), timeBakeStartEnd[1].value())

		# Clean-up
		if stateAutoKeyMode: lma.LMAnimControl.setAutoKeyMode(True)
		rtgMocap.deleteCharacterDefinition()
		if isAnimReferenced:
			lm.LMFile.removeReference(fiAnimFbx.filePath())
		else: 
			om.MNamespace.removeNamespace(namespaceMocap, True)
		# double check for "Mocap" namespace if not all files in referenced file are under a namsepace
		# TODO add referenced file under a group from the file cmds
		if om.MNamespace.namespaceExists("Mocap"): om.MNamespace.removeNamespace("Mocap", True)

		rtgMocap = None
		namespaceMocap = None
		referenceNode = None
		return True

	cmds.warning("Operation was cancelled.")
	return False



def exportAnimation(*args, exportAs=True, bake=True):
	"""Export animaiton to the engine.
	"""
	global fiAnimFbx
	global sceneMetaData

	selectCharacter()

	# Check if selection is valid
	namespaceRig = lm.LMNamespace.getNamespaceFromSelection()
	if not namespaceRig: return None

	if exportAs:
		strFilePath = lm.LMFile.exportDialog(f"{fiAnimations.filePath()}/{sceneMetaData.getText()}")
		if strFilePath != None:
			fiAnimFbx = qtc.QFileInfo(strFilePath[0])

			rtgLunarCtrl, rtgLunarExport = wrapRetargeters(namespaceRig)

			# Source and bake to export skeleton
			if bake:
				rtgLunarExport.setCtrlRigAsSourceAndBake(rtgLunarCtrl)

			rtgLunarExport.exportAnimation(fiAnimFbx.filePath())
			return True

		om.MGlobal.displayWarning("Export operation was cancelled.")
		return False

	namespaceRig = None
	return True



def createTimeEditorClip():
	global fiAnimFbx

	# WrapRetargeters()
	if not cmds.ls(selection=True):
		om.MGlobal.displayWarning("Nothing selected, select the main_ctrl!")
		return False

	if not fiAnimFbx:	clipName = "animation"
	else:	clipName = fiAnimFbx.fileName()

	lma.LMTimeEditor.createClip(clipName)
	cmds.TimeEditorWindow()
	return True



def importMhFaceCtrlAnimatino():
	"""Imports the metahuman face animation onto the ctrls from a json file."""
	return
	global namespaceRig

	wrapRetargeters()

	strFilePath = lm.LMFile.importDialog(fileFilter="JSON ( .json ) (*.json)")
	if strFilePath != None:
		lmr.MMetaHumanUtils.loadFaceCtrlAnimation(strFilePath[0])
		return True

	cmds.warning("Operation was cancelled.")
	return False



def bakeToAnother(*args, ctrlsToSkeleton=True, skeletonToCtrls=False):
	"""Animation shelf wrapper for baking animation between the control rig and skeleton.
	"""
	if ctrlsToSkeleton and skeletonToCtrls:
		om.MGlobal.displayWarning("Only one flag can be set to true at the same time - can't bake both at the same time.")
		return False

	namespaceRig = lm.LMNamespace.getNamespaceFromSelection()
	if not namespaceRig: return None
	rtgLunarCtrl, rtgLunarExport = wrapRetargeters(namespaceRig)

	if ctrlsToSkeleton:
		rtgLunarExport.setCtrlRigAsSourceAndBake(rtgLunarCtrl)
	
	if skeletonToCtrls:
		rtgLunarCtrl.setSourceAndBake(rtgLunarExport, rootMotion=True)
	
	namespaceRig = None
	