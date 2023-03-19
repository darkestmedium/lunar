#include "Ik2bSolver.h"


// Public Data
const MString Ik2bSolver::typeName = "ik2bSolver";
const MTypeId Ik2bSolver::typeId = 0x0066674;

// Node's Input Attributes
Attribute Ik2bSolver::inFkStartAttr;
Attribute Ik2bSolver::inFkMidAttr;
Attribute Ik2bSolver::inFkEndAttr;
Attribute Ik2bSolver::inIkHandleAttr;
// Attribute Ik2bSolver::inPoleVectorAttr;
MObject Ik2bSolver::inPoleVectorAttr;
Attribute Ik2bSolver::inTwistAttr;
MObject Ik2bSolver::inSoftnessAttr;
MObject Ik2bSolver::inFkIkAttr;
MObject Ik2bSolver::AttrInTime;
// Nodes's Output Attributes
Attribute Ik2bSolver::AttrOutUpdateX;
Attribute Ik2bSolver::AttrOutUpdateY;
Attribute Ik2bSolver::AttrOutUpdateZ;
Attribute Ik2bSolver::AttrOutUpdate;


MStatus Ik2bSolver::initialize() {
	/* Node Initializer.
	 *
	 * This method initializes the node, and should be overridden in user-defined nodes.
	 * 
	 * Returns:
	 *	status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
	 *		during the operation
	 *
	 */
	MStatus status;
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;

	// Node's Input Attributes
	createAttribute(inFkStartAttr, "fkStart", DefaultValue<MMatrix>());
	createAttribute(inFkMidAttr, "fkMid", DefaultValue<MMatrix>());
	createAttribute(inFkEndAttr, "fkEnd", DefaultValue<MMatrix>());
	createAttribute(inIkHandleAttr, "ikHandle", DefaultValue<MMatrix>());
	inPoleVectorAttr = nAttr.createPoint("poleVector", "pv");

	createAttribute(inTwistAttr, "twist", DefaultValue<MAngle>());

	inSoftnessAttr = nAttr.create("softness", "sfns", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(10.0);

	inFkIkAttr = nAttr.create("fkIk", "fkik", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	uAttr.setReadable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(100.0);

	AttrInTime = uAttr.create("inTime", "itm", MFnUnitAttribute::kTime);
	uAttr.setKeyable(true);
	uAttr.setReadable(false);

	// Output attributes
	AttrOutUpdateX = nAttr.create("updateX", "updX", MFnNumericData::kDouble, 0.0);
	AttrOutUpdateY = nAttr.create("updateY", "updY", MFnNumericData::kDouble, 0.0);
	AttrOutUpdateZ = nAttr.create("updateZ", "updZ", MFnNumericData::kDouble, 0.0);
	AttrOutUpdate = nAttr.create("update", "upd", AttrOutUpdateX, AttrOutUpdateY, AttrOutUpdateZ);

	// Add attributes
	addAttributes(
		inFkStartAttr, inFkMidAttr,	inFkEndAttr,
		inIkHandleAttr,	inPoleVectorAttr,
		inTwistAttr, inSoftnessAttr, inFkIkAttr,
		AttrInTime,
		AttrOutUpdate
	);

	return MS::kSuccess;
}


bool Ik2bSolver::isPassiveOutput(const MPlug& plug) const {
	/* Sets the specified plug as passive.

	This method may be overridden by the user defined node if it wants to provide output attributes
	which do not prevent value modifications to the destination attribute.

	For example, output plugs on animation curve nodes are passive. This allows the attributes
	driven by the animation curves to be set to new values by the user.
	
	Args:
		plug (MPlug&): Plug representing output in question.

	Returns:
		bool: Wheter or not he specified plug is passive - true indicates passive.

	*/
	if (plug == AttrOutUpdate) {
		return true;
	}
	return MPxNode::isPassiveOutput(plug);
}


double Ik2bSolver::softenEdge(double hardEdge, double chainLength, double dsoft) {
  double da = chainLength - dsoft;
  double softEdge = da + dsoft * (1.0 - std::exp((da-hardEdge)/dsoft));
  return (hardEdge > da && da > 0.0) ? softEdge : hardEdge;
}


double Ik2bSolver::softenIk(double lenAT, double lenAB, double lenCB, double lenABC, double softness) {
	// Wrapper method for softhening the ik solve
	lenAT = std::max(lenAT, lenAB - lenCB);
	return softenEdge(lenAT, lenABC, softness);
}


MStatus Ik2bSolver::parseDataBlock(MDataBlock& dataBlock, MDagPathArray& InOutLinks) {
	/* Parse the data block and get all inputs.
	 *
	 * We're getting the mObj from the .attribute() instead of a numeric data type like double in
	 * order to retrieve the MFnTransform for the input controllers - this also triggers the input as
	 * dirty. All of Maya's solvers get the world position from the .rotatePivot() method.
	 * 
	 */
	MStatus status;

	// Ask for time value to force refresh on the node
	timeCurrent = dataBlock.inputValue(AttrInTime, &status).asTime();
	// Asking for the actuall matrix input helps refreshing the rig if there are no anim curves
	matInFkStart = dataBlock.inputValue(inFkStartAttr).asMatrix();
	matInFkMid = dataBlock.inputValue(inFkMidAttr).asMatrix();
	matInFkEnd = dataBlock.inputValue(inFkEndAttr).asMatrix();
	matInIkHandle = dataBlock.inputValue(inIkHandleAttr).asMatrix();
	posInPoleVector = dataBlock.inputValue(inPoleVectorAttr).asVector();

	// Start fk controller
	MDagPath pathFkStart;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(SelfObj, dataBlock.inputValue(inFkStartAttr).attribute()), pathFkStart);
	if (status == MS::kSuccess) {
		FnFkStart.setObject(pathFkStart);
	} else {
		return MS::kFailure;
	}
	// Mid fk controller
	MDagPath pathFkMid;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(SelfObj, dataBlock.inputValue(inFkMidAttr).attribute()), pathFkMid);
	if (status == MS::kSuccess) {
		FnFkMid.setObject(pathFkMid);
	} else {
		return MS::kFailure;
	}
	// End fk controller
	MDagPath pathFkEnd;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(SelfObj, dataBlock.inputValue(inFkEndAttr).attribute()), pathFkEnd);
	if (status == MS::kSuccess) {
		FnFkEnd.setObject(pathFkEnd);
	} else {
		return MS::kFailure;
	}
	// Ik handle
	MDagPath pathIkHandle;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(SelfObj, dataBlock.inputValue(inIkHandleAttr).attribute()), pathIkHandle);
	if (status == MS::kSuccess) {
		FnIkHandle.setObject(pathIkHandle);
	} else {
		return MS::kFailure;
	}
	// Pole vector
	MDagPath pathPoleVector;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(SelfObj, dataBlock.inputValue(inPoleVectorAttr).attribute()), pathPoleVector);
	if (status == MS::kSuccess) {
		FnPoleVector.setObject(pathPoleVector);
		bIsPoleVectorConnected = true;
	} else {
		FnPoleVector.setObject(MObject::kNullObj);
		bIsPoleVectorConnected = false;
	}

	// Additional attributes
	twist = dataBlock.inputValue(inTwistAttr).asDouble();
	softness = dataBlock.inputValue(inSoftnessAttr).asDouble();
	fkIk = dataBlock.inputValue(inFkIkAttr).asDouble();

	InOutLinks.append(pathFkStart);
	InOutLinks.append(pathFkMid);
	InOutLinks.append(pathFkEnd);
	InOutLinks.append(pathIkHandle);
	InOutLinks.append(pathPoleVector);

	// LimbLength = GetLimbLength();

	return MS::kSuccess;
}


