# Built-in imports
import logging
from abc import ABC, abstractmethod

# Third-party imports



class AbstractRetargeter(ABC):
	"""Abstract retargeter class."""


	def validateInput(self):
		"""Validates if sources is a valid directory with files in it.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	@abstractmethod
	def retarget(self):
		"""Perform the actuall retargeting.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False
