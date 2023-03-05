# Built-in imports

# Third-party imports
import unreal as uep

# Custom imports
from lunar.abstract.retarget import AbstractRetarget



class UnrealSinnersDev(AbstractRetarget):
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
		"Root": 							{"startBone": "trajectory", 		"endBone": "trajectory", 			"ikGoal": "None"},
		"Spine": 							{"startBone": "spinea", 				"endBone": "spined", 					"ikGoal": "None"},
		"Neck":								{"startBone": "neck", 					"endBone": "heada",						"ikGoal": "None"},
		"Head":								{"startBone": "headb", 					"endBone": "headb",						"ikGoal": "None"},
		# Left Arm / Hand
		"LeftArm": 						{"startBone": "l_clavicle", 		"endBone": "l_wrist",					"ikGoal": "None"},
		"LeftHandThumb": 			{"startBone": "l_thumba", 			"endBone": "l_thumbc",				"ikGoal": "None"},
		"LeftHandIndex": 			{"startBone": "l_indexa", 			"endBone": "l_indexc",				"ikGoal": "None"},
		"LeftHandMiddle":			{"startBone": "l_middlea", 			"endBone": "l_middlec",				"ikGoal": "None"},
		"LeftHandRing": 			{"startBone": "l_ringa", 				"endBone": "l_ringc",					"ikGoal": "None"},
		"LeftHandPinky": 			{"startBone": "l_pinkya", 			"endBone": "l_pinkyc",				"ikGoal": "None"},
		"LeftInHandIndex": 		{"startBone": "l_index_meta", 	"endBone": "l_index_meta",		"ikGoal": "None"},
		"LeftInHandMiddle": 	{"startBone": "l_middle_meta", 	"endBone": "l_middle_meta",		"ikGoal": "None"},
		"LeftInHandRing": 		{"startBone": "l_ring_meta", 		"endBone": "l_ring_meta",			"ikGoal": "None"},
		"LeftInHandPinky": 		{"startBone": "l_pinky_meta", 	"endBone": "l_pinky_meta",		"ikGoal": "None"},
		# Right Arm / Hand
		"RightArm": 					{"startBone": "r_clavicle", 		"endBone": "r_wrist", 				"ikGoal": "None"},
		"RightHandThumb": 		{"startBone": "r_thumba", 			"endBone": "r_thumbc",				"ikGoal": "None"},
		"RightHandIndex": 		{"startBone": "r_indexa",				"endBone": "r_indexc",				"ikGoal": "None"},
		"RightHandMiddle":		{"startBone": "r_middlea", 			"endBone": "r_middlec",				"ikGoal": "None"},
		"RightHandRing": 			{"startBone": "r_ringa", 				"endBone": "r_ringc",					"ikGoal": "None"},
		"RightHandPinky": 		{"startBone": "r_pinkya", 			"endBone": "r_pinkyc",				"ikGoal": "None"},
		"RightInHandIndex": 	{"startBone": "r_index_meta", 	"endBone": "r_index_meta",		"ikGoal": "None"},
		"RightInHandMiddle": 	{"startBone": "r_middle_meta", 	"endBone": "r_middle_meta",		"ikGoal": "None"},
		"RightInHandRing": 		{"startBone": "r_ring_meta", 		"endBone": "r_ring_meta",			"ikGoal": "None"},
		"RightInHandPinky": 	{"startBone": "r_pinky_meta", 	"endBone": "r_pinky_meta",		"ikGoal": "None"},
		# Left Leg / Foot
		"LeftLeg": 						{"startBone": "l_upper_leg",					"endBone": "l_ankle", 						"ikGoal": "None"},
		"LeftFootBigToe": 		{"startBone": "bigtoe_01_l",					"endBone": "bigtoe_02_l",					"ikGoal": "None"},
		"LeftFootIndex": 			{"startBone": "indextoe_01_l",				"endBone": "indextoe_02_l",				"ikGoal": "None"},
		"LeftFootMiddle": 		{"startBone": "middletoe_01_l",				"endBone": "middletoe_02_l",			"ikGoal": "None"},
		"LeftFootRing": 			{"startBone": "ringtoe_01_l",					"endBone": "ringtoe_02_l",				"ikGoal": "None"},
		"LeftFootPinky": 			{"startBone": "littletoe_01_l",				"endBone": "littletoe_02_l",			"ikGoal": "None"},
		# Right Leg / Foot
		"RightLeg": 					{"startBone": "r_upper_leg",					"endBone": "r_ankle", 						"ikGoal": "None"},
		"RightFootBigToe": 		{"startBone": "bigtoe_01_r",					"endBone": "bigtoe_02_r",					"ikGoal": "None"},
		"RightFootIndex": 		{"startBone": "indextoe_01_r",				"endBone": "indextoe_02_r",				"ikGoal": "None"},
		"RightFootMiddle": 		{"startBone": "middletoe_01_r",				"endBone": "middletoe_02_r",			"ikGoal": "None"},
		"RightFootRing": 			{"startBone": "ringtoe_01_r",					"endBone": "ringtoe_02_r",				"ikGoal": "None"},
		"RightFootPinky": 		{"startBone": "littletoe_01_r",				"endBone": "littletoe_02_r",			"ikGoal": "None"},
		# Ik Joints
		"LeftHandIk": 		 		{"startBone": "ik_hand_l",						"endBone": "ik_hand_l",						"ikGoal": "None"},
		"LeftFootIk": 		 		{"startBone": "ik_foot_l",						"endBone": "ik_foot_l",						"ikGoal": "None"},
		"RightHandIk": 		 		{"startBone": "ik_hand_r",						"endBone": "ik_hand_r",						"ikGoal": "None"},
		"RightFootIk": 		 		{"startBone": "ik_foot_r",						"endBone": "ik_foot_r",						"ikGoal": "None"},
		"HandRootIk": 		 		{"startBone": "ik_hand_root",					"endBone": "ik_hand_root",				"ikGoal": "None"},
		"FootRootIk": 		 		{"startBone": "ik_foot_root",					"endBone": "ik_foot_root",				"ikGoal": "None"},
		"HandGunIk": 			 		{"startBone": "ik_hand_gun",					"endBone": "ik_hand_gun",					"ikGoal": "None"},
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
		# Check if project has at least two sk / skeletons to work with

		pass


	def validateDefinition(self) -> bool:
		"""Validates if at least a basic set of nodes required for characterization exists.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""


		return False



if __name__ == "__main__":
	uep.log_warning("takie tam")
