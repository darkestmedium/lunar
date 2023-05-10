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




class OutCtrl(Ctrl):
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
		shape="none",
		fillShape=False,
		drawFkIkState=False,
		fkIkStatePosition=(0.0, 0.0, 0.0),
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
			drawFkIkState=drawFkIkState,
			fkIkStatePosition=fkIkStatePosition,
			fillShape=fillShape,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




class TwistCtrl(Ctrl):
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
		name="fkik_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(25.0, 0.0, 0.0),
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
		self.ctrlSpine1 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine1"]),
			parent=parent,
			translateTo=listJoints["Spine"]["Spine1"],
			rotateTo=listJoints["Spine"]["Spine1"],
		)
		self.ctrlSpine2 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine2"]),
			parent=self.ctrlSpine1.transform,
			translateTo=listJoints["Spine"]["Spine2"],
			rotateTo=listJoints["Spine"]["Spine2"],
		)
		self.ctrlSpine3 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine3"]),
			parent=self.ctrlSpine2.transform,
			translateTo=listJoints["Spine"]["Spine3"],
			rotateTo=listJoints["Spine"]["Spine3"],
		)
		self.ctrlSpine4 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine4"]),
			parent=self.ctrlSpine3.transform,
			translateTo=listJoints["Spine"]["Spine4"],
			rotateTo=listJoints["Spine"]["Spine4"],
		)
		self.ctrlSpine5 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine5"]["Root"]),
			parent=self.ctrlSpine4.transform,
			translateTo=listJoints["Spine"]["Spine5"]["Root"],
			rotateTo=listJoints["Spine"]["Spine5"]["Root"],
		)

		# self.ctrlCorrective = []
		# for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}_ctrl",
		# 		parent=self.ctrlSpine5.transform,
		# 		translateTo=joint,
		# 		rotateTo=joint
		# 	)
		# 	self.ctrlCorrective.append(CtrlCorrective)

		lm.LMTransformUtils.postCtrlTransform(listJoints["Spine"])


	def getCtrls(self):
		return (self.ctrlSpine1, self.ctrlSpine2, self.ctrlSpine3, self.ctrlSpine4, self.ctrlSpine5)




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
		self.ctrlToe = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			color=color,
		)
		lm.LMAttribute.copyTransformsToOPM(self.ctrlToe.transform)
		# lm.LMTransformUtils.postCtrlTransform(listJoints["Leg"], sideSuffix)


	def getCtrls(self):
		return (
			self.ctrlToe,
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
		self.ctrlThumb1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb1"], sideSuffix),
			color=color,
		)
		self.ctrlThumb2 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			parent=self.ctrlThumb1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			color=color,
		)
		self.ctrlThumb3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			parent=self.ctrlThumb2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			color=color,
		)
		# Index
		self.ctrlInHandIndex = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandIndex"], sideSuffix),
			color=color,
		)
		self.ctrlIndex1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index1"], sideSuffix),
			parent=self.ctrlInHandIndex.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			color=color,
		)
		self.ctrlIndex2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index2"], sideSuffix),
			parent=self.ctrlIndex1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			color=color,
		)
		self.ctrlIndex3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index3"], sideSuffix),
			parent=self.ctrlIndex2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Index3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index3"], sideSuffix),
			color=color,
		)
		# Middle
		self.ctrlInHandMiddle = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandMiddle"], sideSuffix),
			color=color,
		)
		self.ctrlMiddle1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle1"], sideSuffix),
			parent=self.ctrlInHandMiddle.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			color=color,
		)
		self.ctrlMiddle2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle2"], sideSuffix),
			parent=self.ctrlMiddle1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			color=color,
		)
		self.ctrlMiddle3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle3"], sideSuffix),
			parent=self.ctrlMiddle2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Middle3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle3"], sideSuffix),
			color=color,
		)
		# Ring
		self.ctrlInHandRing = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandRing"], sideSuffix),
			color=color,
		)
		self.ctrlRing1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring1"], sideSuffix),
			parent=self.ctrlInHandRing.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			color=color,
		)
		self.ctrlRing2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring2"], sideSuffix),
			parent=self.ctrlRing1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			color=color,
		)
		self.ctrlRing3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring3"], sideSuffix),
			parent=self.ctrlRing2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Ring3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring3"], sideSuffix),
			color=color,
		)
		# Pinky
		self.ctrlInHandPinky = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["InHandPinky"], sideSuffix),
			color=color,
		)
		self.ctrlPinky1 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			parent=self.ctrlInHandPinky.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			color=color,
		)
		self.ctrlPinky2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			parent=self.ctrlPinky1.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			color=color,
		)
		self.ctrlPinky3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			parent=self.ctrlPinky2.transform,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			color=color,
		)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Hand"], sideSuffix)


	def getCtrls(self):
		return (
			self.ctrlThumb1, self.ctrlThumb2, self.ctrlThumb3,
			self.ctrlInHandIndex, self.ctrlIndex1, self.ctrlIndex2, self.ctrlIndex3,
			self.ctrlInHandMiddle, self.ctrlMiddle1, self.ctrlMiddle2, self.ctrlMiddle3,
			self.ctrlInHandRing, self.ctrlRing1, self.ctrlRing2, self.ctrlRing3,
			self.ctrlInHandPinky, self.ctrlPinky1, self.ctrlPinky2, self.ctrlPinky3,
		)
	
	def getMainCtrls(self):
		return (
			self.ctrlThumb1, self.ctrlThumb2, self.ctrlThumb3,
			self.ctrlIndex1, self.ctrlIndex2, self.ctrlIndex3,
			self.ctrlMiddle1, self.ctrlMiddle2, self.ctrlMiddle3,
			self.ctrlRing1, self.ctrlRing2, self.ctrlRing3,
			self.ctrlPinky1, self.ctrlPinky2, self.ctrlPinky3,
		)

	def getFirstKnucklesCtrls(self):
		return (
			self.ctrlThumb1,
			self.ctrlIndex1,
			self.ctrlMiddle1,
			self.ctrlRing1,
			self.ctrlPinky1, 
		)

	def getZlockCtrls(self):
		return (
			self.ctrlThumb2, self.ctrlThumb3,
			self.ctrlIndex2, self.ctrlIndex3,
			self.ctrlMiddle2, self.ctrlMiddle3,
			self.ctrlRing2, self.ctrlRing3,
			self.ctrlPinky2, self.ctrlPinky3,
		)

	def getInHandCtrls(self):
		return (self.ctrlInHandIndex, self.ctrlInHandMiddle, self.ctrlInHandRing, self.ctrlInHandPinky)

	def getThumbCtrls(self):
		return (self.ctrlThumb1, self.ctrlThumb2, self.ctrlThumb3)

	def getIndexCtrls(self):
		return (self.ctrlInHandIndex, self.ctrlIndex1, self.ctrlIndex2, self.ctrlIndex3)

	def getMiddleCtrls(self):
		return (self.ctrlInHandMiddle, self.ctrlMiddle1, self.ctrlMiddle2, self.ctrlMiddle3)
	
	def getRignCtrls(self):
		return (self.ctrlInHandRing, self.ctrlRing1, self.ctrlRing2, self.ctrlRing3)

	def getPinkyCtrls(self):
		return (self.ctrlInHandPinky, self.ctrlPinky1, self.ctrlPinky2, self.ctrlPinky3)




