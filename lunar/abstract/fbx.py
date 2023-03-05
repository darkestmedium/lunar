# Built-in imports
from abc import ABC, abstractmethod



class AbstractFbx(ABC):
	"""Abstract Fbx class."""


	@abstractmethod
	def gatherTakes(filePath) -> dict:
		"""Returns essential data regarding takes for the specified fbx file.

		Dictionary structure:
			{'Noesis Frames': {'index': 1, 'startFrame': 0.0, 'endFrame': 73.0}}

		Args
			filePath (str): File path to the fbx file.

		Returns:
			dict: Dictonary with all take names, indecxes, start and end frames, see dictonary
				structure.

		"""
		return False


	@abstractmethod
	def importAnimation(self, filePath) -> bool:
		pass


	@abstractmethod
	def exportAnimation(self, filePath) -> bool:
		pass
