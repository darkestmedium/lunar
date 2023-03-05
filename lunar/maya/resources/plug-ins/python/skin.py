"""Python plugin with the import / export skin data commands.

Thanks to Chad Vernon and the developers of mGear for sharing their code.

Reference:
	https://www.cgcircuit.com/tutorial/writing-a-production-ready-skin-exporter
	http://www.mgear-framework.com/

"""

# Built-in imports
import json

# Third-party imports
from maya import cmds

import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

# Custom imports



maya_useNewAPI = True



class SkinCluster():
	"""Class for handling skin clusters.
	
	TODO: move methods:
		getMesh
		getSkinCluster
		getMeshComponents
		getInfluenceWeights

	"""

	# Public data
	fileExtension = ".skin"

	skinFileFilter = f"Skin Files ( {fileExtension} ) ( *{fileExtension} )"

	# Private data
	__selList = om.MSelectionList()
	__filePath = None
	__export = True
	__import = False
	__meshPath = None
	__skinClusterFn = None
	# __skinClusterOutputGeometryPlug = None
	__components = None




class ExportSkinCommand(om.MPxCommand):
	"""Skin export command for exporting skin related data.

	User override of the MPxCommand class.

	TODO:
		getInfluenceWeights split into smaller methods
		skip the 0.0 influences?
		add support for multiple meshes
		add getBlendWeights support

	"""

	# Public data
	commandName = "exportSkin"

	# Command's flags
	filePathFlagShort = "-fp"
	filePathFlagLong = "-filePath"

	helpFlagShort = "-h"
	helpFlagLong = "-help"

	# Private data
	__selList = om.MSelectionList()
	__filePath = None
	__export = True
	__import = False
	__meshPath = None
	__skinClusterFn = None
	# __skinClusterOutputGeometryPlug = None
	__components = None

	__skinData = {
		"mesh": "",
		"verts": 0,
		"influences": 0,
		"vertsPerInfluence": 0,
		"skinningMethod": 0,
		"normalizeWeights": 0,
		"weights": {},
	}


	@classmethod
	def creator(cls):
		"""Creator of the command.

		Method called by Maya to create an instance of this class.

		Returns:
			Class (Instance): Instance of the class that has been created

		"""
		return ExportSkinCommand()


	@classmethod
	def isUndoable(cls):
		"""This method is used to specify whether or not the command is undoable.

		Returns:
			bool: True if command is undobale, False if is not undoable (default)

		"""
		return False


	@classmethod
	def syntaxCreator(cls) -> om.MSyntax:
		"""Creates the command's MSyntax object.

		Returns:
			syntax (MSyntax): Command's syntax object.

		"""
		syntax = om.MSyntax()

		syntax.addFlag(cls.filePathFlagShort, cls.filePathFlagLong, om.MSyntax.kString)
		# syntax.addFlag(cls.exportFlagShort, cls.exportFlagLong, om.MSyntax.kBoolean)
		# syntax.addFlag(cls.importFlagShort, cls.importFlagLong, om.MSyntax.kBoolean)

		syntax.addFlag(cls.helpFlagShort, cls.helpFlagLong)

		syntax.setObjectType(om.MSyntax.kSelectionList, 1, 1)
		syntax.useSelectionAsDefault(True)

		return syntax


	def parseArguments(self, argList):
		"""Parses the commands's flag arguments.

		Can not be a @classmethod since we need to call the syntax method from the current instance.

		Args:
			argList (MArglist): List of arguments passed to the command.

		"""
		argDatabase = om.MArgDatabase(self.syntax(), argList)
		self.__selList = argDatabase.getObjectList()

		# File path flag
		if (argDatabase.isFlagSet(self.filePathFlagShort)):
			self.__filePath = argDatabase.flagArgumentString(self.filePathFlagShort, 0)

		# # Export flag
		# if (argDatabase.isFlagSet(self.exportFlagShort)):
		# 	# __commandMode = kCommandExport
		# 	self.__export = argDatabase.flagArgumentBool(self.exportFlagShort, 0)

		# # Import flag
		# if (argDatabase.isFlagSet(self.importFlagShort)):
		# 	# __commandMode = kCommandImport
		# 	self.__import = argDatabase.flagArgumentBool(self.importFlagShort, 0)

		# Display help
		if argDatabase.isFlagSet(self.helpFlagShort):
			self.displayHelp()


	def getMesh(self) -> bool:
		"""Gets the mesh node from the selected transform.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		self.__meshPath = self.__selList.getDagPath(0)

		if self.__meshPath.apiType() == om.MFn.kTransform:
			self.__meshPath.extendToShape()
	
			if self.__meshPath.apiType() == om.MFn.kMesh:
				self.__skinData["mesh"] = self.__meshPath.partialPathName()
				return True

		return False


	def getSkinCluster(self) -> bool:
		"""Gets the skinCluster node connected to the given mesh node.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		meshFn = om.MFnDependencyNode(self.__meshPath.node())
		meshInMeshPlug = meshFn.findPlug("inMesh", False)

		if meshInMeshPlug.isConnected:
			self.__skinClusterOutputGeometryPlug = meshInMeshPlug.source()

			skinClusterObj = self.__skinClusterOutputGeometryPlug.node()

			if skinClusterObj.apiType() == om.MFn.kSkinClusterFilter:
				self.__skinClusterFn = oma.MFnSkinCluster(self.__skinClusterOutputGeometryPlug.node())

				return True

		return False


	def getMeshComponents(self):
		"""Gets the mesh vertex components of the deformed mesh as an MObject.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		geoDataFn = om.MFnGeometryData(self.__skinClusterOutputGeometryPlug.asMObject())

		# Get mesh vertex components
		self.__components = geoDataFn.resolveComponentTagExpression(
			self.__skinClusterFn.name(),
			om.MFn.kMeshVertComponent
		)


	def getInfluenceWeights(self) -> bool:
		"""Gets the weights for all mesh vertex components for each influence.
		
		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		self.getMeshComponents()

		weights = self.__skinClusterFn.getWeights(self.__meshPath, self.__components, 0)
		influencePaths = self.__skinClusterFn.influenceObjects()

		totalVertexCount = weights.__len__()
		numInfluences = influencePaths.__len__()
		vertsPerInfluence = int(weights.__len__() / numInfluences)

		for ii in range(numInfluences):
			influenceName = influencePaths[ii].partialPathName()
			# We want to store the weights by influence without the namespace so it is easier
			# to import if the namespace is different
			influenceWithoutNamespace = self.removeNamespaceFromString(influenceName)
			self.__skinData["weights"][influenceWithoutNamespace] = (
				[weights[jj*numInfluences+ii] for jj in range(vertsPerInfluence)]
			)

		self.__skinData["influences"] = numInfluences
		self.__skinData["verts"] = totalVertexCount
		self.__skinData["vertsPerInfluence"] = vertsPerInfluence

		# Get skinning method and normalize weights plugs and add them to the skin data dictionary
		for plugName in ['skinningMethod', 'normalizeWeights']:
			skinClusterPlug = self.__skinClusterFn.findPlug(plugName, False)
			self.__skinData[plugName] = skinClusterPlug.asInt()

		if numInfluences > 0 and totalVertexCount > 0:
			return True
		else:
			return False


	def getExportSkinData(self):
		"""Wrapper method for getting all data that is required to export the skin file.

		Method sequence:
			getMesh()
			getSkinCluster()
			getInfluenceWeights()

		"""
		# Get the skin data 
		status = self.getMesh()
		if not status: raise RuntimeError(f"Could not retrieve mesh from: '{self.__meshPath.partialPathName()}'")

		status = self.getSkinCluster()
		if not status: raise RuntimeError(f"Could not retrieve skin cluster from: '{self.__meshPath.partialPathName()}'")

		status = self.getInfluenceWeights()
		if not status: raise RuntimeError(f"Could not retrieve influence weights from: '{self.__skinClusterFn.name()}'")


	def validateExportFilePath(self) -> bool:
		"""Validates the export file path.
		
		If no path was specified in the filePath flag it will call the file dialog to get the path.
		Secondly if the provided path does not have the .skin file extension in it, one will be added.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		# If the file path flag is not set open the file dialog to specify a path.
		if not self.__filePath:
			self.__filePath = cmds.fileDialog2(
				dialogStyle=2,
				fileMode=0,
				fileFilter=SkinCluster.skinFileFilter,
			)
			if not self.__filePath: return False
			# Get the first item from fileDialog2 as it returns an array with strings
			self.__filePath = self.__filePath[0]

		# Add the .skin extension if the path provided does not include it
		if not self.__filePath.endswith(SkinCluster.fileExtension):
			self.__filePath = f"{self.__filePath}{SkinCluster.fileExtension}"

		return True


	def saveSkinFile(self):
		"""Saves the specified file to disk with the json.dump method."""
		jsonFile = open(self.__filePath, "w")
		json.dump(self.__skinData, jsonFile, indent=2)
		jsonFile.close()


	def export(self):
		"""Exports the skindata to a .skin file to the specified output path."""
		status = self.validateExportFilePath()
		if not status: raise RuntimeError(f"Could not retrieve the export file path.")

		# Get export data
		self.getExportSkinData()

		# Write file
		self.saveSkinFile()

		# Print success message
		print(f"Successfully exported skin data to: '{self.__filePath}'")

		# print(self.__skinData)

		# Zero out the skin weights dictionary
		self.__skinData["weights"] = {}


	def doIt(self, argList):
		"""This method should perform a command by setting up internal class data.

		The actual action performed by the command should be done in the redoIt method. This is a pure 
		virtual method, and must be overridden in derived classes.

		Args:
			argList (MArgList): List of arguments passed to the command.

		"""
		self.parseArguments(argList)
	
		self.export()


	@classmethod
	def removeNamespaceFromString(cls, value) -> str:
		"""Removes namespaces from a string.

		Changes NAMESPACE:joint1|NAMESPACE:joint2 to joint1|joint2

		Args:
			value (string): String name with a namespace.

		Returns:
			string: The name without the namespaces

		"""
		tokens = value.split('|')
		result = ''
		for i, token in enumerate(tokens):
			if i > 0:
				result += '|'
			result += token.split(':')[-1]
		return result


	@classmethod
	def displayHelp(cls):
		"""Displays help for the command."""
		print(
			"Flags:\n"
			"   -fp -filePath             String     File path of the skin file.\n"
			"   -h  -help                 N/A        Display this text.\n"
		)



class ImportSkinCommand(om.MPxCommand):
	"""Skin import command for importing skin related data.

	User override of the MPxCommand class.


	TODO:
		getInfluenceWeights split into smaller methods
		skip the 0.0 influences?
		add support for multiple meshes
		add getBlendWeights support

	"""

	# Public data
	commandName = "importSkin"

	# Command's flags
	filePathFlagShort = "-fp"
	filePathFlagLong = "-filePath"

	helpFlagShort = "-h"
	helpFlagLong = "-help"

	# Private data
	__dgMod = om.MDGModifier()
	__selList = om.MSelectionList()
	__filePath = None
	__export = True
	__import = False
	__meshPath = None
	__skinClusterFn = None
	# __skinClusterOutputGeometryPlug = None
	__components = None

	__skinData = {
		"mesh": "",
		"verts": 0,
		"influences": 0,
		"vertsPerInfluence": 0,
		"skinningMethod": 0,
		"normalizeWeights": 0,
		"weights": {},
	}


	@classmethod
	def creator(cls):
		"""Creator of the command.

		Method called by Maya to create an instance of this class.

		Returns:
			Class (Instance): Instance of the class that has been created

		"""
		return ImportSkinCommand()


	@classmethod
	def isUndoable(cls):
		"""This method is used to specify whether or not the command is undoable.

		Returns:
			bool: True if command is undobale, False if is not undoable (default)

		"""
		return True


	@classmethod
	def syntaxCreator(cls) -> om.MSyntax:
		"""Creates the command's MSyntax object.

		Returns:
			syntax (MSyntax): Command's syntax object.

		"""
		syntax = om.MSyntax()

		syntax.addFlag(cls.filePathFlagShort, cls.filePathFlagLong, om.MSyntax.kString)

		syntax.addFlag(cls.helpFlagShort, cls.helpFlagLong)

		syntax.setObjectType(om.MSyntax.kSelectionList, 1, 1)
		syntax.useSelectionAsDefault(True)

		return syntax


	def parseArguments(self, argList):
		"""Parses the commands's flag arguments.

		Can not be a @classmethod since we need to call the syntax method from the current instance.

		Args:
			argList (MArglist): List of arguments passed to the command.

		"""
		argDatabase = om.MArgDatabase(self.syntax(), argList)
		self.__selList = argDatabase.getObjectList()

		# File path flag
		if (argDatabase.isFlagSet(self.filePathFlagShort)):
			self.__filePath = argDatabase.flagArgumentString(self.filePathFlagShort, 0)

		# Display help
		if argDatabase.isFlagSet(self.helpFlagShort):
			self.displayHelp()


	def getMesh(self) -> bool:
		"""Gets the mesh node from the selected transform.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		self.__meshPath = self.__selList.getDagPath(0)

		if self.__meshPath.apiType() == om.MFn.kTransform:
			self.__meshPath.extendToShape()
	
			if self.__meshPath.apiType() == om.MFn.kMesh:
				self.__skinData["mesh"] = self.__meshPath.partialPathName()
				return True

		return False


	def getSkinCluster(self) -> bool:
		"""Gets the skinCluster node connected to the given mesh node.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		meshFn = om.MFnDependencyNode(self.__meshPath.node())
		meshInMeshPlug = meshFn.findPlug("inMesh", False)

		if meshInMeshPlug.isConnected:
			self.__skinClusterOutputGeometryPlug = meshInMeshPlug.source()

			skinClusterObj = self.__skinClusterOutputGeometryPlug.node()

			if skinClusterObj.apiType() == om.MFn.kSkinClusterFilter:
				self.__skinClusterFn = oma.MFnSkinCluster(self.__skinClusterOutputGeometryPlug.node())

				return True

		return False


	def getMeshComponents(self):
		"""Gets the mesh vertex components of the deformed mesh as an MObject.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		geoDataFn = om.MFnGeometryData(self.__skinClusterOutputGeometryPlug.asMObject())

		# Get mesh vertex components
		self.__components = geoDataFn.resolveComponentTagExpression(
			self.__skinClusterFn.name(),
			om.MFn.kMeshVertComponent
		)


	def getInfluenceWeights(self) -> bool:
		"""Gets the weights for all mesh vertex components for each influence.
		
		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		self.getMeshComponents()

		weights = self.__skinClusterFn.getWeights(self.__meshPath, self.__components, 0)
		influencePaths = self.__skinClusterFn.influenceObjects()

		totalVertexCount = weights.__len__()
		numInfluences = influencePaths.__len__()
		vertsPerInfluence = int(weights.__len__() / numInfluences)

		for ii in range(numInfluences):
			influenceName = influencePaths[ii].partialPathName()
			# We want to store the weights by influence without the namespace so it is easier
			# to import if the namespace is different
			influenceWithoutNamespace = self.removeNamespaceFromString(influenceName)
			self.__skinData["weights"][influenceWithoutNamespace] = (
				[weights[jj*numInfluences+ii] for jj in range(vertsPerInfluence)]
			)

		self.__skinData["influences"] = numInfluences
		self.__skinData["verts"] = totalVertexCount
		self.__skinData["vertsPerInfluence"] = vertsPerInfluence

		# Get skinning method and normalize weights plugs and add them to the skin data dictionary
		for plugName in ['skinningMethod', 'normalizeWeights']:
			skinClusterPlug = self.__skinClusterFn.findPlug(plugName, False)
			self.__skinData[plugName] = skinClusterPlug.asInt()

		if numInfluences > 0 and totalVertexCount > 0:
			return True
		else:
			return False


	def getExportSkinData(self):
		"""Wrapper method for getting all data that is required to export the skin file.

		Calls:
			getMesh()
			getSkinCluster()
			getInfluenceWeights()

		"""
		# Get the skin data 
		status = self.getMesh()
		if not status: raise RuntimeError(f"Could not retrieve mesh from: '{self.__meshPath.partialPathName()}'")

		status = self.getSkinCluster()
		if not status: raise RuntimeError(f"Could not retrieve skin cluster from: '{self.__meshPath.partialPathName()}'")

		status = self.getInfluenceWeights()
		if not status: raise RuntimeError(f"Could not retrieve influence weights from: '{self.__skinClusterFn.name()}'")


	def validateExportFilePath(self) -> bool:
		"""Validates the export file path.
		
		If no path was specified in the filePath flag it will call the file dialog to get the path.
		Secondly if the provided path does not have the .skin file extension in it, one will be added.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		# If the file path flag is not set open the file dialog to specify a path.
		if not self.__filePath:
			self.__filePath = cmds.fileDialog2(
				dialogStyle=2,
				fileMode=0,
				fileFilter=SkinCluster.skinFileFilter,
			)
			if not self.__filePath: return False
			# Get the first item from fileDialog2 as it returns an array with strings
			self.__filePath = self.__filePath[0]

		# Add the .skin extension if the path provided does not include it
		if not self.__filePath.endswith(SkinCluster.fileExtension):
			self.__filePath = f"{self.__filePath}{SkinCluster.fileExtension}"

		return True


	def saveSkinFile(self):
		"""Saves the specified file to disk with the json.dump method."""
		jsonFile = open(self.__filePath, "w")
		json.dump(self.__skinData, jsonFile, indent=2)
		jsonFile.close()


	def export(self):
		"""Exports the skindata to a .skin file to the specified output path."""
		status = self.validateExportFilePath()
		if not status: raise RuntimeError(f"Could not retrieve the export file path.")

		# Get export data
		self.getExportSkinData()

		# Write file
		self.saveSkinFile()

		# Print success message
		print(f"Successfully exported skin data to: '{self.__filePath}'")

		# print(self.__skinData)

		# Zero out the skin weights dictionary
		self.__skinData["weights"] = {}


	def doIt(self, argList):
		"""This method should perform a command by setting up internal class data.

		The actual action performed by the command should be done in the redoIt method. This is a pure 
		virtual method, and must be overridden in derived classes.

		Args:
			argList (MArgList): List of arguments passed to the command.

		"""
		self.parseArguments(argList)

		if self.__export:	self.export()

		self.redoIt()


	def redoIt(self):
		"""This method should do the actual work of the command.
	
		Internal class data should be set in the doIt method.

		"""
		pass


	def undoIt(self):
		"""This method should undo the work done by the redoIt method."""
		pass


	@classmethod
	def removeNamespaceFromString(cls, value) -> str:
		"""Removes namespaces from a string.

		Changes NAMESPACE:joint1|NAMESPACE:joint2 to joint1|joint2

		Args:
			value (string): String name with a namespace.

		Returns:
			string: The name without the namespaces

		"""
		tokens = value.split('|')
		result = ''
		for i, token in enumerate(tokens):
			if i > 0:
				result += '|'
			result += token.split(':')[-1]
		return result


	@classmethod
	def displayHelp(cls):
		"""Displays help for the command."""
		print(
			"Flags:\n"
			"   -fp -filePath             String     File path of the skin file.\n"
			"   -h  -help                 N/A        Display this text.\n"
		)



def initializePlugin(pluginObj):
	"""Initialize the script plug-in.

	Args:
		pluginObj (MObject): The plugin to initialize

	"""
	pluginFn = om.MFnPlugin(pluginObj, "Lunatics", "0.2.1")
	pluginFn.registerCommand(
		ExportSkinCommand.commandName,
		ExportSkinCommand.creator,
		ExportSkinCommand.syntaxCreator,
	)

	pluginFn.registerCommand(
		ImportSkinCommand.commandName,
		ImportSkinCommand.creator,
		ImportSkinCommand.syntaxCreator,
	)


def uninitializePlugin(pluginObj):
	"""Unintialize the script plug-in.

	Args:
		pluginObj (MObject): The plugin to uninitialize

	"""
	pluginFn = om.MFnPlugin(pluginObj)
	pluginFn.deregisterCommand(ExportSkinCommand.commandName)
	pluginFn.deregisterCommand(ImportSkinCommand.commandName)
