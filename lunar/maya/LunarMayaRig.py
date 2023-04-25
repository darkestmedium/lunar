# Built-in imports
import json
import platform
import subprocess
import logging
from collections import OrderedDict

# Third-party imports
from maya import cmds
import maya.OpenMaya as om

from PySide2 import QtCore as qtc

# Custom imports
import lunar.maya.LunarMaya as lm




#--------------------------------------------------------------------------------------------------
# Controllers
#--------------------------------------------------------------------------------------------------




class Ctrl():
	"""Class for building the rig controller.
	"""
	defaultTransparency = 0.15
	defaultLineWidth = 2.0
	defaultFingerLineWidth = 2.0
	defaultLockShapeAttributes = False

	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 90.0),
		localScale=(2.0, 2.0, 2.0),
		shape="circle",
		fillShape=False,
		drawFkIkState=False,
		fkIkStatePosition=(0.0, 0.0, 0.0),
		fillTransparency=defaultTransparency,
		lineWidth=defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		"""Init method of the Controller class.

		Args:
			name (string): Name of the controller.
			localScale (float): Scale of the rigController - edits localScaleXYZ attrs on the shape node.
			translateTo (string): Reference object the controller's position.
			rotateTo (string): Reference object for the controller's orientation.
			parent (string): Name of the parent object of the controller.
			shape (string): Name of the display shape of the controller.
			fillShape (bool): Whether or not you want to draw a full shape or just the wireframe outline.
			fillTransparency (float): Transparency of the fill shape.
			lineWidth (float): Line width of the wireframe outline.
			lockChannels (list[string]): List with attribute names to be locked.

		"""
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			drawFkIkState=drawFkIkState,
			fkIkStatePosition=fkIkStatePosition,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class MainCtrl(Ctrl):
	"""Class for building the main controller.
	"""
	def __init__(self,
		name="main_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(100.0, 100.0, 100.0),
		shape="circle",
		fillShape=False,
		fillTransparency=0.0,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["v"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		self.__createUnifiedScale()
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)
		# lm.LMAttribute.lockControlPlugs(self.transform, lockChannels)


	def __createUnifiedScale(self):
		"""Creates unified scale attribute on the main controller.
		"""
		cmds.addAttr(
			self.transform,
			longName="rigScale",
			minValue=0.001,
			maxValue=100,
			defaultValue=1.0
		)
		cmds.setAttr(f"{self.transform}.rigScale", keyable=False, channelBox=True)
		for axis in ["x", "y", "z"]:
			cmds.connectAttr(f"{self.transform}.rigScale", f"{self.transform}.s{axis}")
			cmds.setAttr(f"{self.transform}.s{axis}", keyable=False)




class RootMotionCtrl(Ctrl):
	"""Class for building the root motion controller.
	"""
	def __init__(self,
		name="root_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 45.0, 0.0),
		localScale=(15.0, 1.0, 15.0),
		shape="square",
		fillShape=False,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class PelvisCtrl(Ctrl):
	"""Class for building the center of graivty controller.
	"""
	def __init__(self,
		name="pelvis_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(40.0, 40.0, 40.0),
		shape="square",
		fillShape=False,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class RollCtrl(Ctrl):
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 45.0, 90.0),
		localScale=(4.0, 4.0, 4.0),
		shape="square",
		fillShape=False,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class FingerCtrl():
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 90.0),
		localScale=(3.0, 3.0, 3.0),
		shape="circle",
		fillShape=False,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultFingerLineWidth,
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class IkCtrl():
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(6.0, 6.0, 6.0),
		shape="cube",
		fillShape=False,
		drawFkIkState=False,
		fkIkStatePosition=(0.0, 0.0, 0.0),
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			drawFkIkState=drawFkIkState,
			fkIkStatePosition=fkIkStatePosition,
			fillTransparency=fillTransparency,
			lineWidth=Ctrl.defaultLineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class FkIkSwitchCtrl():
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(2.0, 2.0, 2.0),
		shape="diamond",
		fillShape=False,
		drawFkIkState=False,
		fkIkStatePosition=(0.0, 0.0, 0.0),
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["translate", "rotate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "visibility"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			drawFkIkState=drawFkIkState,
			fkIkStatePosition=fkIkStatePosition,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)
		# lm.LMAttribute.lockTransforms(self.transform)




class PoleVectorCtrl():
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(8.0, 8.0, 8.0),
		shape="locator",
		fillShape=False,
		drawLine=True,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale"]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			drawLine=drawLine,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class CorrectiveCtrl():
	"""Class for building the rig controller.
	"""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(3.0, 3.0, 3.0),
		shape="locator",
		fillShape=True,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=True,
		# lockChannels=["scale", "visibility"]
		lockChannels=[]
	):
		self.transform, self.shape = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




#--------------------------------------------------------------------------------------------------
#	FK Components
#--------------------------------------------------------------------------------------------------




class Fk2bLimbComponent():
	"""Class for building the fk 2b limb component.
	"""

	def __init__(self, parent:str, start:str, mid:str, end:str, root:str=None, side:str="center") -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		self.root = root
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "center":
			sideSuffix = ""
			color = "lightyellow"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		if self.root:
			self.ctrlRoot = Ctrl(
				name=f"{root}{sideSuffix}_ctrl", parent=parent,
				translateTo=f"{root}{sideSuffix}", rotateTo=f"{root}{sideSuffix}",
				color=color,
			)
			parent = self.ctrlRoot.transform

		self.ctrlStart = Ctrl(
			name=f"{start}{sideSuffix}_ctrl",	parent=parent,
			translateTo=f"{start}{sideSuffix}",	rotateTo=f"{start}{sideSuffix}",
			color=color,
		)

		self.ctrlMid = Ctrl(
			name=f"{mid}{sideSuffix}_ctrl", parent=self.ctrlStart.transform,
			translateTo=f"{mid}{sideSuffix}", rotateTo=f"{mid}{sideSuffix}",
			color=color,
		)

		self.ctrlEnd = Ctrl(
			name=f"{end}{sideSuffix}_ctrl", parent=self.ctrlMid.transform,
			translateTo=f"{end}{sideSuffix}",	rotateTo=f"{end}{sideSuffix}",
			color=color,
		)

		[lm.LMAttribute.copyTransformsToOPM(ctrl.transform) for ctrl in self.getCtrls()]


	def getCtrls(self):
		"""Returns all the controller objects.
		"""
		if self.root: return (self.ctrlRoot, self.ctrlStart, self.ctrlMid, self.ctrlEnd)

		return (self.ctrlStart, self.ctrlMid, self.ctrlEnd)