#--------------------------------------------------------------------------------------------------
#	Out Components
#--------------------------------------------------------------------------------------------------




class Out2bLimbComponent():
	"""Class for building the fk 2b limb component.
	"""

	def __init__(self, 
	  	parent:str, start:str, mid:str, end:str, root:str=None,
			upperTwist1:str=None, upperTwist2:str=None, lowerTwist1:str=None, lowerTwist2:str=None, 
			drawFkIkState:bool=True, fkIkStatePosition:tuple=(0.0, 0.0, 0.0), createTwistSolver:bool=True,
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
			colorSwitch = "orange"
		if side == "center":
			sideSuffix = ""
			color = "lightyellow"
			colorSwitch = "yellow"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
			colorSwitch = "blue"

		if self.root:
			self.ctrlRoot = OutCtrl(
				name=f"{root}{sideSuffix}_out", parent=parent,
				translateTo=f"{root}{sideSuffix}", rotateTo=f"{root}{sideSuffix}",
				color=color,
			)
			parent = self.ctrlRoot.transform

		self.ctrlStart = OutCtrl(
			name=f"{start}{sideSuffix}_out",	parent=parent,
			translateTo=f"{start}{sideSuffix}",	rotateTo=f"{start}{sideSuffix}",
			color=color,
		)
		# Upper - twist bones
		if upperTwist1:
			self.ctrlTwistUpper1 = TwistCtrl(
				name=f"{upperTwist1}{sideSuffix}_ctrl",	parent=self.ctrlStart.transform,
				translateTo=f"{upperTwist1}{sideSuffix}",	rotateTo=f"{upperTwist1}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistUpper1.transform)
		if upperTwist2:
			self.ctrlTwistUpper2 = TwistCtrl(
				name=f"{upperTwist2}{sideSuffix}_ctrl",	parent=self.ctrlStart.transform,
				translateTo=f"{upperTwist2}{sideSuffix}",	rotateTo=f"{upperTwist2}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistUpper2.transform)

		self.ctrlMid = OutCtrl(
			name=f"{mid}{sideSuffix}_out", parent=self.ctrlStart.transform,
			translateTo=f"{mid}{sideSuffix}", rotateTo=f"{mid}{sideSuffix}",
			color=color,
		)
		# Lower - twist bones
		if lowerTwist1:
			self.ctrlTwistLower1 = TwistCtrl(
				name=f"{lowerTwist1}{sideSuffix}_ctrl",	parent=self.ctrlMid.transform,
				translateTo=f"{lowerTwist1}{sideSuffix}",	rotateTo=f"{lowerTwist1}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistLower1.transform)
		if lowerTwist2:
			self.ctrlTwistLower2 = TwistCtrl(
				name=f"{lowerTwist2}{sideSuffix}_ctrl",	parent=self.ctrlMid.transform,
				translateTo=f"{lowerTwist2}{sideSuffix}",	rotateTo=f"{lowerTwist2}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistLower2.transform)

		self.ctrlEnd = OutCtrl(
			name=f"{end}{sideSuffix}_out", parent=self.ctrlMid.transform,
			translateTo=f"{end}{sideSuffix}",	rotateTo=f"{end}{sideSuffix}",
			drawFkIkState=drawFkIkState, fkIkStatePosition=fkIkStatePosition,
			color=colorSwitch,
		)

		[lm.LMAttribute.copyTransformsToOPM(ctrl.transform) for ctrl in self.getCtrls()]

		# Create solver setup
		if createTwistSolver:
			# Upper Limb
			self.nodeTwistUpper = cmds.createNode("twistSolver")
			cmds.setAttr(f"{self.nodeTwistUpper}.segmentCount", 4)
			cmds.setAttr(f"{self.nodeTwistUpper}.invertTwist", True)
			cmds.setAttr(f"{self.nodeTwistUpper}.reverseSegments", True)
			# Reverse segments top to bottom or bottom to top
			cmds.connectAttr(f"{self.ctrlStart.transform}.worldMatrix[0]", f"{self.nodeTwistUpper}.inputMatrix")
			cmds.connectAttr(f"{self.nodeTwistUpper}.twistSegmentOut[1]", f"{self.ctrlTwistUpper1.transform}.rotateAxisX")
			cmds.connectAttr(f"{self.nodeTwistUpper}.twistSegmentOut[2]", f"{self.ctrlTwistUpper2.transform}.rotateAxisX")
			# Lower Arm
			self.nodeTwistLower = cmds.createNode("twistSolver")
			cmds.setAttr(f"{self.nodeTwistLower}.segmentCount", 4)
			cmds.setAttr(f"{self.nodeTwistLower}.reverseSegments", True)
			cmds.connectAttr(f"{self.ctrlEnd.transform}.worldMatrix[0]", f"{self.nodeTwistLower}.inputMatrix")
			cmds.connectAttr(f"{self.nodeTwistLower}.twistSegmentOut[1]", f"{self.ctrlTwistLower1.transform}.rotateAxisX")
			cmds.connectAttr(f"{self.nodeTwistLower}.twistSegmentOut[3]", f"{self.ctrlTwistLower2.transform}.rotateAxisX")


	def getCtrls(self):
		"""Returns all the controller objects.
		"""
		if self.root: return (self.ctrlRoot, self.ctrlStart, self.ctrlMid, self.ctrlEnd)

		return (self.ctrlStart, self.ctrlMid, self.ctrlEnd)


	def getTwistCtrls(self):
		return (self.ctrlTwistUpper1, self.ctrlTwistUpper2, self.ctrlTwistLower1, self.ctrlTwistLower2)




#--------------------------------------------------------------------------------------------------
#	Ik Components
#--------------------------------------------------------------------------------------------------




class Ik2bLimbComponent():
	"""Class for building ik comoponents."""

	def __init__(self,
	  name:str, parent:str, rotateTo:str, 
		fkStart:str, fkMid:str, fkEnd:str,
		outStart:str, outMid:str, outEnd:str,
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

		self.ctrlIk = IkCtrl(
			name=f"{name}_ik{sideSuffix}_ctrl",
			parent=parent,
			translateTo=fkEnd,
			rotateTo=fkEnd,
			lineWidth=2.0,
			color=color,
		)

		if self.poleVector != "":
			self.ctrlPoleVector = PoleVectorCtrl(
				name=f"{name}_pv{sideSuffix}_ctrl",
				parent=parent,
				translateTo=poleVector,
				rotateTo=rotateTo,
				lineWidth=2.0,
				color=color,
			)
			poleVector=self.ctrlPoleVector.transform

		self.nodeIk2bSolver = cmds.ik(
			name=f"{name}{sideSuffix}_",
			fkStart=fkStart,
			fkMid=fkMid,
			fkEnd=fkEnd,
			ikHandle=self.ctrlIk.transform,
			poleVector=poleVector,
			outStart=outStart,
			outMid=outMid,
			outEnd=outEnd,
			mode=mode,
		)[0]
	

		self.displFkCtrls = cmds.createNode("displayLayer", name=f"{name}_fk{sideSuffix}_displ")
		self.displIkCtrls = cmds.createNode("displayLayer", name=f"{name}_ik{sideSuffix}_displ")
		cmds.connectAttr(f"{self.nodeIk2bSolver}.fkVisibility", f"{self.displFkCtrls}.visibility")
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkStart}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkMid}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkEnd}.drawOverride", force=True)
		cmds.connectAttr(f"{self.nodeIk2bSolver}.ikVisibility", f"{self.displIkCtrls}.visibility")
		cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.ctrlIk.transform}.drawOverride", force=True)
		if self.poleVector != "":
			cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.ctrlPoleVector.transform}.drawOverride", force=True)
			cmds.connectAttr(f"{outMid}.worldMatrix[0]", f"{self.ctrlPoleVector.shape}.drawLineTo")
			lm.LMAttribute.copyTransformsToOPM(self.ctrlPoleVector.transform)

		lm.LMAttribute.copyTransformsToOPM(self.ctrlIk.transform)


	def getCtrls(self):
		"""Returns all the controller objects.
		"""
		if self.poleVector != "":	return (self.ctrlIk, self.ctrlPoleVector)

		return [self.ctrlIk]




class IkSpineComponent():
	"""Class for building the fk spine component."""


	def __init__(self, parent, listJoints) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		# Main chain
		self.ctrlSpine1 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine1"]),
			parent=parent,
			translateTo=listJoints["Spine"]["Spine1"],
			rotateTo=listJoints["Spine"]["Spine1"],
		)
		# self.ctrlSpine2 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine2"]),
		# 	parent=self.ctrlSpine1.transform,
		# 	translateTo=listJoints["Spine"]["Spine2"],
		# 	rotateTo=listJoints["Spine"]["Spine2"],
		# )
		# self.ctrlSpine3 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine3"]),
		# 	parent=self.ctrlSpine2.transform,
		# 	translateTo=listJoints["Spine"]["Spine3"],
		# 	rotateTo=listJoints["Spine"]["Spine3"],
		# )
		# self.ctrlSpine4 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine4"]),
		# 	parent=self.ctrlSpine3.transform,
		# 	translateTo=listJoints["Spine"]["Spine4"],
		# 	rotateTo=listJoints["Spine"]["Spine4"],
		# )
		# self.ctrlSpine5 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine5"]["Root"]),
		# 	parent=self.ctrlSpine4.transform,
		# 	translateTo=listJoints["Spine"]["Spine5"]["Root"],
		# 	rotateTo=listJoints["Spine"]["Spine5"]["Root"],
		# )

		# self.ctrlCorrective = []
		# for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}_ctrl",
		# 		parent=self.ctrlSpine5.transform,
		# 		translateTo=joint,
		# 		rotateTo=joint
		# 	)
		# 	self.ctrlCorrective.append(CtrlCorrective)

		lm.LMTransformUtils.postCtrlTransform(listJoints["Spine"])


	# def getCtrls(self):
	# 	return (self.ctrlSpine1, self.ctrlSpine2, self.ctrlSpine3, self.ctrlSpine4, self.ctrlSpine5)




