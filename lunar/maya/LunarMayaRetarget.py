# Built-in imports
import os
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
import lunar.maya.LunarMaya as lm
import lunar.maya.LunarMayaAnim as lma

# HumanIk templates
import lunar.maya.resources.retarget.humanik as lmrrhi
import lunar.maya.resources.retarget.lunarctrl as lmrrlc
import lunar.maya.resources.retarget.sinnersdev as lmrrsd
import lunar.maya.resources.retarget.unreal as lmrrue




def __loadDependencies():
	"""Loads all dependencies (hik plugins and mel sources).
	"""
	# [cmds.loadPlugin(plugin) for plugin in ["mayaHIK", "mayaCharacterization", "retargeterNodes"] if cmds.pluginInfo(plugin, query=True, loaded=False)]
	# if cmds.pluginInfo("mayaHIK", query=True, loaded=False): 
	cmds.loadPlugin("mayaHIK")
	# if cmds.pluginInfo("mayaCharacterization", query=True, loaded=False): 
	cmds.loadPlugin("mayaCharacterization")
	# if cmds.pluginInfo("retargeterNodes", query=True, loaded=False): 
	cmds.loadPlugin("retargeterNodes")
	
	
	# "mayaCharacterization", "retargeterNodes"] 
	

	mel.eval('HIKCharacterControlsTool')

	mel.eval(f'source "hikCharacterControlsUI.mel"')
	mel.eval(f'source "hikGlobalUtils.mel"')
	mel.eval(f'source "hikDefinitionOperations.mel"')
	mel.eval(f'source "hikOverrides.mel"')

	log = logging.getLogger('LunarMayaRetarget')
	log.info("Successfully loaded all dependencies.")


if (om.MGlobal.mayaState() == om.MGlobal.kInteractive): __loadDependencies()




#--------------------------------------------------------------------------------------------------
# HumanIk Base
#--------------------------------------------------------------------------------------------------