class FkSpineComponent():
	"""Class for building the fk spine component."""


	def __init__(self, parent, listJoints) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		# Main chain
		self.CtrlSpine1 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine1"]),
			parent=parent,
			translateTo=listJoints["Spine"]["Spine1"],
			rotateTo=listJoints["Spine"]["Spine1"],
		)
		self.CtrlSpine2 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine2"]),
			parent=self.CtrlSpine1.transform,
			translateTo=listJoints["Spine"]["Spine2"],
			rotateTo=listJoints["Spine"]["Spine2"],
		)
		self.CtrlSpine3 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine3"]),
			parent=self.CtrlSpine2.transform,
			translateTo=listJoints["Spine"]["Spine3"],
			rotateTo=listJoints["Spine"]["Spine3"],
		)
		self.CtrlSpine4 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine4"]),
			parent=self.CtrlSpine3.transform,
			translateTo=listJoints["Spine"]["Spine4"],
			rotateTo=listJoints["Spine"]["Spine4"],
		)
		self.CtrlSpine5 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine5"]["Root"]),
			parent=self.CtrlSpine4.transform,
			translateTo=listJoints["Spine"]["Spine5"]["Root"],
			rotateTo=listJoints["Spine"]["Spine5"]["Root"],
		)

		# self.CtrlCorrective = []
		# for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}_ctrl",
		# 		parent=self.CtrlSpine5.transform,
		# 		translateTo=joint,
		# 		rotateTo=joint
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)

		lm.LMTransformUtils.postCtrlTransform(listJoints["Spine"])


	def getCtrls(self):
		return (self.CtrlSpine1, self.CtrlSpine2, self.CtrlSpine3, self.CtrlSpine4, self.CtrlSpine5)




class FkFootComponent():
	"""Class for building the fk hand component.
	"""

	def __init__(self, parent:str, listJoints:dict, side:str="left") -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		# Toe - main bones
		self.CtrlToe = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			color=color,
		)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlToe.transform)
		# lm.LMTransformUtils.postCtrlTransform(listJoints["Leg"], sideSuffix)


	def getCtrls(self):
		return (
			self.CtrlToe,
		)




class FkHandComponent():
	"""Class for building the fk hand component.
	"""

	def __init__(self, parent:str, listJoints:dict, side:str="left") -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		# Thumb
		self.CtrlThumb1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			color=color,
		)
		self.CtrlThumb2 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			parent=self.CtrlThumb1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			color=color,
		)
		self.CtrlThumb3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			parent=self.CtrlThumb2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			color=color,
		)
		# Index
		self.CtrlInHandIndex = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			color=color,
		)
		self.CtrlIndex1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index1"], sideSuffix),
			parent=self.CtrlInHandIndex.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			color=color,
		)
		self.CtrlIndex2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index2"], sideSuffix),
			parent=self.CtrlIndex1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			color=color,
		)
		self.CtrlIndex3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index3"], sideSuffix),
			parent=self.CtrlIndex2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index3"], sideSuffix),
			color=color,
		)
		# Middle
		self.CtrlInHandMiddle = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			color=color,
		)
		self.CtrlMiddle1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle1"], sideSuffix),
			parent=self.CtrlInHandMiddle.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			color=color,
		)
		self.CtrlMiddle2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle2"], sideSuffix),
			parent=self.CtrlMiddle1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			color=color,
		)
		self.CtrlMiddle3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle3"], sideSuffix),
			parent=self.CtrlMiddle2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle3"], sideSuffix),
			color=color,
		)
		# Ring
		self.CtrlInHandRing = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			color=color,
		)
		self.CtrlRing1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring1"], sideSuffix),
			parent=self.CtrlInHandRing.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			color=color,
		)
		self.CtrlRing2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring2"], sideSuffix),
			parent=self.CtrlRing1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			color=color,
		)
		self.CtrlRing3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring3"], sideSuffix),
			parent=self.CtrlRing2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring3"], sideSuffix),
			color=color,
		)
		# Pinky
		self.CtrlInHandPinky = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			color=color,
		)
		self.CtrlPinky1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			parent=self.CtrlInHandPinky.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			color=color,
		)
		self.CtrlPinky2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			parent=self.CtrlPinky1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			color=color,
		)
		self.CtrlPinky3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			parent=self.CtrlPinky2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			color=color,
		)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Hand"], sideSuffix)


	def getCtrls(self):
		return (
			self.CtrlThumb1, self.CtrlThumb2, self.CtrlThumb3,
			self.CtrlInHandIndex, self.CtrlIndex1, self.CtrlIndex2, self.CtrlIndex3,
			self.CtrlInHandMiddle, self.CtrlMiddle1, self.CtrlMiddle2, self.CtrlMiddle3,
			self.CtrlInHandRing, self.CtrlRing1, self.CtrlRing2, self.CtrlRing3,
			self.CtrlInHandPinky, self.CtrlPinky1, self.CtrlPinky2, self.CtrlPinky3,
		)
	
	def getMainCtrls(self):
		return (
			self.CtrlThumb1, self.CtrlThumb2, self.CtrlThumb3,
			self.CtrlIndex1, self.CtrlIndex2, self.CtrlIndex3,
			self.CtrlMiddle1, self.CtrlMiddle2, self.CtrlMiddle3,
			self.CtrlRing1, self.CtrlRing2, self.CtrlRing3,
			self.CtrlPinky1, self.CtrlPinky2, self.CtrlPinky3,
		)

	def getFirstKnucklesCtrls(self):
		return (
			self.CtrlThumb1,
			self.CtrlIndex1,
			self.CtrlMiddle1,
			self.CtrlRing1,
			self.CtrlPinky1, 
		)

	def getZlockCtrls(self):
		return (
			self.CtrlThumb2, self.CtrlThumb3,
			self.CtrlIndex2, self.CtrlIndex3,
			self.CtrlMiddle2, self.CtrlMiddle3,
			self.CtrlRing2, self.CtrlRing3,
			self.CtrlPinky2, self.CtrlPinky3,
		)

	def getInHandCtrls(self):
		return (self.CtrlInHandIndex, self.CtrlInHandMiddle, self.CtrlInHandRing, self.CtrlInHandPinky)

	def getThumbCtrls(self):
		return (self.CtrlThumb1, self.CtrlThumb2, self.CtrlThumb3)

	def getIndexCtrls(self):
		return (self.CtrlInHandIndex, self.CtrlIndex1, self.CtrlIndex2, self.CtrlIndex3)

	def getMiddleCtrls(self):
		return (self.CtrlInHandMiddle, self.CtrlMiddle1, self.CtrlMiddle2, self.CtrlMiddle3)
	
	def getRignCtrls(self):
		return (self.CtrlInHandRing, self.CtrlRing1, self.CtrlRing2, self.CtrlRing3)

	def getPinkyCtrls(self):
		return (self.CtrlInHandPinky, self.CtrlPinky1, self.CtrlPinky2, self.CtrlPinky3)




