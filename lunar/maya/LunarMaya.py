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




class LMFbx(AbstractFbx):
	"""Maya Fbx class, inherited from AbstractFbx.

	TODO add exportAnimation method
	TODO add a methods for merging single take files into multipile ones

	"""

	log = logging.getLogger("MFbx")


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

		cls.__setImportMocapSettings(mode)

		mel.eval(f'FBXImport -f "{filePath}" -t {takeIndex}')

		# The FBXImportSetMayaFrameRate -v 1 and FBXImportFillTimeline -v 1 are executed
		# only in cpu idle state and don't work with batch export
		LMScene.setAnimationRange(startFrame, endFrame, False)
		# cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		# Restore settings saved by the push command
		mel.eval("FBXPopSettings")


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

		cls.__setExportAnimationSettings()

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
	def __setImportMocapSettings(cls, mode:str="add") -> bool:
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
	def __setExportAnimationSettings(cls):
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
		path,
		nameFilters=[],
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




class LMFile():
	""""Class wrapper for file operations.
	"""

	log = logging.getLogger("MFile")

	@classmethod
	def new(cls, force:bool=False) -> bool:
		"""Open a new file.
		"""
		if not force:
			# IsFileModified = cmds.file(query=True, modified=True)
			if cmds.file(query=True, modified=True):
				inputDialog = cls.dialog(
					message=f"Save changes to {cmds.file(query=True, expandName=True)} ?",
					title="Save Changes",
					icon="question",
					buttons=["Save", "Don't Save", "Cancel"],
					cancelButton="Cancel",
				)
				if inputDialog == "Save":
					if not cmds.file(query=True, sceneName=True, shortName=False):
						mel.eval("SaveSceneAs;")
						return True
					cmds.file(save=True)
				if inputDialog == "Cancel":
					return False
		
		# if force:	
		cmds.file(new=True, force=True)
		return True


	@classmethod
	def load(cls, filePath:str, nameSpace:str=None):
		"""Import file wrapper method for fbx and maya native file formats.
		
		If we are importing an fbx file we don't want a namespace in order to import / update
		the animation in the scene. Since importing fbx files with a namespace will bring in
		a new set of joints it is unwanted behaviour for this case. 
		For the maya files on the other hands we need a namespace rig as the target.

		"""
		if filePath.endswith('.fbx'):
			cmds.file(filePath, i=True)

		if filePath.endswith('.ma') or filePath.endswith('.mb'):
			cmds.file(filePath, namespace=nameSpace, reference=True)


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




class LMScene():
	"""Maya Scene wrapper class.

	"""

	log = logging.getLogger("MScene")

	@classmethod
	def getNamespaces(cls) -> list:
		"""Gets all namespaces that are found in the current scene.
		"""
		listNamespaces = [Item[1:] for Item in om.MNamespace.getNamespaces()]
		return [Item for Item in listNamespaces if Item not in ["UI", "shared"]]


	@classmethod
	def getAnimationRange(cls) -> tuple:
		"""Gets the scene's start and end frame.
		"""
		return (oma.MAnimControl.minTime().value(), oma.MAnimControl.maxTime().value())


	@classmethod
	def setFramerate(cls, frameRate:float=30) -> None:
		""""Sets the scene's frame rate.
		"""
		if frameRate == 30:	om.MTime.setUIUnit(8)
		else:	print(f"Framerate {frameRate} unsupported.")


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
		return om.MFnDependencyNode(LMObject.getObjFromString("time1"))




