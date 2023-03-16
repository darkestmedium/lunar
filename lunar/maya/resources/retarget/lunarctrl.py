#--------------------------------------------------------------------------------------------------
# Lunar Ctrls
#--------------------------------------------------------------------------------------------------




templateLC = {
	"minimalDefinition": {
		# Base (required)
		"Hips": 									{"id": 1,		"node": "pelvis_rot_ctrl"},
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
		"Reference": 							{"id": 0, 	"node": "main_ctrl"},
		# Base (required)
		"HipsTranslation": 				{"id": 49, 	"node": "pelvis_pos_ctrl"},
		"Hips":										{"id": 1, 	"node": "pelvis_rot_ctrl"},
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
		'arm_ik_l_ctrl': {'rotateX': 17.359938696874657,
											'rotateY': -37.6883344050464,
											'rotateZ': -54.657443775257704,
											'space': 1,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': -25.286722676516867,
											'translateY': -42.66238503077865,
											'translateZ': 17.219616784206664},
		'arm_ik_r_ctrl': {'rotateX': 17.35993869662534,
											'rotateY': -37.688334403253315,
											'rotateZ': -54.65744377485021,
											'space': 1,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': 25.28644561571783,
											'translateY': 42.662052733753,
											'translateZ': -17.219508541612324},
		'arm_pv_l_ctrl': {'space': 1,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 56.42735059350628,
											'translateY': -50.32526884028607,
											'translateZ': 45.40364320438688},
		'arm_pv_r_ctrl': {'space': 1,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': -56.42804661116971,
											'translateY': -50.32133728968291,
											'translateZ': 45.401172519036365},
		'ball_l_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 2.5444437451708134e-14},
		'ball_r_ctrl': {'rotateX': 0.0,
										'rotateY': 0.0,
										'rotateZ': 2.5444437451708134e-14},
		'calf_l_ctrl': {'rotateZ': 0.0},
		'calf_r_ctrl': {'rotateZ': -6.3611093629270335e-15},
		'calf_twist_01_l_ctrl': {'rotateX': 0.0},
		'calf_twist_01_r_ctrl': {'rotateX': 0.0},
		'calf_twist_02_l_ctrl': {'rotateX': 0.0},
		'calf_twist_02_r_ctrl': {'rotateX': 0.0},
		'clavicle_l_ctrl': {'rotateX': -3.433329446984582,
												'rotateY': -8.777245009295598,
												'rotateZ': -2.6611805827947306},
		'clavicle_r_ctrl': {'rotateX': -3.433329446707889,
												'rotateY': -8.777245009630619,
												'rotateZ': -2.6611805846067003},
		'foot_l_ctrl': {'rotateX': 0.0046693586008895605,
										'rotateY': -3.081201951125142,
										'rotateZ': -0.0002509836394888459},
		'foot_r_ctrl': {'rotateX': 0.004669358600908492,
										'rotateY': -3.0812019511251076,
										'rotateZ': -0.0002509836395036714},
		'hand_l_ctrl': {'fist': 50.0,
										'rotateX': -22.226250244301223,
										'rotateY': 1.1543643818116873,
										'rotateZ': -2.0633785725994502,
										'spread': 50.0},
		'hand_r_ctrl': {'fist': 50.0,
										'rotateX': -22.226248887225882,
										'rotateY': 1.154199554566477,
										'rotateZ': -2.063311206069602,
										'spread': 50.0},
		'head_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_01_l_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.372999646513982},
		'index_01_r_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -23.372999646513964},
		'index_02_l_ctrl': {'rotateZ': -14.892568419110988},
		'index_02_r_ctrl': {'rotateZ': -14.892568419110969},
		'index_03_l_ctrl': {'rotateZ': -12.51640099754697},
		'index_03_r_ctrl': {'rotateZ': -12.51640099754699},
		'index_metacarpal_l_ctrl': {'rotateX': -3.3922147398462905,
																'rotateY': -7.277920384261424,
																'rotateZ': 1.0324813829608421},
		'index_metacarpal_r_ctrl': {'rotateX': -3.3922147398460933,
																'rotateY': -7.277920384261348,
																'rotateZ': 1.0324813829607957},
		'leg_ik_l_ctrl': {'rotateX': -8.510496943038767,
											'rotateY': -0.3451878181841737,
											'rotateZ': -0.5066149232561586,
											'space': 3,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': -0.13321912171194228,
											'translateY': 0.9008701174829753,
											'translateZ': 4.02892210324541},
		'leg_ik_r_ctrl': {'rotateX': -8.51049694303866,
											'rotateY': -0.34518781818415534,
											'rotateZ': -0.5066149232561732,
											'space': 3,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': 0.1338166834430723,
											'translateY': -0.900833272212886,
											'translateZ': -4.028923728833506},
		'leg_pv_l_ctrl': {'space': 3,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': -15.354278780539897,
											'translateY': -0.5026205922437015,
											'translateZ': -0.805131196203341},
		'leg_pv_r_ctrl': {'space': 3,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 15.35436913366542,
											'translateY': -0.5026574112253002,
											'translateZ': -0.805739875303594},
		'lowerarm_l_ctrl': {'rotateZ': 38.979},
		'lowerarm_r_ctrl': {'rotateZ': 38.97882194262594},
		'lowerarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'main_ctrl': {'leftArmFkIk': 0.0,
									'leftArmSoftness': 0.0,
									'leftArmTwist': 0.0,
									'leftLegFkIk': 0.0,
									'leftLegSoftness': 0.0,
									'leftLegTwist': 0.0,
									'rightArmFkIk': 0.0,
									'rightArmSoftness': 0.0,
									'rightArmTwist': 0.0,
									'rightLegFkIk': 0.0,
									'rightLegSoftness': 0.0,
									'rightLegTwist': 0.0,
									'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'middle_01_l_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -31.572682017398268},
		'middle_01_r_ctrl': {'rotateX': 0.0,
													'rotateY': 0.0,
													'rotateZ': -31.572682017398254},
		'middle_02_l_ctrl': {'rotateZ': -20.769210477739502},
		'middle_02_r_ctrl': {'rotateZ': -20.769210477739534},
		'middle_03_l_ctrl': {'rotateZ': -9.999999970953382},
		'middle_03_r_ctrl': {'rotateZ': -9.999999970953347},
		'middle_metacarpal_l_ctrl': {'rotateX': 4.274286984138468,
																	'rotateY': -0.042392353339713876,
																	'rotateZ': 2.32168687175845},
		'middle_metacarpal_r_ctrl': {'rotateX': 4.274286984138482,
																	'rotateY': -0.042392353339722015,
																	'rotateZ': 2.321686871758437},
		'neck_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'neck_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pelvis_pos_ctrl': {'space': 1,
												'spaceUseRotate': False,
												'spaceUseTranslate': True,
												'translateX': 0.0,
												'translateY': 0.0,
												'translateZ': 0.0},
		'pelvis_rot_ctrl': {'rotateX': 0.0,
												'rotateY': 0.0,
												'rotateZ': -3.633106949967569},
		'pinky_01_l_ctrl': {'rotateX': -9.999764978819503,
												'rotateY': -3.2478503919206196,
												'rotateZ': -14.49391036970134},
		'pinky_01_r_ctrl': {'rotateX': -9.99976497881951,
												'rotateY': -3.2478503919205357,
												'rotateZ': -14.493910369701373},
		'pinky_02_l_ctrl': {'rotateZ': -21.286999049243878},
		'pinky_02_r_ctrl': {'rotateZ': -21.286999049243864},
		'pinky_03_l_ctrl': {'rotateZ': -4.917000047022328},
		'pinky_03_r_ctrl': {'rotateZ': -4.917000047022351},
		'pinky_metacarpal_l_ctrl': {'rotateX': 25.358336691053736,
																'rotateY': 22.65256043208401,
																'rotateZ': -1.8189991299226913},
		'pinky_metacarpal_r_ctrl': {'rotateX': 25.358336691053765,
																'rotateY': 22.65256043208397,
																'rotateZ': -1.8189991299226989},
		'ring_01_l_ctrl': {'rotateX': -5.633826864079091,
												'rotateY': -3.0348222875822315,
												'rotateZ': -29.271655648140985},
		'ring_01_r_ctrl': {'rotateX': -5.633826864078888,
												'rotateY': -3.034822287582176,
												'rotateZ': -29.271655648140992},
		'ring_02_l_ctrl': {'rotateZ': -18.964},
		'ring_02_r_ctrl': {'rotateZ': -18.963999541971855},
		'ring_03_l_ctrl': {'rotateZ': -9.16799928999681},
		'ring_03_r_ctrl': {'rotateZ': -9.167999748024975},
		'ring_metacarpal_l_ctrl': {'rotateX': 13.886394588293648,
																'rotateY': 11.10967771354835,
																'rotateZ': 4.333313009904817},
		'ring_metacarpal_r_ctrl': {'rotateX': 13.886394588293527,
																'rotateY': 11.10967771354829,
																'rotateZ': 4.333313009904794},
		'root_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'space': 1,
									'spaceUseRotate': True,
									'spaceUseTranslate': True,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'spine_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_03_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_04_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_05_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_l_ctrl': {'rotateX': -8.21464894950556,
											'rotateY': 3.6070921012111743,
											'rotateZ': 3.0712089883091407},
		'thigh_r_ctrl': {'rotateX': -8.214648949505534,
											'rotateY': 3.6070921012111667,
											'rotateZ': 3.0712089883091553},
		'thigh_twist_01_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_01_r_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_r_ctrl': {'rotateX': 0.0},
		'thumb_01_l_ctrl': {'rotateX': -75.42521984002158,
												'rotateY': -30.400067883741357,
												'rotateZ': 33.588918588564255},
		'thumb_01_r_ctrl': {'rotateX': -75.42521984002158,
												'rotateY': -30.400067883741304,
												'rotateZ': 33.58891858856433},
		'thumb_02_l_ctrl': {'rotateZ': -23.318825988464432},
		'thumb_02_r_ctrl': {'rotateZ': -23.31882598846441},
		'thumb_03_l_ctrl': {'rotateZ': -9.999999970953342},
		'thumb_03_r_ctrl': {'rotateZ': -9.999999970953409},
		'upperarm_l_ctrl': {'rotateX': 1.7268422965460892,
												'rotateY': -46.16271195009719,
												'rotateZ': 1.7794386558438777},
		'upperarm_r_ctrl': {'rotateX': 1.726842296546085,
												'rotateY': -46.16271195009719,
												'rotateZ': 1.7794386558438953},
		'upperarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_r_ctrl': {'rotateX': 0.0}
	},
	"aPose": {
		'arm_ik_l_ctrl': {'rotateX': -5.72499842663433e-14,
											'rotateY': 6.361109362927035e-15,
											'rotateZ': 6.3611093629270296e-15,
											'space': 1,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': -7.105427357601002e-15,
											'translateY': 2.842170943040401e-14,
											'translateZ': 8.881784197001252e-15},
		'arm_ik_r_ctrl': {'rotateX': -1.2722218725854073e-14,
											'rotateY': 1.5952469574215454e-14,
											'rotateZ': -1.5455507905236783e-14,
											'space': 1,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': -2.1316282072803006e-14,
											'translateY': -1.4210854715202004e-14,
											'translateZ': 0.0},
		'arm_pv_l_ctrl': {'space': 1,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 7.105427357601002e-15,
											'translateY': 0.0,
											'translateZ': 0.0},
		'arm_pv_r_ctrl': {'space': 1,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 7.105427357601002e-15,
											'translateY': 0.0,
											'translateZ': 0.0},
		'ball_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ball_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'calf_l_ctrl': {'rotateZ': -2.3854160110976395e-12},
		'calf_r_ctrl': {'rotateZ': -3.473165712158161e-12},
		'calf_twist_01_l_ctrl': {'rotateX': 0.0},
		'calf_twist_01_r_ctrl': {'rotateX': 0.0},
		'calf_twist_02_l_ctrl': {'rotateX': 0.0},
		'calf_twist_02_r_ctrl': {'rotateX': 0.0},
		'clavicle_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'clavicle_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'foot_l_ctrl': {'rotateX': -6.679164831073388e-14,
										'rotateY': 1.590277340731759e-14,
										'rotateZ': 6.361109362927026e-15},
		'foot_r_ctrl': {'rotateX': -1.7174995279902987e-13,
										'rotateY': -6.361109362926984e-15,
										'rotateZ': 3.180554681463517e-14},
		'hand_l_ctrl': {'fist': 50.0,
										'rotateX': 6.043053894780683e-14,
										'rotateY': -1.2722218725854062e-14,
										'rotateZ': -1.2722218725854075e-14,
										'spread': 50.0},
		'hand_r_ctrl': {'fist': 50.0,
										'rotateX': 2.544443745170814e-14,
										'rotateY': -1.5703988739726117e-14,
										'rotateZ': -9.988929546471364e-15,
										'spread': 50.0},
		'head_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_02_l_ctrl': {'rotateZ': 0.0},
		'index_02_r_ctrl': {'rotateZ': 0.0},
		'index_03_l_ctrl': {'rotateZ': 0.0},
		'index_03_r_ctrl': {'rotateZ': 0.0},
		'index_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'index_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'leg_ik_l_ctrl': {'rotateX': 5.4069429584879776e-14,
											'rotateY': -1.5902773407317578e-14,
											'rotateZ': -3.180554681463524e-15,
											'space': 3,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': -1.7763568394002505e-15,
											'translateY': -1.1102230246251565e-16,
											'translateZ': -3.552713678800501e-15},
		'leg_ik_r_ctrl': {'rotateX': 1.4948607002878528e-13,
											'rotateY': 6.361109362927084e-15,
											'rotateZ': -3.8166656177562195e-14,
											'space': 3,
											'spaceUseRotate': True,
											'spaceUseTranslate': True,
											'translateX': 1.7763568394002505e-15,
											'translateY': -1.1102230246251565e-16,
											'translateZ': 1.7763568394002505e-15},
		'leg_pv_l_ctrl': {'space': 3,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 0.0,
											'translateY': 0.0,
											'translateZ': 0.0},
		'leg_pv_r_ctrl': {'space': 3,
											'spaceUseRotate': False,
											'spaceUseTranslate': True,
											'translateX': 0.0,
											'translateY': 0.0,
											'translateZ': 0.0},
		'lowerarm_l_ctrl': {'rotateZ': -8.587497639951494e-14},
		'lowerarm_r_ctrl': {'rotateZ': 1.5902773407317587e-14},
		'lowerarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'lowerarm_twist_02_r_ctrl': {'rotateX': 0.0},
		'main_ctrl': {'leftArmFkIk': 0.0,
									'leftArmSoftness': 0.0,
									'leftArmTwist': 0.0,
									'leftLegFkIk': 0.0,
									'leftLegSoftness': 0.0,
									'leftLegTwist': 0.0,
									'rightArmFkIk': 0.0,
									'rightArmSoftness': 0.0,
									'rightArmTwist': 0.0,
									'rightLegFkIk': 0.0,
									'rightLegSoftness': 0.0,
									'rightLegTwist': 0.0,
									'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'middle_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_02_l_ctrl': {'rotateZ': 0.0},
		'middle_02_r_ctrl': {'rotateZ': 0.0},
		'middle_03_l_ctrl': {'rotateZ': 0.0},
		'middle_03_r_ctrl': {'rotateZ': 0.0},
		'middle_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'middle_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'neck_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'neck_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pelvis_pos_ctrl': {'space': 1,
												'spaceUseRotate': False,
												'spaceUseTranslate': True,
												'translateX': 0.0,
												'translateY': 0.0,
												'translateZ': 0.0},
		'pelvis_rot_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_02_l_ctrl': {'rotateZ': 0.0},
		'pinky_02_r_ctrl': {'rotateZ': 0.0},
		'pinky_03_l_ctrl': {'rotateZ': 0.0},
		'pinky_03_r_ctrl': {'rotateZ': 0.0},
		'pinky_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'pinky_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_02_l_ctrl': {'rotateZ': 0.0},
		'ring_02_r_ctrl': {'rotateZ': 0.0},
		'ring_03_l_ctrl': {'rotateZ': 0.0},
		'ring_03_r_ctrl': {'rotateZ': 0.0},
		'ring_metacarpal_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'ring_metacarpal_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'root_ctrl': {'rotateX': 0.0,
									'rotateY': 0.0,
									'rotateZ': 0.0,
									'space': 1,
									'spaceUseRotate': True,
									'spaceUseTranslate': True,
									'translateX': 0.0,
									'translateY': 0.0,
									'translateZ': 0.0},
		'spine_01_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_02_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_03_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_04_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'spine_05_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thigh_l_ctrl': {'rotateX': -8.142219984546653e-13,
											'rotateY': 2.798888119687748e-13,
											'rotateZ': -2.0578188789068976e-12},
		'thigh_r_ctrl': {'rotateX': 1.272221872586125e-14,
											'rotateY': -1.9401383556927406e-13,
											'rotateZ': -4.242859945072331e-12},
		'thigh_twist_01_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_01_r_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_l_ctrl': {'rotateX': 0.0},
		'thigh_twist_02_r_ctrl': {'rotateX': 0.0},
		'thumb_01_l_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_01_r_ctrl': {'rotateX': 0.0, 'rotateY': 0.0, 'rotateZ': 0.0},
		'thumb_02_l_ctrl': {'rotateZ': 0.0},
		'thumb_02_r_ctrl': {'rotateZ': 0.0},
		'thumb_03_l_ctrl': {'rotateZ': 0.0},
		'thumb_03_r_ctrl': {'rotateZ': 0.0},
		'upperarm_l_ctrl': {'rotateX': 6.3611093629270335e-15,
												'rotateY': 9.54166404439055e-15,
												'rotateZ': 3.1805546814635176e-15},
		'upperarm_r_ctrl': {'rotateX': 1.5902773407317584e-14,
												'rotateY': 9.541664044390558e-15,
												'rotateZ': -4.770832022195276e-14},
		'upperarm_twist_01_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_01_r_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_l_ctrl': {'rotateX': 0.0},
		'upperarm_twist_02_r_ctrl': {'rotateX': 0.0}
	}
}



