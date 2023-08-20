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


dict_colors = {
	"lightyellow": 	[1.0, 1.0, 0.25],
	"yellow": 			[1.0, 0.6, 0.1],
	"lightorange": 	[1.0, 0.467, 0.2],
	"orange": 			[0.8, 0.25, 0.05],
	"lightblue": 		[0.4, 0.8, 1.0],
	"blue": 				[0.05, 0.25, 0.8],
	"magenta": 			[0.6, 0.2, 0.4],
	"green": 				[0.2, 0.8, 0.4]
}



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
		localScale=(3.0, 3.0, 3.0),
		shape="circle",
		hasDynamicAttributes=False,
		drawSolverMode=False,
		solverModePosition=(0.0, 0.0, 0.0),
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
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			hasDynamicAttributes=hasDynamicAttributes,
			drawSolverMode=drawSolverMode,
			solverModePosition=solverModePosition,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
		drawSolverMode=False,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["v"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		self.__createUnifiedScale()
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)
		# lm.LMAttribute.lockControlPlugs(self.node, lockChannels)


	def __createUnifiedScale(self):
		"""Creates unified scale attribute on the main controller.
		"""
		cmds.addAttr(
			self.node,
			longName="rigScale",
			minValue=0.001,
			maxValue=100,
			defaultValue=1.0
		)
		cmds.setAttr(f"{self.node}.rigScale", keyable=False, channelBox=True)
		for axis in ["x", "y", "z"]:
			cmds.connectAttr(f"{self.node}.rigScale", f"{self.node}.s{axis}")
			cmds.setAttr(f"{self.node}.s{axis}", keyable=False)




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
		drawSolverMode=False,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




