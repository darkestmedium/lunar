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

fiPlayerRig = qtc.QFileInfo(f"{fiPlayerRigs.filePath()}/RIG_Player.ma")


namespaceRig = None

ctrlRig = None
exportSkeleton = None
sceneMetaData = None

fiAnimFbx = None



# 1 Build New scene,
# 2 Import mocap
# 3 Export mocap

# 1 Open existing scene -> wrap files in scene, add a callback on new scene / open?
# 2 Import and or export

# init namespaces

# def ValidateNamespaces():
# 	global NamespaceRig

# 	if not NamespaceRig: NamespaceRig = scene.GetNamespaces()[0]


def wrapRetargeters():
	"""Wraps the scene objects into HiK python objects.
	"""
	global namespaceRig
	global ctrlRig
	global exportSkeleton
	global sceneMetaData

	if namespaceRig is None:
		namespaceRig = lm.LMScene.getNamespaces()[0]
		if not namespaceRig: namespaceRig=""

	if ctrlRig is None:	ctrlRig = lmrtg.LMLunarCtrl(f"{namespaceRig}:Ctrl")
	if exportSkeleton is None: exportSkeleton = lmrtg.LMLunarExport(f"{namespaceRig}:Export")
	if sceneMetaData is None: sceneMetaData = lm.LMMetaData()

	
def buildNewAnimationScene() -> bool:
	"""Builds a new animation scene with a clean player rig for working with mocap.

	"""
	global namespaceRig
	global sceneMetaData

	if lm.LMFile.new():
		lm.LMScene.setFramerate()
		namespaceRig = "Player"
		lm.LMFile.load(fiPlayerRig.filePath(), namespaceRig)
		# sceneMetaData = lm.MMetaData(text="untitled")
		wrapRetargeters()
		if not cmds.objExists(sceneMetaData.name): sceneMetaData = lm.LMMetaData()
		return True

	return False


def loadMocap(hikTemplate="MannequinUe5") -> bool:
	"""Import mocap to the control rig from an fbx file.
	"""
	global fiAnimFbx
	global sceneMetaData
	lm.LMScene.setFramerate()
	strFilePath = lm.LMFile.importDialog()

	if strFilePath != None:
		wrapRetargeters()
		stateAutoKey = oma.MAnimControl.autoKeyMode()
		if stateAutoKey: oma.MAnimControl.setAutoKeyMode(False)

		listSceneNamespaces = lm.LMScene.getNamespaces()

		fiAnimFbx = qtc.QFileInfo(strFilePath[0])

		lm.LMFbx.loadAnimation(fiAnimFbx.filePath())
		# Get the namespace from fbx
		# If there are no new namspaces this means that mocap matches the rig so we can import onto
		namespaceMocap = list(set(lm.LMScene.getNamespaces()).difference(listSceneNamespaces))

		# om.MGlobal.displayWarning(f"MOCAP NAMESPACE: {namespaceMocap}")
		if not cmds.objExists(sceneMetaData.name): sceneMetaData = lm.LMMetaData()
		sceneMetaData.setText(fiAnimFbx.baseName())
		# Temp override for array attributes
		cmds.setAttr(f"{sceneMetaData.shape}.metaData[1].text", fiAnimFbx.filePath(), type="string")
		cmds.setAttr(f"{sceneMetaData.shape}.metaData[0].displayInViewport", True)
	

		if hikTemplate == "HumanIk":
			mocapSkeleton = lmrtg.LMHumanIk(f"{namespaceMocap[0]}:Mocap")
			ctrlRig.setSourceAndBake(mocapSkeleton, rootMotion=False)

		elif hikTemplate == 'MannequinUe5':
			# if imported namesapce is the same as the ctrl rig bake from the skeleton since fbx will match replace the animation
			if not namespaceMocap:
				ctrlRig.setSourceAndBake(exportSkeleton, rootMotion=True)
				if stateAutoKey: oma.MAnimControl.setAutoKeyMode(True)
				return True
		
			# om.MGlobal.displayWarning(f"mocap has no namespace: {namespaceMocap}")
			mocapSkeleton = lmrtg.LMMannequinUe5(f"{namespaceMocap[0]}:Mocap")
			ctrlRig.setSourceAndBake(mocapSkeleton, rootMotion=True)

		# Clean up 
		om.MNamespace.removeNamespace(namespaceMocap[0], True)
		if stateAutoKey: oma.MAnimControl.setAutoKeyMode(True)
		mocapSkeleton.deleteCharacterDefinition()
		mocapSkeleton = None
		namespaceMocap = None

		return True
	
	cmds.warning("Operation was cancelled.")
	return False


def exportAnimation(exportAs=True, bake=True):
	"""Export animaiton to the engine.
	"""
	global fiAnimFbx
	global namespaceRig
	global ctrlRig
	global exportSkeleton
	global sceneMetaData

	# namespaceRig = lm.LMScene.getNamespaces()[0]
	wrapRetargeters()

	if exportAs:
		strFilePath = lm.LMFile.exportDialog(f"{fiAnimations.filePath()}/{sceneMetaData.getText()}")
		if strFilePath != None:
			fiAnimFbx = qtc.QFileInfo(strFilePath[0])

			# Source and bake to export skeleton
			if bake:
				exportSkeleton.setCtrlRigAsSourceAndBake(ctrlRig)

			exportSkeleton.exportAnimation(fiAnimFbx.filePath())
			return True

		cmds.warning("Operation was cancelled.")
		return False

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
	global namespaceRig

	wrapRetargeters()

	strFilePath = lm.LMFile.importDialog(fileFilter="JSON ( .json ) (*.json)")
	if strFilePath != None:
		lmr.MMetaHumanUtils.loadFaceCtrlAnimation(strFilePath[0])
		return True

	cmds.warning("Operation was cancelled.")
	return False



def bakeToAnother(ctrlsToSkeleton=True, skeletonToCtrls=False):
	"""Animation shelf wrapper for baking animation between the control rig and skeleton.
	"""
	global namespaceRig
	global ctrlRig
	global exportSkeleton

	if ctrlsToSkeleton and skeletonToCtrls:
		cmds.warning("Only one flag can be set to true at the same time - can't bake both at the same time.")
		return False
	
	wrapRetargeters()

	if ctrlsToSkeleton:
		exportSkeleton.setCtrlRigAsSourceAndBake(ctrlRig)
	
	if skeletonToCtrls:
		ctrlRig.setSourceAndBake(exportSkeleton, rootMotion=True)
	



# if __name__ == "__main__":
# 	"""For Development Only.

# 	Test code to accelerate reloading and testing the plugin.

# 	"""
# 	import importlib
# 	from maya import cmds

# 	import lunar.maya.LunarMaya as lm
# 	import lunar.maya.LunarMayaAnim as lma
# 	import lunar.maya.LunarMayaRig as lmr
# 	import lunar.maya.LunarMayaRetarget as lmrtg

# 	from lunar.maya.toolset import animation

# 	[importlib.reload(module) for module in [lm, lma, lmr, lmrtg]]

# 	animation.buildNewAnimationScene()

# 	animation.ImportMocap()

#		animation.ExportAnimation()
# 	animation.ExportAnimation(True)

# 	cmds.viewFit(all=True)
# 	cmds.modelEditor("modelPanel4", edit=True, jointXray=True)