#--------------------------------------------------------------------------------------------------
#	Out Components
#--------------------------------------------------------------------------------------------------




class Out2bLimbComponent():
	"""Class for building the fk 2b limb component.
	"""

	def __init__(self, 
	  	parent:str, start:str, mid:str, end:str, root:str=None,
		  
			drawFkIkState:bool=True, fkIkStatePosition:tuple=(0.0, 0.0, 0.0),
			side:str="center"
		) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		self.root = root
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "center":
			sideSuffix = ""
			color = "yellow"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		if self.root:
			self.ctrlRoot = Ctrl(
				name=f"{root}{sideSuffix}_out", parent=parent,
				translateTo=f"{root}{sideSuffix}", rotateTo=f"{root}{sideSuffix}",
				color=color,
			)
			parent = self.ctrlRoot.transform

		self.ctrlStart = Ctrl(
			name=f"{start}{sideSuffix}_out",	parent=parent,
			translateTo=f"{start}{sideSuffix}",	rotateTo=f"{start}{sideSuffix}",
			color=color,
		)

		self.ctrlMid = Ctrl(
			name=f"{mid}{sideSuffix}_out", parent=self.ctrlStart.transform,
			translateTo=f"{mid}{sideSuffix}", rotateTo=f"{mid}{sideSuffix}",
			color=color,
		)

		self.ctrlEnd = Ctrl(
			name=f"{end}{sideSuffix}_out", parent=self.ctrlMid.transform,
			translateTo=f"{end}{sideSuffix}",	rotateTo=f"{end}{sideSuffix}",
			drawFkIkState=drawFkIkState, fkIkStatePosition=fkIkStatePosition,
			color=color,
		)

		[lm.LMAttribute.copyTransformsToOPM(ctrl.transform) for ctrl in self.getCtrls()]


	def getCtrls(self):
		"""Returns all the controller objects.
		"""
		if self.root: return (self.ctrlRoot, self.ctrlStart, self.ctrlMid, self.ctrlEnd)

		return (self.ctrlStart, self.ctrlMid, self.ctrlEnd)





class OutLegComponent():
	"""Class for building the out leg component."""


	def __init__(self, parent:str, listJoints:dict, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
			colorDark = "orange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
			colorDark = "blue"

		# UpLeg - main bones
		self.CtrlUpLeg = Ctrl(
			name="{}{}_out".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			color=color,
			shape="none"
		)
		# UpLeg - roll bones
		self.CtrlUpLegRoll1 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["UpLegRoll1"]["Root"], sideSuffix),
			parent=self.CtrlUpLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["UpLegRoll1"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["UpLegRoll1"]["Root"], sideSuffix),
			color=color,
		)
		self.CtrlUpLegRoll2 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["UpLegRoll2"]["Root"], sideSuffix),
			parent=self.CtrlUpLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["UpLegRoll2"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["UpLegRoll2"]["Root"], sideSuffix),
			color=color,
		)

		# Leg - main bones
		self.CtrlLeg = Ctrl(
			name="{}{}_out".format(listJoints["Leg"]["Leg"], sideSuffix),
			parent=self.CtrlUpLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["Leg"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["Leg"], sideSuffix),
			color=color,
			shape="none"
		)
		# Leg - roll bones
		self.CtrlLegRoll1 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["LegRoll1"]["Root"], sideSuffix),
			parent=self.CtrlLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["LegRoll1"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["LegRoll1"]["Root"], sideSuffix),
			color=color,
		)
		self.CtrlLegRoll2 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["LegRoll2"]["Root"], sideSuffix),
			parent=self.CtrlLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["LegRoll2"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["LegRoll2"]["Root"], sideSuffix),
			color=color,
		)

		# Foot - main bones
		self.CtrlFoot = Ctrl(
			name="{}{}_out".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			parent=self.CtrlLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			drawFkIkState=True,
			fkIkStatePosition=fkIkStatePosition,
			color=colorDark,
			shape="none"
		)

		# # Corrective controllers
		# self.CtrlCorrective = []
		# # UpLeg
		# for joint in listJoints["Leg"]["UpLegRoll1"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlUpLegRoll1.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# for joint in listJoints["Leg"]["UpLegRoll2"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlUpLegRoll2.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# for joint in listJoints["Leg"]["UpLegCorrectiveRoot"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlUpLegCorrectiveRoot.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # Leg
		# for joint in listJoints["Leg"]["LegRoll2"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlLegRoll1.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# for joint in listJoints["Leg"]["LegCorrectiveRoot"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlLegCorrectiveRoot.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # Foot
		# for joint in listJoints["Leg"]["Foot"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_out",
		# 		parent=self.CtrlFoot.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# self.CtrlCorrective.append(self.CtrlUpLegCorrectiveRoot)
		# self.CtrlCorrective.append(self.CtrlLegCorrectiveRoot)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlUpLeg.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlUpLegRoll1.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlUpLegRoll2.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlLeg.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlLegRoll1.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlLegRoll2.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlFoot.transform)


	def getCtrls(self):
		return (
			self.CtrlUpLeg, self.CtrlUpLegRoll1,  self.CtrlUpLegRoll2,
			self.CtrlLeg, self.CtrlLegRoll1, self.CtrlLegRoll2,
			self.CtrlFoot
		)


	def getMainCtrls(self):
		return (self.CtrlUpLeg, self.CtrlLeg,	self.CtrlFoot)


	def getRollCtrls(self):
		return (self.CtrlUpLegRoll1,  self.CtrlUpLegRoll2, self.CtrlLegRoll1, self.CtrlLegRoll2)