double Ik2bSolver::GetLimbLength() {
	/* Calculates the limb length. */
	MPoint pFkStart = (FnFkStart.rotatePivot(MSpace::kWorld));
	MPoint pFkMid = (FnFkMid.rotatePivot(MSpace::kWorld));
	MPoint pFkEnd = (FnFkEnd.rotatePivot(MSpace::kWorld));

	return pFkStart.distanceTo(pFkMid) + pFkMid.distanceTo(pFkEnd);
}


void Ik2bSolver::GetFkTransforms() {
	// Position
	PosFkStart = FnFkStart.rotatePivot(MSpace::kWorld);
	PosFkMid = FnFkMid.rotatePivot(MSpace::kWorld);
	PosFkEnd = FnFkEnd.rotatePivot(MSpace::kWorld);
	PosFkHandle = PosFkEnd;
	if (bIsPoleVectorConnected) {PosFkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);}
	else {PosFkPoleVector = posInPoleVector;}

	// Rotations
	FnFkStart.getRotation(QuatFkStart, MSpace::kWorld);
	FnFkMid.getRotation(QuatFkMid, MSpace::kWorld);
	FnFkEnd.getRotation(QuatFkEnd, MSpace::kWorld);

	// Init ik quats to get vectors and orients etc to prevent pops and flips on the ik
	QuatIkStart = QuatFkStart;
	QuatIkMid = QuatFkMid;
	QuatIkEnd = QuatFkEnd;
}


