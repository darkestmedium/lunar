# Built-in imports

# Third-party imports
import unreal as uep

# Custom imports
from lunar.abstract.retarget import AbstractRetarget



class UnrealMetaHuman(AbstractRetarget):
	"""Retargeting in the Unreal Engine 5 using IK Rig Retargeting.
	
	The setup in unreal would be as following:

	You are familiar with creating and using IK Rig Assets. Refer to the IK Rig Editor page for how to do this.
	Your project has two different Skeletal Meshes to evaluate the retargeting process.

	1. Create Retargeting node
	2. Specify Source / Target skeletal meshes
		make sure they have ik rigs - if not create / define them

	3. Create / set aPose tPoses for retargeting

	4. Retarget
		
	"""

	# In the Hierarchy panel, right-click on the Bone and select Set Retarget Root. Do this in both IK Rig Assets.

	definition = {
		# Base
		"RootMotion": 				{"startBone": "root", 								"endBone": "root", 								"ikGoal": "None"},
		"Spine": 							{"startBone": "spine_01", 						"endBone": "spine_05", 						"ikGoal": "None"},
		"Neck":								{"startBone": "neck_01", 							"endBone": "neck_02",							"ikGoal": "None"},
		"Head":								{"startBone": "head", 								"endBone": "head",								"ikGoal": "None"},
		# Left Arm / Hand
		"LeftShoulder": 			{"startBone": "clavicle_l", 					"endBone": "clavicle_l",					"ikGoal": "None"},
		"LeftArm": 						{"startBone": "upperarm_l", 					"endBone": "hand_l",							"ikGoal": "None"},
		"LeftHandThumb": 			{"startBone": "thumb_01_l", 					"endBone": "thumb_03_l",					"ikGoal": "None"},
		"LeftInHandIndex": 		{"startBone": "index_metacarpal_l", 	"endBone": "index_metacarpal_l",	"ikGoal": "None"},
		"LeftHandIndex": 			{"startBone": "index_01_l", 					"endBone": "index_03_l",					"ikGoal": "None"},
		"LeftInHandMiddle": 	{"startBone": "middle_metacarpal_l", 	"endBone": "middle_metacarpal_l",	"ikGoal": "None"},
		"LeftHandMiddle":			{"startBone": "middle_01_l", 					"endBone": "middle_03_l",					"ikGoal": "None"},
		"LeftInHandRing": 		{"startBone": "ring_metacarpal_l", 		"endBone": "ring_metacarpal_l",		"ikGoal": "None"},
		"LeftHandRing": 			{"startBone": "ring_01_l", 						"endBone": "ring_03_l",						"ikGoal": "None"},
		"LeftInHandPinky": 		{"startBone": "pinky_metacarpal_l", 	"endBone": "pinky_metacarpal_l",	"ikGoal": "None"},
		"LeftHandPinky": 			{"startBone": "pinky_01_l", 					"endBone": "pinky_03_l",					"ikGoal": "None"},
		# Right Arm / Hand
		"RightShoulder": 			{"startBone": "clavicle_r", 					"endBone": "clavicle_r", 					"ikGoal": "None"},
		"RightArm": 					{"startBone": "upperarm_r", 					"endBone": "hand_r", 							"ikGoal": "None"},
		"RightHandThumb": 		{"startBone": "thumb_01_r", 					"endBone": "thumb_03_r",					"ikGoal": "None"},
		"RightInHandIndex": 	{"startBone": "index_metacarpal_r", 	"endBone": "index_metacarpal_r",	"ikGoal": "None"},
		"RightHandIndex": 		{"startBone": "index_01_r",						"endBone": "index_03_r",					"ikGoal": "None"},
		"RightInHandMiddle": 	{"startBone": "middle_metacarpal_r", 	"endBone": "middle_metacarpal_r",	"ikGoal": "None"},
		"RightHandMiddle":		{"startBone": "middle_01_r", 					"endBone": "middle_03_r",					"ikGoal": "None"},
		"RightInHandRing": 		{"startBone": "ring_metacarpal_r", 		"endBone": "ring_metacarpal_r",		"ikGoal": "None"},
		"RightHandRing": 			{"startBone": "ring_01_r", 						"endBone": "ring_03_r",						"ikGoal": "None"},
		"RightInHandPinky": 	{"startBone": "pinky_metacarpal_r", 	"endBone": "pinky_metacarpal_r",	"ikGoal": "None"},
		"RightHandPinky": 		{"startBone": "pinky_01_r", 					"endBone": "pinky_03_r",					"ikGoal": "None"},
		# Left Leg / Foot
		"LeftLeg": 						{"startBone": "thigh_l",							"endBone": "ball_l", 							"ikGoal": "None"},
		"LeftFootBigToe": 		{"startBone": "bigtoe_01_l",					"endBone": "bigtoe_02_l",					"ikGoal": "None"},
		"LeftFootIndex": 			{"startBone": "indextoe_01_l",				"endBone": "indextoe_02_l",				"ikGoal": "None"},
		"LeftFootMiddle": 		{"startBone": "middletoe_01_l",				"endBone": "middletoe_02_l",			"ikGoal": "None"},
		"LeftFootRing": 			{"startBone": "ringtoe_01_l",					"endBone": "ringtoe_02_l",				"ikGoal": "None"},
		"LeftFootPinky": 			{"startBone": "littletoe_01_l",				"endBone": "littletoe_02_l",			"ikGoal": "None"},
		# Right Leg / Foot
		"RightLeg": 					{"startBone": "thigh_r",							"endBone": "ball_r", 							"ikGoal": "None"},
		"RightFootBigToe": 		{"startBone": "bigtoe_01_r",					"endBone": "bigtoe_02_r",					"ikGoal": "None"},
		"RightFootIndex": 		{"startBone": "indextoe_01_r",				"endBone": "indextoe_02_r",				"ikGoal": "None"},
		"RightFootMiddle": 		{"startBone": "middletoe_01_r",				"endBone": "middletoe_02_r",			"ikGoal": "None"},
		"RightFootRing": 			{"startBone": "ringtoe_01_r",					"endBone": "ringtoe_02_r",				"ikGoal": "None"},
		"RightFootPinky": 		{"startBone": "littletoe_01_r",				"endBone": "littletoe_02_r",			"ikGoal": "None"},
		# Ik Joints
		"RootHandIk": 		 		{"startBone": "ik_hand_root",					"endBone": "ik_hand_root",				"ikGoal": "None"},
		"HandGunIk": 			 		{"startBone": "ik_hand_gun",					"endBone": "ik_hand_gun",					"ikGoal": "None"},
		"LeftHandIk": 		 		{"startBone": "ik_hand_l",						"endBone": "ik_hand_l",						"ikGoal": "None"},
		"RightHandIk": 		 		{"startBone": "ik_hand_r",						"endBone": "ik_hand_r",						"ikGoal": "None"},
		"RootFootIk": 		 		{"startBone": "ik_foot_root",					"endBone": "ik_foot_root",				"ikGoal": "None"},
		"LeftFootIk": 		 		{"startBone": "ik_foot_l",						"endBone": "ik_foot_l",						"ikGoal": "None"},
		"RightFootIk": 		 		{"startBone": "ik_foot_r",						"endBone": "ik_foot_r",						"ikGoal": "None"},
		# Roll
		"LeftArmRoll1": 			{"startBone": "upperarm_twist_01_l",	"endBone": "upperarm_twist_01_l",	"ikGoal": "None"},
		"LeftArmRoll2": 			{"startBone": "upperarm_twist_02_l",	"endBone": "upperarm_twist_02_l",	"ikGoal": "None"},
		"LeftForeArmRoll1": 	{"startBone": "lowerarm_twist_02_l",	"endBone": "lowerarm_twist_02_l",	"ikGoal": "None"},
		"LeftForeArmRoll2": 	{"startBone": "lowerarm_twist_01_l",	"endBone": "lowerarm_twist_01_l",	"ikGoal": "None"},
		"RightArmRoll1": 			{"startBone": "upperarm_twist_01_r",	"endBone": "upperarm_twist_01_r",	"ikGoal": "None"},
		"RightArmRoll2": 			{"startBone": "upperarm_twist_02_r",	"endBone": "upperarm_twist_02_r",	"ikGoal": "None"},
		"RightForeArmRoll1": 	{"startBone": "lowerarm_twist_02_r",	"endBone": "lowerarm_twist_02_r",	"ikGoal": "None"},
		"RightForeArmRoll2": 	{"startBone": "lowerarm_twist_01_r",	"endBone": "lowerarm_twist_01_r",	"ikGoal": "None"},
		"LeftUpLegRoll1": 		{"startBone": "thigh_twist_01_l",			"endBone": "thigh_twist_01_l",		"ikGoal": "None"},
		"LeftUpLegRoll2": 		{"startBone": "thigh_twist_02_l",			"endBone": "thigh_twist_02_l",		"ikGoal": "None"},
		"LeftLegRoll1": 			{"startBone": "calf_twist_02_l",			"endBone": "calf_twist_02_l",			"ikGoal": "None"},
		"LeftLegRoll2": 			{"startBone": "calf_twist_01_l",			"endBone": "calf_twist_01_l",			"ikGoal": "None"},
		"RightUpLegRoll1": 		{"startBone": "thigh_twist_01_r",			"endBone": "thigh_twist_01_r",		"ikGoal": "None"},
		"RightUpLegRoll2": 		{"startBone": "thigh_twist_02_r",			"endBone": "thigh_twist_02_r",		"ikGoal": "None"},
		"RightLegRoll1": 			{"startBone": "calf_twist_02_r",			"endBone": "calf_twist_02_r",			"ikGoal": "None"},
		"RightLegRoll2": 			{"startBone": "calf_twist_01_r",			"endBone": "calf_twist_01_r",			"ikGoal": "None"},
	}

	def validateProject(self) -> bool:
		# Check if project has at least two skeletal meshes / skeletons to work with
		# Make sure source and target has ik rig

		pass


	def validateDefinition(self) -> bool:
		"""Validates if at least a basic set of nodes required for characterization exists.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""


		return False



if __name__ == "__main__":
	uep.log_warning("takie tam")