class LMHumanIk():
	"""Retargeting with HumanIk in Maya, inherited from AbstractRetarget.

	Logic Flow:
	__init__():
		_initSetup():
			if isValid() ->	characterExists() -> isLocked() -> getPropertiesNode()
			
			if not valid ->	validateDefinition()

	TODO:
	 	bakeAnimation -> Add animationLayer support
		deleteAnimation -> ADD animationLayer support
		setSource -> ADD support for setting the stance, control rig option.
		setup mayaBatch -> create a gui independent mode (batch mode with ui scripts dependend

	"""
	minimalDefinition = lmrrhi.templateHik["minimalDefinition"]
	definition = lmrrhi.templateHik["definition"]

	rootMotion = "root"

	def __init__(self, name:str="HiK") -> None:
		"""Maya human ik init function for wrapping the in scene skeleton to the python object.
		"""
		self.log = logging.getLogger(f"{self.__class__.__name__} - {name}")

		# Get and set internal character name variables
		self.nameSpace = self.extractNameSpace(name)
		self.character = name

		self._initSetup()

		self.root = self.getRoot()
		self.rootMotion = self.getRootMotion()
		self.rootCnst = None


	def _initSetup(self):
		"""Tries to setup the character directly in the __init__ method.

		In case a character with the initiated name already exists, check if it is validated and assign
		class from its properties.

		"""
		if self.isValid():
			self.log.info(f"Initiated from existing character.")
		else:
			if self.validateDefinition:
				self.setupCharacter()
				self.valid = True
			else:
				self.log.critical("Could not validate definiton.")
				self.valid = False
				return


	def isValid(self) -> bool:
		"""Checks if the character is valid.

		1 Check if character exists.
		2 Check if character definition is locked.
		3 Check if character has a propertiesNode.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.characterExists():
			if self.isLocked():
				self.nodeProperties = self.getPropertiesNode()
				if self.nodeProperties:
					self.valid = True
					return self.valid

		self.valid = False
		return self.valid


	def characterExists(self) -> bool:
		"""Checks if the object is a valid HiK character node.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if cmds.objExists(self.character):
			if cmds.objectType(self.character) == "HIKCharacterNode":
				self.log.debug("Character exists and is a valid 'HIKCharacterNode'")
				return True

		return False
	

	def isLocked(self) -> bool:
		"""Checks if the specified characters definition is locked.

		Returns:
			bool: Character locked state - True if the character is locked, False if unlocked.

		"""		
		return cmds.getAttr(f'{self.character}.InputCharacterizationLock')


	def validateDefinition(self) -> bool:
		"""Validates if at least a basic set of nodes required for characterization exist.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		missingNodes = []
		for indx in self.minimalDefinition:
			node = self.returnNodeWithNameSpace(self.minimalDefinition[indx]["node"])
			if not cmds.objExists(node):
				missingNodes.append(node)

		if missingNodes:
			self.log.critical(
				f"Minimal definition could not be validated, the following nodes are missing: {missingNodes}."
			)
			return False

		self.log.info(f"Successfully validated definition.")
		return True


	def _isSourceValid(self, source) -> bool:
		"""Validates if the source is a valid HiK character.

		1 Check if character exists.
		2 Check if character definition is locked.

		Args:
			source (str): Name of the source character to validate

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		# First step check if it exists and is a valid HIKCharacterNode
		if cmds.objExists(self.character):
			if cmds.objectType(self.character) == "HIKCharacterNode":
				# Second step check if the characterization is locked on the source character
				if cmds.getAttr(f'{self.character}.InputCharacterizationLock'):
					self.log.debug(f"'{source}' as source input for {self.character} successfuly validated.")
					return True
		
		self.log.critical(f"'{source}' could not be validated as source input for {self.character}")
		return False


	def _updateUI(self, updateCharacter:bool=False, updateSource:bool=False) -> None:
		"""Updates the contextual HumanIk UI - not available in batch mode.

		Args:
			updateCharacter (bool): Wheter or not you want to update the current active character from
				the	contextual UI.
			updateSource (bool): Whether or not you want to update the source input contextuxal drop down
				which requires additional queries (slow).

		"""
		if updateCharacter:
			mel.eval('hikUpdateCharacterList')
			mel.eval('hikUpdateCurrentCharacterFromUI()')

		if updateSource:
			mel.eval('hikUpdateSourceList()')
			mel.eval('hikUpdateCurrentSourceFromUI')

		# Is always called when updating the HiK contextual UI
		mel.eval('hikUpdateContextualUI()')


	def extractNameSpace(self, name) -> str:
		"""Extracts namespaces from given name.

		Args:
			name (str): Name of the character which might contain namespace e.g. 'input:Hik'.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		splitName = name.split(':')

		# One namespace
		if len(splitName) == 2:
			self.log.debug(f"Successfully extracted namespace: '{splitName[0]}'.")
			return splitName[0]

		# Two and more namespaces
		elif len(splitName) > 2:
			splitName.pop()
			nameSpace = ":".join(splitName)
			self.log.debug(f"Successfully extracted namespace: '{nameSpace}'.")
			return nameSpace

		# No namespace
		else:  
			self.log.debug(f"'{name}' does not contain a namespace.")
			return False


	def returnNodeWithNameSpace(self, node) -> str:
		"""Checks if the class has a namespace and if it does it returns it.

		Args:
			node (str): Name of the node.

		Returns:
			str: Name of the node with namespace if one was set while initiating the class.

		"""
		if self.nameSpace: node = f'{self.nameSpace}:{node}'

		return node


	def getAttributesFromChannelBox(self, node) -> list:
		"""Gets all keyable attributes from channel box for the specified node.

		Args:
			node (str): Name of the node to return the attributes from.

		Returns:
			list: List with all keyable attributes e.g. ['translateX', 'translateY', 'translateZ']

		"""
		return [attr.split('.')[-1] for attr in cmds.listAnimatable(node)]


	def getPose(self, nodes) -> bool:
		"""Gets all values for translate and rotate for the selected nodes.

		Args:
			nodes (list): List with nodes to iterate over.

		Returns:
			dict: Dictonary with attribute values for the pose.

		"""
		pose = {}
		for node in nodes:
			pose[node] = {attr: cmds.getAttr(f'{node}.{attr}') for attr in self.getAttributesFromChannelBox(node)}

		return pose


	def setPose(self, pose):
		"""Sets a pose from the given set-dictionary.

		Args:
			pose (dict): Dictonary with complete set of nodes and their values for all keyable attributes.

		"""
		for node in pose:
			ctrl = self.returnNodeWithNameSpace(node)
			if not cmds.objExists(ctrl): continue
			for attr in pose[node]:
				attrNs = f'{ctrl}.{attr}'
				if cmds.getAttr(attrNs, settable=True):	cmds.setAttr(attrNs, pose[node][attr])


	def setTPose(self, moveToOrigin=False) -> bool:
		"""Set a T-Pose in order to characterize the character / creature.

		Args:
			moveToOrigin (bool): Whether or not you want to move the character to world origin
				(recommended for characterization).

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		for i in self.definition:
			node = self.returnNodeWithNameSpace(self.definition[i]["node"])
			if not cmds.objExists(node): continue
			for attr in ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]:
				try: cmds.setAttr(f'{node}.{attr}', 0)
				except:	pass

		if moveToOrigin:
			hipNode = self.returnNodeWithNameSpace(self.minimalDefinition["Hips"]["node"])
			if not cmds.objExists(hipNode): return False
			for attr in ["translateX", "translateZ"]:
				hipAttr = f'{hipNode}.{attr}'
				if cmds.getAttr(hipAttr, settable=True):
					cmds.setAttr(f'{hipNode}.{attr}', 0)

		self.log.info(f"T-pose was set for '{self.character}'")

		return True


	def setAPose(self):
		"""Sets the character / creature in A-Pose."""
		self.setPose(self.aPose)


	def fixFloorContact(self, fixPositiveY=False) -> bool:
		"""Fixes the contact position for better ground collisions solving.

		When setting the character in T-pose for characterizing sometimes the feet can be
		below the ground plane Y=0 resulting in a warning:
			file: C:/Program Files/Autodesk/Maya2022/scripts/others/hikDefinitionOperations.mel
			lunar 125: Feet appear to be located below the ground. Foot Bottom To Ankle value may be wrong.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		contactNode = self.returnNodeWithNameSpace(self.definition["LeftToeBase"]["node"])
		if not cmds.objExists(contactNode): return False

		hipNode = self.returnNodeWithNameSpace(self.definition["Hips"]["node"])
		if not cmds.objExists(hipNode): return False

		contactNodeYPosition = cmds.xform(contactNode, query=True, translation=True, worldSpace=True)[1]
		if contactNodeYPosition < 0:
			cmds.move(0, abs(contactNodeYPosition), 0, hipNode, worldSpace=True, relative=True)

		if fixPositiveY:
			if contactNodeYPosition > 0:
				cmds.move(0, -contactNodeYPosition, 0, hipNode, worldSpace=True, relative=True)

		return True


	def getRootMotion(self):

		node = self.returnNodeWithNameSpace(self.rootMotion)
		if cmds.objExists(node):
			return node
		
		logging.critical(f"Root motion node could not be retrieved for '{self.character}' character.")
		return False


	def getRoot(self) -> str or bool:
		"""Gets the root joint from the character definition dictionary.

		If the Reference slot is empty it will attempt to get get the HipsTranslation node and if that
		also does not exist it will lastly get the Hips node.

		Returns:
			str or bool: If the root joint does not exist False will be returned, if it does exist the
				node name will be returned as a string.

		"""
		# Firstly attempt to get the Reference node
		node = self.returnNodeWithNameSpace(self.definition['Reference']['node'])
		if cmds.objExists(node):
			return node
		else:
			# Secondly attempt to get the Hips node
			node = self.returnNodeWithNameSpace(self.definition['Hips']['node'])
			if cmds.objExists(node):
				return node
			else:
				# Thirdly attempt to get the HipsTranslation node
				node = self.returnNodeWithNameSpace(self.definition['HipsTranslation']['node'])
				if cmds.objExists(node):
					return node

		logging.critical(f"Root node could not be retrieved.")
		return False


	def getExportNodes(self) -> list or None:
		"""Get the export nodes.

		Returns:
			list or None: All nodes that will be exported, otherwise None will be returned.

		"""
		if self.getRoot():
			nodes = cmds.listRelatives(self.root, allDescendents=True, type="joint")
			nodes.append(self.root)
			# Make sure that at least the minimalDefinition set exists for export
			if nodes.__len__() >= self.minimalDefinition.__len__():
				return nodes
		
		self.log.critical(f"Could not retrieve minimal joint set.")
		return None


	def createCharacterDefinition(self) -> bool:
		"""Creates a new HiK character definition for the current object.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		self.character = mel.eval(f'hikCreateCharacter("{self.character}")')
		self.nodeProperties = self.getPropertiesNode()
		cmds.rename(self.nodeProperties, f'{self.character}Properties')
		self.nodeProperties = self.getPropertiesNode()

		return True


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.	

		"""
		self.setTPose()
		self.fixFloorContact()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()

		solverNode = self.getSolverNode()
		if solverNode != 0: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode != 0: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True


	def characterize(self) -> None:
		"""Characterize the skeleton definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		for i in self.definition:
			node = self.returnNodeWithNameSpace(self.definition[i]["node"])
			if not cmds.objExists(node): continue
			mel.eval(f'setCharacterObject("{node}", "{self.character}", {self.definition[i]["id"]}, 0);')


	def lockCharacter(self, value=True):
		"""Set the lock state on the specified character.

		Args:
			lock (bool): Lock state - true is locked, false is unlocked.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		lockState = self.isLocked()
		# TODO fix print statement if mel.eval actually failed
		if value and lockState is False:
			mel.eval('hikToggleLockDefinition;')

		if not value and lockState is True:
			mel.eval('hikToggleLockDefinition;')


	def active(self) -> str or None:
		"""Gets the currently active character.

		Reference:
			hikGlobalUtils.mel -> hikGetCurrentCharacter()

		Returns:
			str or None: Name of the active character, otherwise None.

		"""
		if self.characterExists():
			activeCharacter = mel.eval("$tempVar=$gHIKCurrentCharacter")
			if activeCharacter:	return activeCharacter

		return None


	def setActive(self, none=True) -> str or None:
		"""Sets the current object as the active character.

		Reference:
			hikGlobalUtils.mel -> hikSetCurrentCharacter()

		Args:
			none: If set to False the active character will be set to None, otherwise it will set the
				current object as the active one.

		Returns:
			str or None: Name of the character that was set as active, otherwise None.

		"""
		if none == False:
			mel.eval(f'global string $gHIKCurrentCharacter; $gHIKCurrentCharacter=""')
			self._updateUI(updateCharacter=True)
			
		if none == True:
			if self.valid:
				mel.eval(f'global string $gHIKCurrentCharacter; $gHIKCurrentCharacter="{self.character}"')
				self._updateUI(updateCharacter=True)
				self.log.debug(f"'{self.character}' was set as the active character.")
				return self.character

			self.log.critical(f"'{self.character}' is invalid and could not be set as the active character.")

		return None


	def source(self) -> str or None:
		"""Gets the current source input for the currently active character from the contextual UI.

		Reference:
			hikGlobalUtils.mel -> hikGetCurrentSource()

		Returns:
			str or None: Name of the current character that is currently plugged in as source, otherwise None will
				be returned instead.

		"""
		currentSource = mel.eval("$tempVar=$gHIKCurrentSource")
		if currentSource: return currentSource

		return None


	def setSource(self, source) -> str or None:
		"""Sets the specifed input as source for the current object.

		TODO ADD support for setting the stance, control rig option.

		Args:
			source (str): Name of the character to be set as source input.

		Returns:
			str or None: Name of the character that was set as source input, otherwise None.

		"""
		if source == "None":
			mel.eval(f'hikSetCharacterInput("{self.character}", "")')
			self._updateUI(updateSource=True)
		else:
			if self.valid:
				if self._isSourceValid(source):
					if self.active != self.character: self.setActive()
					if source != self.source():
						mel.eval(f'hikSetCharacterInput("{self.character}", "{source}")')
						self._updateUI(updateSource=True)
						self.log.debug(f"'{source}' was set as source input for '{self.character}'")
					else:
						self.log.debug(f"'{source}' is already set as source input for '{self.character}'")

					return source

				self.log.critical(f"'{source}' could not be validated as source input for '{self.character}'")

		return None


	def getCharacters(self) -> list or None:
		"""Returns a list of all hik character nodes in the scene.

		Returns:
			list of strings or None: All hik character nodes found in the scene, None if scene does not
				contain any.

		"""
		characterNodes = cmds.ls(type="HIKCharacterNode")

		if characterNodes: return characterNodes

		return None


	def getCharacterNodes(self) -> list or False:
		"""Returns a list with all nodes that are pluged into the specified character definition.

		Returns:
			list: List of all characterized nodes if any were found, False otherwise.

		"""
		if self.characterExists():
			return mel.eval(f'hikGetSkeletonNodes "{self.character}"')

		return False


	def getNode(self, node, attribute, type, source, destination):
		"""Returns the specified node type at the given input / output.
		
		Args:
			node (str): Name of the node.
			attribute (str): Name of the attribute.
			type (str): Type of the node to be filtered.
			source (bool): 
		
		"""
		connections = cmds.ls(
			cmds.listConnections(f'{node}.{attribute}', source=source, destination=destination),
			type=type
		)
		if len(connections) >= 1:
			self.nodeProperties = connections[0]
			return self.nodeProperties
		
		return False


	def getPropertiesNode(self) -> str or False:
		"""Returns the HIKPropertie2State node if one is connected to the character definition.

		Returns:
			string or bool: Name of the HIKPropertie2State node is there is one connected,
				otherwise it will return False.

		"""
		node = self.getNode(self.character, 'propertyState', 'HIKProperty2State', True, False)
		if node: return node

		return False


	def getSolverNode(self) -> str or False:
		"""Returns the HIKSolverNode node if one is connected to a character definition.

		Returns:
			string or bool: Name of the HIKSolverNode node is there is one connected,
				otherwise it will return False.

		"""
		if self.characterExists():
			node = self.getNode(self.character, 'OutputCharacterDefinition', 'HIKSolverNode', False, True)
			if node: return node

		return False


	def getState2SkNode(self) -> str or False:
		"""Returns the HIKPropertie2State node if one is connected to a character definition.

		A fully valid HumanIk definition has the following connections:

			HIKPropeties.message -> HIKCharacterNode.propertyState

			HIKChracterNode.OutputCharacterDefinition -> HIKSolverNode.InputCharacterDefinition
																								-> HIKState2SK.InputCharacterDefinition

			HIKSolverNode.OutputCharacterState -> HIKState2SK.InputCharacterState

		Returns:
			string or bool: Name of the HIKPropertie2State node is there is one connected,
				otherwise it will return False.

		"""
		if self.characterExists():
			node = self.getNode(self.character, 'OutputCharacterDefinition', 'HIKState2SK', False, True)
			if node: return node

		return False


	def getRetargeterNode(self) -> str or False:
		"""Returns the HIKRetargeterNode node if one is connected to a character definition.

		Returns:
			string or bool: Name of the HIKRetargeterNode node is there is one connected,
				otherwise it will return False.

		"""
		if self.characterExists():
			node = self.getNode(self.character, 'OutputCharacterDefinition', 'HIKRetargeterNode', False, True)
			if node: return node

		return False


	def setMatchSource(self, value=True) -> bool:
		"""Sets the match source option on the hik properties node for the current object.

		Args:
			value (bool): If set to True - match source will be ON, False - OFF

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.		

		"""
		if self.valid:
			cmds.setAttr(f'{self.nodeProperties}.ForceActorSpace', value)
			self.log.debug(f"Match source option was set to '{value}' for '{self.character}'")
			return True
		
		self.log.critical(f"'{self.character}' is invalid, cannot continue.")
		return False
	

	def setFeetGroundContact(self, value=True) -> bool:
		"""Sets the feet ground contact option on the hik properties node.

		Args:
			value (bool): If set to True - feet ground contact will be ON, False - OFF

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.		

		"""
		if self.isValid():
			cmds.setAttr(f'{self.nodeProperties}.FloorContact', value)
			self.log.debug(f"Feet ground contact option was set to '{value}' for '{self.character}'")
			return True

		self.log.critical(f"'{self.character}' is invalid, cannot continue.")
		return False


	def setMirror(self, value=True) -> bool:
		"""Sets the mirror animation option on the hik properties node.

		Args:
			value (bool): If set to True - mirror animation will be ON, False - OFF

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			cmds.setAttr(f'{self.nodeProperties}.Mirror', value)
			self.log.debug(f"Mirror animation option was set to '{value}' for '{self.character}'")
			return True

		self.log.critical(f"'{self.character}' is invalid, cannot continue.")
		return False


	def setReachActorChest(self, value) -> bool:
		"""Sets the reach actor chest attribute on the hik properties node.

		Args:
			value (Float): Float value of the reach actor chest attribute.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			cmds.setAttr(f'{self.nodeProperties}.ReachActorChest', value)
			self.log.debug(f"Reach actor chest attribute was set to '{value}' for '{self.character}'")
			return True
		
		self.log.critical(f"'{self.character}' is invalid, cannot continue.")
		return False


	def filterRotations(self, nodes):
		"""Filters the euler rotations on specified animations curves.

		Args:
			nodes (list): List with nodes to filter the animations curves.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if len(nodes) >= 1:
			animCurves = []
			for node in nodes:
				for attr in ['rx', 'ry', 'rz']:
					connections = cmds.ls(
						cmds.listConnections(f'{node}.{attr}', source=True, destination=False),
						type='animCurve'
					)
					if len(connections) >= 1: animCurves.append(connections[0])

			cmds.filterCurve(animCurves)
			return True

		return False


	def getExportNodes(self) -> bool:
		"""Gets the export nodes.

		The export nodes may be different than the character nodes there more a seprate
		method is nesseccary for quering them between different rigs.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			nodes = self.getCharacterNodes()

			if len(nodes) >= 1: return nodes

		return False


	def cleanUpPairBlendNodes(self):
		# Clean up pairBlend nodes after bake
		# TODO this could be probably better
		state2SKNode = self.getState2SkNode()
		pairBlendNodes = cmds.listConnections(state2SKNode, type='pairBlend')
		if pairBlendNodes: cmds.delete(pairBlendNodes)

	
	def connectSourceAndSaveAnimNew(self, pTransform:str, pSrcT:str="", pSrcR:str="", forcePairBlendCreation:bool=True):
		"""Python override of the global proc connectSourceAndSaveAnimNew()

		If nodes already has sources, create a pairblend to preserve the animation.

		Note: 
			pairBlends are just supporting T and R, not S, anim on S will be lost if $pSrcS is set.

		Args:
			pTransform (string): The transform for which the pairBlend node will be created.
			pSrcT (string):	State2SK nodes output translation attribute.
			pSrcR (string): State2SK nodes output rotation attribute.
			forcePairBlendCreation (int): Whether or not we want to force creation of the pairBlend node.

		"""
		nbSrc = 0

		if forcePairBlendCreation:
			for attr in ["translate", "translateX", "translateY", "translateZ", "rotate",	"rotateX", "rotateY", "rotateZ"]:
				connections = cmds.listConnections(f"{pTransform}.{attr}", destination=False, source=True)
				if connections:	nbSrc += len(connections)

		if forcePairBlendCreation or nbSrc:
			animatableAttributes = [attr.split('.')[-1] for attr in cmds.listAnimatable(pTransform)]
			pairBlend = cmds.pairBlend(node=pTransform, attribute=animatableAttributes)
			if pSrcT != "":	cmds.connectAttr(pSrcT, f"{pairBlend}.inTranslate2")
			if pSrcR != "":cmds.connectAttr(pSrcR, f"{pairBlend}.inRotate2")
			cmds.setAttr(f"{pairBlend}.weight", True)
			cmds.setAttr(f"{pairBlend}.currentDriver", True)

		else:
			if pSrcT != "":
				if cmds.getAttr(f"{pTransform}.translateX", lock=True) == 0: cmds.connectAttr(f"{pSrcT}x", f"{pTransform}.translateX")
				if cmds.getAttr(f"{pTransform}.translateY", lock=True) == 0: cmds.connectAttr(f"{pSrcT}y", f"{pTransform}.translateY")
				if cmds.getAttr(f"{pTransform}.translateZ", lock=True) == 0: cmds.connectAttr(f"{pSrcT}z", f"{pTransform}.translateZ")

			if pSrcR != "":
				if cmds.getAttr(f"{pTransform}.translateX", lock=True) == 0: cmds.connectAttr(f"{pSrcR}x", f"{pTransform}.rotateX")
				if cmds.getAttr(f"{pTransform}.translateY", lock=True) == 0: cmds.connectAttr(f"{pSrcR}y", f"{pTransform}.rotateY")
				if cmds.getAttr(f"{pTransform}.translateZ", lock=True) == 0: cmds.connectAttr(f"{pSrcR}z", f"{pTransform}.rotateZ")


	def setSourceAndBake(self, source, startFrame=None, endFrame=None,  oversamplingRate=1):
		"""Wrapper method for setting the source and baking in one go."""
		self.setSource(source)
		self.bakeAnimation(startFrame, endFrame)


	def bakeAnimation(self, startFrame=None, endFrame=None) -> bool:
		"""Bakes the animation of characterized nodes.

		Args:
			startFrame (int): First frame, if none it will query the timesliders start frame.
			endFrame (int): Last frame, if none it will query the timesliders end frame.
			oversamplingRate (int): Number of frames in between full frames, use for upresing the animation
				from 30 to 60 fps.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			nodes = self.getExportNodes()
			if nodes.__len__() >= self.minimalDefinition.__len__():

				if not startFrame: startFrame = oma.MAnimControl.minTime().value()
				if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

				lma.LMAnimBake.bakeTransform(nodes, (startFrame, endFrame))
				self.filterRotations(nodes)

				self.cleanUpPairBlendNodes()

				self.setSource("None")

				self.log.info(f"Successfully baked animation from '{startFrame}' to '{endFrame}'")
				return True

		return False


	def exportAnimation(self, filePath, startFrame=None, endFrame=None, bake=False) -> bool:
		"""Exports the animation to the specified path.

		Currently only FBX export is supported. If start and end frames are not specified it will grab
		the current time slider range.

		Args:
			filePath (str): Path to the exported file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			bake (bool): Whether or not to perform the bake operation on fbx export.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if not startFrame: startFrame = oma.MAnimControl.minTime().value()
		if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

		cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		# Check if visibility is off, if it is turn it off
		# attribute.editLocked(f"{self.root}.visibility", True)

		cmds.select(self.root)

		lm.LMFbx.exportAnimation(filePath, startFrame, endFrame, bake)

		# cmds.setAttr(f"{self.root}.visibility", False)


	def deleteAnimation(self) -> bool:
		"""Deletes all animation curve nodes on the current object.

		TODO ADD animationLayer support
		TODO fix pairBlend connection

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		# get character nodes
		nodes = self.getCharacterNodes()
		if nodes:
			# get all animation curve nodes
			animCurves = cmds.listConnections(nodes, type='animCurve')
			if animCurves:
				# check if it is from a referenced source
				for animCurve in animCurves:
					if not cmds.referenceQuery(animCurve, isNodeReferenced=True):
						cmds.delete(animCurve)
				return True

		return False


	def deleteCharacterDefinition(self) -> bool:
		"""Deletes the character definition for the current object.
		
		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.characterExists():
			if not cmds.referenceQuery(self.character, isNodeReferenced=True):
				mel.eval(f'deleteCharacter("{self.character}")')
				self.character = None
				self.nodeProperties = None
				self.valid = False
				self.log.debug(f"'{self.character}' character was successfully deleted.")
				return True

			self.log.critical(f"'{self.character}' character is from a referenced file and can't be deleted.")

		self.log.debug(f"'{self.character}' character does not exist - nothing to delete.")
		return False


	def __str__(self) -> str:
		"""String representation of the HiK object.

		Returns:
			self.character (str): String name of the character that has been characterized.

		"""
		return self.character




#--------------------------------------------------------------------------------------------------
# Unreal Engine
#--------------------------------------------------------------------------------------------------




class LMMetaHuman(LMHumanIk):
	"""Class for setting up the MetaHuman skeleton in Maya.

	Contains full hik joint definition which propagates down to the UE5 and UE4 Skeleton
	TODO replace print with logger
	TODO Bake to Ik and Fk?
	TODO split the metahuman rig into body and rig file

	"""
	minimalDefinition = lmrrue.templateMH["minimalDefinition"]
	definition = lmrrue.templateMH["definition"]
	tPose = lmrrue.templateMH["tPose"]
	aPose = lmrrue.templateMH["aPose"]


	def accessoryJoints(self, value=False):
		"""Hides additional joints on the metahuman rig."""

		referenceNode = self.returnNodeWithNameSpace(self.definition['Reference']['node'])
		if not cmds.objExists(referenceNode): return False

		nodes = cmds.listRelatives(referenceNode, allDescendents=True, type="joint")

		jointSuffixes = [
			"_twist", "_corrective", "_latissimus", "_latissimus", "_out", "_scap", "_pec",
			"_bck", "_fwd", "_inn", "_in", "_pip", "_bulge", "_mcp", "_inn", "_slide", "_dip",
			"_palm", "_half", "DHIhead:spine_04"
		]
		for node in nodes:
			for suffix in jointSuffixes:
				if suffix in node:
					cmds.setAttr(f"{node}.visibility", value)


	def setTPose(self) -> None:
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def setAPose(self) -> None:
		"""Sets the character / creature in A-Pose."""
		self.setPose(self.aPose)


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.	

		"""
		self.setTPose()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()
		self.setAPose()

		solverNode = self.getSolverNode()
		if solverNode: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True
	

	def importSetup(self):
		"""Wrapper method for setup from scratch with import."""
		self.setUpAxis()
		self.orient()
		self.accessoryJoints()
		self.setupCharacter()
		self.setAPose()


	def setSource(self, source, rootMotion=True, rootRotationOffset=0) -> bool:
		"""Set source for the specified character.

		TODO Try to make it work without the ui
		TODO validate source

		"""
		if source == "None":
			mel.eval(f'hikSetCharacterInput("{self.character}", "")')
			self._updateUI(updateSource=True)

		else:
			if self.valid:
				if self._isSourceValid(source):
					if self.active != self.character: self.setActive()
					if source != self.source():
						mel.eval(f'hikSetCharacterInput("{self.character}", "{source}")')

						# Root motion setup outside Hik feautres. (Manual override)
						if rootMotion:
							self.rootCnst = cmds.parentConstraint(source.rootMotion, self.rootMotion, mo=False)[0]
							cmds.setAttr(f"{self.rootCnst}.target[0].targetOffsetRotateX", rootRotationOffset)

						self._updateUI(updateSource=True)
						self.log.debug(f"'{source}' was set as source input for '{self.character}'")
					else:
						self.log.debug(f"'{source}' is already set as source input for '{self.character}'")

					return source

				self.log.critical(f"'{source}' could not be validated as source input for '{self.character}'")

		return None


	def getExportNodes(self) -> bool:
		"""Gets the export nodes.

		The exports nodes may be different than the character nodes there more a seprate
		method is nesseccary for quering them between different rigs.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if self.isValid():
			nodes = cmds.listRelatives(self.rootMotion, allDescendents=True, type="joint")
			nodes.append(self.rootMotion)
			if len(nodes) >= 1: return nodes

		return False


	def bakeAnimation(self, startFrame=None, endFrame=None) -> bool:
		"""Bakes the animation of characterized nodes.

		Args:
			startFrame (int): First frame, if none it will query the timesliders start frame.
			endFrame (int): Last frame, if none it will query the timesliders end frame.
			oversamplingRate (int): Number of frames in between full frames, use for upresing the animation
				from 30 to 60 fps.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			nodes = self.getCharacterNodes()
			nodes.append(self.rootMotion)

			if len(nodes) >= len(self.minimalDefinition):

				if not startFrame: startFrame = cmds.playbackOptions(minTime=True, query=True)
				if not endFrame: endFrame = cmds.playbackOptions(maxTime=True, query=True)

				lma.LMAnimBake.bakeTransform(nodes, (startFrame, endFrame))
				self.filterRotations(nodes)

				self.cleanUpPairBlendNodes()
				if self.rootCnst: cmds.delete(self.rootCnst)

				if cmds.attributeQuery("blendParent1", node=self.rootMotion, exists=True):
					cmds.deleteAttr(self.rootMotion, attribute="blendParent1")

				self.setSource("None")

				self.log.info(f"Successfully baked animation from '{startFrame}' to '{endFrame}'")
				return True

		return False