void Ik2bSolver::GetIkTransforms() {
	// Position
	PosIkHandle = FnIkHandle.rotatePivot(MSpace::kWorld);

	if (bIsPoleVectorConnected) {PosIkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);}
	else {PosIkPoleVector = posInPoleVector;}
	// PosIkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);
	FnIkHandle.getRotation(QuatIkEnd, MSpace::kWorld);
}


void Ik2bSolver::BlendFkIk() {
	// because we wantto use 0 - 100 in the channel box, yeah i know :|
	double ScaledWeight = fkIk * 0.01;

	QuatOutStart = slerp(QuatFkStart, QuatIkStart, ScaledWeight);
	QuatOutMid = slerp(QuatFkMid, QuatIkMid, ScaledWeight);
	QuatOutEnd = slerp(QuatFkEnd, QuatIkEnd, ScaledWeight);
	QuatOutHandle = slerp(QuatFkEnd, QuatIkHandle, ScaledWeight);
	// so this still is an issue since it's a bit off from the fk end ctrl pos, maybe we just snap to it
	PosOutHandle = Lerp(PosFkHandle, PosIkHandle, ScaledWeight);
	PosOutPoleVector = Lerp(PosFkPoleVector, PosIkPoleVector, ScaledWeight);
}


MStatus Ik2bSolver::solve(MDagPathArray& InOutLinks) {
	/* */
	MStatus status;

	GetFkTransforms();
	GetIkTransforms();

	solveLimb(InOutLinks);

	// Cache time change
	timeCached = timeCurrent;

	return MS::kSuccess;
}


bool Ik2bSolver::solveLimb(MDagPathArray& InOutLinks) {
	/* Solves the limb. 

	Main fk / ik routing method. 

	TODO:
		Rework routing, we need to always solve and extract / isolate the editing mode.

	Args:
		InOutLinks (MDagPathArray&): Array with path to the input transforms.

	*/
	// Editing
	if (!LMAnimControl::timeChanged(ctrlAnim, timeCached, timeCurrent)) {
		if (LMGLobal::currentToolIsTransformContext()) {
			MGlobal::getActiveSelectionList(listSel);
			// 1 If selection has fk solve fk
			if (listSel.hasItem(InOutLinks[0]) || listSel.hasItem(InOutLinks[1]) || listSel.hasItem(InOutLinks[2])) {
				SolveFk();
			} else {
				SolveIk();
			}
			return true;
		}
	}
	// Solve for playback and all other possible cases - just solve something
	if (fkIk == 0.0) {
		SolveFk();
	}	else if (fkIk > 0.0 && fkIk < 100.0) {
		SolveBlendedIk();
	} else if (fkIk == 100.0) {
		SolveIk();
	}
	return true;
}