class OutArmComponent():
	"""Class for building the fk leg component."""


	def __init__(self, parent:str, listJoints:dict, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
			colorDark = "orange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
			colorDark = "blue"

		# # Shouleder - main bones
		# self.CtrlShoulder = Ctrl(
		# 	name="{}{}_out".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
		# 	parent=parent,
		# 	translateTo="{}{}".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
		# 	rotateTo="{}{}".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
		# 	color=color,
		# )
	
		# Arm - main bones
		self.CtrlArm = Ctrl(
			name="{}{}_out".format(listJoints["Arm"]["Arm"], sideSuffix),
			# parent=self.CtrlShoulder.transform,
			parent=parent,
			translateTo="{}{}".format(listJoints["Arm"]["Arm"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["Arm"], sideSuffix),
			color=color,
		)
		# Arm - roll bones
		self.CtrlArmRoll1 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ArmRoll1"]["Root"], sideSuffix),
			parent=self.CtrlArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ArmRoll1"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ArmRoll1"]["Root"], sideSuffix),
			color=color,
		)
		self.CtrlArmRoll2 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ArmRoll2"]["Root"], sideSuffix),
			parent=self.CtrlArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ArmRoll2"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ArmRoll2"]["Root"], sideSuffix),
			color=color,
		)
		# # Arm - corrective root
		# self.CtrlArmCorrectiveRoot = CorrectiveCtrl(
		# 	name="{}{}_ctrl".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	parent=self.CtrlArm.transform,
		# 	translateTo="{}{}".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	rotateTo="{}{}".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	color=color,
		# )

		# Forearm - main bones
		self.CtrlForeArm = Ctrl(
			name="{}{}_out".format(listJoints["Arm"]["ForeArm"], sideSuffix),
			parent=self.CtrlArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ForeArm"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ForeArm"], sideSuffix),
			color=color,
		)
	
		# Forearm - roll bones
		self.CtrlForeArmRoll1 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ForeArmRoll1"], sideSuffix),
			parent=self.CtrlForeArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ForeArmRoll1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ForeArmRoll1"], sideSuffix),
			color=color,
		)
		self.CtrlForeArmRoll2 = RollCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ForeArmRoll2"], sideSuffix),
			parent=self.CtrlForeArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ForeArmRoll2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ForeArmRoll2"], sideSuffix),
			color=color,
		)
		# Forearm - corrective root
		# self.CtrlForeArmCorrectiveRoot = CorrectiveCtrl(
		# 	name="{}{}_ctrl".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	parent=self.CtrlForeArm.transform,
		# 	translateTo="{}{}".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	rotateTo="{}{}".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
		# 	color=color,
		# )
		# Hand - corrective root
		self.CtrlHand = Ctrl(
			name="{}{}_out".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			parent=self.CtrlForeArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			drawFkIkState=True,
			fkIkStatePosition=fkIkStatePosition,
			color=colorDark,
			shape="none"
		)
		# # Corrective controllers
		# self.CtrlCorrective = []
		# # Shoulder
		# for joint in listJoints["Arm"]["Shoulder"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlShoulder.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # Armroll1
		# for joint in listJoints["Arm"]["ArmRoll1"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlArmRoll1.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # Armroll2
		# for joint in listJoints["Arm"]["ArmRoll2"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlArmRoll2.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # ArmCorrectiveRoot
		# for joint in listJoints["Arm"]["ArmCorrectiveRoot"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlArmCorrectiveRoot.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # ForeArmCorrectiveRoot
		# for joint in listJoints["Arm"]["ForeArmCorrectiveRoot"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlForeArmCorrectiveRoot.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# # Hand
		# for joint in listJoints["Arm"]["Hand"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}{sideSuffix}_ctrl",
		# 		parent=self.CtrlHand.transform,
		# 		translateTo=f"{joint}{sideSuffix}",
		# 		rotateTo=f"{joint}{sideSuffix}",
		# 		color=color,
		# 	)
		# 	self.CtrlCorrective.append(CtrlCorrective)
		# self.CtrlCorrective.append(self.CtrlArmCorrectiveRoot)
		# self.CtrlCorrective.append(self.CtrlForeArmCorrectiveRoot)
		# lm.LMAttribute.copyTransformsToOPM(self.CtrlShoulder.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlArm.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlArmRoll1.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlArmRoll2.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlForeArm.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlForeArmRoll1.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlForeArmRoll2.transform)
		lm.LMAttribute.copyTransformsToOPM(self.CtrlHand.transform)


	def getCtrls(self):
		return (
			# self.CtrlShoulder,
			self.CtrlArm, self.CtrlArmRoll1,  self.CtrlArmRoll2,
			# self.CtrlArm,
			self.CtrlForeArm, self.CtrlForeArmRoll1, self.CtrlForeArmRoll2,
			# self.CtrlForeArm,
			self.CtrlHand
		)


	def getMainCtrls(self):
		return (self.CtrlShoulder, self.CtrlArm,	self.CtrlForeArm, self.CtrlHand)
	

	# def getRollCtrls(self):
	# 	return (self.CtrlArmRoll1,  self.CtrlArmRoll2, self.CtrlForeArmRoll1, self.CtrlForeArmRoll2)




