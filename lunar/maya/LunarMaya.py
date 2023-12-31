"""
Do's:
	Selection:
	lm.LMGlobal.selectByName is on average faster than cmds.select by 0.001s (0.00155s vs 0.00145s)

"""


# Built-in imports
import json
import platform
import subprocess
import logging
from collections import OrderedDict

# Third-party imports
from maya import cmds
from maya import mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
from PySide2 import QtCore as qtc

# Custom imports
from lunar.abstract.fbx import AbstractFbx
# Api overrides
import lunar.maya.LunarMayaAnim as lma
import lunar.maya.LunarMayaRig as lmr




#---------------------------------------------------------------------------------------
# DEFINITIONS
#---------------------------------------------------------------------------------------

listAttrT = ["translate"]
listAttrR = ["rotate"]
listAttrS = ["scale"]
listAttrTR = ["translate", "rotate"]
listAttrTRS = ["translate", "rotate", "scale"]

listAttrTXYZ = ["translateX", "translateY", "translateZ"]
listAttrRXYZ = ["rotateX", "rotateY", "rotateZ"]
listAttrSXYZ = ["scaleX", "scaleY", "scaleZ"]

listAttrRC = ["rotate", "rotateX", "rotateY", "rotateZ"]
listAttrSC = ["scale", "scaleX", "scaleY", "scaleZ"]

listAttrTRXYZ = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
listAttrTRSXYZ = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]
listAttrFkIk = [
	"headFkIk", "headSoftness", "headTwist",
	"leftArmFkIk", "leftArmSoftness", "leftArmTwist",
	"rightArmFkIk", "rightArmSoftness", "rightArmTwist",
	"leftLegFkIk", "leftLegSoftness", "leftLegTwist",
	"rightLegFkIk", "rightLegSoftness", "rightLegTwist",
]



def loadDependencies():
	"""Loads all dependencies (hik plugins and mel sources).
	"""
	mel.eval(f'source "melOverrides.mel"')
	mel.eval(f'source "dagMenuProcOverride.mel"')
	# mel.eval(f'source "teCreateContainerOverride.mel"')

	log = logging.getLogger('Lunar Maya')
	log.info("Successfully loaded all dependencies.")


if (om.MGlobal.mayaState() == om.MGlobal.kInteractive): loadDependencies()



class LMScene():
	"""Maya Scene wrapper class.
	"""
	log = logging.getLogger("MScene")


	@classmethod
	def getAnimationRange(cls) -> tuple:
		"""Gets the scene's start and end frame.
		"""
		return(oma.MAnimControl.minTime().value, oma.MAnimControl.maxTime().value)


	@classmethod
	def setFramerate(cls, frameRate:float=30) -> None:
		""""Sets the scene's frame rate.
		"""
		if frameRate == 30:	om.MTime.setUIUnit(8)
		else:
			print(f"Framerate {frameRate} unsupported.")


	@classmethod
	def setAnimationRange(cls, timeStart:int, timeEnd:int, animation:bool=True) -> None:
		"""Sets the playback range on the timeline.
		"""
		timeUiUnit = om.MTime.uiUnit()
		timeStart = om.MTime(timeStart, timeUiUnit)
		timeEnd = om.MTime(timeEnd, timeUiUnit)
		oma.MAnimControl.setMinMaxTime(timeStart, timeEnd)
		if animation: oma.MAnimControl.setAnimationStartEndTime(timeStart, timeEnd)


	@classmethod
	def getTimeNode(cls) -> om.MFnDependencyNode:
		"""Gets the function set for the scene's time1 node.
		"""
		return om.MFnDependencyNode(MObject.getObjFromString("time1"))



