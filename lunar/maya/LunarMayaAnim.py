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



class LMAnimControl(oma.MAnimControl):
	"""Wrapped MAnimControl class with additional methods.
	"""

	log = logging.getLogger("LMAnimControl")


	@classmethod
	def selectedStartEndTime(cls) -> tuple[om.MTime, om.MTime] or None:
		"""Gets the selected start and end time the timeslider.

		"""
		uiTimeSlider = cmds.lsUI(type="timeControl")[0]
		if uiTimeSlider:
			if cmds.timeControl(uiTimeSlider, query=True, rangeVisible=True):
				return tuple(om.MTime(time, om.MTime.uiUnit()) for time in cmds.timeControl(uiTimeSlider, query=True, rangeArray=True))

			cls.log.debug("No range is selected on the timeslider.")
			return None

		cls.log.error("No timeslider found - is maya working properly?.")
		return None


	@classmethod
	def activeStartEndTime(cls) -> tuple[om.MTime, om.MTime]:
		"""Gets the active time range.

		If nothing is selected on the timeslider the min / max range will be returned instead.

		"""
		timeRange = cls.selectedStartEndTime()
		if timeRange:
			return timeRange

		return tuple([time for time in [cls.minTime(), cls.maxTime()]])


	@classmethod
	def minMaxStartEndTime(cls) -> tuple[om.MTime, om.MTime]:
		"""Gets the min and max time range.

		If nothing is selected on the timeslider the min / max range will be returned instead.

		"""
		return tuple([time for time in [cls.minTime(), cls.maxTime()]])


	@classmethod
	def animationStartEndTime(cls) -> tuple[om.MTime, om.MTime]:
		"""Returns the animation start and end time.
		"""
		return tuple([time for time in [cls.animationStartTime(), cls.animationEndTime()]])


	@classmethod
	def startEndTimeFromAnimCurves(cls, nodes:list) -> tuple or None:
		"""Returns the first and last keyframes from all joints in a reference.
		"""
		if not nodes: return None

		listKeyframes = []
		for node in nodes:
			listKeyframes.append(cmds.keyframe(node, query=True, timeChange=True))

		listKeyframesSorted = sorted(listKeyframes)
		listStartEnd = []
		listStartEnd.append(min(listKeyframesSorted[0]))
		listStartEnd.append(max(listKeyframesSorted[1]))
				
		return tuple([om.MTime(keyframe, om.MTime.uiUnit()) for keyframe in listStartEnd])


	@classmethod
	def widestRange(cls, timeRange:list) -> tuple[om.MTime, om.MTime]:
		"""Returns the smallest and biggest time value in a tuple
		"""
		return tuple([time for time in [min(timeRange), max(timeRange)]])
		
		
	@classmethod
	def setStartTime(cls, timeStart:om.MTime):
		""""Sets and syncs start times for the scene.
		"""
		oma.MAnimControl.setAnimationStartTime(timeStart)
		oma.MAnimControl.setMinTime(timeStart)


	@classmethod
	def setEndTime(cls, timeStart:om.MTime):
		""""Sets and syncs end times for the scene.
		"""
		oma.MAnimControl.setAnimationEndTime(timeStart)
		oma.MAnimControl.setMaxTime(timeStart)


	@classmethod
	def setStartEndTime(cls, timeStart:om.MTime, timeEnd:om.MTime):
		""""Sets and syncs start and end times for the scene.
		"""
		oma.MAnimControl.setAnimationStartEndTime(timeStart, timeEnd)
		oma.MAnimControl.setMinMaxTime(timeStart, timeEnd)


	@classmethod
	def offsetKeyframes(cls, nodes, timeOffset):
		""""Offset all keyframes for the given object by the specified time offset
		"""
		cmds.keyframe(nodes, animation="objects", edit=True, relative=True, option="over", timeChange=timeOffset)


	@classmethod
	def setAutoKeyModeOffIfOn(cls) -> bool:
		"""Sets the AutoKeyMode off if is on.

		Returns:
			bool: Returns the initial state of the auto key mode.

		"""
		stateAutoKeyMode = oma.MAnimControl.autoKeyMode()
		if stateAutoKeyMode: oma.MAnimControl.setAutoKeyMode(False)

		return stateAutoKeyMode


	@classmethod
	def setAutoKeyModeOnIfOff(cls) -> bool:
		"""Sets the AutoKeyMode on if is off.

		Returns:
			bool: Returns the initial state of the auto key mode.

		"""
		stateAutoKeyMode = oma.MAnimControl.autoKeyMode()
		if not stateAutoKeyMode: oma.MAnimControl.setAutoKeyMode(True)

		return stateAutoKeyMode


	@classmethod
	def toggleAutoKeyMode(cls):
		"""Toggles the AutoKeyMode.

		Returns:
			bool: Returns the state of the auto key mode after the operation.

		"""
		oma.MAnimControl.setAutoKeyMode(not oma.MAnimControl.autoKeyMode())
		return oma.MAnimControl.autoKeyMode()





class LMTimeEditor():
	"""Wrapper class for the time editor.

	"""
	defaultComposition = "Composition1"

	log = logging.getLogger("LMTimeEditor")

	@classmethod
	def initTimeEditor(cls) -> None:
		"""Checks if there are any time editor compositions in the scene.

		If there are no time editor composition present in the scene it will create	Composition1,
		otherwise it will query the active composition.

		"""
		if not cmds.ls(type="timeEditorTracks"):
			cmds.timeEditorComposition("Composition1", createTrack=True)

		return cmds.timeEditorComposition(query=True, active=True)


	@classmethod
	def createClip(cls, objects:list, name:str, startFrame:int=None) -> None:
		"""Creates a time editor clip.

		Args:
			name (str): Name of the animation clip, it will be suffixed with _animClip
			startFrame (int): Starting frame of the animation clip
			endFrame (int): End frame - duration of the animation clip

		"""
		if not name.startswith("AS_"): name = f"AS_{name}"
		if not startFrame: startFrame = oma.MAnimControl.minTime().value()
		# if not endFrame: endFrame = oma.MAnimControl.maxTime().value()

		# nodes = cmds.ls(selection=True)
		listAttrs = []
		for object in objects:
			listAttrsKeyable = [attr.split("|")[-1] for attr in cmds.listAnimatable(object)]
			[listAttrs.append(attr) for attr in listAttrsKeyable]

		cmds.timeEditorClip(
			name,
			addObjects=";".join(listAttrs),
			startTime=startFrame,
			removeSceneAnimation=True,
			includeRoot=False,
			recursively=False,
			track=f"{cls.initTimeEditor()}:-1"
		)




class LMAnimBake():
	"""Wrappper class for custom baking.
	"""

	log = logging.getLogger("LMAnimBake")

	@classmethod
	def bakeTransform(cls, nodes:list, startEnd:tuple, preserveOutsideKeys:bool=True, simulation:bool=False, attributes:bool=['tx','ty','tz','rx','ry','rz']):
		cmds.bakeResults(
			nodes,
			attribute=attributes,
			# animation="objects",
			simulation=simulation,
			time=startEnd,
			sampleBy=1,
			oversamplingRate=1,
			disableImplicitControl=True,
			preserveOutsideKeys=preserveOutsideKeys,
			sparseAnimCurveBake=False,
			removeBakedAttributeFromLayer=False,
			removeBakedAnimFromLayer=False,
			# destinationLayer="BaseAnimation",
			bakeOnOverrideLayer=False,
			minimizeRotation=True,
			controlPoints=False,
			shape=False,
		)