#--------------------------------------------------------------------------------------------------
#	Ik Components
#--------------------------------------------------------------------------------------------------




class Ik2bLimbComponent():
	"""Class for building ik comoponents."""


	def __init__(self,
	  name:str, parent:str, rotateTo:str, 
		fkStart:str, fkMid:str, fkEnd:str,
		outStart:str, outMid:str, outEnd:str,
		upperTwist1:str, upperTwis2:str, lowerTwist1:str, lowerTwist2:str, 
		poleVector:str="",
		side:str="left", mode:str="ik",
		) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		self.poleVector = poleVector
		if side == "left":
			sideSuffix = "_l"
			color = "orange"
		if side == "center":
			sideSuffix = ""
			color = "yellow"
		if side == "right":
			sideSuffix = "_r"
			color = "blue"

		self.CtrlIk = IkCtrl(
			name=f"{name}_ik{sideSuffix}_ctrl",
			parent=parent,
			translateTo=fkEnd,
			rotateTo=fkEnd,
			lineWidth=2.0,
			color=color,
		)

		if self.poleVector != "":
			self.CtrlPoleVector = PoleVectorCtrl(
				name=f"{name}_pv{sideSuffix}_ctrl",
				parent=parent,
				translateTo=poleVector,
				rotateTo=rotateTo,
				lineWidth=2.0,
				color=color,
			)
			poleVector=self.CtrlPoleVector.transform

		self.NodeIk2bSolver = cmds.ik(
			name=f"{name}{sideSuffix}_",
			fkStart=fkStart,
			fkMid=fkMid,
			fkEnd=fkEnd,
			ikHandle=self.CtrlIk.transform,
			poleVector=poleVector,
			outStart=outStart,
			outMid=outMid,
			outEnd=outEnd,
			mode=mode,
		)[0]
	

		self.displFkCtrls = cmds.createNode("displayLayer", name=f"{name}_fk{sideSuffix}_displ")
		self.displIkCtrls = cmds.createNode("displayLayer", name=f"{name}_ik{sideSuffix}_displ")
		cmds.connectAttr(f"{self.NodeIk2bSolver}.fkVisibility", f"{self.displFkCtrls}.visibility")
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkStart}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkMid}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkEnd}.drawOverride", force=True)
		cmds.connectAttr(f"{self.NodeIk2bSolver}.ikVisibility", f"{self.displIkCtrls}.visibility")
		cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.CtrlIk.transform}.drawOverride", force=True)
		if self.poleVector != "":
			cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.CtrlPoleVector.transform}.drawOverride", force=True)
			cmds.connectAttr(f"{outMid}.worldMatrix[0]", f"{self.CtrlPoleVector.shape}.drawLineTo")
			lm.LMAttribute.copyTransformsToOPM(self.CtrlPoleVector.transform)

		lm.LMAttribute.copyTransformsToOPM(self.CtrlIk.transform)


	def getCtrls(self):
		"""Returns all the controller objects.
		"""
		if self.poleVector != "":	return (self.CtrlIk, self.CtrlPoleVector)

		return (self.CtrlIk)




#--------------------------------------------------------------------------------------------------
# Limb Components
#--------------------------------------------------------------------------------------------------




class BaseComponent():
	"""Class for building the top rig structure.

	Dependencies:
		lunar plugin (custom rig controller)

	TODO:
		Fix rollControllers on CtrlMain

	"""
	sceneObjectType = "rig"

	def __init__(self, rigName="new"):
		"""Class constructor.

		Args:
			rigName (string): Name of the character / rig.
			localScale (float): Scale of the rigController - edits localScaleXYZ attrs on the shape node.

		"""
		self.rigName = rigName
		# Rig groups setup
		self.grpBase = cmds.group(name="rig", empty=True)  # we're going to use a namespace anyway
		self.ctrlMain = MainCtrl(parent=self.grpBase, localRotate=(90.0, 0.0, 0.0))
		self.grpMesh = cmds.group(name="mesh_grp", empty=True, parent=self.grpBase)


		self.setupRigGroups()

		self.setupVisibilityAttributesAndConnections()

		cmds.setAttr(f"{self.grpBase}.rotateX", -90)

		# for group in [self.grpBase, self.grpMesh]:
		[lm.LMAttribute.lockControlChannels(Object, ["translate", "scale", "visibility"]) for Object in [self.grpBase, self.grpMesh]]


	def setupRigGroups(self):
		"""Sets main rig groups: base, ctrl, mesh and export.
		"""
		# Extra attribute creation
		rigNameAttr = "rigName"
		sceneObjectTypeAttr = "sceneObjectType"
		[cmds.addAttr(self.grpBase, longName=attr, dataType="string") for attr in [rigNameAttr, sceneObjectTypeAttr]]
		
		cmds.setAttr(f"{self.grpBase}.{rigNameAttr}", self.rigName, type="string", lock=True)
		cmds.setAttr(f"{self.grpBase}.{sceneObjectTypeAttr}", self.sceneObjectType, type="string", lock=True)


	def setupVisibilityAttributesAndConnections(self):
		"""Creates visibility and display type attributes on the main cotroller and connects them.
		"""

		lm.LMAttribute.addSeparator(self.ctrlMain.transform)

		self.displCtrls = cmds.createNode("displayLayer", name="ctrls_displ")
		self.displMesh = cmds.createNode("displayLayer", name="mesh_displ")
		self.displJnts = cmds.createNode("displayLayer", name="outs_displ")
	
		# Visibility
		# Main Ctrls
		self.attrCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "ctrlsVisibility")
		cmds.connectAttr(self.attrCtrlsVisibility, f"{self.displCtrls}.visibility")
		cmds.connectAttr(f"{self.displCtrls}.drawInfo", f"{self.ctrlMain.transform}.drawOverride", force=True)

		# Meshes
		self.attrMeshVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "meshVisibility")
		cmds.connectAttr(self.attrMeshVisibility, f"{self.displMesh}.visibility")
		cmds.connectAttr(f"{self.displMesh}.drawInfo", f"{self.grpMesh}.drawOverride", force=True)
	
		# Export Skeleton
		self.attrExportSkeletonVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "exportSkeletonVisibility", False)
		cmds.connectAttr(self.attrExportSkeletonVisibility, f"{self.displJnts}.visibility")


		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "__")


		# Diplay Type Overrides
		# Main Ctrls 
		self.attrCtrlsDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "ctrlsDisplayType")
		cmds.connectAttr(self.attrCtrlsDisplayType, f"{self.displCtrls}.displayType")
		cmds.connectAttr(f"{self.displCtrls}.displayType", f"{self.ctrlMain.transform}.overrideDisplayType")
		cmds.connectAttr(f"{self.displCtrls}.displayType", f"{self.ctrlMain.shape}.overrideDisplayType")

		# Meshes
		self.attrMeshDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "meshDisplayType", 2)
		cmds.connectAttr(self.attrMeshDisplayType, f"{self.displMesh}.displayType")
		cmds.connectAttr(f"{self.displMesh}.displayType", f"{self.grpMesh}.overrideDisplayType")

		# Export Skeleton
		self.attrExportSkeletonDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "exportSkeletonDisplayType", 2)
		cmds.connectAttr(self.attrExportSkeletonDisplayType, f"{self.displJnts}.displayType")


		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "___")


		# Hide Ctrls On Playback
		self.attrHideCtrlsOnPlayback = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "hideCtrlsOnPlayback", False)
		cmds.connectAttr(self.attrHideCtrlsOnPlayback, f"{self.displCtrls}.hideOnPlayback")
		cmds.connectAttr(f"{self.displCtrls}.hideOnPlayback", f"{self.ctrlMain.shape}.hideOnPlayback")