class LMFbx(AbstractFbx):
	"""Maya Fbx class, inherited from AbstractFbx.

	TODO add exportAnimation method
	TODO add a methods for merging single take files into multipile ones

	"""

	log = logging.getLogger("LMFbx")


	@classmethod
	def gatherTakes(cls, filePath:str) -> dict:
		"""Returns essential data regarding takes for the specified fbx file.

		Dictionary structure:
			{'Main Walk': {'index': 1, 'startFrame': 0.0, 'endFrame': 73.0}}

		Args
			filePath (str): File path to the fbx file.

		Returns:
			dict: Dictonary with all take names, indecies, start and end frames, see dictonary structure.

		"""
		mel.eval(f'FBXRead -f "{filePath}"')
		takes = OrderedDict()
		for i in range(mel.eval("FBXGetTakeCount")):
			# Increment and convert to string since takes are counted from 1 not 0
			iStr = str(i+1)
			takeName = mel.eval(f"FBXGetTakeName {iStr}")
			takeFrameRange = mel.eval(f"FBXGetTakeLocalTimeSpan {iStr}")
			takes[takeName] = {
				"index": i+1,
				"startFrame": takeFrameRange[0],
				"endFrame": takeFrameRange[1],
			}
		mel.eval("FBXClose")

		return takes


	@classmethod
	def importAnimation(cls, filePath:str, startFrame:int, endFrame:int, takeIndex:int=1, mode:str="exmerge") -> bool:
		"""Imports the animation from the specified file.

		Args:
			filePath (str): filePath (str): File path to the fbx file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			takeIndex (int): Index of the take to load
			mode (string): FBXImportMode -v [exmerge, add, merge]

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		mel.eval("FBXPushSettings")  # Save current settings

		cls.setImportMocapSettings(mode)

		mel.eval(f'FBXImport -f "{filePath}" -t {takeIndex}')

		# The FBXImportSetMayaFrameRate -v 1 and FBXImportFillTimeline -v 1 are executed
		# only in cpu idle state and don't work with batch export
		LMScene.setAnimationRange(startFrame, endFrame, False)
		# cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		# Restore settings saved by the push command
		mel.eval("FBXPopSettings")


	@classmethod
	def loadAnimation(cls, filePath:str, mode:str="exmerge"):
		"""Wrapper method for importing fbx animation.
		"""
		LMFile.load(filePath, reference=False)
		# Import fbx animation (gather takes)
		takes = LMFbx.gatherTakes(filePath)
		take = list(takes.keys())[0]
		LMFbx.importAnimation(
			filePath,
			takes[take]['startFrame'], takes[take]['endFrame'], takes[take]['index'],
			mode
		)


	@classmethod
	def exportAnimation(cls, filePath:str, startFrame:int=None, endFrame:int=None, bake:bool=False) -> bool:
		"""Imports the animation from the specified file.

		Args:
			filePath (str): File path to the fbx file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			takeIndex (int): Index of the take to load

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if not startFrame: startFrame = cmds.playbackOptions(minTime=True, query=True)
		if not endFrame: endFrame = cmds.playbackOptions(maxTime=True, query=True)

		# Save current settings
		mel.eval("FBXPushSettings")

		cls.setExportAnimationSettings()

		LMFinder.createDirectory(qtc.QFileInfo(filePath).absolutePath())

		if bake:
			mel.eval("FBXExportBakeComplexAnimation -v 1")
			mel.eval(f"FBXExportBakeComplexStart -v {startFrame}")
			mel.eval(f"FBXExportBakeComplexEnd -v {endFrame}")
			mel.eval("FBXExportBakeResampleAnimation -v 1")

		mel.eval(f'FBXExport -f "{filePath}" -s')
		# cmds.file("/Users/luky/Desktop/Manny/asdsadsa.fbx", force=True, options="v=0", typ="FBX export", pr=True, es=True)

		# Restore settings saved by the push command
		mel.eval("FBXPopSettings")

		return True


	@classmethod
	def setImportMocapSettings(cls, mode:str="add") -> bool:
	# def __setImportMocapSettings(cls, mode:str="exmerge") -> bool:
		"""Sets import settings for bare bone mocap import.

		Args:
			mode (string): FBXImportMode -v [exmerge, add, merge]

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		mel.eval("FBXResetImport")

		mel.eval(f"FBXImportMode -v {mode}")
		mel.eval("FBXImportCameras -v 0")
		mel.eval("FBXImportLights -v 0")
		mel.eval("FBXImportCacheFile -v 0")
		mel.eval("FBXImportShapes -v 0")
		mel.eval("FBXImportSkins -v 0")

		mel.eval("FBXImportUpAxis y")
		mel.eval("FBXImportSetMayaFrameRate -v 1")  # These two need an idle cycle to work
		mel.eval("FBXImportFillTimeline -v 1")
		mel.eval("FBXImportGenerateLog -v 0")

		return True
	

	@classmethod
	def setExportAnimationSettings(cls):
		"""Sets export settings for bare bone mocap export."""
	
		mel.eval("FBXResetExport")
		# mel.eval("FBXExportAnimationOnly -v 1")  # Export only transform nodes

		mel.eval('FBXProperty "Export|IncludeGrp|Animation" -v 1')
		mel.eval("FBXExportSmoothMesh -v 0")  # Do not export subdivision version
		mel.eval("FBXExportShapes -v 0")  # Needed for skin and blend shapes
		mel.eval("FBXExportSkins -v 0")

		# Curve Filters
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter" -v 1')
		mel.eval("FBXExportQuaternion -v resample")
		mel.eval("FBXExportApplyConstantKeyReducer -v 1")
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedTPrec" -v 0.0001')
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedRPrec" -v 0.0090')
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedSPrec" -v 0.0040')
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|CurveFilterCstKeyRedOPrec" -v 0.0090')
		mel.eval('FBXProperty "Export|IncludeGrp|Animation|CurveFilter|CurveFilterApplyCstKeyRed|AutoTangentsOnly" -v 1')

		mel.eval("FBXExportInputConnections -v 0")
		mel.eval("FBXExportIncludeChildren -v 1")
		mel.eval("FBXExportSkeletonDefinitions -v 0")
		mel.eval("FBXExportUpAxis y")

		# FBX file format
		mel.eval("FBXExportInAscii -v 0")
		mel.eval("FBXExportFileVersion -v FBX201800")
		mel.eval("FBXExportGenerateLog -v 0")




class LMFinder(qtc.QObject):
	"""Class for cross platform file managment based on QtCore.

	Convinience methods for automating file - related common tasks like listing files in directories,
	creating new directories, copying files, etc.

	This class ensures path '/' foward slash compability on windows.

	TODO:
		getDirectoriesInPath - filtering empty parent directories

	"""
	locationHome = qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.HomeLocation)
	locationDesktop = qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.DesktopLocation)
	locationDownload = qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.DownloadLocation)
	locationDocuments = qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.DocumentsLocation)

	nameOs = platform.system()
	log = logging.getLogger("MFinder")


	@classmethod
	def __str__(cls) -> str:
		return f"Finder - cross platform file operation helper."


	@classmethod
	def createDirectory(cls, path) -> bool:
		"""Creates the specified directory if it does not already exist.

		Args:
			path (string): The path for the directory to be created.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		directory = qtc.QDir(path)
		if not directory.exists():
			directory.mkpath(directory.absolutePath())
			cls.log.info(f"Directory '{directory.absolutePath()}' was successfully created.")
		else:
			cls.log.debug(f"Directory '{directory.absolutePath()}' already exists.")

		return True


	@classmethod
	def getDirectoriesInPath(cls,
		path,
		nameFilters=["*.fbx"],
		filters=qtc.QDir.Dirs,
		includeSubDirectories=qtc.QDirIterator.Subdirectories,
	) -> list[qtc.QFileInfo] or None:
		"""List all directories that are found under the specified path."""
		dirInfo = qtc.QFileInfo(path)
		if dirInfo.exists() and dirInfo.isDir():
			dirInfoList = []

			dirIter = qtc.QDirIterator(path, nameFilters, filters, includeSubDirectories)
			while dirIter.hasNext():
				dirIter.next()
				currDir = qtc.QDir(dirIter.filePath())
				if(
					dirIter.filePath().endswith("/.") or 
					dirIter.filePath().endswith("/..") or 
					currDir.isEmpty() or
					currDir.entryList(filters=qtc.QDir.Files).__len__() == 0  # NEEDS TO BE FIXED TO PREVENT DOUBLE CLLIPS Entries
				): continue

				dirInfoList.append(dirIter.filePath())

			if dirInfoList.__len__ != 0: return dirInfoList

		return None


	@classmethod
	def getFilesInDirectory(cls,
		path:str,
		nameFilters:list=[],
		filters=qtc.QDir.Files,
		includeSubDirectories=qtc.QDirIterator.Subdirectories,
	) -> list[qtc.QFileInfo] or False:
		"""Returns a list with files contained in the specified directory.

		Args:
			path (string): Path to the directory.
			nameFilters (list): A list with name filters e.g. ['sara*'], ['*.fbx'].
			filters (QDir.Flag): NoFilter, Files, Dirs.
			includeSubDirectories (QDirIterator.IteratorFlag): Whether or not search in	sub-directories,
				Subdirectories - true, NoIteratorFlags - false.

		Returns:
			fileInfoList (List[QFileInfo] or False): List with QFileInfo objects that the	directory
				contains,	if the list is empty or the directory does not exis it will	return False.

		"""
		fileInfo = qtc.QFileInfo(path)
		if fileInfo.exists() and fileInfo.isDir():
			fileInfoList = []

			dirIter = qtc.QDirIterator(path, nameFilters, filters, includeSubDirectories)
			while dirIter.hasNext():
				dirIter.next()
				fileInfoList.append(dirIter.fileInfo())
		
			if fileInfoList.__len__ != 0: return fileInfoList
	
			cls.log.warning(f"'{path}' contains no files with those {nameFilters} name filters.")

		else:	cls.log.warning(f"Entry: '{path}' does not exist or is not a directory - nothing to return.")

		return False


	@classmethod
	def validateFileInfo(cls, path) -> qtc.QFileInfo or False:
		"""Validate the specified file.

		Args:
			path (str): Path to the object.

		Returns:
			fileInfo (QFileInfo): If the specified object exists it will be returned,
				if it does not exist False will be returned instead.

		"""
		fileInfo = qtc.QFileInfo(path)
		if fileInfo.exists():
			cls.log.debug(f"'{path}' file or directory exists.")
			return fileInfo

		cls.log.warning(f"'{path}' file or directory does not exists.")
		return False


	@classmethod
	def copy(cls, source, destination, overwrite=True) -> bool:
		"""Copies the source file / directory to the destination.

		Args:
			source (str): Source file or directory path.
			destination (str): Destination directory path.
			overwrite (bool): If destination file / directory exists, it will be overwritten.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		fileInfo = cls.validateFileInfo(source)
		if not fileInfo: return False

		# Input can be a directory or a file
		finished = False
		if fileInfo.isDir():
			fileObjs = cls.getFilesInDirectory(source)
			if fileObjs.__len__() != 0:
				for fileObj in fileObjs:
					destinationFilePath = fileObj.filePath().replace(source, destination)
					destinationFile = qtc.QFile(destinationFilePath)
					if overwrite and destinationFile.exists(): destinationFile.remove()
					destinationDir = qtc.QFileInfo(destinationFilePath).dir()
					cls.createDirectory(destinationDir)

					finished = qtc.QFile(fileObj.filePath()).copy(destinationFilePath)
				cls.log.info(f'{fileObjs.__len__()} files copied successfully.')

			else:
				cls.log.info('Did not find any files to copy in the given directory')

		if fileInfo.isFile():
			cls.createDirectory(destination)
			destinationFilePath = f'{destination}/{fileInfo.fileName()}'
			destinationFile = qtc.QFile(destinationFilePath)
			if overwrite and destinationFile.exists(): destinationFile.remove()
	
			finished = qtc.QFile(fileInfo.filePath()).copy(destinationFilePath)

		if finished:
			cls.log.info("Copy operation finished")
			return True

		return False


	@classmethod
	def openInFileManager(cls, path:str):
		if cls.nameOs == "Windows":
			subprocess.Popen(f'explorer "{qtc.QDir.toNativeSeparators(path)}"')
		elif cls.nameOs == "Darwin":
			subprocess.Popen(f"open {path}", shell=True)
		elif cls.nameOs == "Linux":
			subprocess.Popen(f"gnome-open {path}", shell=True)
		else:
			cls.log.critical(f"Unsupported operating system: '{cls.nameOs}'.")




class LMFile(om.MFileIO):
	""""Class wrapper for file operations - inherited from MFileIO.
	"""

	log = logging.getLogger("LMFile")


	@classmethod
	def new(cls, force:bool=False) -> bool:
		"""Open a new file.
		"""
		if not force:
			if cmds.file(query=True, modified=True):
				inputDialog = cls.dialog(
					message=f"Save changes to '{om.MFileIO.currentFile()}' ?",
					title="Save Changes",
					icon="question",
					buttons=["Save", "Don't Save", "Cancel"],
					cancelButton="Cancel",
				)
				if inputDialog == "Save":
					if not cmds.file(query=True, sceneName=True, shortName=False):
						mel.eval("SaveSceneAs;")
						return True
					om.MFileIO.save()
				if inputDialog == "Cancel":
					return False

		# if force and file is not modified:	
		om.MFileIO.newFile(True)
		return True


	@classmethod
	def load(cls, filePath:str, nameSpace:str=None, reference:bool=True):
		"""Import file wrapper method for fbx and maya native file formats.
		
		If we are importing an fbx file we don't want a namespace in order to import / update
		the animation in the scene. Since importing fbx files with a namespace will bring in
		a new set of joints it is unwanted behaviour for this case. 
		For the maya files on the other hands we need a namespace rig as the target.

		"""
		if reference:
			om.MFileIO.reference(filePath, False, False, nameSpace)
			return True

		# Legacy batch retarget support
		if filePath.endswith('.fbx'):
			om.MFileIO.importFile(filePath)
		if filePath.endswith('.ma') or filePath.endswith('.mb'):
			cls.reference(filePath, nameSpace)


	@classmethod
	def importFile(cls, filePath:str, nameSpace:str, importTimeRange:str="combine", importFrameRate:bool=False):
		"""Imports the specified file into the current scene.
		"""
		cmds.file(
			filePath,
			namespace=nameSpace,
			i=True,
			importTimeRange=importTimeRange,
			importFrameRate=importFrameRate,
		)


	@classmethod
	def reference(cls, filePath:str, nameSpace:str, lockReference:bool=False, deferReference:bool=False) -> str:
	# def reference(cls, filePath:str, nameSpace:str) -> str:
		"""Adds the speciefied file as a reference to the current scene.

		Args:
			filePath (string): name of the file to add as a reference.
			nameSpace (string):	name space to add the contents of the referenced file to. If no namespace is provided, name-clashes will be resolved by prefixing with the filename.
			lockReference (bool):	If true, all nodes and attributes from the referenced file will be locked.
			deferReference (bool): boolean to indicate whether loading has to be deferred.

		"""
		om.MFileIO.reference(filePath, deferReference, lockReference, nameSpace)

		return cmds.file(filePath, query=True, referenceNode=True)


	@classmethod
	def importReference(cls, filePath:str):
		"""Ïmports the specified reference.
		"""
		cmds.file(filePath, importReference=True)


	@classmethod
	def removeReference(cls, filePath:str, deleteNamespaceContent:bool=True):
		"""Removes the specified reference from the scene.
		"""
		if deleteNamespaceContent:
			om.MFileIO.removeReference(filePath, om.MFileIO.kForceDeleteNamespaceContent)
			return

		om.MFileIO.removeReference(filePath)


	@classmethod
	def getReferenceNodesByType(cls, filePath:str, nodeType:str="joint") -> list:
		"""Returns the nodes of a specified type from the given reference node.

		"""
		listReferenceNodes = []
		om.MFileIO.getReferenceNodes(filePath, listReferenceNodes)
		# Filter out node type
		listNodesByTpe = []
		[listNodesByTpe.append(node) for node in listReferenceNodes if cmds.nodeType(node) == nodeType]

		return listNodesByTpe


	@classmethod
	def loadDataFromJson(cls, filePath:str) -> dict:
		"""Loads data from a json file.
		"""
		with open(filePath, "r") as file:
			return json.loads(file.read())


	@classmethod
	def importDialog(cls,
			startingDirectory:str=qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.DesktopLocation),
			fileFilter:str="FBX ( .fbx ) (*.fbx)",
		) -> str:
		return cmds.fileDialog2(
			fileMode=4,
			dialogStyle=2,
			okCaption="Import",
			fileFilter=fileFilter,
			startingDirectory=startingDirectory,
		)


	@classmethod
	def exportDialog(cls,
			startingDirectory:str=qtc.QStandardPaths.writableLocation(qtc.QStandardPaths.DesktopLocation),
			fileFilter:str="FBX ( .fbx ) (*.fbx)",
		) -> str:
		return cmds.fileDialog2(
			fileMode=0,
			dialogStyle=2,
			okCaption="Export",
			fileFilter=fileFilter,
			startingDirectory=startingDirectory,
		)


	@classmethod
	def characterDialog(cls) -> str or None:
		result = cmds.promptDialog(
			title='Character Namespace',
			message='Enter Namespace:',
			button=['OK', 'Cancel'],
			defaultButton='OK',
			cancelButton='Cancel',
			dismissString='Cancel',
		)
		if result == 'OK':
			return cmds.promptDialog(query=True, text=True)
		
		om.MGlobal.displayWarning("Import operation was canceled")
		return None


	@classmethod
	def dialog(cls,
			message="Default Message",
			title="Default Title",
			icon="question",
			buttons=["Install", "Cancel"],
			cancelButton="Cancel"
		) -> str:
		"""Convinience wrapper method for creating confirm dialogs.

		Returns:
			str: Input from user as string e.g. "Install" or "Cancel".

		"""
		return cmds.confirmDialog(
			title=title,
			message=message,
			icon=icon,
			button=buttons,
			cancelButton=cancelButton,
			dismissString=cancelButton
		)




class LMGlobal(om.MGlobal):
	"""Wrapper class for MGlobal with additional methods.
	"""

	@classmethod
	def isSomethingSelected(cls) -> bool:
		"""Checks if there are any nodes currently selected.

		Returns:
			bool: True is something is selected, False otherwise.

		"""
		listSelection = om.MSelectionList()
		LMGlobal.getActiveSelectionList(listSelection)

		if not listSelection.isEmpty(): return True
		return False


	@classmethod
	def getSelection(cls) -> om.MSelectionList:
		"""Returns the active selection list.
		"""
		listSelection = om.MSelectionList()
		LMGlobal.getActiveSelectionList(listSelection)

		return listSelection




class LMObject(om.MObject):
	"""Wrapper class with MObjects utils.
	"""

	log = logging.getLogger("LMObject")


	@classmethod
	def getObjFromString(cls, object:str) -> om.MObject:
		"""Gets the MObject from the given name.

		"""
		listSelection = om.MSelectionList()
		listSelection.add(object)
		mObject = om.MObject()
		listSelection.getDependNode(0, mObject)

		return mObject


	@classmethod
	def getDagPathFromString(cls, object:str) -> om.MDagPath:
		"""Gets the dag path from the given name."""
		listSelection = om.MSelectionList()
		listSelection.add(object)
		dpObject = om.MDagPath()
		listSelection.getDagPath(0, dpObject)

		return dpObject




class LMSceneObject():
	"""Class for wrapping scene objects.
	"""

	objectType = "LMSceneObject"

	@classmethod
	def sceneObjectType(cls, node:str, type:str="rig") -> bool:
		"""Checks if the given object is a scene object.
		"""
		typeSceneObject = cmds.getAttr(f"{node}.sceneObjectType")
		if cmds.getAttr(f"{node}.sceneObjectType") == type:
			return True

		return False




class LMRigObject():
	"""Wrapper class for rig objects in maya.

	Rig Structure:
		root
		components:
			main_ctrl
			root
			pelvis
			spine fk 
			head fk/ik
			left_arm fk/ik
			left_hand
			right_arm fk/ik
			right_hand
			left_leg fk/ik
			left_foot
			right_leg fk/ik
			right_foot

	"""
	objectType = "LMRig"

	def __init__(self, name) -> None:
		import lunar.maya.LunarMayaRetarget as lmrtg
		self.root = name
		self.namespace = LMNamespace.getNamespaceFromName(name)

		self.rtgCtrl = lmrtg.LMLunarCtrl(f"{self.namespace}:Ctrl")
		self.rtgSkeleton = lmrtg.LMLunarExport(f"{self.namespace}:Export")




class LMMetaData():
	"""Wrapper class for the metaData node.
	"""

	def __init__(self,
		name:str="sceneMetaData",
		text:str="",
		textPosition:tuple=(50, 50),
		textColor:tuple=(2.0, 2.0, 2.0),
		textVisibility:bool=True,
	):
		self.log = logging.getLogger(f"{self.__class__.__name__} - {name}")
		self.name = name
		self.text = text
		self.textPosition = textPosition
		self.textColor = textColor
		self.textVisibility = textVisibility

		self.validate()
		self.text = self.getText()


	def validate(self) -> bool:
		if self.isValid():
			self.log.info(f"Initiated from existing object")
			return True

		if self.text == "":
			sceneName = cmds.file(query=True, sceneName=True, shortName=True)
			if not sceneName: self.text = "untitled"

		self.node = cmds.metaData(
			name=self.name,
			# text=self.text, // this is not implemented in the cpp part due to compound array attrs
			textPosition=self.textPosition,
			textColor=self.textColor,
			textVisibility=self.textVisibility,
		)
		# Temp override for array attributes
		cmds.setAttr(f"{self.node}.metaData[0].text", self.text, type="string")
		cmds.setAttr(f"{self.node}.metaData[0].displayInViewport", True)

		self.name = self.node
		self.log.info(f"Initiated from a new object")

		return True


	def isValid(self) -> bool:

		if self.objOfTypeExists(self.name, "metaData"):
			self.node = self.name
			return True
			# self.node = cmds.listRelatives(self.node, shapes=True)[0]
			# if self.node:
			# 	if self.objOfTypeExists(self.node, "metaData"):

		return False


	def objOfTypeExists(self, object:str, type:str) -> bool:

		if cmds.objExists(object) and cmds.objectType(object) == type:
			return True

		return False


	def setText(self, text:str):
		cmds.setAttr(f"{self.node}.metaData[0].text", text, type="string")
		cmds.setAttr(f"{self.node}.metaData[0].displayInViewport", True)


	def setTextPosition(self, value:tuple):
		cmds.setAttr(f"{self.node}.textPositionX", value[0])
		cmds.setAttr(f"{self.node}.textPositionY", value[1])


	def setTextColor(self, value:tuple):
		cmds.setAttr(f"{self.node}.textColorR", value[0])
		cmds.setAttr(f"{self.node}.textColorG", value[1])
		cmds.setAttr(f"{self.node}.textColorB", value[2])


	def getText(self):
		return cmds.getAttr(f"{self.node}.metaData[0].text")


	def setFromSceneName(self):
		cmds.setAttr(f"{self.node}.metaData[0].text", cmds.file(query=True, sceneName=True, shortName=True), type="string")
		



class LMNamespace(om.MNamespace):
	"""Wrapper class for MNamespace.
	"""
	log = logging.getLogger("LMNamespace")


	@classmethod
	def getNameWithNamespace(cls, name:str, namespace:str) -> str:
		"""Returns the given object with the specified namesapce
		Args:
			name (str): Name of the node/object.
			namespace (str): Name of the node/object.

		Returns:
			str: If the namespace is not an empty string, name with namespace will be returned. Otherwise
				just the name.

		"""
		if namespace != "":
			return f"{namespace}:{name}"

		return name
	

	@classmethod
	def getNamespaceFromSelection(cls) -> str or None:
		"""Returns the namespace from current selection.
		"""
		nodes = cmds.ls(selection=True)
		if nodes:
			namespace = om.MNamespace.getNamespaceFromName(nodes[0])
			if namespace: return namespace
			cls.log.warning("Selection has to have a namespace")
			return None
		cls.log.info("Nothing is currently selected.")
		return None


	@classmethod
	def getNamespaceFromName(cls, name:str) -> str:
		"""Overrides the custom method to not throw errors when there is no namespace.
		"""
		if name != "":
			name = om.MNamespace.getNamespaceFromName(name)

		return name


	@classmethod
	def removeNamespaceFromName(cls, name:str) -> str:
		"""Returns the given object with the specified namesapce
		Args:
			name (str): Name of the node/object.

		Returns:
			str: If the namespace is not an empty string, name with namespace will be returned. Otherwise
				just the name.

		"""
		if name != "":
			nameWithoutNamespace = name.split(":")[-1]
			if nameWithoutNamespace: return nameWithoutNamespace

		return name




#--------------------------------------------------------------------------------------------------
# Utilities
#--------------------------------------------------------------------------------------------------




class LMAttribute():
	"""Wrapper class for attribute utilities.
	"""
	log = logging.getLogger("MAttrUtils")
	dgMod = om.MDGModifier()


	@classmethod
	def copyTransformsToOPM(cls, object:str):
		"""Copies the translation and rotation values to the offset parent matrix attribute.
		"""
		arrayLocalMatrix = cmds.xform(object, query=True, matrix=True, worldSpace=False)
		cmds.setAttr(f"{object}.offsetParentMatrix", arrayLocalMatrix, type="matrix")
		cmds.xform(object, translation=(0,0,0), rotation=(0,0,0))


	@classmethod
	def hide(cls, name:str) -> None:
		"""Hides the specified attribute from channel box.
		
		Args:
			name (string): Name of the attribute to be locked.
		
		"""
		cmds.setAttr(name, lock=True, keyable=False, channelBox=False)


	@classmethod
	def addDisplayType(cls, object:str, name:str, defaultValue:int=0) -> str:
		"""Adds a display type attribute on the given object.
		"""
		attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="enum", enumName="normal=0:template=1:reference=2", keyable=False, defaultValue=defaultValue)
		cmds.setAttr(attrName, channelBox=True)
		# cmds.setAttr(f"{object}.overrideEnabled", True)
		return attrName


	@classmethod
	def addFloat(cls, object:str, name:str, defaultValue:float=0.0) -> str:
		"""Adds a float attribute on the given object.
		"""
		attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="float", keyable=True, defaultValue=defaultValue)
		return attrName


	@classmethod
	def addOnOff(cls, object:str, name:str, defaultValue:bool=True) -> str:
		"""Adds a on / off attribute on the given object.
		"""
		attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="enum", enumName="off=0:on=1", keyable=False, defaultValue=defaultValue)
		cmds.setAttr(attrName, channelBox=True)
		return attrName


	@classmethod
	def addSeparator(cls, object:str, name:str="_") -> str:
		"""Adds a separator attribute on the given object.
		"""
		attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="enum", enumName=" =0:", defaultValue=False, keyable=False)
		cmds.setAttr(attrName, lock=True, channelBox=True)
		return attrName


	@classmethod
	def addFloatFkIk(cls, object:str, name:str, minValue:float=0.0, maxValue:float=100.0, defaultValue:float=0.0) -> str:
		"""Adds a float attribute on the given object.
		"""
		attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="float", minValue=minValue, maxValue=maxValue, keyable=True, defaultValue=defaultValue)
		return attrName


	@classmethod
	def addFkIkMode(cls, object:str, name:str, defaultValue:int=0) -> str:
		"""Adds a display type attribute on the given object.
		"""
		# attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="enum", enumName="Fk=0:Ik=1", keyable=True, defaultValue=defaultValue)
		# cmds.setAttr(attrName, channelBox=True)
		cmds.setAttr(f"{object}.overrideEnabled", True)
		return f"{object}.{name}"


	@classmethod
	def addMessage(cls, object:str, name:str, isArray:bool=False):
		# attrName = f"{object}.{name}"
		cmds.addAttr(object, longName=name, attributeType="message", multi=isArray)
		return f"{object}.{name}"


	@classmethod
	def lockControlChannels(cls, object:str, lockChannels:list):
		"""Locks the given attributes.
		"""
		if lockChannels != []:
			singleAttributeLockList = []
			for lockChannel in lockChannels:
				if lockChannel in ["translate", "rotate", "scale"]:
					[singleAttributeLockList.append(f"{lockChannel}{axis}") for axis in ["X", "Y", "Z"]]
				else:
					singleAttributeLockList.append(lockChannel)
			[cmds.setAttr(f"{object}.{attr}", channelBox=False, keyable=False, lock=True) for attr in singleAttributeLockList]


	@classmethod
	def lockControlPlugs(cls, object:str, lockChannels:list):
		"""Locks the given attributes.
		"""
		mObj = LMObject.getObjFromString(object)
		fnObj = om.MFnDependencyNode(mObj)

		if lockChannels != []:
			singleAttributeLockList = []
			for channel in lockChannels:
				if channel in ["translate", "rotate", "scale"]:
					[singleAttributeLockList.append(f"{channel}{axis}") for axis in ["X", "Y", "Z"]]
				else:
					singleAttributeLockList.append(channel)

			for attr in singleAttributeLockList:
				plug = fnObj.findPlug(attr, False)
				plug.setKeyable(False)
				plug.setChannelBox(False)
				plug.setLocked(True)
			# [cmds.setAttr(f"{object}.{attr}", lock=True, keyable=False, channelBox=False) for attr in singleAttributeLockList]


	@classmethod
	def lockTransforms(cls, object:str, lockChannels:list=["translate", "rotate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"]):
		"""Locks all transform attributes on the given object.
		"""
		cls.lockControlChannels(object, lockChannels)


	@classmethod
	def editLocked(cls, name:str, value:float, relock:bool=True) -> None:
		"""Allows to edit a locked attribute.
		
		Unlocks the specified attribute, edits it and then locks it again.

		Args:
			name (string): Name of the attribute.
			value (float): Value for the attribute.
		
		"""
		cls.unlockIfLocked(name)
		cmds.setAttr(name, value)
		if relock: cmds.setAttr(name, lock=True)


	@classmethod
	def isLocekd(cls, name:str):
		"""Unlocks the given attribute if it is locked.

		TODO:
			Replace with the api method to unlock Attributes from referenced files 8-)

		"""
		return cmds.getAttr(name, lock=True)


	@classmethod
	def unlockIfLocked(cls, name:str):
		"""Unlocks the given attribute if it is locked.

		TODO:
			Replace with the api method to unlock Attributes from referenced files 8-)

		"""
		if cmds.getAttr(name, lock=True):	cmds.setAttr(name, lock=False)


	@classmethod
	def unlockPlugIfLocked(cls, node:str, attributes:list):
		"""Unlocks the given attributes if they're locked.

		TODO:
			Replace with the api method to unlock Attributes from referenced files 8-)

		"""
		fnNode = om.MFnDependencyNode(LMObject.getObjFromString(node))
		# for attr in attributes:
		# 	plug = fnNode.findPlug(attr, False)
		# 	if plug.isLocked():	
		# 		plug.setLocked(False)
		[fnNode.findPlug(attr, False).setLocked(False) for attr in attributes if fnNode.findPlug(attr, False).isLocked()]

		cls.dgMod.doIt()


	@classmethod
	def connectSceneTime(cls, object:str, plug:str="inTime") -> None:
		"""Connects the scene's default time1 node to the given target.
		"""
		fnTarget = om.MFnDependencyNode(LMObject.getObjFromString(object))
		plugInTime = fnTarget.findPlug(plug, False)
		plugTime1Out =  LMScene.getTimeNode().findPlug("outTime", False)
		cls.dgMod.connect(plugTime1Out, plugInTime)
		cls.dgMod.doIt()




class LMTransformUtils():
	"""Wrapper class for transforms utilities.
	"""
	log = logging.getLogger("MTransformUtils")	


	@classmethod
	def getDistanceBetween(cls, source:str):
		"""Gets the distance between source and target node.
		"""
		# Get child obj
		if cmds.objExists(source) and type(source) != "NoneType":
			target = cmds.listRelatives(source, children=True, type="transform")
			if target == None:
				return False
			else:
				sourcePt = cmds.xform(source, query=True, translation=True, worldSpace=True)
				targetPt = cmds.xform(target[0], query=True, translation=True, worldSpace=True)
				sourcePoint = om.MPoint(sourcePt[0], sourcePt[1], sourcePt[2])
				targetPoint = om.MPoint(targetPt[0], targetPt[1], targetPt[2])
				distance = sourcePoint.distanceTo(targetPoint)

				return distance
		return False


	@classmethod
	def reconnectSkin(cls, source:str, destination:str):
		"""Recconects the skin cluster from the source to the target object.
		"""
		worldMatrix0Attr = ".worldMatrix[0]"
		skinMatrixAttr = cmds.listConnections(f"{source}{worldMatrix0Attr}", plugs=True)[0]
		if skinMatrixAttr:
			cmds.connectAttr(f"{destination}{worldMatrix0Attr}", f"{skinMatrixAttr}", force=True)
		

	@classmethod
	def postCtrlTransform(cls, listJoint:dict, side:str=""):
		# With specified commponent like ListJoint["Spine"]
		ListUnpackedJoints = []
		for key, value in listJoint.items():
			if type(value) == dict:
				for key, value in value.items():
					if type(value) == list:
						[ListUnpackedJoints.append(f"{joint}{side}") for joint in value]
					else:
						ListUnpackedJoints.append(f"{value}{side}")
			else:
				ListUnpackedJoints.append(f"{value}{side}")

		ListControllers = []
		for joint in ListUnpackedJoints:
			if joint == "pelvis": joint = "pelvis_rot"
			ListControllers.append(f"{joint}_ctrl")
		# [ListControllers.append(f"{joint}_ctrl") for joint in ListUnpackedJoints]

		for ctrl, jnt in zip(ListControllers, ListUnpackedJoints):
			if cmds.objExists(ctrl):
				LMAttribute.copyTransformsToOPM(ctrl)
				# cls.reconnectSkin(jnt, ctrl)
				if ctrl == "pelvis_rot_ctrl": continue
				# LMAttribute.lockControlChannels(ctrl, lockChannels=["offsetParentMatrix"])

				# if "twist" not in jnt:
				# 	distance = cls.getDistanceBetween(jnt)
				# 	if distance:
				# 		LMAttribute.editLocked(f"{ctrl}Shape.localScaleX", distance*0.7)
				# 		LMAttribute.editLocked(f"{ctrl}Shape.localPositionX", distance*0.5)
