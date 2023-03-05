# Built-in imports
import json
import platform
import subprocess
import logging
from collections import OrderedDict

# Third-party imports
from maya import cmds
from maya import mel
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
from PySide2 import QtCore as qtc

# Custom imports




class MTimeEditor():
	"""Wrapper class for the time editor.

	"""
	defaultComposition = "Composition1"

	log = logging.getLogger("MTimeEditor")


	@classmethod
	def createClip(cls, name:str, startFrame:int=None, endFrame:int=None) -> None:
		"""Creates a time editor clip.

		Args:
			name (str): Name of the animation clip, it will be suffixed with _animClip
			startFrame (int): Starting frame of the animation clip
			endFrame (int): End frame - duration of the animation clip

		"""
		if not name.startswith("AS_"): name = f"AS_{name}"
		if not startFrame: startFrame = oma.MAnimControl.minTime().value
		if not endFrame: endFrame = oma.MAnimControl.maxTime().value

		cmds.timeEditorClip(
			name,
			# addObjects=nodes,
			addSelectedObjects=True,
			includeRoot=True,
			recursively=True,
			removeSceneAnimation=True,
			startTime=startFrame,
			duration=endFrame-startFrame,
			type=["animCurveTL", "animCurveTA", "animCurveTT", "animCurveTU"],
			track=f"{cls.__initTimeEditor()}:-1"
		)


	@classmethod
	def __initTimeEditor(cls) -> None:
		"""Checks if there are any time editor compositions in the scene.

		If there are no time editor composition present in the scene it will create	Composition1,
		otherwise it will query the active composition.

		"""
		if not cmds.ls(type="timeEditorTracks"):
			cmds.timeEditorComposition("Composition1", createTrack=True)
		
		return cmds.timeEditorComposition(query=True, active=True)




class MAnimBake():
	"""Wrappper class for custom baking."""

	log = logging.getLogger("MAnimBake")


	@classmethod
	def bakeTransform(cls, nodes:list, startEnd:tuple, simulation:bool=False, attributes:bool=['tx','ty','tz','rx','ry','rz']):
		cmds.bakeResults(
			nodes,
			simulation=simulation,
			time=startEnd,
			sampleBy=1,
			oversamplingRate=1,
			disableImplicitControl=True,
			preserveOutsideKeys=False,
			sparseAnimCurveBake=False,
			removeBakedAttributeFromLayer=False,
			removeBakedAnimFromLayer=False,
			# destinationLayer="BaseAnimation",
			bakeOnOverrideLayer=False,
			minimizeRotation=True,
			controlPoints=False,
			shape=False,
			attribute=attributes,
		)
