#--------------------------------------------------------------------------------------------------
# Lunar Ctrls
#--------------------------------------------------------------------------------------------------




templateLC = {
	"minimalDefinition": {
		# Base (required)
		"Hips": 									{"id": 1,		"node": "pelvis_ctrl"},
		"LeftUpLeg": 							{"id": 2,		"node": "thigh_l_ctrl"},
		"LeftLeg":								{"id": 3,		"node": "calf_l_ctrl"},
		"LeftFoot": 							{"id": 4,		"node": "foot_l_ctrl"},
		"RightUpLeg": 						{"id": 5,		"node": "thigh_r_ctrl"},
		"RightLeg":								{"id": 6,		"node": "calf_r_ctrl"},
		"RightFoot":							{"id": 7,		"node": "foot_r_ctrl"},
		"Spine":									{"id": 8,		"node": "spine_01_ctrl"},
		"LeftArm":								{"id": 9,		"node": "upperarm_l_ctrl"},
		"LeftForeArm":						{"id": 10, 	"node": "lowerarm_l_ctrl"},
		"LeftHand":								{"id": 11, 	"node": "hand_l_ctrl"},
		"RightArm":								{"id": 12, 	"node": "upperarm_r_ctrl"},
		"RightForeArm":						{"id": 13, 	"node": "lowerarm_r_ctrl"},
		"RightHand":							{"id": 14, 	"node": "hand_r_ctrl"},
		"Head":										{"id": 15, 	"node": "head_ctrl"},
	},
	"definition": {
		# "Reference": 							{"id": 0,	"node": "root_ctrl"},
    "Root": 									{"id": 500,	"node": "root_ctrl"},
		# Base (required)
		"Hips":										{"id": 1, 	"node": "pelvis_ctrl"},
		"LeftUpLeg": 							{"id": 2, 	"node": "thigh_l_ctrl"},
		"LeftLeg": 								{"id": 3, 	"node": "calf_l_ctrl"},
		"LeftFoot": 							{"id": 4, 	"node": "foot_l_ctrl"},
		"RightUpLeg":							{"id": 5, 	"node": "thigh_r_ctrl"},
		"RightLeg": 							{"id": 6, 	"node": "calf_r_ctrl"},
		"RightFoot": 							{"id": 7, 	"node": "foot_r_ctrl"},
		"Spine": 									{"id": 8, 	"node": "spine_01_ctrl"},
		"LeftArm": 								{"id": 9, 	"node": "upperarm_l_ctrl"},
		"LeftForeArm": 						{"id": 10, 	"node": "lowerarm_l_ctrl"},
		"LeftHand": 							{"id": 11, 	"node": "hand_l_ctrl"},
		"RightArm": 							{"id": 12, 	"node": "upperarm_r_ctrl"},
		"RightForeArm": 					{"id": 13, 	"node": "lowerarm_r_ctrl"},
		"RightHand": 							{"id": 14, 	"node": "hand_r_ctrl"},
		"Head": 									{"id": 15, 	"node": "head_ctrl"},
		# Auxiliary
		"LeftToeBase": 						{"id": 16, 	"node": "ball_l_ctrl"},
		"RightToeBase": 					{"id": 17, 	"node": "ball_r_ctrl"},
		"LeftShoulder": 					{"id": 18, 	"node": "clavicle_l_ctrl"},
		"RightShoulder": 					{"id": 19, 	"node": "clavicle_r_ctrl"},
		"Neck": 									{"id": 20, 	"node": "neck_01_ctrl"},
		# Spine
		"Spine1": 								{"id": 23, 	"node": "spine_02_ctrl"},
		"Spine2": 								{"id": 24, 	"node": "spine_03_ctrl"},
		"Spine3": 								{"id": 25, 	"node": "spine_04_ctrl"},
		"Spine4": 								{"id": 26, 	"node": "spine_05_ctrl"},
		# Neck
		"Neck1": 									{"id": 32, 	"node": "neck_02_ctrl"},
		# Roll - Leaf
		# We don't bake the twist ctrls because they're calculated in the solver
		"LeafLeftArmRoll1": 			{"id": 176, "node": "upperarm_twist_01_l_ctrl"},
		"LeafLeftArmRoll2": 			{"id": 184, "node": "upperarm_twist_02_l_ctrl"},
		"LeafLeftForeArmRoll1": 	{"id": 177, "node": "lowerarm_twist_02_l_ctrl"},
		"LeafLeftForeArmRoll2": 	{"id": 185, "node": "lowerarm_twist_01_l_ctrl"},
		"LeafRightArmRoll1":			{"id": 178, "node": "upperarm_twist_01_r_ctrl"},
		"LeafRightArmRoll2":			{"id": 186, "node": "upperarm_twist_02_r_ctrl"},
		"LeafRightForeArmRoll1": 	{"id": 179, "node": "lowerarm_twist_02_r_ctrl"},
		"LeafRightForeArmRoll2": 	{"id": 187, "node": "lowerarm_twist_01_r_ctrl"},
		"LeafLeftUpLegRoll1": 		{"id": 172, "node": "thigh_twist_01_l_ctrl"},
		"LeafLeftUpLegRoll2": 		{"id": 180, "node": "thigh_twist_02_l_ctrl"},
		"LeafLeftLegRoll1": 			{"id": 173, "node": "calf_twist_02_l_ctrl"},
		"LeafLeftLegRoll2": 			{"id": 181, "node": "calf_twist_01_l_ctrl"},
		"LeafRightUpLegRoll1": 		{"id": 174, "node": "thigh_twist_01_r_ctrl"},
		"LeafRightUpLegRoll2": 		{"id": 182, "node": "thigh_twist_02_r_ctrl"},
		"LeafRightLegRoll1": 			{"id": 175, "node": "calf_twist_02_r_ctrl"},
		"LeafRightLegRoll2": 			{"id": 183, "node": "calf_twist_01_r_ctrl"},
		# Left Hand
		"LeftHandThumb1": 				{"id": 50, 	"node": "thumb_01_l_ctrl"},
		"LeftHandThumb2": 				{"id": 51, 	"node": "thumb_02_l_ctrl"},
		"LeftHandThumb3": 				{"id": 52, 	"node": "thumb_03_l_ctrl"},
		"LeftHandIndex1": 				{"id": 54, 	"node": "index_01_l_ctrl"},
		"LeftHandIndex2": 				{"id": 55, 	"node": "index_02_l_ctrl"},
		"LeftHandIndex3": 				{"id": 56, 	"node": "index_03_l_ctrl"},
		"LeftHandMiddle1": 				{"id": 58, 	"node": "middle_01_l_ctrl"},
		"LeftHandMiddle2": 				{"id": 59, 	"node": "middle_02_l_ctrl"},
		"LeftHandMiddle3": 				{"id": 60, 	"node": "middle_03_l_ctrl"},
		"LeftHandRing1": 					{"id": 62, 	"node": "ring_01_l_ctrl"},
		"LeftHandRing2": 					{"id": 63, 	"node": "ring_02_l_ctrl"},
		"LeftHandRing3": 					{"id": 64, 	"node": "ring_03_l_ctrl"},
		"LeftHandPinky1": 				{"id": 66, 	"node": "pinky_01_l_ctrl"},
		"LeftHandPinky2": 				{"id": 67, 	"node": "pinky_02_l_ctrl"},
		"LeftHandPinky3": 				{"id": 68, 	"node": "pinky_03_l_ctrl"},
		# Right Hand
		"RightHandThumb1": 				{"id": 74, 	"node": "thumb_01_r_ctrl"},
		"RightHandThumb2": 				{"id": 75, 	"node": "thumb_02_r_ctrl"},
		"RightHandThumb3": 				{"id": 76, 	"node": "thumb_03_r_ctrl"},
		"RightHandIndex1": 				{"id": 78, 	"node": "index_01_r_ctrl"},
		"RightHandIndex2": 				{"id": 79, 	"node": "index_02_r_ctrl"},
		"RightHandIndex3": 				{"id": 80, 	"node": "index_03_r_ctrl"},
		"RightHandMiddle1": 			{"id": 82, 	"node": "middle_01_r_ctrl"},
		"RightHandMiddle2": 			{"id": 83, 	"node": "middle_02_r_ctrl"},
		"RightHandMiddle3": 			{"id": 84, 	"node": "middle_03_r_ctrl"},
		"RightHandRing1": 				{"id": 86, 	"node": "ring_01_r_ctrl"},
		"RightHandRing2": 				{"id": 87, 	"node": "ring_02_r_ctrl"},
		"RightHandRing3": 				{"id": 88, 	"node": "ring_03_r_ctrl"},
		"RightHandPinky1": 				{"id": 90, 	"node": "pinky_01_r_ctrl"},
		"RightHandPinky2": 				{"id": 91, 	"node": "pinky_02_r_ctrl"},
		"RightHandPinky3": 				{"id": 92, 	"node": "pinky_03_r_ctrl"},
		# Inner Finger
		"LeftInHandIndex": 				{"id": 147, "node": "index_metacarpal_l_ctrl"},
		"LeftInHandMiddle": 			{"id": 148, "node": "middle_metacarpal_l_ctrl"},
		"LeftInHandRing":					{"id": 149, "node": "ring_metacarpal_l_ctrl"},
		"LeftInHandPinky": 				{"id": 150, "node": "pinky_metacarpal_l_ctrl"},
		"RightInHandIndex": 			{"id": 153, "node": "index_metacarpal_r_ctrl"},
		"RightInHandMiddle": 			{"id": 154, "node": "middle_metacarpal_r_ctrl"},
		"RightInHandRing": 				{"id": 155, "node": "ring_metacarpal_r_ctrl"},
		"RightInHandPinky": 			{"id": 156, "node": "pinky_metacarpal_r_ctrl"},
		# Left Foot
		"LeftFootIndex1": 				{"id": 102, "node": "indextoe_01_l_ctrl"},
		"LeftFootIndex2": 				{"id": 103, "node": "indextoe_02_l_ctrl"},
		"LeftFootMiddle1": 				{"id": 106, "node": "middletoe_01_l_ctrl"},
		"LeftFootMiddle2": 				{"id": 107, "node": "middletoe_02_l_ctrl"},
		"LeftFootRing1": 					{"id": 110, "node": "ringtoe_01_l_ctrl"},
		"LeftFootRing2": 					{"id": 111, "node": "ringtoe_02_l_ctrl"},
		"LeftFootPinky1": 				{"id": 114, "node": "littletoe_01_l_ctrl"},
		"LeftFootPinky2": 				{"id": 115, "node": "littletoe_02_l_ctrl"},
		# "LeftFootExtraFinger1": 	{"id": 118, "node": "ball_l_ctrl"},
		# "LeftFootExtraFinger1": 	{"id": 118, "node": "bigtoe_01_l_ctrl"},
		# "LeftFootExtraFinger2": 	{"id": 119, "node": "bigtoe_02_l_ctrl"},
		# Left Foot
		"RightFootIndex1": 				{"id": 126, "node": "indextoe_01_r_ctrl"},
		"RightFootIndex2": 				{"id": 127, "node": "indextoe_02_r_ctrl"},
		"RightFootMiddle1": 			{"id": 130, "node": "middletoe_01_r_ctrl"},
		"RightFootMiddle2": 			{"id": 131, "node": "middletoe_02_r_ctrl"},
		"RightFootRing1": 				{"id": 134, "node": "ringtoe_01_r_ctrl"},
		"RightFootRing2": 				{"id": 135, "node": "ringtoe_02_r_ctrl"},
		"RightFootPinky1": 				{"id": 138, "node": "littletoe_01_r_ctrl"},
		"RightFootPinky2": 				{"id": 139, "node": "littletoe_02_r_ctrl"},
		# "RightFootExtraFinger1": 	{"id": 142, "node": "ball_r_ctrl"},
		# "RightFootExtraFinger1": 	{"id": 142, "node": "bigtoe_01_r_ctrl"},
		# "RightFootExtraFinger2": 	{"id": 143, "node": "bigtoe_02_r_ctrl"},
	},
	"tPose": {
		'arm_ik_l_ctrl': {'rotateX': 17.35993869687529,
											'rotateY': -37.688334405046376,
											'rotateZ': -54.65744377525774,
											# 'space': 1,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': -25.286646369995964,
											'translateY': -42.66242447467424,
											'translateZ': 17.219516366743342},
		'arm_ik_r_ctrl': {'rotateX': 17.35993869662584,
											'rotateY': -37.688334403253364,
											'rotateZ': -54.657443774850194,
											# 'space': 1,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': 25.286418445361058,
											'translateY': 42.66206651628546,
											'translateZ': -17.21947200958451},
		'arm_pv_l_ctrl': {
			# 'space': 1,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
			# 47.022954481046554 146.45453127655196 -53.56518813808574
											'translateX': -24.174,
											'translateY': -30.327,
											'translateZ': -8.63},
		'arm_pv_r_ctrl': {
			# 'space': 1,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
			# -47.007864843158906 146.45403973947492 -53.56471909821015
											'translateX': 24.18,
											'translateY': 30.317,
											'translateZ': 8.639},
		'ball_l_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 4.4527765540489235e-14,
										'translateX': 3.979580061042043e-07,
										'translateY': 4.885283955147202e-09,
										'translateZ': -4.1723404109461626e-07},
		'ball_r_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': -2.5444437451708134e-14,
										'translateX': 3.593348392172402e-07,
										'translateY': 1.2493799772528291e-08,
										'translateZ': 4.172276497627081e-07},
		'calf_l_ctrl': {'rotateZ': 3.004844555942174},
		'calf_r_ctrl': {'rotateZ': 3.004844555807813},
		# 'calf_l_ik': {'rotateZ': 3.004844555942174},
		# 'calf_r_ik': {'rotateZ': 3.004844555807813},
		'calf_twist_01_l_ctrl': {'rotateX': 0.0},
		'calf_twist_01_r_ctrl': {'rotateX': 0.0},
		'calf_twist_02_l_ctrl': {'rotateX': 0.0},
		'calf_twist_02_r_ctrl': {'rotateX': 0.0},
		'clavicle_l_ctrl': {'rotateX': -3.4333294468700877,
												'rotateY': -8.777245010360375,
												'rotateZ': -2.6611805835416873},
		'clavicle_r_ctrl': {'rotateX': -3.4333294468700877,
												'rotateY': -8.777245008565831,
												'rotateZ': -2.6611805838597316},
		'foot_l_ctrl': {'rotateX': 0.14801845934854388,
										'rotateY': -3.077651516528107,
										'rotateZ': -2.6682064825039036},
		'foot_r_ctrl': {'rotateX': 0.1480184593720812,
										'rotateY': -3.077651516523797,
										'rotateZ': -2.6682064823692717},
		'hand_l_ctrl': {'rotateX': -22.226164845738964,
										'rotateY': 1.1439457621935432,
										'rotateZ': -2.0591203960176605},
		'hand_r_ctrl': {'rotateX': -22.22616484509012,
										'rotateY': 1.1439456826735446,
										'rotateZ': -2.0591203635173088},
		'head_ctrl': {'rotateX': -3.01198528334595e-11,
									'rotateY': 3.180554681463099e-14,
									'rotateZ': -1.5902773407325943e-14},
		# 'foot_l_ik': {'rotateX': 0.14801845934854388,
		# 								'rotateY': -3.077651516528107,
		# 								'rotateZ': -2.6682064825039036},
		# 'foot_r_ik': {'rotateX': 0.1480184593720812,
		# 								'rotateY': -3.077651516523797,
		# 								'rotateZ': -2.6682064823692717},
		# 'hand_l_ik': {'rotateX': -22.226164845738964,
		# 								'rotateY': 1.1439457621935432,
		# 								'rotateZ': -2.0591203960176605},
		# 'hand_r_ik': {'rotateX': -22.22616484509012,
		# 								'rotateY': 1.1439456826735446,
		# 								'rotateZ': -2.0591203635173088},
		# 'head_ik': {'rotateX': -3.01198528334595e-11,
		# 							'rotateY': 3.180554681463099e-14,
		# 							'rotateZ': -1.5902773407325943e-14},
		'head_ik_ctrl': {'rotateX': 3.013294821684476e-11,
											'rotateY': -1.5838211932148108e-06,
											'rotateZ': 1.5838224209080845e-06,
											# 'space': 0,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': 0.0,
											'translateY': -5.329070518200751e-15,
											'translateZ': -8.470329472543003e-22},
		'fkik_ctrl': {
			# 'headFkIk': 0,
			# 'headSoftness': 0.0,
			# 'headTwist': 0.0,
			# 'leftArmFkIk': 0,
			'leftArmSoftness': 0.0,
			'leftArmTwist': 0.0,
			# 'leftLegFkIk': 0,
			'leftLegSoftness': 0.0,
			'leftLegTwist': 0.0,
			# 'rightArmFkIk': 0,
			'rightArmSoftness': 0.0,
			'rightArmTwist': 0.0,
			# 'rightLegFkIk': 0,
			'rightLegSoftness': 0.0,
			'rightLegTwist': 0.0
		},
		'index_01_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.372999646513968},
		'index_01_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.372999646513954},
		'index_02_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -14.892568419111004},
		'index_02_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -14.892568419110978},
		'index_03_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -12.516400997546972},
		'index_03_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -12.516400997546976},
		'index_metacarpal_l_ctrl': {'rotateX': -3.392214739846164,
																'rotateY': -7.277920384261332,
																'rotateZ': 1.032481382960804},
		'index_metacarpal_r_ctrl': {'rotateX': -3.3922147398461147,
																'rotateY': -7.277920384261377,
																'rotateZ': 1.0324813829608037},
		'leg_ik_l_ctrl': {'rotateX': -8.512378893241221,
											'rotateY': -0.29475584273450334,
											'rotateZ': -0.1696226233462818,
											# 'space': 2,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': -0.19942807852882538,
											'translateY': -1.2876436693668962,
											'translateZ': 4.35620604771675},
		'leg_ik_r_ctrl': {'rotateX': -8.512378893241234,
											'rotateY': -0.2947558427344649,
											'rotateZ': -0.16962262334627834,
											# 'space': 2,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': 0.20002569410172555,
											'translateY': 1.287682294273894,
											'translateZ': -4.356207939436647},
		'leg_pv_l_ctrl': {
			# 'space': 2,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': 1.296,
											'translateY': 1.501,
											'translateZ': 14.994
		},
		'leg_pv_r_ctrl': {
			# 'space': 2,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': -1.295,
											'translateY': -1.501,
											'translateZ': -14.994
		},
		'lowerarm_l_ctrl': {'rotateZ': 38.95697362510834},
		'lowerarm_r_ctrl': {'rotateZ': 38.95697352574442},
		# 'lowerarm_l_ik': {'rotateZ': 38.95697362510834},
		# 'lowerarm_r_ik': {'rotateZ': 38.95697352574442},
		'lowerarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'main_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'middle_01_l_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -31.57268201739826},
		'middle_01_r_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -31.572682017398208},
		'middle_02_l_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -20.769210477739502},
		'middle_02_r_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -20.769210477739517},
		'middle_03_l_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -9.999999970953365},
		'middle_03_r_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -9.999999970953379},
		'middle_metacarpal_l_ctrl': {'rotateX': 4.2742869841384366,
																	'rotateY': -0.04239235333973031,
																	'rotateZ': 2.321686871758419},
		'middle_metacarpal_r_ctrl': {'rotateX': 4.274286984138468,
																	'rotateY': -0.04239235333976848,
																	'rotateZ': 2.321686871758424},
		'neck_01_ctrl': {'rotateX': -3.1805546814635704e-15,
											'rotateY': 1.590277340731757e-14,
											'rotateZ': -3.8802767113854903e-13},
		'neck_02_ctrl': {'rotateX': 3.1805546814635176e-15,
											'rotateY': 4.9435750538161805e-30,
											'rotateZ': -1.7811106216195696e-13},
		# 'neck_01_ik': {'rotateX': -3.1805546814635704e-15,
		# 									'rotateY': 1.590277340731757e-14,
		# 									'rotateZ': -3.8802767113854903e-13},
		# 'neck_02_ik': {'rotateX': 3.1805546814635176e-15,
		# 									'rotateY': 4.9435750538161805e-30,
		# 									'rotateZ': -1.7811106216195696e-13},
		'pelvis_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': -3.6331069499670683,
										# 'space': 0,
										# 'spaceUseRotate': True,
										# 'spaceUseTranslate': True,
										'translateX': 0.0,
										'translateY': 0.0,
										'translateZ': -3.1554436208840472e-30},
		'pelvis_rot_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_01_l_ctrl': {'rotateX': -9.999764978819476,
												'rotateY': -3.2478503919205512,
												'rotateZ': -14.493910369701384},
		'pinky_01_r_ctrl': {'rotateX': -9.999764978819524,
												'rotateY': -3.2478503919205433,
												'rotateZ': -14.493910369701393},
		'pinky_02_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -21.28699904924387},
		'pinky_02_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -21.28699904924381},
		'pinky_03_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -4.917000047022361},
		'pinky_03_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -4.917000047022356},
		'pinky_metacarpal_l_ctrl': {'rotateX': 25.358336691053672,
																'rotateY': 22.652560432083973,
																'rotateZ': -1.8189991299227142},
		'pinky_metacarpal_r_ctrl': {'rotateX': 25.358336691053765,
																'rotateY': 22.65256043208395,
																'rotateZ': -1.8189991299227075},
		'ring_01_l_ctrl': {'rotateX': -5.633826864078882,
												'rotateY': -3.0348222875821964,
												'rotateZ': -29.271655648141063},
		'ring_01_r_ctrl': {'rotateX': -5.633826864078884,
												'rotateY': -3.0348222875821786,
												'rotateZ': -29.271655648141017},
		'ring_02_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -18.96399954197176},
		'ring_02_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -18.963999541971805},
		'ring_03_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -9.167999748024997},
		'ring_03_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -9.167999748024979},
		'ring_metacarpal_l_ctrl': {'rotateX': 13.886394588293472,
																'rotateY': 11.109677713548278,
																'rotateZ': 4.3333130099048125},
		'ring_metacarpal_r_ctrl': {'rotateX': 13.886394588293507,
																'rotateY': 11.109677713548265,
																'rotateZ': 4.3333130099048},
		'root_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									# 'space': 1,
									# 'spaceUseRotate': True,
									# 'spaceUseTranslate': True,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'spine_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_03_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_04_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_05_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_l_ctrl': {'rotateX': -8.214648949493862,
											'rotateY': 3.607092101212202,
											'rotateZ': 3.071208988308576},
		'thigh_r_ctrl': {'rotateX': -8.214648949524806,
											'rotateY': 3.6070921012086874,
											'rotateZ': 3.071208988309044},
		# 'thigh_l_ik': {'rotateX': -8.214648949493862,
		# 									'rotateY': 3.607092101212202,
		# 									'rotateZ': 3.071208988308576},
		# 'thigh_r_ik': {'rotateX': -8.214648949524806,
		# 									'rotateY': 3.6070921012086874,
		# 									'rotateZ': 3.071208988309044},
		'thigh_twist_01_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_01_r_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_r_ctrl': {'rotateX': 0.0},
		'thumb_01_l_ctrl': {'rotateX': -75.42521984002168,
												'rotateY': -30.400067883741325,
												'rotateZ': 33.58891858856432},
		'thumb_01_r_ctrl': {'rotateX': -75.42521984002161,
												'rotateY': -30.400067883741325,
												'rotateZ': 33.58891858856437},
		'thumb_02_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.318825988464383},
		'thumb_02_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.318825988464447},
		'thumb_03_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -9.99999997095338},
		'thumb_03_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -9.999999970953382},
		'upperarm_l_ctrl': {'rotateX': 1.715629509725695,
												'rotateY': -46.16303548931691,
												'rotateZ': 1.7949836533557042},
		'upperarm_r_ctrl': {'rotateX': 1.7156294974432327,
												'rotateY': -46.1630354917084,
												'rotateZ': 1.7949836703834072},
		# 'upperarm_l_ik': {'rotateX': 1.715629509725695,
		# 										'rotateY': -46.16303548931691,
		# 										'rotateZ': 1.7949836533557042},
		# 'upperarm_r_ik': {'rotateX': 1.7156294974432327,
		# 										'rotateY': -46.1630354917084,
		# 										'rotateZ': 1.7949836703834072},
		'upperarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'weapon_l_ctrl': {
			'rotateX': 0.0,
			'rotateY': 0.0,
			'rotateZ': 0.0,
			'translateX': 6.5,
			'translateY': 0.5,
			'translateZ': -3.0,
		},
		'weapon_r_ctrl': {
			'rotateX': 0.0,
			'rotateY': 0.0,
			'rotateZ': 0.0,
			'translateX': -6.5,
			'translateY': -0.5,
			'translateZ': 3.0,
		},
	},
	"aPose": {
		'arm_ik_l_ctrl': {'rotateX': -5.724998426634331e-14,
											'rotateY': 6.361109362927035e-15,
											'rotateZ': 6.36110936292703e-15,
											# 'space': 1,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': -7.105427357601002e-15,
											'translateY': 2.842170943040401e-14,
											'translateZ': 8.881784197001252e-15},
		'arm_ik_r_ctrl': {'rotateX': -1.2722218725854073e-14,
											'rotateY': 1.5952469574215454e-14,
											'rotateZ': -1.5455507905236783e-14,
											# 'space': 1,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': -2.1316282072803006e-14,
											'translateY': -1.4210854715202004e-14,
											'translateZ': 0.0},
		'arm_pv_l_ctrl': {
			# 'space': 1,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': 7.105427357601002e-15,
											'translateY': 7.105427357601002e-15,
											'translateZ': -1.4210854715202004e-14},
		'arm_pv_r_ctrl': {
			# 'space': 1,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': 7.105427357601002e-15,
											'translateY': -7.105427357601002e-15,
											'translateZ': 0.0},
		'ball_l_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 0.0,
										'translateX': 3.979580061042043e-07,
										'translateY': 4.885283955147202e-09,
										'translateZ': -4.1723404109461626e-07},
		'ball_r_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 0.0,
										'translateX': 3.593348392172402e-07,
										'translateY': 1.2493799772528291e-08,
										'translateZ': 4.172276497627081e-07},
		'calf_l_ctrl': {'rotateZ': 0.0},
		'calf_r_ctrl': {'rotateZ': 0.0},
		# 'calf_l_ik': {'rotateZ': 0.0},
		# 'calf_r_ik': {'rotateZ': 0.0},
		'calf_twist_01_l_ctrl': {'rotateX': 0.0},
		'calf_twist_01_r_ctrl': {'rotateX': 0.0},
		'calf_twist_02_l_ctrl': {'rotateX': 0.0},
		'calf_twist_02_r_ctrl': {'rotateX': 0.0},
		'clavicle_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'clavicle_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'foot_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'foot_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'hand_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'hand_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'head_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'foot_l_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'foot_r_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'hand_l_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'hand_r_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'head_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'head_ik_ctrl': {'rotateX': 3.015203154493355e-11,
											'rotateY': -1.5838212250203584e-06,
											'rotateZ': 1.583822389102538e-06,
											# 'space': 0,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': 2.842170943040401e-14,
											'translateY': -6.8833827526759706e-15,
											'translateZ': 0.0},
		'fkik_ctrl': {
			# 'headFkIk': 0,
			# 'headSoftness': 0.0,
			# 'headTwist': 0.0,
			# 'leftArmFkIk': 0,
			'leftArmSoftness': 0.0,
			'leftArmTwist': 0.0,
			# 'leftLegFkIk': 0,
			'leftLegSoftness': 0.0,
			'leftLegTwist': 0.0,
			# 'rightArmFkIk': 0,
			'rightArmSoftness': 0.0,
			'rightArmTwist': 0.0,
			# 'rightLegFkIk': 0,
			'rightLegSoftness': 0.0,
			'rightLegTwist': 0.0
		},
		'index_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_02_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_02_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_03_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_03_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'leg_ik_l_ctrl': {'rotateX': 5.4069429584879776e-14,
											'rotateY': -1.5902773407317578e-14,
											'rotateZ': -3.180554681463524e-15,
											# 'space': 2,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': -1.7763568394002505e-15,
											'translateY': -1.1102230246251565e-16,
											'translateZ': -3.552713678800501e-15},
		'leg_ik_r_ctrl': {'rotateX': 9.223608576244199e-14,
											'rotateY': 6.361109362927069e-15,
											'rotateZ': -4.452776554048923e-14,
											# 'space': 2,
											# 'spaceUseRotate': True,
											# 'spaceUseTranslate': True,
											'translateX': 1.7763568394002505e-15,
											'translateY': 0.0,
											'translateZ': -1.7763568394002505e-15},
		'leg_pv_l_ctrl': {
			# 'space': 2,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': 0.0,
											'translateY': 0.0,
											'translateZ': 0.0},
		'leg_pv_r_ctrl': {
			# 'space': 2,
			# 								'spaceUseRotate': False,
			# 								'spaceUseTranslate': True,
											'translateX': 0.0,
											'translateY': 0.0,
											'translateZ': 0.0},
		'lowerarm_l_ctrl': {'rotateZ': 0.0},
		'lowerarm_r_ctrl': {'rotateZ': 0.0},
		# 'lowerarm_l_ik': {'rotateZ': 0.0},
		# 'lowerarm_r_ik': {'rotateZ': 0.0},
		'lowerarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'main_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'middle_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_02_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_02_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_03_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_03_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'neck_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'neck_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'neck_01_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		# 'neck_02_ik': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pelvis_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 0.0,
										# 'space': 0,
										# 'spaceUseRotate': True,
										# 'spaceUseTranslate': True,
										'translateX': 0.0,
										'translateY': 0.0,
										'translateZ': -3.1554436208840472e-30},
		'pelvis_rot_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_02_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_02_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_03_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_03_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_02_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_02_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_03_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_03_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'root_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									# 'space': 1,
									# 'spaceUseRotate': True,
									# 'spaceUseTranslate': True,
									'translateX': 6.310887241768095e-30,
									'translateY': -8.881784197001252e-16,
									'translateZ': 1.9721522630525295e-31},
		'spine_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_03_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_04_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_05_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_twist_01_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_01_r_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_r_ctrl': {'rotateX': 0.0},
		'thumb_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_02_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_02_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_03_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_03_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'upperarm_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'upperarm_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'upperarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'weapon_l_ctrl': {
			'rotateX': 0.0,
			'rotateY': 0.0,
			'rotateZ': 0.0,
			'translateX': 6.5,
			'translateY': 0.5,
			'translateZ': -3.0,
		},
		'weapon_r_ctrl': {
			'rotateX': 0.0,
			'rotateY': 0.0,
			'rotateZ': 0.0,
			'translateX': -6.5,
			'translateY': -0.5,
			'translateZ': 3.0,
		},
	}
}