class LMMannequinUe5(LMMetaHuman):
	"""Class for setting up the mannequin ue5 rig in maya.

	TODO replace print with logger
	TODO hookUp rootMotion reconnect method
	TODO methodForHidingGeometries for retargeting and baking
	TODO hookup ik joints

	"""
	tPose = lmrrue.templateUe5["tPose"]
	aPose = lmrrue.templateUe5["aPose"]


	def setTPose(self):
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def importSetup(self):
		"""Wrapper method for setup from scratch with import."""

		self.accessoryJoints()

		self.setupCharacter()

		self.setAPose()



class LMMannequinUe4(LMMetaHuman):
	"""Class for setting up the mannequin ue4 rig in maya.

	TODO replace print with logger
	TODO hookUp rootMotion reconnect method
	TODO methodForHidingGeometries for retargeting and baking
	TODO hookup ik joints

	"""
	tPose = lmrrue.templateUe4["tPose"]
	aPose = lmrrue.templateUe4["aPose"]



class LMMannequinAsRig(LMMetaHuman):
	"""Class for setting up the UE5 manneuqin rigged with Advanced Skeleton in Maya.

	TODO hookUp rootMotion reconnect method
	TODO methodForHidingGeometries for retargeting and baking
	TODO hookup ik joints

	"""
	minimalDefinition = lmrrue.templateASC["minimalDefinition"]
	definition = lmrrue.templateASC["definition"]
	tPose = lmrrue.templateASC["tPose"]
	aPose = lmrrue.templateASC["aPose"]

	rootMotion = "RootMotion"

	def setTPose(self) -> None:
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.	

		"""
		self.setTPose()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()

		solverNode = self.getSolverNode()
		if solverNode: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True


	def importSetup(self):
		"""Wrapper method for setup from scratch with import."""

		self.accessoryJoints()

		self.setupCharacter()

		self.setAPose()


	def getExportNodes(self) -> bool:
		"""Gets the export nodes.

		The exports nodes may be different than the character nodes there more a seprate
		method is nesseccary for quering them between different rigs.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if self.isValid():
			# TODO TEMP SinndersDev Workaround
			nodes = self.getCharacterNodes()

			if len(nodes) >= 1: return nodes

		return False


	def bakeAnimation(self, startFrame=None, endFrame=None, oversamplingRate=1) -> bool:
		"""Bakes the animation of characterized nodes.

		Args:
			startFrame (int): First frame, if none it will query the timesliders start frame.
			endFrame (int): Last frame, if none it will query the timesliders end frame.
			oversamplingRate (int): Number of frames in between full frames, use for upresing the animation
				from 30 to 60 fps.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			nodes = self.getCharacterNodes()
			nodes.append(self.rootMotion)

			if len(nodes) >= len(self.minimalDefinition):

				if not startFrame: startFrame = cmds.playbackOptions(minTime=True, query=True)
				if not endFrame: endFrame = cmds.playbackOptions(maxTime=True, query=True)

				cmds.bakeResults(
					nodes,
					simulation=False,
					time=(startFrame, endFrame),
					sampleBy=1,
					oversamplingRate=oversamplingRate,
					disableImplicitControl=True,
					preserveOutsideKeys=False,
					sparseAnimCurveBake=False,
					removeBakedAttributeFromLayer=False,
					removeBakedAnimFromLayer=False,
					bakeOnOverrideLayer=False,
					minimizeRotation=True,
					controlPoints=False,
				 	shape=False,
					attribute=['tx','ty','tz','rx','ry','rz']
				)
				# self.filterRotations(nodes)

				# Clean up pairBlend nodes and constraints after bake
				# TODO this could be probably better
				state2SKNode = self.getState2SkNode()
				pairBlendNodes = cmds.listConnections(state2SKNode, type='pairBlend')
				if pairBlendNodes: cmds.delete(pairBlendNodes)
				if self.rootCnst: cmds.delete(self.rootCnst)

				self.setSource("None")

				self.log.info(f"'Successfully baked from '{startFrame}' to '{endFrame}'")
				return True

		return False



class LMMannequinAsSkeleton(LMMetaHuman):
	"""Class for setting up the UE5 manneuqin export skeleton in Maya.

	TODO hookUp rootMotion reconnect method
	TODO methodForHidingGeometries for retargeting and baking
	TODO hookup ik joints

	"""
	tPose = lmrrue.templateASS["tPose"]
	aPose = lmrrue.templateASS["aPose"]

	def exportAnimation(self, filePath, startFrame=None, endFrame=None, bake=False) -> bool:
		"""Exports the animation to the specified path.

		Currently only FBX export is supported. If start and end frames are not specified it will grab
		the current time slider range.

		Args:
			filePath (str): Path to the exported file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			bake (bool): Whether or not to perform the bake operation on fbx export.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if not startFrame: startFrame = cmds.playbackOptions(minTime=True, query=True)
		if not endFrame: endFrame = cmds.playbackOptions(maxTime=True, query=True)

		cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		# Unhide the joints for export
		exportNode = self.returnNodeWithNameSpace("Export")
		cmds.setAttr(f"{exportNode}.visibility", True)

		cmds.select(self.rootMotion)
		lm.LMFbx.exportAnimation(filePath, startFrame, endFrame, bake)

		# Unhide the joints after export
		cmds.setAttr(f"{exportNode}.visibility", False)