class LMMetaData():
	"""Wrapper class for the metaData node.
	"""
	def __init__(self,
		name:str="sceneMetaData",
		text:str="untitled",
		textPosition:tuple=(100, 100),
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

		self.transfom, self.shape = cmds.metaData(
			name=self.name,
			text=self.text,
			textPosition=self.textPosition,
			textColor=self.textColor,
			textVisibility=self.textVisibility,
		)
		self.name = self.transfom
		self.log.info(f"Initiated from a new object")

		return True
			

	def isValid(self) -> bool:

		if self.objOfTypeExists(self.name, "transform"):
			self.transfom = self.name
			self.shape = cmds.listRelatives(self.transfom, shapes=True)
			if self.shape:
				if self.objOfTypeExists(self.shape, "metaData"):
					return True
				
		return False


	def objOfTypeExists(self, object:str, type:str) -> bool:
		if cmds.objExists(object):
			if cmds.objectType(object) == type:
				return True

		return False


	def setText(self, text:str):
		cmds.setAttr(f"{self.name}.text", text, type="string")


	def setTextPosition(self, value:tuple):
		cmds.setAttr(f"{self.name}.textPositionX", value[0])
		cmds.setAttr(f"{self.name}.textPositionY", value[1])


	def setTextColor(self, value:tuple):
		cmds.setAttr(f"{self.name}.textColorR", value[0])
		cmds.setAttr(f"{self.name}.textColorG", value[1])
		cmds.setAttr(f"{self.name}.textColorB", value[2])

	def getText(self):
		return cmds.getAttr(f"{self.name}.text")




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
		arrayLocalMatrix = cmds.xform(object, query=True, matrix=True, worldSpace=False),
		cmds.setAttr(f"{object}.offsetParentMatrix", arrayLocalMatrix[0], type="matrix")
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
		cmds.setAttr(f"{object}.overrideEnabled", True)
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
			[cmds.setAttr(f"{object}.{attr}", lock=True, keyable=False, channelBox=False) for attr in singleAttributeLockList]


	@classmethod
	def editLocked(cls, name:str, value:float) -> None:
		"""Allows to edit a locked attribute.
		
		Unlocks the specified attribute, edits it and then locks it again.

		Args:
			name (string): Name of the attribute.
			value (float): Value for the attribute.
		
		"""
		cls.unlockIfLocked(name)
		cmds.setAttr(name, value)


	@classmethod
	def unlockIfLocked(cls, name:str):
		"""Unlocks the given attribute if it is locked.

		TODO:
			Replace with the api method to unlock Attributes from referenced files 8-)

		"""
		if cmds.getAttr(name, lock=True):	cmds.setAttr(name, lock=False)


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
			# print(target)
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
				cls.reconnectSkin(jnt, ctrl)
				if ctrl == "pelvis_rot_ctrl": continue
				LMAttribute.lockControlChannels(ctrl, lockChannels=["offsetParentMatrix"])

				if "twist" not in jnt:
					distance = cls.getDistanceBetween(jnt)
					if distance:
						LMAttribute.editLocked(f"{ctrl}Shape.localScaleX", distance*0.7)
						LMAttribute.editLocked(f"{ctrl}Shape.localPositionX", distance*0.5)


	@classmethod
	def getPoleVectorPosition(cls, start:str, mid:str, end:str) -> om.MVector:
		"""Gets the best pole vector position from the input of three nodes.
		"""
		# Get world position from strings
		PosStart = cmds.xform(start, q=True, ws=True, t=True)
		PosMid = cmds.xform(mid, q=True, ws=True, t=True)
		PosEnd = cmds.xform(end, q=True, ws=True, t=True)

		# Get vectors
		PosFkStart = om.MVector(PosStart[0], PosStart[1], PosStart[2])
		PosFkMid = om.MVector(PosMid[0], PosMid[1], PosMid[2])
		PosFkEnd = om.MVector(PosEnd[0], PosEnd[1], PosEnd[2])

		VecStartEnd = (PosFkEnd - PosFkStart)
		VecMidEnd = (PosFkEnd - PosFkMid)

		ValScale = (VecStartEnd * VecMidEnd) / (VecStartEnd * VecStartEnd)
		VecProjection = (VecStartEnd * ValScale) + PosFkStart
		LenLimb = (PosFkMid - PosFkStart).length() + VecMidEnd.length()

		return (PosFkMid - VecProjection).normal() * LenLimb + PosFkMid




class LMObject():
	"""Wrapper class with MObjects utils.
	"""

	log = logging.getLogger("MObjectUtils")


	@classmethod
	def getObjFromString(cls, object:str) -> om.MObject:
		"""Gets the MObject from the given name.

		"""
		listSelection = om.MSelectionList()
		listSelection.add(object)
		mObject = om.MObject()
		listSelection.getDependNode(0, mObject)

		return mObject
	