void Ik2bSolver::SolveFk() {
	/* Set the fk transforms.

	We don't actually solve fk - it's called like this just for consistency and readability.
	The isEditing flag is reserved for editing the fk transforms where we move the pole vector by
	a constant distance (limb length) calculated from the mid transform. 

	*/
	if (bIsPoleVectorConnected) {
		FnPoleVector.setTranslation(LMRigUtils::getPoleVectorPosition(PosFkStart, PosFkMid, PosFkEnd), MSpace::kWorld);
	}

	// Set ik transforms
	FnIkHandle.setTranslation(PosFkHandle, MSpace::kWorld);
	FnIkHandle.setRotation(QuatFkEnd, MSpace::kWorld);
}


void Ik2bSolver::SolveBlendedIk() {
	/* So kind of does what the name says but not really.
	*/
	MStatus status;

	solveTwoBoneIk();

	BlendFkIk();

	// Set rotations
	FnFkStart.setRotation(QuatOutStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatOutMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatOutEnd, MSpace::kWorld);
	FnIkHandle.setRotation(QuatOutHandle, MSpace::kWorld);

	// Sync the ik ctrl to the fk end bone due to differences in fk / ik blending
	FnIkHandle.setTranslation(PosOutHandle, MSpace::kWorld);
	FnPoleVector.setTranslation(PosOutPoleVector, MSpace::kWorld);
}


void Ik2bSolver::SolveIk() {
	// Neat optimization though i couldn't get the single joint solve to work properley without flips
	solveTwoBoneIk();

	// Get chain length
	// GetLimbLength();

	// if (RootTargetDistance >= LimbLength) {
	// 	SolveStraightLimb();
	// } else {
	// 	solveTwoBoneIk();
	// }

	// Set fk rotations
	FnFkStart.setRotation(QuatIkStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatIkMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatIkEnd, MSpace::kWorld);
}


void Ik2bSolver::SolveStraightLimb() {
	MVector FkEndLocation = FnFkEnd.rotatePivot(MSpace::kWorld);
	MVector FkMidLocation = FnFkMid.rotatePivot(MSpace::kWorld);
	MVector FkStartLocation = FnFkStart.rotatePivot(MSpace::kWorld);
	MVector IkHandleLocation = FnIkHandle.rotatePivot(MSpace::kWorld);
	MVector PoleVectorLocation = FnPoleVector.rotatePivot(MSpace::kWorld);

	MVector PoleVector = makeNonZero(PoleVectorLocation - FkStartLocation).normal();
	MVector Direction = makeNonZero(IkHandleLocation - FkStartLocation).normal();

	// compute cross products
	// MVector dir = (PosFkMid - (PosFkStart + (ac * ((vecAB) * ac)))).normal();

	MVector Cross = Direction ^ PoleVector;
	MVector UpVector = Cross ^ Direction;

	double ArrayRotation[4][4] = {
		{Direction.x, Direction.y, Direction.z, 0},
		{UpVector.x, UpVector.y, UpVector.z, 0}, 
		{Cross.x, Cross.y, Cross.z, 0}, 
		{FkStartLocation.x, FkStartLocation.y, FkStartLocation.z, 1}
	};
	const MMatrix MatrixRotation(ArrayRotation);
	MTransformationMatrix FnMatrixRotation(MatrixRotation);

	QuatIkStart = FnMatrixRotation.rotation();

	MQuaternion QuatTwist(twist, Direction);

	QuatIkStart *= QuatTwist;

	QuatIkMid *= QuatIkStart;

	FnIkHandle.getRotation(QuatIkEnd, MSpace::kWorld);

	FnFkStart.setRotation(QuatIkStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatIkMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatIkEnd, MSpace::kWorld);
}