#--------------------------------------------------------------------------------------------------
# Lunar Rig
#--------------------------------------------------------------------------------------------------




class LMLunarCtrl(LMHumanIk):
	"""Class for setting up the Maya Lunar Control rig in Maya.

	Must share same namespace with the MLunarExport. Used for animating inside Maya.

	TODO:
		Sync with other modules / classes
	
	"""
	definition = lmrrlc.templateLC["definition"]
	tPose = lmrrlc.templateLC["tPose"]
	aPose = lmrrlc.templateLC["aPose"]

	CtrlMain = "main_ctrl"
	rootMotion = "root_ctrl"
	exportRoot = "root"

	CtrlIk = [
		"arm_ik_l_ctrl", "arm_ik_r_ctrl", "arm_pv_l_ctrl", "arm_pv_r_ctrl",
		"leg_ik_l_ctrl", "leg_ik_r_ctrl", "leg_pv_l_ctrl", "leg_pv_r_ctrl",
		"head_ik_ctrl",
	]

	ctrlIkEffectors = {
		"LeftArmHandle":		"arm_ik_l_ctrl",
		"LeftArmPv": 				"arm_pv_l_ctrl",
		"RightArmHandle": 	"arm_ik_r_ctrl",
		"RightArmPv": 			"arm_pv_r_ctrl",
		"LeftLegHandle": 		"leg_ik_l_ctrl",
		"LeftLegPv": 				"leg_pv_l_ctrl",
		"RightLegHandle": 	"leg_ik_r_ctrl",
		"RightLegPv": 			"leg_pv_r_ctrl",
		"HeadHandle": 			"head_ik_ctrl",
	}
	CtrlIkHandles = ["arm_ik_l_ctrl", "arm_ik_r_ctrl", "leg_ik_l_ctrl", "leg_ik_r_ctrl"]
	CtrlFkHands = ["hand_l_ctrl", "hand_r_ctrl"]

	AttrIk = ["headFkIk", "leftArmFkIk", "rightArmFkIk", "leftLegFkIk", "rightLegFkIk"]


	def __init__(self, name="HiK") -> None:
		"""Maya human ik init function for wrapping the in scene skeleton to the python object."""
		# Get and set internal character name variables
		self.log = logging.getLogger(f"{self.__class__.__name__} - {name}")
		
		self.nameSpace = self.extractNameSpace(name)
		self.character = name

		self._initSetup()

		self.nodeProperties = self.getPropertiesNode()
		self.nodeState2Sk = self.getState2SkNode()
	
		self.CtrlMain = self.getCtrlMain()
		self.root = self.getRoot()
		self.rootMotion = self.getRootMotion()


	def getCtrlMain(self):

		node = self.returnNodeWithNameSpace(self.CtrlMain)
		if cmds.objExists(node):
			return node
		
		logging.critical(f"Main ctrl could not be retrieved for '{self.character}' character.")
		return False


	def setTPose(self):
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def setAPose(self):
		"""Sets the character / creature in A-Pose.
		
		Since the lunar rig is set to 0 values for transformation call the parent class set t-pose method.
		
		"""
		self.setPose(self.aPose)


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.	

		"""
		self.setTPose()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()
		self.setAPose()

		solverNode = self.getSolverNode()
		if solverNode: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True


	def setSource(self, source, rootMotion=True, rootRotationOffset=0) -> bool:
		"""Set source for the specified character.

		TODO Try to make it work without the ui

		"""
		if source == "None":
			mel.eval(f'hikSetCharacterInput("{self.character}", "")')
			self._updateUI(updateSource=True)

		else:
			if self.valid:
				if self._isSourceValid(source):
					if self.active != self.character: self.setActive()
					if source != self.source():
						mel.eval(f'hikSetCharacterInput("{self.character}", "{source}")')

						self.setCtrlsIkToFk()

						# Start override of hik setSource method
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace("pelvis_rot_ctrl"),
							f"{self.nodeState2Sk}.HipsR",
							# f"{self.nodeState2Sk}.LeftHandR",
						)
		
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["LeftArmHandle"]),
							f"{self.nodeState2Sk}.LeftHandT",
							f"{self.nodeState2Sk}.LeftHandR",
						)
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["LeftArmPv"]),
							f"{self.nodeState2Sk}.LeftForeArmT",
							# f"{self.nodeState2Sk}.LeftForeArmR",
						)

						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["RightArmHandle"]),
							f"{self.nodeState2Sk}.RightHandT",
							f"{self.nodeState2Sk}.RightHandR",
						)
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["RightArmPv"]),
							f"{self.nodeState2Sk}.RightForeArmT",
							# f"{self.nodeState2Sk}.RightForeArmR",
						)
	
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["LeftLegHandle"]),
							f"{self.nodeState2Sk}.LeftFootT",
							f"{self.nodeState2Sk}.LeftFootR",
						)
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["LeftLegPv"]),
							f"{self.nodeState2Sk}.LeftLegT",
							# f"{self.nodeState2Sk}.LeftLegR",
						)

						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["RightLegHandle"]),
							f"{self.nodeState2Sk}.RightFootT",
							f"{self.nodeState2Sk}.RightFootR",
						)
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["RightLegPv"]),
							f"{self.nodeState2Sk}.RightLegT",
							# f"{self.nodeState2Sk}.RightLegR",
						)
						self.connectSourceAndSaveAnimNew(
							self.returnNodeWithNameSpace(self.ctrlIkEffectors["HeadHandle"]),
							f"{self.nodeState2Sk}.HeadT",
							f"{self.nodeState2Sk}.HeadR",
						)

						# Root motion setup outside Hik feautres. (Manual override)
						if rootMotion:
							self.rootCnst = cmds.parentConstraint(source.rootMotion, self.rootMotion, mo=False)[0]
							cmds.setAttr(f"{self.rootCnst}.target[0].targetOffsetRotateX", rootRotationOffset)

						self._updateUI(updateSource=True)
						self.log.debug(f"'{source}' was set as source input for '{self.character}'")
					else:
						self.log.debug(f"'{source}' is already set as source input for '{self.character}'")

					return source

				self.log.critical(f"'{source}' could not be validated as source input for '{self.character}'")

		return None


	def getExportNodes(self) -> list:
		"""Gets the export nodes.

		The exports nodes may be different than the character nodes there more a seprate
		method is nesseccary for quering them between different rigs.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if self.isValid():
			nodes = cmds.listRelatives(self.CtrlMain, allDescendents=True, type="transform")
			nodes.append(self.CtrlMain)
			if len(nodes) >= 1: return nodes

		return []


	def getCtrlsIk(self) -> bool:

		if self.isValid():
			ikCtrlsWithNameSpace = []
			[ikCtrlsWithNameSpace.append(self.returnNodeWithNameSpace(Ctrl)) for Ctrl in self.CtrlIk]
			return ikCtrlsWithNameSpace

		return False


	# def getCtrlIkHandles(self) -> list:

	# 	ListCtrlsNamespace = []
	# 	if self.isValid():
	# 		[ListCtrlsNamespace.append(self.returnNodeWithNameSpace(Ctrl)) for Ctrl in self.CtrlIkHandles]

	# 	return ListCtrlsNamespace


	def getCtrlFkHand(self):

		ListCtrlsNamespace = []
		if self.isValid():
			[ListCtrlsNamespace.append(self.returnNodeWithNameSpace(Ctrl)) for Ctrl in self.CtrlFkHands]

		return ListCtrlsNamespace
	

	def setCtrlsIkToFk(self):

		ListFkHand = self.getCtrlFkHand()
		[cmds.setAttr(f"{self.CtrlMain}.{attr}", 0) for attr in self.AttrIk]

		[cmds.setAttr(f"{ctrl}.fist", 50) for ctrl in ListFkHand]
		[cmds.setAttr(f"{ctrl}.spread", 50) for ctrl in ListFkHand]


	def __validateIkCtrlsBeforeBaking(self, ikCtrls):
		for ctrl in ikCtrls:
			if cmds.objExists(ctrl):
				animAttributes = cmds.listAnimatable(ctrl)
				for attribute in animAttributes:
					numKeyframes = cmds.keyframe(attribute, query=True, keyframeCount=True)
					if numKeyframes == 0:
						print(f"ctrl: {ctrl} has no animation, setting keyframe")
						cmds.setKeyframe(ctrl)


	def bakeAnimation(self, startFrame=None, endFrame=None, oversamplingRate=1) -> bool:
		"""Bakes the animation of characterized nodes.

		Args:
			startFrame (int): First frame, if none it will query the timesliders start frame.
			endFrame (int): Last frame, if none it will query the timesliders end frame.
			oversamplingRate (int): Number of frames in between full frames, use for upresing the animation
				from 30 to 60 fps.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if self.isValid():
			nodes = self.getExportNodes()

			if nodes.__len__() >= self.minimalDefinition.__len__():

				if not startFrame: startFrame = oma.MAnimControl.minTime().value()
				if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

				# Needs one cpu cycle after import to properly move ik solvers
				oma.MAnimControl.setCurrentTime(om.MTime(startFrame, om.MTime.uiUnit()))

				lma.LMAnimBake.bakeTransform(nodes, (startFrame, endFrame), True)
				self.filterRotations(nodes)

				# Clean up
				self.cleanUpPairBlendNodes()
				if self.rootCnst: cmds.delete(self.rootCnst)

				if cmds.attributeQuery("blendParent1", node=self.rootMotion, exists=True):
					cmds.deleteAttr(self.rootMotion, attribute="blendParent1")

				self.setSource("None")
				
				# oma.MAnimControl.setCurrentTime(om.MTime(startFrame, om.MTime.uiUnit()))

				self.log.info(f"Successfully baked animation from '{startFrame}' to '{endFrame}'")
				return True

		return False


	def deleteAnimationOnIk(self) -> bool:
		"""Deletes all animation curve nodes on the current object.

		TODO ADD animationLayer support
		TODO fix pairBlend connection

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		# get character nodes
		nodes = self.getCtrlsIk()
		if nodes:
			# get all animation curve nodes
			animCurves = cmds.listConnections(nodes, type='animCurve')
			if animCurves:
				# check if it is from a referenced source
				for animCurve in animCurves:
					if not cmds.referenceQuery(animCurve, isNodeReferenced=True):
						cmds.delete(animCurve)
				return True

		return False


	def exportAnimation(self, filePath, startFrame=None, endFrame=None, bake=False) -> bool:
		"""Exports the animation to the specified path.

		Currently only FBX export is supported. If start and end frames are not specified it will grab
		the current time slider range.

		Args:
			filePath (str): Path to the exported file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			bake (bool): Whether or not to perform the bake operation on fbx export.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if not startFrame: startFrame = oma.MAnimControl.minTime().value()
		if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

		cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		self.mainCtrl = self.returnNodeWithNameSpace(self.mainCtrl)

		# Check if visibility is off, if it is turn it off
		if not cmds.getAttr(f"{self.mainCtrl}.controlsVisibility"):
			cmds.setAttr(f"{self.mainCtrl}.controlsVisibility", True)

		cmds.select(self.mainCtrl)

		lm.LMFbx.exportAnimation(filePath, startFrame, endFrame, bake)



class LMLunarExport(LMMannequinUe5):
	"""Class for setting up the Maya Lunar Export Skeleton rig in Maya.

	Must share same namespace with the MLunarCtrl. Used for exporting animation to the game engine.

	"""
	# mainCtrl = "main_ctrl"
	
	# ModDg = om.MDGModifier()


	def exportAnimation(self, filePath, startFrame=None, endFrame=None, bake=False) -> bool:
		"""Exports the animation to the specified path.

		Currently only FBX export is supported. If start and end frames are not specified it will grab
		the current time slider range.

		Args:
			filePath (str): Path to the exported file.
			startFrame (int): Start frame of the animation.
			endFrame (int): End frame of the animation.
			bake (bool): Whether or not to perform the bake operation on fbx export.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		if not startFrame: startFrame = oma.MAnimControl.minTime().value()
		if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

		cmds.playbackOptions(minTime=startFrame, maxTime=endFrame, edit=True)

		# Get the main ctrl with namespace
		CtrlMain = self.returnNodeWithNameSpace(LMLunarCtrl.CtrlMain)
		# FnMainCtrl = om.MFnDependencyNode(coreApi.getObjectFromString(mainCtrl))
		# PlugExportSkeletonVisibility = FnMainCtrl.findPlug("exportSkeletonVisibility", False)
		# # Check if visibility is off,
		# # We need to do this with the api since the file can be referenced and we don't want to chek for that
		# IsVisible = PlugExportSkeletonVisibility.asBool()
		# if not IsVisible:
		# 	if PlugExportSkeletonVisibility.isLocked:	PlugExportSkeletonVisibility.setLocked(False)
		# 	PlugExportSkeletonVisibility.setBool(True)
		# 	self.ModDg.doIt()

		# Check if visibility is off, if it is turn it off check if referenced file
		IsVisible = cmds.getAttr(f"{CtrlMain}.exportSkeletonVisibility")
		IsSelectable = cmds.getAttr(f"{CtrlMain}.exportSkeletonDisplayType")
		if not IsVisible:
			cmds.setAttr(f"{CtrlMain}.exportSkeletonVisibility", True)
		if IsSelectable != 0:
			cmds.setAttr(f"{CtrlMain}.exportSkeletonDisplayType", 0)

		cmds.select(self.rootMotion)

		lm.LMFbx.exportAnimation(filePath, startFrame, endFrame, bake)

		# Hide it back
		if not IsVisible:
			cmds.setAttr(f"{CtrlMain}.exportSkeletonVisibility", False)
			# PlugExportSkeletonVisibility.setBool(False)
			# self.ModDg.doIt()
		if IsSelectable != 0:
			cmds.setAttr(f"{CtrlMain}.exportSkeletonDisplayType", IsSelectable)




