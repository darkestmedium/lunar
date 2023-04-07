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
# NamespaceMocap = None

ctrlRig = None
exportSkeleton = None

fiAnimFbx = None

sceneMetaData = None


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

	if not namespaceRig:
		namespaceRig = lm.LMScene.getNamespaces()
		if not namespaceRig: namespaceRig=""

	if not ctrlRig:	ctrlRig = lmrtg.LMLunarCtrl(f"{namespaceRig}:Ctrl")
	if not exportSkeleton: exportSkeleton = lmrtg.LMLunarExport(f"{namespaceRig}:Export")
	if not sceneMetaData: sceneMetaData = lm.LMMetaData()

	
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


def loadMocap() -> bool:
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
		
		lm.LMFile.load(fiAnimFbx.filePath())  # Import mocap source skeletonß
		# Import fbx animation
		takes = lm.LMFbx.gatherTakes(fiAnimFbx.filePath())
		take = list(takes.keys())[0]
		lm.LMFbx.importAnimation(
			fiAnimFbx.filePath(),
			takes[take]['startFrame'], takes[take]['endFrame'], takes[take]['index']
		)
		# Get the namespace from fbx
		namespaceMocap = list(set(lm.LMScene.getNamespaces()).difference(listSceneNamespaces))
		# If there are no new namspaces this means that mocap matches the rig so we can import onto 

		if not cmds.objExists(sceneMetaData.name): sceneMetaData = lm.LMMetaData()
		sceneMetaData.setText(fiAnimFbx.fileName())
	
		# the export skeleton 
		if not namespaceMocap:
			ctrlRig.setSourceAndBake(exportSkeleton)
			if stateAutoKey: oma.MAnimControl.setAutoKeyMode(True)
			return True

		mocapSkeleton = lmrtg.LMMannequinUe5(f"{namespaceMocap[0]}:Mocap")
		ctrlRig.setSourceAndBake(mocapSkeleton)

		# Clean up namespaces
		om.MNamespace.removeNamespace(namespaceMocap[0], True)
		if stateAutoKey: oma.MAnimControl.setAutoKeyMode(True)

		return True
	
	cmds.warning("Operation was cancelled.")
	return False


def exportAnimation(exportAs=False):
	"""Export animaiton to the engine.
	"""
	# global fiAnimFbx
	global sceneMetaData
	# wrapRetargeters()

	if exportAs:
		strFilePath = lm.LMFile.exportDialog(f"{fiAnimations.filePath()}/{sceneMetaData.getText()}")
		if strFilePath != None:
			FiAnimFbx = qtc.QFileInfo(strFilePath[0])
			# Source and bake to export skeleton
			exportSkeleton.setSourceAndBake(ctrlRig)
			exportSkeleton.exportAnimation(FiAnimFbx.filePath())
			return True

		cmds.warning("Operation was cancelled.")
		return False

	# Source and bake to export skeleton
	# exportSkeleton.setSourceAndBake(ctrlRig)
	# # exportSkeleton.exportAnimation(f"{fiAnimations.filePath()}/{fiAnimFbx.fileName()}")

	# return True


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

	strFilePath = lm.MFile.importDialog(fileFilter="JSON ( .json ) (*.json)")
	if strFilePath != None:
		lmr.MMetaHumanUtils.loadFaceCtrlAnimation(strFilePath[0])
		return True

	cmds.warning("Operation was cancelled.")
	return False




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