void Ik2bSolver::solveTwoBoneIk() {
	/* Calculates the ik for a two bone limb.
	
	Reference:
		https://github.com/chadmv/cmt/blob/master/src/ikRigNode.cpp
		https://theorangeduck.com/page/simple-two-joint

	*/
	MStatus status;

	// GetIkTransforms();

	// Position vectors
	MVector vecA = PosFkStart;
	MVector vecB = PosFkMid;
	MVector vecC = PosFkEnd;
	MVector vecT = PosIkHandle;
	MVector vecPv = PosFkPoleVector;
	// From to Vectors - reusable
	MVector vecAB = vecB - vecA;
	MVector vecAC = vecC - vecA;
	MVector vecAT = vecT - vecA;
	// Direction vector
	MVector vecD = (vecB - (vecA + (vecAC * (vecAB * vecAC)))).normal();
	// Lengths
	double lenAB = vecAB.length();
	double lenCB = (vecB - vecC).length();
	double lenABC = lenAB + lenCB;
	double lenAT = clamp(vecAT.length(), kEpsilon, lenABC - kEpsilon);

	// Soften the edge if required
	if (softness > 0.0) {lenAT = softenIk(lenAT, lenAB, lenCB, lenABC, softness);}

	// Get current interior angles of start and mid
	double ac_ab_0 = acos(clamp((vecAC).normal() * (vecAB).normal(), -1.0, 1.0));
	double ba_bc_0 = acos(clamp((vecA - vecB).normal() * (vecC - vecB).normal(), -1.0, 1.0));
	double ac_at_0 = acos(clamp((vecAC).normal() * (vecAT).normal(), -1.0, 1.0));
	// Get desired interior angles
	double ac_ab_1 = acos(clamp((lenCB * lenCB - lenAB * lenAB - lenAT * lenAT) / (-2 * lenAB * lenAT), -1.0, 1.0));
	double ba_bc_1 = acos(clamp((lenAT * lenAT - lenAB * lenAB - lenCB * lenCB) / (-2 * lenAB * lenCB), -1.0, 1.0));

	MVector axis0 = (vecAC ^ vecD).normal();
	MVector axis1 = (vecAC ^ vecAT).normal();

	MQuaternion r0(ac_ab_1 - ac_ab_0, axis0);
	MQuaternion r1(ba_bc_1 - ba_bc_0, axis0);
	MQuaternion r2(ac_at_0, axis1);

	// Pole vector rotation
  // Determine the rotation used to rotate the normal of the triangle formed by
  // a.b.c post r0*r2 rotation to the normal of the triangle formed by triangle a.pv.t
	MVector n1 = (vecAC ^ vecAB).normal().rotateBy(r0).rotateBy(r2);
	MVector n2 = (vecAT ^ (vecPv - vecA)).normal();
	MQuaternion r3 = n1.rotateTo(n2);
	
	// Rotation cross vectors and twist
	MQuaternion quatTwist(twist, vecAT);

	// Start rotation
	QuatIkStart *= r0 * r2 * r3 * quatTwist;
	
	// Mid rotation
	// QuatIkMid *= r1;
	QuatIkMid *= r1 * r0 * r2 * r3 * quatTwist;

}


MStatus Ik2bSolver::updateOutput(const MPlug& plug, MDataBlock& dataBlock) {	
	/* Sets the outputs and data block clean.

	Args:
		plug (MPlug&): Plug representing the attribute that needs to be recomputed.
		dataBlock (MDataBlock&): Data block containing storage for the node's attributes.

	Returns:
		status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
			during the operation.

	*/
	MStatus status;

	MDataHandle dhOutUpdate = dataBlock.outputValue(AttrOutUpdate, &status);
	dhOutUpdate.set3Double(0.0, 0.0, 0.0);
	dhOutUpdate.setClean();

	dataBlock.setClean(plug);

	return MS::kSuccess;
}