class PelvisCtrl(Ctrl):
	"""Class for building the center of graivty controller."""
	def __init__(self,
		name="pelvis_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(40.0, 40.0, 40.0),
		shape="square",
		drawSolverMode=False,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
		hasDynamicAttributes=True,
		drawSolverMode=False,
		solverModePosition=(0.0, 0.0, 0.0),
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=True,
		lockChannels=["scale", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			hasDynamicAttributes=hasDynamicAttributes,
			drawSolverMode=drawSolverMode,
			solverModePosition=solverModePosition,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
		drawSolverMode=False,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




class FingerCtrl():
	"""Class for building the rig controller."""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 90.0),
		localScale=(3.0, 3.0, 3.0),
		shape="circle",
		# fillShape=False,
		drawSolverMode=False,
		#fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultFingerLineWidth,
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			# fillShape=fillShape,
			#fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




class IkCtrl():
	"""Class for building the rig controller."""
	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(6.0, 6.0, 6.0),
		shape="cube",
		drawSolverMode=False,
		solverModePosition=(0.0, 0.0, 0.0),
		lineWidth=Ctrl.defaultLineWidth,
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			solverModePosition=solverModePosition,
			lineWidth=Ctrl.defaultLineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
		drawSolverMode=False,
		solverModePosition=(0.0, 0.0, 0.0),
		lineWidth=Ctrl.defaultLineWidth,
		color="yellow",
		lockShapeAttributes=True,
		lockChannels=["translate", "rotate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "visibility"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			solverModePosition=solverModePosition,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)





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
		drawSolverMode=False,
		drawLine=True,
		hasDynamicAttributes=True,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
		lockChannels=["scale"]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			drawLine=drawLine,
			hasDynamicAttributes=hasDynamicAttributes,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
		drawSolverMode=False,
		lineWidth=Ctrl.defaultLineWidth,
		color="lightyellow",
		lockShapeAttributes=True,
		# lockChannels=["scale", "visibility"]
		lockChannels=[]
	):
		self.node = cmds.ctrl(
			name=name,
			parent=parent,
			translateTo=translateTo,
			rotateTo=rotateTo,
			localPosition=localPosition,
			localRotate=localRotate,
			localScale=localScale,
			shape=shape,
			drawSolverMode=drawSolverMode,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.node, lockChannels)




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
			parent = self.ctrlRoot.node

		self.ctrlStart = Ctrl(
			name=f"{start}{sideSuffix}_ctrl",	parent=parent,
			translateTo=f"{start}{sideSuffix}",	rotateTo=f"{start}{sideSuffix}",
			color=color,
		)

		self.ctrlMid = Ctrl(
			name=f"{mid}{sideSuffix}_ctrl", parent=self.ctrlStart.node,
			translateTo=f"{mid}{sideSuffix}", rotateTo=f"{mid}{sideSuffix}",
			color=color,
		)

		self.ctrlEnd = Ctrl(
			name=f"{end}{sideSuffix}_ctrl", parent=self.ctrlMid.node,
			translateTo=f"{end}{sideSuffix}",	rotateTo=f"{end}{sideSuffix}",
			color=color,
		)

		[lm.LMAttribute.copyTransformsToOPM(ctrl.node) for ctrl in self.getCtrls()]


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
			parent=self.ctrlSpine1.node,
			translateTo=listJoints["Spine"]["Spine2"],
			rotateTo=listJoints["Spine"]["Spine2"],
		)
		self.ctrlSpine3 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine3"]),
			parent=self.ctrlSpine2.node,
			translateTo=listJoints["Spine"]["Spine3"],
			rotateTo=listJoints["Spine"]["Spine3"],
		)
		self.ctrlSpine4 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine4"]),
			parent=self.ctrlSpine3.node,
			translateTo=listJoints["Spine"]["Spine4"],
			rotateTo=listJoints["Spine"]["Spine4"],
		)
		self.ctrlSpine5 = Ctrl(
			name="{}_ctrl".format(listJoints["Spine"]["Spine5"]["Root"]),
			parent=self.ctrlSpine4.node,
			translateTo=listJoints["Spine"]["Spine5"]["Root"],
			rotateTo=listJoints["Spine"]["Spine5"]["Root"],
		)

		# self.ctrlCorrective = []
		# for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}_ctrl",
		# 		parent=self.ctrlSpine5.node,
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
		lm.LMAttribute.copyTransformsToOPM(self.ctrlToe.node)
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
			parent=self.ctrlThumb1.node,
			translateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Thumb2"], sideSuffix),
			color=color,
		)
		self.ctrlThumb3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Thumb3"], sideSuffix),
			parent=self.ctrlThumb2.node,
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
			parent=self.ctrlInHandIndex.node,
			translateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index1"], sideSuffix),
			color=color,
		)
		self.ctrlIndex2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index2"], sideSuffix),
			parent=self.ctrlIndex1.node,
			translateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Index2"], sideSuffix),
			color=color,
		)
		self.ctrlIndex3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Index3"], sideSuffix),
			parent=self.ctrlIndex2.node,
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
			parent=self.ctrlInHandMiddle.node,
			translateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle1"], sideSuffix),
			color=color,
		)
		self.ctrlMiddle2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle2"], sideSuffix),
			parent=self.ctrlMiddle1.node,
			translateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Middle2"], sideSuffix),
			color=color,
		)
		self.ctrlMiddle3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Middle3"], sideSuffix),
			parent=self.ctrlMiddle2.node,
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
			parent=self.ctrlInHandRing.node,
			translateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring1"], sideSuffix),
			color=color,
		)
		self.ctrlRing2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring2"], sideSuffix),
			parent=self.ctrlRing1.node,
			translateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Ring2"], sideSuffix),
			color=color,
		)
		self.ctrlRing3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Ring3"], sideSuffix),
			parent=self.ctrlRing2.node,
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
			parent=self.ctrlInHandPinky.node,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky1"], sideSuffix),
			color=color,
		)
		self.ctrlPinky2= FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			parent=self.ctrlPinky1.node,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky2"], sideSuffix),
			color=color,
		)
		self.ctrlPinky3 = FingerCtrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			parent=self.ctrlPinky2.node,
			translateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Pinky3"], sideSuffix),
			color=color,
		)
	
		# Weapon
		self.ctrlWeapon = Ctrl(
			name="{}{}_ctrl".format(listJoints["Hand"]["Weapon"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Hand"]["Weapon"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Hand"]["Weapon"], sideSuffix),
			shape="cube",
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
			# self.ctrlWeapon,
		)
	
	def getWeaponCtrls(self):
		return (self.ctrlWeapon)
	
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
	  	parent:str, compRig,
			start:str, mid:str, end:str, root:str=None,
			upperTwist1:str=None, upperTwist2:str=None, lowerTwist1:str=None, lowerTwist2:str=None, 
			drawSolverMode:bool=True, solverModePosition:tuple=(0.0, 0.0, 0.0), createTwistSolver:bool=True,
			side:str="center", hasDynamicAttributes:bool=True,
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
			lm.LMAttribute.copyTransformsToOPM(self.ctrlRoot.node)
			parent = self.ctrlRoot.node

		self.ctrlStart = OutCtrl(
			name=f"{start}{sideSuffix}_out",	parent=parent,
			translateTo=f"{start}{sideSuffix}",	rotateTo=f"{start}{sideSuffix}",
			color=color,
		)
		lm.LMAttribute.copyTransformsToOPM(self.ctrlStart.node)
	
		# Upper - twist bones
		if upperTwist1:
			self.ctrlTwistUpper1 = TwistCtrl(
				name=f"{upperTwist1}{sideSuffix}_ctrl",	parent=parent,
				translateTo=f"{upperTwist1}{sideSuffix}",	rotateTo=f"{upperTwist1}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistUpper1.node)
			self.twistUpper1cnstMat = LMRigUtils.createMatrixConstraint(
				parent=self.ctrlStart.node, 
				child=self.ctrlTwistUpper1.node,
				offset=compRig.ctrlMain.node, 
				sourceNode=f"{upperTwist1}{sideSuffix}",
			)
		# cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.ctrlStart.node}.offsetParentMatrix")
		if upperTwist2:
			self.ctrlTwistUpper2 = TwistCtrl(
				name=f"{upperTwist2}{sideSuffix}_ctrl",	parent=parent,
				translateTo=f"{upperTwist2}{sideSuffix}",	rotateTo=f"{upperTwist2}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistUpper2.node)
			self.twistUpper2cnstMat = LMRigUtils.createMatrixConstraint(
				parent=self.ctrlStart.node, 
				child=self.ctrlTwistUpper2.node,
				offset=compRig.ctrlMain.node, 
				sourceNode=f"{upperTwist2}{sideSuffix}",
			)

		self.ctrlMid = OutCtrl(
			name=f"{mid}{sideSuffix}_out", parent=self.ctrlStart.node,
			translateTo=f"{mid}{sideSuffix}", rotateTo=f"{mid}{sideSuffix}",
			color=color,
		)
		# Lower - twist bones
		if lowerTwist1:
			self.ctrlTwistLower1 = TwistCtrl(
				name=f"{lowerTwist1}{sideSuffix}_ctrl",	parent=parent,
				translateTo=f"{lowerTwist1}{sideSuffix}",	rotateTo=f"{lowerTwist1}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistLower1.node)
			self.twistLower1cnstMat = LMRigUtils.createMatrixConstraint(
				parent=self.ctrlMid.node, 
				child=self.ctrlTwistLower1.node,
				offset=compRig.ctrlMain.node, 
				sourceNode=f"{lowerTwist1}{sideSuffix}",
			)
		if lowerTwist2:
			self.ctrlTwistLower2 = TwistCtrl(
				name=f"{lowerTwist2}{sideSuffix}_ctrl",	parent=parent,
				translateTo=f"{lowerTwist2}{sideSuffix}",	rotateTo=f"{lowerTwist2}{sideSuffix}",
				color=color,
			)
			lm.LMAttribute.copyTransformsToOPM(self.ctrlTwistLower2.node)
			self.twistLower2cnstMat = LMRigUtils.createMatrixConstraint(
				parent=self.ctrlMid.node, 
				child=self.ctrlTwistLower2.node,
				offset=compRig.ctrlMain.node, 
				sourceNode=f"{lowerTwist2}{sideSuffix}",
			)

		self.ctrlEnd = OutCtrl(
			name=f"{end}{sideSuffix}_out", parent=self.ctrlMid.node,
			translateTo=f"{end}{sideSuffix}",	rotateTo=f"{end}{sideSuffix}",
			drawSolverMode=drawSolverMode, solverModePosition=solverModePosition,
			color=colorSwitch, hasDynamicAttributes=hasDynamicAttributes,
		)

		[lm.LMAttribute.copyTransformsToOPM(ctrl.node) for ctrl in self.getCtrls()]

		cmds.setAttr(f"{self.ctrlStart.node}.hiddenInOutliner", True)

		# Create solver setup
		if createTwistSolver:
			# Upper Limb
			self.nodeTwistUpper = cmds.createNode("twistSolver")
			cmds.setAttr(f"{self.nodeTwistUpper}.segmentCount", 4)
			cmds.setAttr(f"{self.nodeTwistUpper}.invertTwist", True)
			cmds.setAttr(f"{self.nodeTwistUpper}.reverseSegments", True)
			# Reverse segments top to bottom or bottom to top
			cmds.connectAttr(f"{self.ctrlStart.node}.worldMatrix[0]", f"{self.nodeTwistUpper}.inputMatrix")
			cmds.connectAttr(f"{self.nodeTwistUpper}.twistSegmentOut[1]", f"{self.ctrlTwistUpper1.node}.rotateAxisX")
			cmds.connectAttr(f"{self.nodeTwistUpper}.twistSegmentOut[2]", f"{self.ctrlTwistUpper2.node}.rotateAxisX")
			# Lower Arm
			self.nodeTwistLower = cmds.createNode("twistSolver")
			cmds.setAttr(f"{self.nodeTwistLower}.segmentCount", 4)
			cmds.setAttr(f"{self.nodeTwistLower}.reverseSegments", True)
			cmds.connectAttr(f"{self.ctrlEnd.node}.worldMatrix[0]", f"{self.nodeTwistLower}.inputMatrix")
			cmds.connectAttr(f"{self.nodeTwistLower}.twistSegmentOut[1]", f"{self.ctrlTwistLower1.node}.rotateAxisX")
			cmds.connectAttr(f"{self.nodeTwistLower}.twistSegmentOut[3]", f"{self.ctrlTwistLower2.node}.rotateAxisX")


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
		ikStart:str, ikMid:str, ikEnd:str,
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

		self.ctrlStart = OutCtrl(
			name=f"{ikStart}{sideSuffix}_ik",	parent=parent,
			translateTo=f"{ikStart}{sideSuffix}",	rotateTo=f"{ikStart}{sideSuffix}",
			color=color,
		)

		self.ctrlMid = OutCtrl(
			name=f"{ikMid}{sideSuffix}_ik", parent=self.ctrlStart.node,
			translateTo=f"{ikMid}{sideSuffix}", rotateTo=f"{ikMid}{sideSuffix}",
			color=color,
		)
	
		self.ctrlEnd = OutCtrl(
			name=f"{ikEnd}{sideSuffix}_ik", parent=self.ctrlMid.node,
			translateTo=f"{ikEnd}{sideSuffix}",	rotateTo=f"{ikEnd}{sideSuffix}",
			color=color,
		)

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
			poleVector=self.ctrlPoleVector.node

		self.nodeIk2bSolver = cmds.ik(
			name=f"{name}{sideSuffix}_",
			fkStart=fkStart,
			fkMid=fkMid,
			fkEnd=fkEnd,
			ikStart=self.ctrlStart.node,
			ikMid=self.ctrlMid.node,
			ikEnd=self.ctrlEnd.node,
			ikHandle=self.ctrlIk.node,
			poleVector=poleVector,
			outStart=outStart,
			outMid=outMid,
			outEnd=outEnd,
			mode=mode,
		)[0]


		self.displFkCtrls = cmds.createNode("displayLayer", name=f"{name}_fk{sideSuffix}_displ")
		cmds.setAttr(f"{self.displFkCtrls}.enabled", True)
		cmds.setAttr(f"{self.displFkCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{self.displFkCtrls}.overrideColorR", dict_colors[color][0])
		cmds.setAttr(f"{self.displFkCtrls}.overrideColorG", dict_colors[color][1])
		cmds.setAttr(f"{self.displFkCtrls}.overrideColorB", dict_colors[color][2])
		self.displIkCtrls = cmds.createNode("displayLayer", name=f"{name}_ik{sideSuffix}_displ")
		cmds.setAttr(f"{self.displIkCtrls}.enabled", True)
		cmds.setAttr(f"{self.displIkCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{self.displIkCtrls}.overrideColorR", dict_colors[colorSwitch][0])
		cmds.setAttr(f"{self.displIkCtrls}.overrideColorG", dict_colors[colorSwitch][1])
		cmds.setAttr(f"{self.displIkCtrls}.overrideColorB", dict_colors[colorSwitch][2])
	
	
		cmds.connectAttr(f"{self.nodeIk2bSolver}.fkVisibility", f"{self.displFkCtrls}.visibility")
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkStart}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkMid}.drawOverride", force=True)
		cmds.connectAttr(f"{self.displFkCtrls}.drawInfo", f"{fkEnd}.drawOverride", force=True)
		cmds.connectAttr(f"{self.nodeIk2bSolver}.ikVisibility", f"{self.displIkCtrls}.visibility")
		cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.ctrlIk.node}.drawOverride", force=True)
		if self.poleVector != "":
			cmds.connectAttr(f"{self.displIkCtrls}.drawInfo", f"{self.ctrlPoleVector.node}.drawOverride", force=True)
			cmds.connectAttr(f"{outMid}.worldMatrix[0]", f"{self.ctrlPoleVector.node}.drawLineTo")
			lm.LMAttribute.copyTransformsToOPM(self.ctrlPoleVector.node)

		lm.LMAttribute.copyTransformsToOPM(self.ctrlStart.node)
		lm.LMAttribute.copyTransformsToOPM(self.ctrlMid.node)
		lm.LMAttribute.copyTransformsToOPM(self.ctrlEnd.node)
		lm.LMAttribute.copyTransformsToOPM(self.ctrlIk.node)


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
		# 	parent=self.ctrlSpine1.node,
		# 	translateTo=listJoints["Spine"]["Spine2"],
		# 	rotateTo=listJoints["Spine"]["Spine2"],
		# )
		# self.ctrlSpine3 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine3"]),
		# 	parent=self.ctrlSpine2.node,
		# 	translateTo=listJoints["Spine"]["Spine3"],
		# 	rotateTo=listJoints["Spine"]["Spine3"],
		# )
		# self.ctrlSpine4 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine4"]),
		# 	parent=self.ctrlSpine3.node,
		# 	translateTo=listJoints["Spine"]["Spine4"],
		# 	rotateTo=listJoints["Spine"]["Spine4"],
		# )
		# self.ctrlSpine5 = Ctrl(
		# 	name="{}_ctrl".format(listJoints["Spine"]["Spine5"]["Root"]),
		# 	parent=self.ctrlSpine4.node,
		# 	translateTo=listJoints["Spine"]["Spine5"]["Root"],
		# 	rotateTo=listJoints["Spine"]["Spine5"]["Root"],
		# )

		# self.ctrlCorrective = []
		# for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
		# 	CtrlCorrective = CorrectiveCtrl(
		# 		name=f"{joint}_ctrl",
		# 		parent=self.ctrlSpine5.node,
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
		self.ctrlMain = MainCtrl(parent=self.grpBase, localRotate=(0.0, 0.0, 0.0))
		self.grpMesh = cmds.group(name="mesh_grp", empty=True, parent=self.grpBase)


		self.setupRigGroups()

		self.setupVisibilityAttributesAndConnections()

		# cmds.setAttr(f"{self.grpBase}.rotateX", -90)

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

		lm.LMAttribute.addSeparator(self.ctrlMain.node)

		self.displCtrls = cmds.createNode("displayLayer", name="ctrls_displ")
		cmds.setAttr(f"{self.displCtrls}.enabled", True)
		cmds.setAttr(f"{self.displCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{self.displCtrls}.overrideColorR", dict_colors["lightyellow"][0])
		cmds.setAttr(f"{self.displCtrls}.overrideColorG", dict_colors["lightyellow"][1])
		cmds.setAttr(f"{self.displCtrls}.overrideColorB", dict_colors["lightyellow"][2])


		self.displMesh = cmds.createNode("displayLayer", name="mesh_displ")
		self.displJnts = cmds.createNode("displayLayer", name="outs_displ")
	
		# Visibility
		# Main Ctrls
		self.attrCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.node, "ctrlsVisibility")
		cmds.connectAttr(self.attrCtrlsVisibility, f"{self.displCtrls}.visibility")
		cmds.connectAttr(f"{self.displCtrls}.drawInfo", f"{self.ctrlMain.node}.drawOverride", force=True)

		# Meshes
		self.attrMeshVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.node, "meshVisibility")
		cmds.connectAttr(self.attrMeshVisibility, f"{self.displMesh}.visibility")
		cmds.connectAttr(f"{self.displMesh}.drawInfo", f"{self.grpMesh}.drawOverride", force=True)
	
		# Export Skeleton
		self.attrExportSkeletonVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.node, "exportSkeletonVisibility", False)
		cmds.connectAttr(self.attrExportSkeletonVisibility, f"{self.displJnts}.visibility")


		lm.LMAttribute.addSeparator(self.ctrlMain.node, "__")


		# Diplay Type Overrides
		# Main Ctrls 
		self.attrCtrlsDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.node, "ctrlsDisplayType")
		cmds.connectAttr(self.attrCtrlsDisplayType, f"{self.displCtrls}.displayType")
		cmds.connectAttr(f"{self.displCtrls}.displayType", f"{self.ctrlMain.node}.overrideDisplayType")


		# Meshes
		self.attrMeshDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.node, "meshDisplayType", 2)
		cmds.connectAttr(self.attrMeshDisplayType, f"{self.displMesh}.displayType")
		cmds.connectAttr(f"{self.displMesh}.displayType", f"{self.grpMesh}.overrideDisplayType")

		# Export Skeleton
		self.attrExportSkeletonDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.node, "exportSkeletonDisplayType", 2)
		cmds.connectAttr(self.attrExportSkeletonDisplayType, f"{self.displJnts}.displayType")


		lm.LMAttribute.addSeparator(self.ctrlMain.node, "___")


		# Hide Ctrls On Playback
		self.attrHideCtrlsOnPlayback = lm.LMAttribute.addOnOff(self.ctrlMain.node, "hideCtrlsOnPlayback", False)
		cmds.connectAttr(self.attrHideCtrlsOnPlayback, f"{self.displCtrls}.hideOnPlayback")
		cmds.connectAttr(f"{self.displCtrls}.hideOnPlayback", f"{self.ctrlMain.node}.hideOnPlayback")




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
			parent=self.ctrlPelvis.node,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
		)

		lm.LMAttribute.copyTransformsToOPM(self.ctrlPelvis.node)
		lm.LMAttribute.lockControlChannels(self.ctrlPelvis.node, lockChannels=["scale", "visibility"])
		lm.LMAttribute.copyTransformsToOPM(self.ctrlPelvisRot.node)
		lm.LMAttribute.lockControlChannels(self.ctrlPelvisRot.node, lockChannels=["translate", "scale", "visibility"])

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		return (self.ctrlPelvis, self.ctrlPelvisRot)




