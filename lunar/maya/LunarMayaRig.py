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
	defaultFingerLineWidth = 5.0
	defaultLockShapeAttributes = True

	def __init__(self,
		name="new_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(2.0, 2.0, 2.0),
		shape="cube",
		fillShape=True,
		drawText=False,
		textPosition=(0.0, 0.0, 0.0),
		fillTransparency=defaultTransparency,
		lineWidth=defaultLineWidth,
		color="yellow",
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
			drawText=drawText,
			textPosition=textPosition,
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
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
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
		self.__createUnifiedScale()
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)


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




class PelvisPosCtrl(Ctrl):
	"""Class for building the center of graivty controller.
	"""
	def __init__(self,
		name="pelvis_pos_ctrl",
		parent="",
		translateTo="",
		rotateTo="",
		localPosition=(0.0,	0.0, 0.0),
		localRotate=(0.0, 0.0, 0.0),
		localScale=(20.0, 20.0, 30.0),
		shape="square",
		fillShape=False,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
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
		localRotate=(0.0, 0.0, 0.0),
		localScale=(0.75, 0.75, 0.75),
		shape="line",
		fillShape=True,
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
		drawText=True,
		textPosition=(0.0, 0.0, 0.0),
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
		color="magenta",
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
			drawText=drawText,
			textPosition=textPosition,
			fillTransparency=fillTransparency,
			lineWidth=lineWidth,
			color=color,
			lockShapeAttributes=lockShapeAttributes,
		)
		lm.LMAttribute.lockControlChannels(self.transform, lockChannels)




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
		localScale=(6.0, 6.0, 6.0),
		shape="diamond",
		fillShape=False,
		drawLine=True,
		fillTransparency=Ctrl.defaultTransparency,
		lineWidth=Ctrl.defaultLineWidth,
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
		color="yellow",
		lockShapeAttributes=Ctrl.defaultLockShapeAttributes,
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




class Base():
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

		self._setupRigGroups()

		self._setupVisibilityAttributesAndConnections()

		cmds.setAttr(f"{self.grpBase}.rotateX", -90)

		# for group in [self.grpBase, self.grpMesh]:
		[lm.LMAttribute.lockControlChannels(Object, ["translate", "scale", "visibility"]) for Object in [self.grpBase, self.grpMesh]]


	def _setupRigGroups(self):
		"""Sets main rig groups: base, ctrl, mesh and export"""
		# Extra attribute creation
		rigNameAttr = "rigName"
		sceneObjectTypeAttr = "sceneObjectType"
		[cmds.addAttr(self.grpBase, longName=attr, dataType="string") for attr in [rigNameAttr, sceneObjectTypeAttr]]
		
		cmds.setAttr(f"{self.grpBase}.{rigNameAttr}", self.rigName, type="string", lock=True)
		cmds.setAttr(f"{self.grpBase}.{sceneObjectTypeAttr}", self.sceneObjectType, type="string", lock=True)


	def _setupVisibilityAttributesAndConnections(self):
		"""Creates visibility and display type attributes on the main cotroller and connects them.
		
		"""

		lm.LMAttribute.addSeparator(self.ctrlMain.transform)

		# Left Arm
		self.AttrLeftArmFkIk = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "leftArmFkIk")
		self.AttrLeftArmSoftness = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "leftArmSoftness", 0, 10)
		self.AttrLeftArmTwist = lm.LMAttribute.addFloat(self.ctrlMain.transform, "leftArmTwist")

		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "__")

		# Right Arm
		self.AttrRightArmFkIk = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "rightArmFkIk")
		self.AttrRightArmSoftness = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "rightArmSoftness", 0, 10)
		self.AttrRightArmTwist = lm.LMAttribute.addFloat(self.ctrlMain.transform, "rightArmTwist")

		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "___")

		# Left Leg
		self.AttrLeftLegFkIk = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "leftLegFkIk")
		self.AttrLeftLegSoftness = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "leftLegSoftness", 0, 10)
		self.AttrLeftLegTwist = lm.LMAttribute.addFloat(self.ctrlMain.transform, "leftLegTwist")

		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "____")

		# Right Leg
		self.AttrRightLegFkIk = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "rightLegFkIk")
		self.AttrRightLegSoftness = lm.LMAttribute.addFloatFkIk(self.ctrlMain.transform, "rightLegSoftness", 0, 10)
		self.AttrRightLegTwist = lm.LMAttribute.addFloat(self.ctrlMain.transform, "rightLegTwist")

		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "_____")

		# Visibility
		# Main Ctrls
		self.AttrCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "ctrlsVisibility")
		cmds.connectAttr(self.AttrCtrlsVisibility, f"{self.ctrlMain.transform}.visibility")
		lm.LMAttribute.lockControlChannels(self.ctrlMain.transform, ["visibility"])
		# Roll Ctrls
		self.AttrRollCtrlsVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "rollCtrlsVisibility")
		# Meshes
		self.AttrMeshVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "meshVisibility")
		cmds.connectAttr(self.AttrMeshVisibility, f"{self.grpMesh}.visibility")
		# Export Skeleton
		self.AttrExportSkeletonVisibility = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "exportSkeletonVisibility", False)

		# Hide Ctrls On Playback
		self.AttrHideCtrlsOnPlayback = lm.LMAttribute.addOnOff(self.ctrlMain.transform, "hideCtrlsOnPlayback", False)
		cmds.connectAttr(self.AttrHideCtrlsOnPlayback, f"{self.ctrlMain.shape}.hideOnPlayback")

		lm.LMAttribute.addSeparator(self.ctrlMain.transform, "______")

		# Diplay Type Overrides
		# Main Ctrls 
		self.AttrCtrlsDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "ctrlsDisplayType")
		cmds.connectAttr(self.AttrCtrlsDisplayType, f"{self.ctrlMain.transform}.overrideDisplayType")
		# Roll Ctrls
		self.AttrRollCtrlsDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "rollCtrlsDisplayType")
		# Meshes
		self.AttrMeshDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "meshDisplayType", 2)
		cmds.setAttr(f"{self.grpMesh}.overrideEnabled", True)
		cmds.connectAttr(self.AttrMeshDisplayType, f"{self.grpMesh}.overrideDisplayType")
		# Export Skeleton
		self.AttrExportSkeletonDisplayType = lm.LMAttribute.addDisplayType(self.ctrlMain.transform, "exportSkeletonDisplayType", 2)