class PelvisComponent():
	"""Class for building the fk pelvis component.
	"""

	def __init__(self, parent:str, listJoints:dict) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		
		self.grpComp = cmds.group(name="pelvis_grp", parent=parent, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)
		
		# Main chain
		self.CtrlPelvis = PelvisCtrl(
			parent=self.grpComp,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
			# color="yellow",
		)
		self.CtrlPelvisRot = Ctrl(
			name="{}_rot_ctrl".format(listJoints["Spine"]["Pelvis"]),
			parent=self.CtrlPelvis.transform,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
		)

		lm.LMAttribute.copyTransformsToOPM(self.CtrlPelvis.transform)
		lm.LMAttribute.lockControlChannels(self.CtrlPelvis.transform, lockChannels=["scale", "visibility"])
		lm.LMAttribute.copyTransformsToOPM(self.CtrlPelvisRot.transform)
		lm.LMAttribute.lockControlChannels(self.CtrlPelvisRot.transform, lockChannels=["translate", "scale", "visibility"])

	def getCtrls(self):
		return (self.CtrlPelvis, self.CtrlPelvisRot)




class SpineComponent():

	def __init__(self, compRig, attachTo:str, listJoints:list) -> None:
		
		self.grpComp = cmds.group(name="spine_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkSpineComponent(self.grpComp, listJoints)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlSpine1.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode=listJoints["Spine"]["Spine1"]
		)


	def getCtrlsFk(self):
		return self.fk.getCtrls()




class HeadComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0)) -> None:
		
		self.grpComp = cmds.group(name="head_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Head"]["Neck1"],
			mid=listJoints["Head"]["Neck2"],
			end=listJoints["Head"]["Head"],
			side="center",
		)
	
		self.out = Out2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Head"]["Neck1"],
			mid=listJoints["Head"]["Neck2"],
			end=listJoints["Head"]["Head"],
			fkIkStatePosition=fkIkStatePosition,
			side="center",
		)

		self.ik = Ik2bLimbComponent(
			name="head",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.transform,
			fkStart=self.fk.ctrlStart.transform,
			fkMid=self.fk.ctrlMid.transform,
			fkEnd=self.fk.ctrlEnd.transform,
			outStart=self.out.ctrlStart.transform,
			outMid=self.out.ctrlMid.transform,
			outEnd=self.out.ctrlEnd.transform,
			mode="ik",
			side="center",
		)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlStart.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode=listJoints["Head"]["Neck1"]
		)
		cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.ctrlStart.transform}.offsetParentMatrix")


	def getCtrlsFk(self):
		return self.fk.getCtrls()




class LegComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		self.grpComp = cmds.group(name=f"leg{sideSuffix}_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Leg"]["UpLeg"],
			mid=listJoints["Leg"]["Leg"],
			end=listJoints["Leg"]["Foot"]["Root"],
			side=side,
		)
		self.out = OutLegComponent(self.grpComp, listJoints, fkIkStatePosition, side)
		self.ik = Ik2bLimbComponent(
			name="leg",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.transform,
			fkStart=self.fk.ctrlStart.transform,
			fkMid=self.fk.ctrlMid.transform,
			fkEnd=self.fk.ctrlEnd.transform,
			poleVector=f"leg_pv{sideSuffix}",
			outStart=self.out.CtrlUpLeg.transform,
			outMid=self.out.CtrlLeg.transform,
			outEnd=self.out.CtrlFoot.transform,
			side=side,
		)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlStart.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Leg"]["UpLeg"]), sideSuffix)
		)
		cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.CtrlUpLeg.transform}.offsetParentMatrix")


	def getCtrlsFk(self):
		return self.fk.getCtrls()




class FootComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
		
		self.grpComp = cmds.group(name=f"foot{sideSuffix}_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkFootComponent(self.grpComp, listJoints, side)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlToe.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Leg"]["ToeBase"]), sideSuffix)
		)


	def getCtrlsFk(self):
		return self.fk.getCtrls()




class ArmComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		
		self.grpComp = cmds.group(name=f"arm{sideSuffix}_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		# self.fk = FkArmComponent(self.grpComp, listJoints, side)
		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			root=listJoints["Arm"]["Shoulder"]["Root"],
			start=listJoints["Arm"]["Arm"],
			mid=listJoints["Arm"]["ForeArm"],
			end=listJoints["Arm"]["Hand"]["Root"],
			side=side,
		)

		self.out = OutArmComponent(self.grpComp, listJoints, fkIkStatePosition, side)
		self.ik = Ik2bLimbComponent(
			name="arm",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.transform,
			fkStart=self.fk.ctrlStart.transform,
			fkMid=self.fk.ctrlMid.transform,
			fkEnd=self.fk.ctrlEnd.transform,
			poleVector=f"arm_pv{sideSuffix}",
			outStart=self.out.CtrlArm.transform, outMid=self.out.CtrlForeArm.transform,	outEnd=self.out.CtrlHand.transform,
			side=side,
		)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlRoot.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Arm"]["Shoulder"]["Root"]), sideSuffix)
		)
		self.cnstMat2 = LMRigUtils.createMatrixConstraint(
			parent=self.fk.ctrlRoot.transform, 
			child=self.out.CtrlArm.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Arm"]["Arm"]), sideSuffix)
		)
		# cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.CtrlArm.transform}.offsetParentMatrix")


	def getCtrlsFk(self):
		return self.fk.getCtrls()




class HandComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
		
		self.grpComp = cmds.group(name=f"hand{sideSuffix}_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkHandComponent(self.grpComp, listJoints, side)

		self.cnstThumb = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlThumb1.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["Thumb1"]), sideSuffix)
		)
		self.cnstIndex = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlInHandIndex.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandIndex"]), sideSuffix)
		)
		self.cnstMiddle = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlInHandMiddle.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandMiddle"]), sideSuffix)
		)
		self.cnstPinky = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlInHandPinky.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandPinky"]), sideSuffix)
		)
		self.cnstRing = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.CtrlInHandRing.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandRing"]), sideSuffix)
		)


	def getCtrlsFk(self):
		return self.fk.getCtrls()





#--------------------------------------------------------------------------------------------------
# Utilities
#--------------------------------------------------------------------------------------------------




class LMRigUtils():
	"""Wrapper class for rig utilities.
	"""

	log = logging.getLogger("LMRigUtils")


	@classmethod
	def getPoleVectorPosition(cls, start:str, mid:str, end:str, space:str="world") -> om.MVector:
		"""Gets the pole vector position from the input of three objects.
		"""
		# Get world position from strings
		posStart = cmds.xform(start, q=True, ws=True, t=True)
		posMid = cmds.xform(mid, q=True, ws=True, t=True)
		posEnd = cmds.xform(end, q=True, ws=True, t=True)
		# Get vectors
		vecA = om.MVector(posStart[0], posStart[1], posStart[2])
		vecB = om.MVector(posMid[0], posMid[1], posMid[2])
		vecC = om.MVector(posEnd[0], posEnd[1], posEnd[2])

		vecAC = vecC - vecA
		vecAB = vecB - vecA
		vecBC = vecC - vecB

		valScale = (vecAC * vecAB) / (vecAC * vecAC)
		vecProjection = vecAC * valScale + vecA
		lenABC = vecAB.length() + vecBC.length()

		posPv = ((vecB - vecProjection).normal() * lenABC)

		if space == "world": return posPv + vecB
		return posPv


	@classmethod
	def createMatrixConstraint(cls, parent, child, offset, sourceNode:str=None) -> str:

		nodeMultMatrix = cmds.createNode("multMatrix", name=f"{child}_matCnst")
		if sourceNode:
			arrayLocalMatrix = cmds.xform(sourceNode, query=True, matrix=True, worldSpace=False),
			cmds.setAttr(f"{nodeMultMatrix}.matrixIn[0]", arrayLocalMatrix[0], type="matrix")

		cmds.connectAttr(f"{parent}.worldMatrix[0]", f"{nodeMultMatrix}.matrixIn[1]")
		cmds.connectAttr(f"{offset}.worldInverseMatrix[0]", f"{nodeMultMatrix}.matrixIn[2]")

		cmds.connectAttr(f"{nodeMultMatrix}.matrixSum", f"{child}.offsetParentMatrix")

		return nodeMultMatrix