#--------------------------------------------------------------------------------------------------
# Components
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
		self.ctrlPelvis = PelvisCtrl(
			parent=self.grpComp,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
			# color="yellow",
		)
		self.ctrlPelvisRot = Ctrl(
			name="{}_rot_ctrl".format(listJoints["Spine"]["Pelvis"]),
			parent=self.ctrlPelvis.transform,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
		)

		lm.LMAttribute.copyTransformsToOPM(self.ctrlPelvis.transform)
		lm.LMAttribute.lockControlChannels(self.ctrlPelvis.transform, lockChannels=["scale", "visibility"])
		lm.LMAttribute.copyTransformsToOPM(self.ctrlPelvisRot.transform)
		lm.LMAttribute.lockControlChannels(self.ctrlPelvisRot.transform, lockChannels=["translate", "scale", "visibility"])


	def getCtrls(self):
		return (self.ctrlPelvis, self.ctrlPelvisRot)




class SpineComponent():

	def __init__(self, compRig, attachTo:str, listJoints:list) -> None:
		
		self.grpComp = cmds.group(name="spine_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkSpineComponent(self.grpComp, listJoints)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlSpine1.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode=listJoints["Spine"]["Spine1"]
		)


	def getCtrls(self):
		""""Returns all ctrl from the component.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())

		return listCtrls




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
			createTwistSolver=False,
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


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.extend(self.out.getCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class Leg2bComponent():
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

		self.out = Out2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Leg"]["UpLeg"],
			mid=listJoints["Leg"]["Leg"],
			end=listJoints["Leg"]["Foot"]["Root"],
			upperTwist1=listJoints["Leg"]["UpLegRoll1"]["Root"],
			upperTwist2=listJoints["Leg"]["UpLegRoll2"]["Root"],
			lowerTwist1=listJoints["Leg"]["LegRoll1"]["Root"],
			lowerTwist2=listJoints["Leg"]["LegRoll2"]["Root"],
			fkIkStatePosition=fkIkStatePosition, 
			side=side
		)

		self.ik = Ik2bLimbComponent(
			name="leg",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.transform,
			fkStart=self.fk.ctrlStart.transform,
			fkMid=self.fk.ctrlMid.transform,
			fkEnd=self.fk.ctrlEnd.transform,
			poleVector=f"leg_pv{sideSuffix}",
			outStart=self.out.ctrlStart.transform,
			outMid=self.out.ctrlMid.transform,
			outEnd=self.out.ctrlEnd.transform,
			side=side,
		)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlStart.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Leg"]["UpLeg"]), sideSuffix)
		)
		cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.ctrlStart.transform}.offsetParentMatrix")


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.extend(self.out.getCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




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
			child=self.fk.ctrlToe.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Leg"]["ToeBase"]), sideSuffix)
		)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		# listCtrls.extend(self.out.getCtrls())
		# listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class Arm2bComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, fkIkStatePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
			colorSwitch = "orange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
			colorSwitch = "blue"

		self.grpComp = cmds.group(name=f"arm{sideSuffix}_grp", parent=compRig.ctrlMain.transform, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			root=listJoints["Arm"]["Shoulder"]["Root"],
			start=listJoints["Arm"]["Arm"],
			mid=listJoints["Arm"]["ForeArm"],
			end=listJoints["Arm"]["Hand"]["Root"],
			side=side,
		)

		self.out = Out2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Arm"]["Arm"],
			mid=listJoints["Arm"]["ForeArm"],
			end=listJoints["Arm"]["Hand"]["Root"],
			upperTwist1=listJoints["Arm"]["ArmRoll1"]["Root"],
			upperTwist2=listJoints["Arm"]["ArmRoll2"]["Root"],
			lowerTwist1=listJoints["Arm"]["ForeArmRoll1"],
			lowerTwist2=listJoints["Arm"]["ForeArmRoll2"],
			fkIkStatePosition=fkIkStatePosition, 
			side=side
		)

		self.ik = Ik2bLimbComponent(
			name="arm",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.transform,
			fkStart=self.fk.ctrlStart.transform,
			fkMid=self.fk.ctrlMid.transform,
			fkEnd=self.fk.ctrlEnd.transform,
			poleVector=f"arm_pv{sideSuffix}",
			outStart=self.out.ctrlStart.transform, outMid=self.out.ctrlMid.transform,	outEnd=self.out.ctrlEnd.transform,
			side=side,
		)

		self.cnstMatFk = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlRoot.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Arm"]["Shoulder"]["Root"]), sideSuffix)
		)
		self.cnstMatOut = LMRigUtils.createMatrixConstraint(
			parent=self.fk.ctrlRoot.transform, 
			child=self.out.ctrlStart.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Arm"]["Arm"]), sideSuffix)
		)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.extend(self.out.getCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




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
			child=self.fk.ctrlThumb1.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["Thumb1"]), sideSuffix)
		)
		self.cnstIndex = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandIndex.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandIndex"]), sideSuffix)
		)
		self.cnstMiddle = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandMiddle.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandMiddle"]), sideSuffix)
		)
		self.cnstPinky = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandPinky.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandPinky"]), sideSuffix)
		)
		self.cnstRing = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandRing.transform,
			offset=compRig.ctrlMain.transform, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandRing"]), sideSuffix)
		)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		# listCtrls.extend(self.out.getCtrls())
		# listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class FkIkSwitchComponent():
	"""Class for building the rig controller.
	"""

	def __init__(self,
	  compRig,
		compHead,
		compLeftArm, compRightArm,
		compLeftLeg, compRightLeg, 
		parent="",
		translateTo="",	rotateTo="",
		color="yellow",
	):
		# Create controller
		self.ctrlFkIkSwitch = FkIkSwitchCtrl(
			parent=compRig.ctrlMain.transform,
			translateTo=compRig.ctrlMain.transform, rotateTo=compRig.ctrlMain.transform,
			# localPosition=localPosition,
			# fkIkStatePosition=fkIkStatePosition
		)
		self.matCnst = LMRigUtils.createMatrixConstraint(
			parent=compHead.out.ctrlEnd.transform, 
			child=self.ctrlFkIkSwitch.transform,
			offset=compRig.ctrlMain.transform, 
		)

		# TODO split this into a method
		# Create switch attrs
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "headFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "headSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.transform, "headTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.headFkIk", f"{compHead.ik.nodeIk2bSolver}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.headFkIk", f"{compHead.out.ctrlEnd.shape}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.headSoftness", f"{compHead.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.headTwist", f"{compHead.ik.nodeIk2bSolver}.twist")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.transform)

		# Left Arm
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "leftArmFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "leftArmSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.transform, "leftArmTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftArmFkIk", f"{compLeftArm.ik.nodeIk2bSolver}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftArmFkIk", f"{compLeftArm.out.ctrlEnd.shape}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftArmTwist", f"{compLeftArm.ik.nodeIk2bSolver}.twist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftArmSoftness", f"{compLeftArm.ik.nodeIk2bSolver}.softness")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.transform, "leftArmTwistCtrlsVisibility")
		displLeftArmTwistCtrls = cmds.createNode("displayLayer", name="arm_twist_l_displ")
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displLeftArmTwistCtrls}.visibility")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistUpper1.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistUpper2.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistLower1.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistLower2.transform}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.transform, "__")

		# Right Arm
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "rightArmFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "rightArmSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.transform, "rightArmTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightArmFkIk", f"{compRightArm.ik.nodeIk2bSolver}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightArmFkIk", f"{compRightArm.out.ctrlEnd.shape}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightArmTwist", f"{compRightArm.ik.nodeIk2bSolver}.twist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightArmSoftness", f"{compRightArm.ik.nodeIk2bSolver}.softness")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.transform, "rightArmTwistCtrlsVisibility")
		displRightArmTwistCtrls = cmds.createNode("displayLayer", name="arm_twist_r_displ")
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displRightArmTwistCtrls}.visibility")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistUpper1.transform}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistUpper2.transform}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistLower1.transform}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistLower2.transform}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.transform, "___")

		# Left Leg
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "leftLegFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "leftLegSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.transform, "leftLegTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftLegFkIk", f"{compLeftLeg.ik.nodeIk2bSolver}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftLegFkIk", f"{compLeftLeg.out.ctrlEnd.shape}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftLegSoftness", f"{compLeftLeg.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.leftLegTwist", f"{compLeftLeg.ik.nodeIk2bSolver}.twist")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.transform, "leftLegTwistCtrlsVisibility")
		displLeftLegTwistCtrls = cmds.createNode("displayLayer", name="leg_twist_l_displ")
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displLeftLegTwistCtrls}.visibility")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistUpper1.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistUpper2.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistLower1.transform}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistLower2.transform}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.transform, "____")

		# Right Leg
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "rightLegFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.transform, "rightLegSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.transform, "rightLegTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightLegFkIk", f"{compRightLeg.ik.nodeIk2bSolver}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightLegFkIk", f"{compRightLeg.out.ctrlEnd.shape}.fkIk")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightLegSoftness", f"{compRightLeg.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.transform}.rightLegTwist", f"{compRightLeg.ik.nodeIk2bSolver}.twist")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.transform, "rightLegTwistCtrlsVisibility")
		displRightLegTwistCtrls = cmds.createNode("displayLayer", name="leg_twist_r_displ")
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displRightLegTwistCtrls}.visibility")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistUpper1.transform}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistUpper2.transform}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistLower1.transform}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistLower2.transform}.drawOverride")




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