class PelvisComponent():
	"""Class for building the fk pelvis component."""

	def __init__(self, parent, listJoints) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		# Main chain
		self.CtrlPelvisPos = PelvisPosCtrl(
			parent=parent,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
		)
		self.CtrlPelvisRot = Ctrl(
			name="{}_rot_ctrl".format(listJoints["Spine"]["Pelvis"]),
			parent=self.CtrlPelvisPos.transform,
			translateTo=listJoints["Spine"]["Pelvis"],
			rotateTo=listJoints["Spine"]["Pelvis"],
		)

		lm.LMAttribute.copyTransformsToOPM(self.CtrlPelvisPos.transform)
		lm.LMAttribute.lockControlChannels(self.CtrlPelvisPos.transform, lockChannels=["rotate", "scale", "visibility"])
		lm.LMAttribute.copyTransformsToOPM(self.CtrlPelvisRot.transform)
		lm.LMAttribute.lockControlChannels(self.CtrlPelvisRot.transform, lockChannels=["translate", "scale", "visibility"])

	def getCtrls(self):
		return (self.CtrlPelvisPos, self.CtrlPelvisRot)



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

		self.CtrlCorrective = []
		for joint in listJoints["Spine"]["Spine5"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}_ctrl",
				parent=self.CtrlSpine5.transform,
				translateTo=joint,
				rotateTo=joint
			)
			self.CtrlCorrective.append(CtrlCorrective)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Spine"])


	def getCtrls(self):
		return (self.CtrlSpine1, self.CtrlSpine2, self.CtrlSpine3, self.CtrlSpine4, self.CtrlSpine5)



class FkHeadComponent():
	"""Class for building the fk head component.
	"""

	def __init__(self, parent, listJoints) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		# Main chain
		self.CtrlNeck1 = Ctrl(
			name="{}_ctrl".format(listJoints["Head"]["Neck1"]),
			parent=parent,
			translateTo=listJoints["Head"]["Neck1"],
			rotateTo=listJoints["Head"]["Neck1"],
		)
		self.CtrlNeck2 = Ctrl(
			name="{}_ctrl".format(listJoints["Head"]["Neck2"]),
			parent=self.CtrlNeck1.transform,
			translateTo=listJoints["Head"]["Neck2"],
			rotateTo=listJoints["Head"]["Neck2"],
		)
		self.CtrlHead = Ctrl(
			name="{}_ctrl".format(listJoints["Head"]["Head"]),
			parent=self.CtrlNeck2.transform,
			translateTo=listJoints["Head"]["Head"],
			rotateTo=listJoints["Head"]["Head"],
		)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Head"])


	def getCtrls(self):
		return (self.CtrlNeck1, self.CtrlNeck2, self.CtrlHead)