class SpineComponent():

	def __init__(self, compRig, attachTo:str, listJoints:list) -> None:
		
		self.grpComp = cmds.group(name="spine_grp", parent=compRig.ctrlMain.node, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkSpineComponent(self.grpComp, listJoints)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlSpine1.node,
			offset=compRig.ctrlMain.node, 
			sourceNode=listJoints["Spine"]["Spine1"]
		)

		# attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		# [lm.LMAttribute.addMessage(object.node, "component") for object in self.getCtrls()]
		# cmds.connectAttr(f"{self.ctrlPelvis.node}.component", f"{attrComp}[0]")
		# cmds.connectAttr(f"{self.ctrlPelvisRot.node}.component", f"{attrComp}[1]")
		# cmds.setAttr(attrComp, lock=True)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		""""Returns all ctrl from the component.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())

		return listCtrls




class HeadComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, solverModePosition:tuple=(0,0,0)) -> None:
		
		self.grpComp = cmds.group(name="head_grp", parent=compRig.ctrlMain.node, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Head"]["Neck1"],
			mid=listJoints["Head"]["Neck2"],
			end=listJoints["Head"]["Head"],
			side="center",
		)
	
		self.out = Out2bLimbComponent(
			compRig=compRig,
			parent=self.grpComp,
			start=listJoints["Head"]["Neck1"],
			mid=listJoints["Head"]["Neck2"],
			end=listJoints["Head"]["Head"],
			solverModePosition=solverModePosition,
			side="center",
			createTwistSolver=False,
			hasDynamicAttributes=True,
		)

		self.ik = Ik2bLimbComponent(
			name="head",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.node,
			fkStart=self.fk.ctrlStart.node,
			fkMid=self.fk.ctrlMid.node,
			fkEnd=self.fk.ctrlEnd.node,
			ikStart=listJoints["Head"]["Neck1"],
			ikMid=listJoints["Head"]["Neck2"],
			ikEnd=listJoints["Head"]["Head"],
			outStart=self.out.ctrlStart.node,
			outMid=self.out.ctrlMid.node,
			outEnd=self.out.ctrlEnd.node,
			mode="ik",
			side="center",
		)

		# Chains with no root can re-use the same constraint
		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode=listJoints["Head"]["Neck1"]
		)
		cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.out.ctrlStart.node}.offsetParentMatrix")
		cmds.connectAttr(f"{self.cnstMat}.matrixSum", f"{self.ik.ctrlStart.node}.offsetParentMatrix")

		# Lock additional transforms
		lm.LMAttribute.lockTransforms(self.out.ctrlStart.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlMid.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlEnd.node)

		lm.LMAttribute.lockTransforms(self.ik.ctrlStart.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlMid.node, ["translate", "rotateX", "rotateY", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlEnd.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])

		[cmds.setAttr(f"{self.ik.ctrlStart.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]
		[cmds.setAttr(f"{self.ik.ctrlMid.node}.{attr}", channelBox=False, keyable=False) for attr in ["rz"]]
		[cmds.setAttr(f"{self.ik.ctrlEnd.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]

		cmds.setAttr(f"{self.ik.ctrlStart.node}.hiddenInOutliner", True)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		# listCtrls.extend(self.out.getCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class Leg2bComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, solverModePosition:tuple=(0,0,0), side:str="left",
		createTwistSolver:bool=True,
	) -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"

		self.grpComp = cmds.group(name=f"leg{sideSuffix}_grp", parent=compRig.ctrlMain.node, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)
		# lm.LMAttribute.lockTransforms(self.grpComp)

		# self.grpFkComp = cmds.group(name="fk_grp", parent=self.grpComp, empty=True)
		# cmds.matchTransform(self.grpFkComp, self.grpComp, position=True, rotation=True)
		# lm.LMAttribute.copyTransformsToOPM(self.grpFkComp)
		# lm.LMAttribute.lockTransforms(self.grpFkComp)

		# self.grpOutComp = cmds.group(name="out_grp", parent=self.grpComp, empty=True)
		# cmds.matchTransform(self.grpOutComp, self.grpComp, position=True, rotation=True)
		# lm.LMAttribute.copyTransformsToOPM(self.grpOutComp)
		# lm.LMAttribute.lockTransforms(self.grpOutComp)

		self.fk = Fk2bLimbComponent(
			parent=self.grpComp,
			start=listJoints["Leg"]["UpLeg"],
			mid=listJoints["Leg"]["Leg"],
			end=listJoints["Leg"]["Foot"]["Root"],
			side=side,
		)

		self.out = Out2bLimbComponent(
			# parent=self.grpOutComp,
			compRig=compRig,
			parent=self.grpComp,
			start=listJoints["Leg"]["UpLeg"],
			mid=listJoints["Leg"]["Leg"],
			end=listJoints["Leg"]["Foot"]["Root"],
			upperTwist1=listJoints["Leg"]["UpLegRoll1"]["Root"],
			upperTwist2=listJoints["Leg"]["UpLegRoll2"]["Root"],
			lowerTwist1=listJoints["Leg"]["LegRoll1"]["Root"],
			lowerTwist2=listJoints["Leg"]["LegRoll2"]["Root"],
			solverModePosition=solverModePosition, 
			side=side,
			createTwistSolver=createTwistSolver,
		)

		self.ik = Ik2bLimbComponent(
			name="leg",
			# parent=self.grpIkComp,
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.node,
			fkStart=self.fk.ctrlStart.node,
			fkMid=self.fk.ctrlMid.node,
			fkEnd=self.fk.ctrlEnd.node,
			ikStart=listJoints["Leg"]["UpLeg"],
			ikMid=listJoints["Leg"]["Leg"],
			ikEnd=listJoints["Leg"]["Foot"]["Root"],
			poleVector=f"leg_pv{sideSuffix}",
			outStart=self.out.ctrlStart.node,
			outMid=self.out.ctrlMid.node,
			outEnd=self.out.ctrlEnd.node,
			side=side,
		)

		# Chains with no root can re-use the same constraint
		self.cnstMatFk = LMRigUtils.createMatrixConstraint(
			parent=attachTo,
			# child=self.grpFkComp,
			child=self.fk.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Leg"]["UpLeg"]), sideSuffix)
		)
		self.cnstMatIk = LMRigUtils.createMatrixConstraint(
			parent=attachTo,
			child=self.ik.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Leg"]["UpLeg"]), sideSuffix)
		)
		self.cnstMatOut = LMRigUtils.createMatrixConstraint(
			parent=attachTo,
			child=self.out.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Leg"]["UpLeg"]), sideSuffix)
		)

		# Lock additional transforms
		lm.LMAttribute.lockTransforms(self.out.ctrlStart.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlMid.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlEnd.node)

		lm.LMAttribute.lockTransforms(self.ik.ctrlStart.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlMid.node, ["translate", "rotateX", "rotateY", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlEnd.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])

		[cmds.setAttr(f"{self.ik.ctrlStart.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]
		[cmds.setAttr(f"{self.ik.ctrlMid.node}.{attr}", channelBox=False, keyable=False) for attr in ["rz"]]
		[cmds.setAttr(f"{self.ik.ctrlEnd.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]

		cmds.setAttr(f"{self.ik.ctrlStart.node}.hiddenInOutliner", True)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.extend(self.out.getTwistCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class FootComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, solverModePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
		
		self.grpComp = cmds.group(name=f"foot{sideSuffix}_grp", parent=compRig.ctrlMain.node, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkFootComponent(self.grpComp, listJoints, side)

		self.cnstMat = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlToe.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Leg"]["ToeBase"]), sideSuffix)
		)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


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

	def __init__(self, compRig, attachTo:str, listJoints:list, solverModePosition:tuple=(0,0,0), side:str="left",
		createTwistSolver:bool=True,
	) -> None:
		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
			colorSwitch = "orange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
			colorSwitch = "blue"

		self.grpComp = cmds.group(name=f"arm{sideSuffix}_grp", parent=compRig.ctrlMain.node, empty=True)
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
			compRig=compRig,
			parent=self.grpComp,
			start=listJoints["Arm"]["Arm"],
			mid=listJoints["Arm"]["ForeArm"],
			end=listJoints["Arm"]["Hand"]["Root"],
			upperTwist1=listJoints["Arm"]["ArmRoll1"]["Root"],
			upperTwist2=listJoints["Arm"]["ArmRoll2"]["Root"],
			lowerTwist1=listJoints["Arm"]["ForeArmRoll1"],
			lowerTwist2=listJoints["Arm"]["ForeArmRoll2"],
			solverModePosition=solverModePosition, 
			side=side,
			createTwistSolver=createTwistSolver,
		)

		self.ik = Ik2bLimbComponent(
			name="arm",
			parent=self.grpComp,
			rotateTo=self.fk.ctrlEnd.node,
			fkStart=self.fk.ctrlStart.node,
			fkMid=self.fk.ctrlMid.node,
			fkEnd=self.fk.ctrlEnd.node,
			ikStart=listJoints["Arm"]["Arm"],
			ikMid=listJoints["Arm"]["ForeArm"],
			ikEnd=listJoints["Arm"]["Hand"]["Root"],
			poleVector=f"arm_pv{sideSuffix}",
			outStart=self.out.ctrlStart.node, outMid=self.out.ctrlMid.node,	outEnd=self.out.ctrlEnd.node,
			side=side,
		)

		# We need seprate constraints for each chain since the arm has a root (clavilce joint)
		self.cnstMatFk = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlRoot.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Arm"]["Shoulder"]["Root"]), sideSuffix)
		)
		self.cnstMatOut = LMRigUtils.createMatrixConstraint(
			parent=self.fk.ctrlRoot.node, 
			child=self.out.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Arm"]["Arm"]), sideSuffix)
		)
		self.cnstMatIk = LMRigUtils.createMatrixConstraint(
			parent=self.fk.ctrlRoot.node, 
			child=self.ik.ctrlStart.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Arm"]["Arm"]), sideSuffix)
		)


		# Lock additional transforms
		lm.LMAttribute.lockTransforms(self.out.ctrlStart.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlMid.node)
		lm.LMAttribute.lockTransforms(self.out.ctrlEnd.node)

		lm.LMAttribute.lockTransforms(self.ik.ctrlStart.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlMid.node, ["translate", "rotateX", "rotateY", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])
		lm.LMAttribute.lockTransforms(self.ik.ctrlEnd.node, ["translate", "scale", "shear", "rotateOrder", "rotateAxis", "inheritsTransform", "offsetParentMatrix", "visibility"])

		[cmds.setAttr(f"{self.ik.ctrlStart.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]
		[cmds.setAttr(f"{self.ik.ctrlMid.node}.{attr}", channelBox=False, keyable=False) for attr in ["rz"]]
		[cmds.setAttr(f"{self.ik.ctrlEnd.node}.{attr}", channelBox=False, keyable=False) for attr in ["rx", "ry", "rz"]]

		cmds.setAttr(f"{self.ik.ctrlStart.node}.hiddenInOutliner", True)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.extend(self.out.getTwistCtrls())
		listCtrls.extend(self.ik.getCtrls())

		return listCtrls




class HandComponent():
	"""Class for building the head component.
	"""

	def __init__(self, compRig, attachTo:str, listJoints:list, solverModePosition:tuple=(0,0,0), side:str="left") -> None:

		if side == "left":
			sideSuffix = "_l"
			color = "lightorange"
		if side == "right":
			sideSuffix = "_r"
			color = "lightblue"
		
		self.grpComp = cmds.group(name=f"hand{sideSuffix}_grp", parent=compRig.ctrlMain.node, empty=True)
		lm.LMAttribute.lockTransforms(self.grpComp)

		self.fk = FkHandComponent(self.grpComp, listJoints, side)

		self.cnstThumb = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlThumb1.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["Thumb1"]), sideSuffix)
		)
		self.cnstIndex = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandIndex.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandIndex"]), sideSuffix)
		)
		self.cnstMiddle = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandMiddle.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandMiddle"]), sideSuffix)
		)
		self.cnstPinky = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandPinky.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandPinky"]), sideSuffix)
		)
		self.cnstRing = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlInHandRing.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["InHandRing"]), sideSuffix)
		)
		self.cnstWeapon = LMRigUtils.createMatrixConstraint(
			parent=attachTo, 
			child=self.fk.ctrlWeapon.node,
			offset=compRig.ctrlMain.node, 
			sourceNode="{}{}".format((listJoints["Hand"]["Weapon"]), sideSuffix)
		)

		# Message Attrs Setup
		attrComp = lm.LMAttribute.addMessage(self.grpComp, "ctrl", True)
		[lm.LMAttribute.addMessage(ctrl.node, "component") for ctrl in self.getCtrls()]
		[cmds.connectAttr(f"{ctrl.node}.component", f"{attrComp}[{indx}]") for ctrl, indx in zip(self.getCtrls(), range(self.getCtrls().__len__()))]
		cmds.setAttr(attrComp, lock=True)


	def getCtrls(self):
		""""Returns all ctrls from the component - fk, out, ik.
		"""
		listCtrls = []
		listCtrls.extend(self.fk.getCtrls())
		listCtrls.append(self.fk.getWeaponCtrls())
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
			parent=compRig.ctrlMain.node,
			translateTo=compRig.ctrlMain.node, rotateTo=compRig.ctrlMain.node,
			# localPosition=localPosition,
			# solverModePosition=solverModePosition
		)
		self.matCnst = LMRigUtils.createMatrixConstraint(
			parent=compHead.out.ctrlEnd.node, 
			child=self.ctrlFkIkSwitch.node,
			offset=compRig.ctrlMain.node, 
		)

		# TODO split this into a method
		# Create switch attrs
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "headFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "headSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.node, "headTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.headFkIk", f"{compHead.ik.nodeIk2bSolver}.fkIk")
		cmds.setAttr(f"{compHead.out.ctrlEnd.node}.fkIk", lock=False)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.headFkIk", f"{compHead.out.ctrlEnd.node}.fkIk")
		cmds.setAttr(f"{compHead.out.ctrlEnd.node}.fkIk", lock=True)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.headSoftness", f"{compHead.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.headTwist", f"{compHead.ik.nodeIk2bSolver}.twist")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.node)

		# Left Arm
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "leftArmFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "leftArmSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.node, "leftArmTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftArmFkIk", f"{compLeftArm.ik.nodeIk2bSolver}.fkIk")
		cmds.setAttr(f"{compLeftArm.out.ctrlEnd.node}.fkIk", lock=False)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftArmFkIk", f"{compLeftArm.out.ctrlEnd.node}.fkIk")
		cmds.setAttr(f"{compLeftArm.out.ctrlEnd.node}.fkIk", lock=True)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftArmTwist", f"{compLeftArm.ik.nodeIk2bSolver}.twist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftArmSoftness", f"{compLeftArm.ik.nodeIk2bSolver}.softness")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.node, "leftArmTwistCtrlsVisibility")
		displLeftArmTwistCtrls = cmds.createNode("displayLayer", name="arm_twist_l_displ")
		cmds.setAttr(f"{displLeftArmTwistCtrls}.enabled", True)
		cmds.setAttr(f"{displLeftArmTwistCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{displLeftArmTwistCtrls}.overrideColorR", dict_colors["lightorange"][0])
		cmds.setAttr(f"{displLeftArmTwistCtrls}.overrideColorG", dict_colors["lightorange"][1])
		cmds.setAttr(f"{displLeftArmTwistCtrls}.overrideColorB", dict_colors["lightorange"][2])
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displLeftArmTwistCtrls}.visibility")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistUpper1.node}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistUpper2.node}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistLower1.node}.drawOverride")
		cmds.connectAttr(f"{displLeftArmTwistCtrls}.drawInfo", f"{compLeftArm.out.ctrlTwistLower2.node}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.node, "__")

		# Right Arm
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "rightArmFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "rightArmSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.node, "rightArmTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightArmFkIk", f"{compRightArm.ik.nodeIk2bSolver}.fkIk")
		cmds.setAttr(f"{compRightArm.out.ctrlEnd.node}.fkIk", lock=False)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightArmFkIk", f"{compRightArm.out.ctrlEnd.node}.fkIk")
		cmds.setAttr(f"{compRightArm.out.ctrlEnd.node}.fkIk", lock=True)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightArmTwist", f"{compRightArm.ik.nodeIk2bSolver}.twist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightArmSoftness", f"{compRightArm.ik.nodeIk2bSolver}.softness")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.node, "rightArmTwistCtrlsVisibility")
		displRightArmTwistCtrls = cmds.createNode("displayLayer", name="arm_twist_r_displ")
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displRightArmTwistCtrls}.visibility")
		cmds.setAttr(f"{displRightArmTwistCtrls}.enabled", True)
		cmds.setAttr(f"{displRightArmTwistCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{displRightArmTwistCtrls}.overrideColorR", dict_colors["lightblue"][0])
		cmds.setAttr(f"{displRightArmTwistCtrls}.overrideColorG", dict_colors["lightblue"][1])
		cmds.setAttr(f"{displRightArmTwistCtrls}.overrideColorB", dict_colors["lightblue"][2])
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistUpper1.node}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistUpper2.node}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistLower1.node}.drawOverride")
		cmds.connectAttr(f"{displRightArmTwistCtrls}.drawInfo", f"{compRightArm.out.ctrlTwistLower2.node}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.node, "___")

		# Left Leg
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "leftLegFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "leftLegSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.node, "leftLegTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftLegFkIk", f"{compLeftLeg.ik.nodeIk2bSolver}.fkIk")
		cmds.setAttr(f"{compLeftLeg.out.ctrlEnd.node}.fkIk", lock=False)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftLegFkIk", f"{compLeftLeg.out.ctrlEnd.node}.fkIk")
		cmds.setAttr(f"{compLeftLeg.out.ctrlEnd.node}.fkIk", lock=True)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftLegSoftness", f"{compLeftLeg.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.leftLegTwist", f"{compLeftLeg.ik.nodeIk2bSolver}.twist")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.node, "leftLegTwistCtrlsVisibility")
		displLeftLegTwistCtrls = cmds.createNode("displayLayer", name="leg_twist_l_displ")
		cmds.setAttr(f"{displLeftLegTwistCtrls}.enabled", True)
		cmds.setAttr(f"{displLeftLegTwistCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{displLeftLegTwistCtrls}.overrideColorR", dict_colors["lightorange"][0])
		cmds.setAttr(f"{displLeftLegTwistCtrls}.overrideColorG", dict_colors["lightorange"][1])
		cmds.setAttr(f"{displLeftLegTwistCtrls}.overrideColorB", dict_colors["lightorange"][2])
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displLeftLegTwistCtrls}.visibility")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistUpper1.node}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistUpper2.node}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistLower1.node}.drawOverride")
		cmds.connectAttr(f"{displLeftLegTwistCtrls}.drawInfo", f"{compLeftLeg.out.ctrlTwistLower2.node}.drawOverride")

		lm.LMAttribute.addSeparator(self.ctrlFkIkSwitch.node, "____")

		# Right Leg
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "rightLegFkIk", 0, 100)
		lm.LMAttribute.addFloatFkIk(self.ctrlFkIkSwitch.node, "rightLegSoftness", 0, 10)
		lm.LMAttribute.addFloat(self.ctrlFkIkSwitch.node, "rightLegTwist")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightLegFkIk", f"{compRightLeg.ik.nodeIk2bSolver}.fkIk")
		cmds.setAttr(f"{compRightLeg.out.ctrlEnd.node}.fkIk", lock=False)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightLegFkIk", f"{compRightLeg.out.ctrlEnd.node}.fkIk")
		cmds.setAttr(f"{compRightLeg.out.ctrlEnd.node}.fkIk", lock=True)
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightLegSoftness", f"{compRightLeg.ik.nodeIk2bSolver}.softness")
		cmds.connectAttr(f"{self.ctrlFkIkSwitch.node}.rightLegTwist", f"{compRightLeg.ik.nodeIk2bSolver}.twist")
		attrTwistCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlFkIkSwitch.node, "rightLegTwistCtrlsVisibility")
		displRightLegTwistCtrls = cmds.createNode("displayLayer", name="leg_twist_r_displ")
		cmds.setAttr(f"{displRightLegTwistCtrls}.enabled", True)
		cmds.setAttr(f"{displRightLegTwistCtrls}.overrideRGBColors", True)
		cmds.setAttr(f"{displRightLegTwistCtrls}.overrideColorR", dict_colors["lightblue"][0])
		cmds.setAttr(f"{displRightLegTwistCtrls}.overrideColorG", dict_colors["lightblue"][1])
		cmds.setAttr(f"{displRightLegTwistCtrls}.overrideColorB", dict_colors["lightblue"][2])
		cmds.connectAttr(attrTwistCtrlsVisibility, f"{displRightLegTwistCtrls}.visibility")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistUpper1.node}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistUpper2.node}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistLower1.node}.drawOverride")
		cmds.connectAttr(f"{displRightLegTwistCtrls}.drawInfo", f"{compRightLeg.out.ctrlTwistLower2.node}.drawOverride")




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