#--------------------------------------------------------------------------------------------------
# Sinners dev
#--------------------------------------------------------------------------------------------------




class LMSinnersDev2(LMHumanIk):
	"""Class for setting up the Sinners Dev Rig in Maya with HumanIk.

	TODO add scaleGrp to root
	TODO upade eccessoryJoint with new self.root and self.getExportNodes

	"""
	minimalDefinition = lmrrsd.templateSD2["minimalDefinition"]
	definition = lmrrsd.templateSD2["definition"]
	tPose = lmrrsd.templateSD2["tPose"]
	aPose = lmrrsd.templateSD2["aPose"]

	rootMotion = "trajectory"


	def accessoryJoints(self, value=False):
		"""Hides additional joints on the metahuman rig."""

		if self.root and cmds.objExists(self.root):
			jointSuffixes = ["_helper", "_prop", "_grp", "headb"]
			for node in self.getExportNodes():
				node = self.returnNodeWithNameSpace(node)
				for suffix in jointSuffixes:
					if suffix in node:
						cmds.setAttr(f"{node}.visibility", value)
			return True

		return False


	def importCleanUp(self) -> bool:
		"""Sequence of commands to clean up the imported file."""

		if self.root and cmds.objExists(self.root):
			for node in self.getExportNodes():
				cmds.setAttr(f'{node}.radius', 0.1)
			return True

		return False


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.	

		"""
		# self.importCleanUp()
		self.setTPose()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()

		solverNode = self.getSolverNode()
		if solverNode: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True


	def setTPose(self):
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def setAPose(self):
		"""Sets the character / creature in A-Pose."""
		self.setPose(self.aPose)


	def importSetup(self):
		"""Wrapper method for setup from scratch with import."""

		self.importCleanUp()
		self.accessoryJoints()
		

		# self.setupCharacter()




class LMSinnersDev1(LMHumanIk):
	"""Class for setting up the Sinners Dev Rig in Maya with HumanIk.

	TODO add scaleGrp to root
	TODO upade eccessoryJoint with new self.root and self.getExportNodes

	"""
	minimalDefinition = lmrrsd.templateSD1["minimalDefinition"]
	definition = lmrrsd.templateSD1["definition"]
	tPose = lmrrsd.templateSD1["tPose"]
	aPose = lmrrsd.templateSD1["aPose"]


	def accessoryJoints(self, value=False):
		"""Hides additional joints on the metahuman rig."""

		if self.root and cmds.objExists(self.root):
			jointSuffixes = ["_helper", "_prop", "_grp", "headb"]
			for node in self.getExportNodes():
				node = self.returnNodeWithNameSpace(node)
				for suffix in jointSuffixes:
					if suffix in node:
						cmds.setAttr(f"{node}.visibility", value)
			return True

		return False


	def importCleanUp(self) -> bool:
		"""Sequence of commands to clean up the imported file."""

		if self.root and cmds.objExists(self.root):
			for node in self.getExportNodes():
				cmds.setAttr(f'{node}.radius', 0.1)
			return True

		return False


	def setupCharacter(self) -> bool:
		"""Sequence of methods for setting up the character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.	

		"""
		# self.importCleanUp()
		self.setTPose()
		self.createCharacterDefinition()
		self.characterize()
		self.lockCharacter()

		solverNode = self.getSolverNode()
		if solverNode: cmds.rename(solverNode, f'{self.character}Solver')

		state2kSKNode = self.getState2SkNode()
		if state2kSKNode: cmds.rename(state2kSKNode, f'{self.character}State2SK')

		return True


	def setTPose(self):
		"""Sets the character / creature in T-Pose."""
		self.setPose(self.tPose)


	def setAPose(self):
		"""Sets the character / creature in A-Pose."""
		self.setPose(self.aPose)


	def importSetup(self):
		"""Wrapper method for setup from scratch with import."""

		self.importCleanUp()
		self.accessoryJoints()

		self.setupCharacter()




#--------------------------------------------------------------------------------------------------
# Retargeter
#--------------------------------------------------------------------------------------------------




class LMRetargeter():
	"""Maya retargeter class.

	TODO:
		Better error checking - true / False raiseRuntimeError (cpp MStatus style)

		Support decimal precision frames
		Add progress bar
		Print procesin clip X out of 250
		If retargeter crashes don't retarget files that already exist in output directory
		Create Validation method for checking if fbx file has animation and the required / specified
			content define in the constructor.
		!Sometimes the fbx is not imported Content/Animations/External/UTA have to manualy import it
		Add support for scaling clips x2 x1.5 whatever
		Add batch mode with uiScripts openMaya
		Add override existing clips in output folder

	"""
	totalClipCount = 0
	currentClip = 0

	log = logging.getLogger("MRetargeter")

	def __init__(self,
		sources,
		targets,
		outputDirectory,
		sourceNameSpace="",
		sourceTemplate="HumanIk",
		targetNameSpace="Output",
		targetTemplate="MetaHuman",
		sourceFilters=["*.fbx"],
		targetFilters=["*.mb", "*.ma"],
	):
		# checkStatus function does not return the exact error line number
		self.sources = self.validateInput(sources, sourceFilters)
		if not self.status: raise RuntimeError(f"Could not validate any sources from: {sources}")

		self.targets = self.validateInput(targets, targetFilters)
		if not self.status: raise RuntimeError(f"Could not validate any targets from: {targets}")

		# Internal variables
		self.inputDirectory = qtc.QFileInfo(sources[0])
		self.outputDirectory = qtc.QFileInfo(outputDirectory)
		self.sourceNameSpace = sourceNameSpace
		self.sourceTemplate = sourceTemplate
		self.targetNameSpace = targetNameSpace
		self.targetTemplate = targetTemplate


	@classmethod
	def __str__(cls) -> str:
		return f"MayaRetargeter - HumanIk retargeter for Maya."


	def validateInput(self, entry, nameFilters) -> list[qtc.QFileInfo] or bool:
		"""Validates the specified input.

		If the entry is a string containing a file or directory it will be appended	to the
		items list. If the entry is a list of strings it will be re-assigned as the	items list.

		Args:
			entry (List[str] or str): Entries for validation, can be single string with files	or list with
				single files or directories

		Returns:
			list[qtc.QFileInfo] and self.status(bool): List with QFileInfo objects if found any	and
				status - True if the operation was successful, otherwise False.

		"""
		entries = []
		if type(entry) == str:
			entries.append(entry)

		if type(entry) == list:
			entries = entry

		filePathList = []
		for entry in entries:
			fileInfo = lm.LMFinder.validateFileInfo(entry)  # Check if entry exists
			if fileInfo:
				if fileInfo.isDir():
					self.log.debug(f"Entry '{entry}' is a directory.")
					fileInfoList = lm.LMFinder.getFilesInDirectory(entry, nameFilters)
					if fileInfoList:
						for fileInfo in fileInfoList:
							self.log.debug(f"Adding entry '{fileInfo.filePath()}'")
							filePathList.append(fileInfo.filePath())

				if fileInfo.isFile():
					self.log.debug(f"Adding entry '{fileInfo.filePath()}' which is a single file.")
					filePathList.append(fileInfo.filePath())

		if filePathList.__len__() != 0:
			fileInfoList = []
			filePathSet = set(filePathList)  # Make sure entries are not duplicated
			for filePath in filePathSet:
				fileInfoList.append(qtc.QFileInfo(filePath))

			self.log.info(f"'{fileInfoList.__len__()}' entries have been successfully validated.")

			self.status = True
			return fileInfoList

		self.status = False


	def __getClipsInOutputDir(self):
		"""Gets existing clips in output directory."""
		# __compareInputOutputClips()
		pass


	def __compareInputOutputClips(self):
		"""Compare input with existing output clips and return the result."""
		pass


	def nameOutputClip(self):
		pass


	def initRig(self, slotTemplate, name="HiK", nameSpace=None) -> bool:
		"""Initiates the rig with the coresponding class for the specified slot.

		Args:
			slotTemplate (str): Template for initiation	['HumanIk', 'Mannequin', 'MetaHuman', 'SinnersDev']
			nameSpace (str): Name space to use for the rig
 
		Returns:
			slot (Class): Initialized class ['MayaHumanIk', 'MayaMannequin', 'LMMetaHuman', 'MayaSinnersDev'] 

		"""
		if nameSpace:	name = f'{nameSpace}:{name}'

		if slotTemplate == 'HumanIk':
			slot = LMHumanIk(name)

		elif slotTemplate == 'LunarCtrl':
			slot = LMLunarCtrl(name)

		elif slotTemplate == 'LunarExport':
			slot = LMLunarExport(name)
	
		elif slotTemplate == 'MannequinUe4':
			slot = LMMannequinUe4(name)

		elif slotTemplate == 'MannequinUe5':
			slot = LMMannequinUe5(name)

		elif slotTemplate == 'MetaHuman':
			slot = LMMetaHuman(name)

		elif slotTemplate == 'SinnersDev2':
			slot = LMSinnersDev2(name)

		elif slotTemplate == 'SinnersDev1':
			slot = LMSinnersDev1(name)

		else:
			self.log.critical(f"'{slotTemplate}' slot rig type unsupported!")
			return False

		return slot


	def setupTarget(self, matchSource, reachActorChest) -> bool:
		"""Sets up the target rig."""

		lm.LMFile.load(self.targets[0].filePath(), self.targetNameSpace)

		name = "HiK"
		if self.targetTemplate == "LunarExport":
			name = "Export"

		self.target = self.initRig(self.targetTemplate, name, self.targetNameSpace)

		return True


	def setupSource(self) -> bool:

		lm.LMFile.load(self.sources[0].filePath())

		# Temp Sinners override
		if self.sourceTemplate == 'SinnersDev2':
			# # self.source.importSetup()
			locator = cmds.spaceLocator(name='scaleGrp')
			cmds.parent('trajectory', locator)
			cmds.scale(100, 100, 100, locator)
			rootMotion = "trajectory"
			nodes = cmds.listRelatives(rootMotion, allDescendents=True, type="joint")
			nodes.append(rootMotion)
			[cmds.setAttr(f'{node}.radius', 0.01) for node in nodes]
		
		# Temp Sinners1 override
		if self.sourceTemplate == 'SinnersDev1':
			# self.source.importSetup()
			locator = cmds.spaceLocator(name='scaleGrp')
			cmds.parent('NUXRoot', locator)
			cmds.scale(100, 100, 100, locator)
		
		self.source = self.initRig(self.sourceTemplate, self.sourceNameSpace)

		return True


	def scaleAnimation(self, value=1.0):
		"""Scales the animation by the given amount."""
		pass


	def deleteConnection(self, plug):
		if cmds.connectionInfo(plug, isDestination=True):
			plug = cmds.connectionInfo(plug, getExactDestination=True)
			readOnly = cmds.ls(plug, ro=True)
			#delete -icn doesn't work if destination attr is readOnly 
			if readOnly:
				source = cmds.connectionInfo(plug, sourceFromDestination=True)
				cmds.disconnectAttr(source, plug)
			else:
				cmds.delete(plug, icn=True)


	def __doRetargeting(self, preserveFolderHierarchy, trimStart, trimEnd, oversamplingRate, rootMotion, rootRotationOffset):
		"""Wrapper method for sequencing retargeting calls."""
		# Iterate through source list with QFileInfo's
		for source in self.sources:
			# Get takes name and start / end frame
			takes = lm.LMFbx.gatherTakes(source.filePath())
			for take in takes:
				index = takes[take]['index']
				startFrame = takes[take]['startFrame'] + trimStart
				endFrame = takes[take]['endFrame'] + trimEnd

				lm.LMFbx.importAnimation(source.filePath(), startFrame, endFrame, index)

				# Test
				self.target.deleteAnimation()
				# self.setSourceAndBake(self.source)
				self.target.setTPose()
				self.target.setSource(self.source, rootMotion, rootRotationOffset)
				self.target.bakeAnimation(startFrame, endFrame)

				if preserveFolderHierarchy:
					self.outputFile = qtc.QFileInfo(source.filePath().replace(self.inputDirectory.absolutePath(), self.outputDirectory.filePath()))
					lm.LMFinder.createDirectory(self.outputFile.absolutePath())
				else:
					self.outputFile = qtc.QFileInfo(f'{self.outputDirectory.filePath()}/{source.fileName()}')

				if takes.__len__() > 1: self.outputFile = f'{self.outputFile}_{take}'

				self.log.info(f"Exporting '{source.fileName()}' ...")
				# TODO cleanUp
				cmds.select(f'{self.targetNameSpace}:root')
				self.target.exportAnimation(self.outputFile.filePath(), startFrame, endFrame)
				self.log.info(f"Successfully exported '{self.outputFile.filePath()}'")


	def retarget(self,
		preserveFolderHierarchy=True,
		overwriteExisting=False,
		matchSource=True,
		reachActorChest=0.0,
		trimStart=0.0,
		trimEnd=0.0,
		# scaleAnimation=1.0,
		oversamplingRate=1,
		rootMotion=True,
		rootRotationOffset=0,
	) -> bool:
		"""Performs the actuall retargeting.

		TODO:
			add oversamplingRate attr to every instance
			add trimStart, trimEnd flags

		Args:
			overwriteExisting (bool): If you want to overwrite clips that already exist in the output directory.
			matchSource (bool): Wheter or not to use the match source option on the HIK solver.
			trimStart (int): Trim the start time of the clip by the given amount of frames.
			trimEnd (int): Trim the end time of the clip by the given amount of frames.
			scaleAnimation (float): Scales the animation by the given amount e.x. 2.0 will extend the length
				two times.
			oversamplingRate (int): Number of frames in between full frames, use for upresing the animation
				from 30 to 60 fps.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		status = self.setupTarget(matchSource, reachActorChest)
		if not status: raise RuntimeError(f"Could not setup target from: '{self.targets[0].filePath()}'")

		status = self.setupSource()
		if not status: raise RuntimeError(f"Could not setup source from: '{self.sources[0].filePath()}'")

		# Set solver attributes
		if matchSource: self.target.setMatchSource()
		if reachActorChest: self.target.setReachActorChest(reachActorChest)

		lm.LMFinder.createDirectory(self.outputDirectory.absolutePath())
		# if not status: raise RuntimeError(f"Could not setup output directory: '{self.outputDirectory}'")

		self.__doRetargeting(preserveFolderHierarchy, trimStart, trimEnd, oversamplingRate, rootMotion, rootRotationOffset)

		return True




