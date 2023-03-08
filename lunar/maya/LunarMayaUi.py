# Built-in imports
# import json
# import platform
# import subprocess
import logging
# from collections import OrderedDict

# Third-party imports
from maya import cmds
# from maya import mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
from PySide2 import QtCore as qtc

# Custom imports



class LMViewport():
	"""Class wrapper for the 3d viewport.
	"""
	log = logging.getLogger("MViewport")


	@classmethod
	def getActiveViewport(cls) -> str or None:
		"""Gets the active 3d viewport.
		"""
		currentModelPanel = None
		for modelPanel in cmds.getPanel(type="modelPanel"):
			if cmds.modelEditor(modelPanel, query=True, activeView=True):
				currentModelPanel = modelPanel
				break
		if currentModelPanel: return currentModelPanel
		return False


	@classmethod
	def toggleXrayJoints(cls) -> bool:
		"""Toggles the xray joints state.
		"""
		activeViewport = cls.getActiveViewport()
		if activeViewport:
			statusXrayJoints = cmds.modelEditor(activeViewport, query=True, jointXray=True)
			cmds.modelEditor(activeViewport, edit=True, jointXray=not statusXrayJoints)
			return True
		cls.log.warning("Select a 3d viewport!")
		return False