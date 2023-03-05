# Built-in imports
from abc import ABC, abstractmethod



class AbstractRetarget(ABC):
	"""Abstract retargeting class.

	TODO Add methods from MayaHumanIk

	"""

	# minimalDefinition = {}

	definition = {}


	@abstractmethod
	def validateDefinition(self) -> bool:
		"""Validates if at least a basic set of nodes required for characterization exists.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def getCharacters(self) -> list:
		"""Returns a list of all character nodes in the scene.

		Returns:
			list: All character nodes - valid and invalid characterizations.

		"""
		return False


	@abstractmethod
	def setPose(self, pose):
		"""Sets a pose from the given set-dictionary.

		Args:
			pose (dict): Dictonary with complete set of nodes and their values for all keyable attributes.

		"""
		pass


	@abstractmethod
	def setTPose(self) -> bool:
		"""Set a T-Pose in order to characterize the character / creature.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def getRoot(self) -> bool:
		"""Gets the root joint from the character definition dictionary.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def getExportNodes(self) -> list or None:
		"""Get the export nodes.

		Returns:
			list or None: All nodes that will be exported, otherwise None will be returned.

		"""
		return None


	@abstractmethod
	def characterExists(self) -> bool:
		"""Check if the specified object is a valid HiK character definition.

		Args:
			name (string): Character name to query.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def isValid(self) -> bool:
		"""Checks if the character is valid.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def createCharacterDefinition(self) -> bool:
		"""Creates a new HiK character definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def characterize(self) -> bool:
		"""Characterize the definition.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def isLocked(self) -> bool:
		"""Checks if the specified characters definition is locked.

		Returns:
			bool: Character locked state - True if the character is locked, False if unlocked.

		"""
		return False


	@abstractmethod
	def lockCharacter(self, value=True) -> bool:
		"""Set the lock state on the specified character.

		Args:
			lock (bool): Lock state - true is locked, false is unlocked.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def active(self) -> str or None:
		"""Gets the currently active character.

		Returns:
			str or None: Name of the active character, otherwise None.

		"""
		return None


	@abstractmethod
	def setActive(self, none=True) -> str or None:
		"""Sets the current object as the active character.

		Args:
			none: If set to False the active character will be set to None, otherwise it will set the
				current object as the active one.

		Returns:
			str or None: Name of the character that was set as active, otherwise None.

		"""
		return None


	@abstractmethod
	def bakeAnimation(self, startFrame=None, endFrame=None) -> bool:
		"""Bakes the animation on all character nodes for the current object.

		Args:
			startFrame (int): First frame, if none it will query the time sliders start frame.
			endFrame (int): Last frame, if none it will query the time sliders end frame.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
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
		return False


	@abstractmethod
	def deleteCharacterDefinition(self) -> bool:
		"""Deletes the character definition for the current object.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False