if __name__ == "__main__":
	# import importlib
	from maya import cmds
	# from lunar.maya.retarget import unreal
	# [importlib.reload(module) for module in [retargeter, lunar]]

	# finder = Finder()
	# # Source list
	# sourceList = finder.getFilesInDirectory("C:/Users/lukyb/Desktop/Animations/Mocap/Anton/input/traversal")
	# # print(sourceList)
	# alredyRetargetedList = finder.getFilesInDirectory("C:/Users/lukyb/Desktop/npc/Manny")
	# alredyRetargetedFileNameList = [retargeted.fileName() for retargeted in alredyRetargetedList]
	# missingRetargetList = []
	# for anim in sourceList:
	# 	if anim.fileName() not in alredyRetargetedFileNameList:
	# 		missingRetargetList.append(anim.filePath())

	cmds.file(new=True, force=True)

	retargeter = LMRetargeter(
		sources=[
			# "C:/Users/lbiernat/My Drive/Bambaa/Content/Sinners/Animations/Mocap/Player/player-gestures/AS_player_backpack_adjust_01__part.fbx",
			# "/Users/luky/My Drive/Bambaa/Content/Sinners/Animations/Mocap/Player",
			"/Users/luky/My Drive/Bambaa/Content/Sinners/Animations/Mocap/Player/anim-player-movement-push-pull",
		],
		targets=["/Users/luky/My Drive/Bambaa/Content/Sinners/Characters/Player/AnimationKit/Rigs/RIG_Player.ma"],
		outputDirectory="/Users/luky/Desktop/push_pull",
		# sourceNameSpace="Anton",
		sourceTemplate="SinnersDev2",
		# sourceTemplate="MannequinUe5",
		targetNameSpace="Player",
		targetTemplate="LunarExport",
	)

	retargeter.retarget(
		preserveFolderHierarchy=False,
		trimStart=1,  # if baking from sinnersDev set
		matchSource=True,
		# reachActorChest=1.0,
		oversamplingRate=1,
		# rootMotion=True,
		rootRotationOffset=-90, # if baking from sinnersDev set
	)