class MMetaHumanUtils():
	"""Wrapper class for utils related to the meta human rig in maya.
	"""

	log = logging.getLogger("MMetaHumanUtils")

	@classmethod
	def loadFaceCtrlAnimation(cls, filePath:str, timeStart:int=0, setRange:bool=True,  namespace:str=""):
		"""Load the blend space weights onto the metahuman face ctrls from nvidia's face2audio.

		listMhCtrls is the mapping between metahuman rig and a2f facs rig.
		each entry in the list specifies the mapping of
		[mh_rig_ctrl_name, a2f_facs_name1, a2f_facs_weight1, a2f_facs_name2, a2f_facs_weight2, ...]

		"""
		listMhCtrls = [
			['CTRL_R_brow_down.ty', "browLowerR", 1.0],  
			['CTRL_L_brow_down.ty', "browLowerL", 1.0], 
			['CTRL_R_brow_lateral.ty', "browLowerR", 1.0],
			['CTRL_L_brow_lateral.ty', "browLowerL", 1.0],
			['CTRL_R_brow_raiseIn.ty', "innerBrowRaiserR", 1.0], 
			['CTRL_L_brow_raiseIn.ty', "innerBrowRaiserL", 1.0],
			['CTRL_R_brow_raiseOut.ty', "innerBrowRaiserR", 1.0], 
			['CTRL_L_brow_raiseOut.ty', "innerBrowRaiserL", 1.0],
			['CTRL_C_eye.ty', "eyesLookUp", 1.0, "eyesLookDown", -1.0],
			['CTRL_C_eye.tx', "eyesLookLeft", 1.0, "eyesLookRight", -1.0],
			['CTRL_R_eye_blink.ty', "eyesCloseR", 1.0, "eyesUpperLidRaiserR", -1.0],
			['CTRL_L_eye_blink.ty', "eyesCloseL", 1.0, "eyesUpperLidRaiserL", -1.0],
			['CTRL_R_eye_squintInner.ty', "squintR", 1.0], 
			['CTRL_L_eye_squintInner.ty', "squintL", 1.0],
			['CTRL_R_eye_cheekRaise.ty', "cheekRaiserR", 1.0], 
			['CTRL_L_eye_cheekRaise.ty', "cheekRaiserL", 1.0],
			['CTRL_R_mouth_suckBlow.ty', "cheekPuffR", 0.5], 
			['CTRL_L_mouth_suckBlow.ty', "cheekPuffL", 0.5],
			['CTRL_R_nose.ty', "noseWrinklerR", 1.0], 
			['CTRL_L_nose.ty', "noseWrinklerL", 1.0],
			['CTRL_C_jaw.ty', "jawDrop", 1.0, "jawDropLipTowards", 0.6],
			['CTRL_R_mouth_lipsTogetherU', "jawDropLipTowards", 1.0],
			['CTRL_L_mouth_lipsTogetherU', "jawDropLipTowards", 1.0],
			['CTRL_R_mouth_lipsTogetherD', "jawDropLipTowards", 1.0],
			['CTRL_L_mouth_lipsTogetherD', "jawDropLipTowards", 1.0],
			['CTRL_C_jaw_fwdBack.ty', "jawThrust", -1.0],
			['CTRL_C_jaw.tx', "jawSlideLeft", -1.0, "jawSlideRight", 1.0],
			['CTRL_C_mouth.tx', "mouthSlideLeft", 0.5, "mouthSlideRight", -0.5],
			['CTRL_R_mouth_dimple.ty', "dimplerR", 1.0], 
			['CTRL_L_mouth_dimple.ty', "dimplerL", 1.0],
			['CTRL_R_mouth_cornerPull.ty', "lipCornerPullerR", 1.0], 
			['CTRL_L_mouth_cornerPull.ty', "lipCornerPullerL", 1.0],
			['CTRL_R_mouth_cornerDepress.ty', "lipCornerDepressorR", 1.0], 
			['CTRL_L_mouth_cornerDepress.ty', "lipCornerDepressorL", 1.0],
			['CTRL_R_mouth_stretch.ty', "lipStretcherR", 1.0], 
			['CTRL_L_mouth_stretch.ty', "lipStretcherL", 1.0],
			['CTRL_R_mouth_upperLipRaise.ty', "upperLipRaiserR", 1.0], 
			['CTRL_L_mouth_upperLipRaise.ty', "upperLipRaiserL", 1.0],
			['CTRL_R_mouth_lowerLipDepress.ty', "lowerLipDepressorR", 1.0], 
			['CTRL_L_mouth_lowerLipDepress.ty', "lowerLipDepressorR", 1.0],
			['CTRL_R_jaw_ChinRaiseD.ty', "chinRaiser", 1.0], 
			['CTRL_L_jaw_ChinRaiseD.ty', "chinRaiser", 1.0],
			['CTRL_R_mouth_lipsPressU.ty', "lipPressor", 1.0], 
			['CTRL_L_mouth_lipsPressU.ty', "lipPressor", 1.0],
			['CTRL_R_mouth_towardsU.ty', "pucker", 1.0], 
			['CTRL_L_mouth_towardsU.ty', "pucker", 1.0], 
			['CTRL_R_mouth_towardsD.ty', "pucker", 1.0], 
			['CTRL_L_mouth_towardsD.ty', "pucker", 1.0], 
			['CTRL_R_mouth_purseU.ty', "pucker", 1.0], 
			['CTRL_L_mouth_purseU.ty', "pucker", 1.0], 
			['CTRL_R_mouth_purseD.ty', "pucker", 1.0], 
			['CTRL_L_mouth_purseD.ty', "pucker", 1.0],
			['CTRL_R_mouth_funnelU.ty', "funneler", 1.0], 
			['CTRL_L_mouth_funnelU.ty', "funneler", 1.0], 
			['CTRL_L_mouth_funnelD.ty', "funneler", 1.0], 
			['CTRL_R_mouth_funnelD.ty', "funneler", 1.0],
			['CTRL_R_mouth_pressU.ty', "lipSuck", 1.0], 
			['CTRL_L_mouth_pressU.ty', "lipSuck", 1.0], 
			['CTRL_R_mouth_pressD.ty', "lipSuck", 1.0], 
			['CTRL_L_mouth_pressD.ty', "lipSuck", 1.0]
		]

		dataFacs = lm.MFile.loadDataFromJson(filePath)

		facsNames = dataFacs["facsNames"]
		numFrames = dataFacs["numFrames"]
		weightMat = dataFacs["weightMat"]
		timeEnd = timeStart + numFrames - 1

		if setRange: lm.MScene.setAnimationRange(timeStart, timeEnd)

		for frame in range(numFrames):
			for indxCtrl in range(listMhCtrls.__len__()):
				ctrlValue = 0
				numInputs = int((len(listMhCtrls[indxCtrl])-1) / 2)
				for indxInput in range(numInputs):
					poseIdx = facsNames.index(listMhCtrls[indxCtrl][indxInput*2+1])
					ctrlValue += weightMat[frame][poseIdx] * listMhCtrls[indxCtrl][indxInput*2+2]

				cmds.setKeyframe(f"{namespace}{listMhCtrls[indxCtrl][0]}", value=ctrlValue, time=(timeStart+frame))
		
		cls.log.info(f"Successfuly loaded animation from '{timeStart}' to '{timeEnd}'")

