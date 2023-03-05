# Built-in imports
import logging
from abc import ABC, abstractmethod

# Third-party imports




class AbstractRig(ABC):
	"""Abstract rig class.

	TODO:
		Add some basic methods and variables

	"""




	@abstractmethod
	def getCtrls(self) -> bool:
		"""Validates if at least a basic set of nodes required for characterization exists.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def getBones(self) -> bool:
		return False