MStatus Ik2bSolver::compute(const MPlug& plug, MDataBlock& dataBlock) {
	/* This method should be overridden in user defined nodes.

	Recompute the given output based on the nodes inputs. The plug represents the data
	value that needs to be recomputed, and the data block holds the storage for all of
	the node's attributes.

	The MDataBlock will provide smart handles for reading and writing this node's
	attribute values. Only these values should be used when performing computations.

	When evaluating the dependency graph, Maya will first call the compute method for
	this node. If the plug that is provided to the compute indicates that the attribute
	was defined by the Maya parent node, the compute method should return
	MS::kUnknownParameter. When this occurs, Maya will call the internal Maya node from
	which the user-defined node is derived to compute the plug's value.

	This means that a user defined node does not need to be concerned with computing
	inherited output attributes. However, if desired, these can be safely recomputed by
	this method to change the behaviour of the node.

	Args:
		plug (MPlug&): Plug representing the attribute that needs to be recomputed.
		dataBlock (MDataBlock&): Data block containing storage for the node's attributes.

	Returns:
		status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
			during the operation.

	*/
	MStatus status;

	// Check if all inputs are connected and parse the data block
	MDagPathArray InOutLinks;
	status = parseDataBlock(dataBlock, InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Solve the limb
	status = solve(InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Set the output and data block clean
	status = updateOutput(plug, dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}


MStatus Ik2bSolver::setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) {
	/* Sets the relation between attributes and marks the specified plugs dirty.

	Args:
		plugBeingDirtied (&MPlug): Plug which is being set dirty by Maya.
		affectedPlugs (&MPlugArray): The programmer should add any plugs which they want to set dirty
			to this list.

	*/
	if ( plugBeingDirtied == inFkEndAttr
		|| plugBeingDirtied == inFkMidAttr
		|| plugBeingDirtied == inFkStartAttr
		|| plugBeingDirtied == inIkHandleAttr
		|| plugBeingDirtied == inPoleVectorAttr
		|| plugBeingDirtied == inTwistAttr
		|| plugBeingDirtied == inSoftnessAttr
		|| plugBeingDirtied == inFkIkAttr
		|| plugBeingDirtied == AttrInTime
	)	{
		affectedPlugs.append(MPlug(SelfObj, AttrOutUpdate));
	}

	return MS::kSuccess;
}


void Ik2bSolver::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const {
	/* Disables Cached Playback support by default.

	Built-in locators all enable Cached Playback by default, but plug-ins have to
	explicitly enable it by overriding this method.
	This method should be overridden to enable Cached Playback by default for custom locators.

	Args:
		evalNode (MEvaluationNode&): This node's evaluation node, contains animated plug information
		disablingInfo (MNodeCacheDisablingInfo&): Information about why the node disables caching to be reported to the user
		cacheSetup (MNodeCacheSetupInfo&): Preferences and requirements this node has for caching
		monitoredAttribures (MObjectArray&): Attributes impacting the behavior of this method that will be monitored for change

	*/
	MPxNode::getCacheSetup(evalNode, disablingInfo, cacheSetupInfo, monitoredAttributes);
	assert(!disablingInfo.getCacheDisabled());
	cacheSetupInfo.setPreference(MNodeCacheSetupInfo::kWantToCacheByDefault, true);
}


void Ik2bSolver::postConstructor() {
	/* Post constructor.

	Internally maya creates two objects when a user defined node is created, the internal MObject and
	the user derived object. The association between the these two objects is not made until after the
	MPxNode constructor is called. This implies that no MPxNode member function can be called from the
	MPxNode constructor. The postConstructor will get called immediately after the constructor when it
	is safe to call any MPxNode member function.

	Reimplemented in MPxTransform, and MPxPolyTrg.

	*/
	SelfObj = thisMObject();
}