class FkLegComponent():
	"""Class for building the fk leg component."""


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

		# UpLeg - main bones
		self.CtrlUpLeg = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["UpLeg"], sideSuffix),
			color=color,
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
		# UpLeg - corrective root
		self.CtrlUpLegCorrectiveRoot = CorrectiveCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["UpLegCorrectiveRoot"]["Root"], sideSuffix),
			parent=self.CtrlUpLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["UpLegCorrectiveRoot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["UpLegCorrectiveRoot"]["Root"], sideSuffix),
			color=color,
		)

		# Leg - main bones
		self.CtrlLeg = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["Leg"], sideSuffix),
			parent=self.CtrlUpLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["Leg"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["Leg"], sideSuffix),
			color=color,
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
		# Leg - corrective root
		self.CtrlLegCorrectiveRoot = CorrectiveCtrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["LegCorrectiveRoot"]["Root"], sideSuffix),
			parent=self.CtrlLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["LegCorrectiveRoot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["LegCorrectiveRoot"]["Root"], sideSuffix),
			color=color,
		)

		# Foot - main bones
		self.CtrlFoot = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			parent=self.CtrlLeg.transform,
			translateTo="{}{}".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["Foot"]["Root"], sideSuffix),
			color=color,
		)

		# Toe - main bones
		self.CtrlToe = Ctrl(
			name="{}{}_ctrl".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			parent=self.CtrlFoot.transform,
			translateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Leg"]["ToeBase"], sideSuffix),
			color=color,
		)

		# Corrective controllers
		self.CtrlCorrective = []
		# UpLeg
		for joint in listJoints["Leg"]["UpLegRoll1"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlUpLegRoll1.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		for joint in listJoints["Leg"]["UpLegRoll2"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlUpLegRoll2.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		for joint in listJoints["Leg"]["UpLegCorrectiveRoot"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlUpLegCorrectiveRoot.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# Leg
		for joint in listJoints["Leg"]["LegRoll1"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlLegRoll1.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		for joint in listJoints["Leg"]["LegCorrectiveRoot"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlLegCorrectiveRoot.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# Foot
		for joint in listJoints["Leg"]["Foot"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlFoot.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		self.CtrlCorrective.append(self.CtrlUpLegCorrectiveRoot)
		self.CtrlCorrective.append(self.CtrlLegCorrectiveRoot)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Leg"], sideSuffix)


	def getCtrls(self):
		return (
			self.CtrlUpLeg,
			self.CtrlLeg, self.CtrlUpLegRoll1,  self.CtrlUpLegRoll2,
			self.CtrlFoot, self.CtrlLegRoll1, self.CtrlLegRoll2,
			self.CtrlToe
		)


	def getMainCtrls(self):
		return (self.CtrlUpLeg, self.CtrlLeg,	self.CtrlFoot, self.CtrlToe)


	def getRollCtrls(self):
		return (self.CtrlUpLegRoll1,  self.CtrlUpLegRoll2, self.CtrlLegRoll1, self.CtrlLegRoll2)




class FkArmComponent():
	"""Class for building the fk leg component."""


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

		# Shouleder - main bones
		self.CtrlShoulder = Ctrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
			parent=parent,
			translateTo="{}{}".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["Shoulder"]["Root"], sideSuffix),
			color=color,
		)
		# Arm - main bones
		self.CtrlArm = Ctrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["Arm"], sideSuffix),
			parent=self.CtrlShoulder.transform,
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
		# Arm - corrective root
		self.CtrlArmCorrectiveRoot = CorrectiveCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
			parent=self.CtrlArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ArmCorrectiveRoot"]["Root"], sideSuffix),
			color=color,
		)

		# Forearm - main bones
		self.CtrlForeArm = Ctrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ForeArm"], sideSuffix),
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
		self.CtrlForeArmCorrectiveRoot = CorrectiveCtrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
			parent=self.CtrlForeArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["ForeArmCorrectiveRoot"]["Root"], sideSuffix),
			color=color,
		)
		# Hand - corrective root
		self.CtrlHand = Ctrl(
			name="{}{}_ctrl".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			parent=self.CtrlForeArm.transform,
			translateTo="{}{}".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			rotateTo="{}{}".format(listJoints["Arm"]["Hand"]["Root"], sideSuffix),
			color=color,
		)
		# Corrective controllers
		self.CtrlCorrective = []
		# Shoulder
		for joint in listJoints["Arm"]["Shoulder"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlShoulder.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# Armroll1
		for joint in listJoints["Arm"]["ArmRoll1"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlArmRoll1.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# Armroll2
		for joint in listJoints["Arm"]["ArmRoll2"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlArmRoll2.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# ArmCorrectiveRoot
		for joint in listJoints["Arm"]["ArmCorrectiveRoot"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlArmCorrectiveRoot.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# ForeArmCorrectiveRoot
		for joint in listJoints["Arm"]["ForeArmCorrectiveRoot"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlForeArmCorrectiveRoot.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		# Hand
		for joint in listJoints["Arm"]["Hand"]["Corrective"]:
			CtrlCorrective = CorrectiveCtrl(
				name=f"{joint}{sideSuffix}_ctrl",
				parent=self.CtrlHand.transform,
				translateTo=f"{joint}{sideSuffix}",
				rotateTo=f"{joint}{sideSuffix}",
				color=color,
			)
			self.CtrlCorrective.append(CtrlCorrective)
		self.CtrlCorrective.append(self.CtrlArmCorrectiveRoot)
		self.CtrlCorrective.append(self.CtrlForeArmCorrectiveRoot)
		lm.LMTransformUtils.postCtrlTransform(listJoints["Arm"], sideSuffix)


	def getCtrls(self):
		return (
			self.CtrlShoulder,
			self.CtrlArm, self.CtrlArmRoll1,  self.CtrlArmRoll2,
			self.CtrlForeArm, self.CtrlForeArmRoll1, self.CtrlForeArmRoll2,
			self.CtrlHand
		)


	def getMainCtrls(self):
		return (self.CtrlShoulder, self.CtrlArm,	self.CtrlForeArm, self.CtrlHand)
	

	def getRollCtrls(self):
		return (self.CtrlArmRoll1,  self.CtrlArmRoll2, self.CtrlForeArmRoll1, self.CtrlForeArmRoll2)




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
#	Ik Components
#--------------------------------------------------------------------------------------------------




class Ik2bLimbComponent():
	"""Class for building ik comoponents."""


	def __init__(self,
	  name:str, parent:str, rotateTo:str,
		fkStart:str, fkMid:str, fkEnd:str, poleVector:str="", side:str="left",
		textPosition:tuple=(0.0, 0.0, 0.0),
		) -> None:
		"""Class constructor.

		Args:
			parent (string): Parent of the component to be parented to.

		"""
		self.poleVector = poleVector
		if side == "center":
			sideSuffix = ""
			color = "yellow"
		if side == "left":
			sideSuffix = "_l"
			color = "orange"
		if side == "right":
			sideSuffix = "_r"
			color = "blue"

		self.CtrlIk = IkCtrl(
			name=f"{name}_ik{sideSuffix}_ctrl",
			parent=parent,
			translateTo=fkEnd,
			rotateTo=fkEnd,
			lineWidth=3,
			textPosition=textPosition,
			color=color,
		)

		if poleVector != "":
			self.CtrlPoleVector = PoleVectorCtrl(
				name=f"{name}_pv{sideSuffix}_ctrl",
				parent=parent,
				translateTo=poleVector,
				rotateTo=rotateTo,
				localScale=(4.0, 4.0, 4.0),
				lineWidth=2.0,
				color=color,
			)
			self.NodeIk2bSolver = cmds.ik(
					name=f"{name}{sideSuffix}_Ik2bSolver",
					fkStart=fkStart,
					fkMid=fkMid,
					fkEnd=fkEnd,
					ikHandle=self.CtrlIk.transform,
					poleVector=self.CtrlPoleVector.transform,
			)[0]
		else:
			self.NodeIk2bSolver = cmds.ik(
				name=f"{name}{sideSuffix}_Ik2bSolver",
				fkStart=fkStart,
				fkMid=fkMid,
				fkEnd=fkEnd,
				ikHandle=self.CtrlIk.transform,
			)[0]

		# Post setup
		lm.LMAttribute.copyTransformsToOPM(self.CtrlIk.transform)
		# lm.LMAttribute.lockControlChannels(self.CtrlIk.transform, lockChannels=["offsetParentMatrix"])
		if poleVector:
			lm.LMAttribute.copyTransformsToOPM(self.CtrlPoleVector.transform)
			# lm.LMAttribute.lockControlChannels(self.CtrlPoleVector.transform, lockChannels=["offsetParentMatrix"])


	def getCtrls(self):
		if self.poleVector != "":
			return (self.CtrlIk, self.CtrlPoleVector)
		else:
			return (self.CtrlIk)




#--------------------------------------------------------------------------------------------------
# Utilities
#--------------------------------------------------------------------------------------------------




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

