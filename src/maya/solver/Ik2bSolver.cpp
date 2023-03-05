#include "Ik2bSolver.h"


// Public Data
const MString Ik2bSolver::typeName = "ik2bSolver";
const MTypeId Ik2bSolver::typeId = 0x0066674;

// Node's Input Attributes
Attribute Ik2bSolver::inFkStartAttr;
Attribute Ik2bSolver::inFkMidAttr;
Attribute Ik2bSolver::inFkEndAttr;
Attribute Ik2bSolver::inIkHandleAttr;
Attribute Ik2bSolver::inPoleVectorAttr;
Attribute Ik2bSolver::inTwistAttr;
MObject Ik2bSolver::inSoftnessAttr;
MObject Ik2bSolver::inFkIkAttr;
MObject Ik2bSolver::AttrInTime;
// Nodes's Output Attributes
Attribute Ik2bSolver::AttrOutUpdateX;
Attribute Ik2bSolver::AttrOutUpdateY;
Attribute Ik2bSolver::AttrOutUpdateZ;
Attribute Ik2bSolver::AttrOutUpdate;


MStatus Ik2bSolver::initialize() 
{
	/* Node Initializer.

	This method initializes the node, and should be overridden in user-defined nodes.

	Returns:
	status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
		during the operation

	*/
	MStatus status;
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;
	// MFnCompoundAttribute cAttr;

	// Node's Input Attributes
	createAttribute(inFkStartAttr, "fkStart", DefaultValue<MMatrix>());
	createAttribute(inFkMidAttr, "fkMid", DefaultValue<MMatrix>());
	createAttribute(inFkEndAttr, "fkEnd", DefaultValue<MMatrix>());
	createAttribute(inIkHandleAttr, "ikHandle", DefaultValue<MMatrix>());
	createAttribute(inPoleVectorAttr, "poleVector", DefaultValue<MMatrix>());
	createAttribute(inTwistAttr, "twist", DefaultValue<MAngle>());

	inSoftnessAttr = nAttr.create("softness", "sfns", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(10.0);

	inFkIkAttr = nAttr.create("fkIk", "fki", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
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


bool Ik2bSolver::isPassiveOutput(const MPlug& plug) const
{
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
	if (plug == AttrOutUpdate)
	{
		return true;
	}
	return MPxNode::isPassiveOutput(plug);
}


MObject Ik2bSolver::getSourceObjFromPlug(const MObject& Object, const MObject& Plug)
{
	/* Gets the object from the given plug if it is connected.

	Args:
		Plug (MObject&): Object for the given plug.
	
	Returns:
		MObject: If the plug is a valid connection it will return the obj, otherwise a null object will
			be returned instead.

	*/
	MPlug PlugDestination(Object, Plug);
	if (PlugDestination.isConnected())
	{
		return PlugDestination.source().node();
	}
	return MObject::kNullObj;
}


double Ik2bSolver::softenEdge(double hardEdge, double chainLength, double dsoft)
{
  double da = chainLength - dsoft;
  double softEdge = da + dsoft * (1.0 - std::exp((da-hardEdge)/dsoft));
  return (hardEdge > da && da > 0.0) ? softEdge : hardEdge;
}


double Ik2bSolver::softenIk(double startIkLen, double startMidLen, double midEndLen, double startMidEndLen, double softness)
{
	// Wrapper method for softhening the ik solve

	startIkLen = std::max(startIkLen, startMidLen - midEndLen);

	return softenEdge(startIkLen, startMidEndLen, softness);
}


MStatus Ik2bSolver::ParseDataBlock(MDataBlock& DataBlock, MDagPathArray& InOutLinks)
{
	/* Parse the data block and get all inputs.	*/
	MStatus status;

	// TODO:
	// 	Add error checking - we need at least four inputs

	// Ask for time value to force refresh on the node
	TimeCurrent = DataBlock.inputValue(AttrInTime, &status).asTime();

	// We're getting the mObj from the .attribute() instead of a numeric data type like double in
	// order to retrieve the MFnTransform for the input controllers - this also triggers the input as
	//  dirty. All of Maya's solvers get the world position from the .rotatePivot() method.
	// Start fk controller
	MDagPath PathFkStart;
	__dp.getAPathTo(getSourceObjFromPlug(SelfObj, DataBlock.inputValue(inFkStartAttr).attribute()), PathFkStart);
	FnFkStart.setObject(PathFkStart);
	// Mid fk controller
	MDagPath PathFkMid;
	__dp.getAPathTo(getSourceObjFromPlug(SelfObj, DataBlock.inputValue(inFkMidAttr).attribute()), PathFkMid);
	FnFkMid.setObject(PathFkMid);
	// End fk controller
	MDagPath PathFkEnd;
	__dp.getAPathTo(getSourceObjFromPlug(SelfObj, DataBlock.inputValue(inFkEndAttr).attribute()), PathFkEnd);
	FnFkEnd.setObject(PathFkEnd);
	// Ik handle
	MDagPath PathIkHandle;
	__dp.getAPathTo(getSourceObjFromPlug(SelfObj, DataBlock.inputValue(inIkHandleAttr).attribute()), PathIkHandle);
	FnIkHandle.setObject(PathIkHandle);
	// Pole vector
	MDagPath PathPoleVector;
	__dp.getAPathTo(getSourceObjFromPlug(SelfObj, DataBlock.inputValue(inPoleVectorAttr).attribute()), PathPoleVector);
	FnPoleVector.setObject(PathPoleVector);

	// MDagPathArray InOutLinks;
	InOutLinks.append(PathFkStart);		// Hip / Root
	InOutLinks.append(PathFkMid);			// Knee
	InOutLinks.append(PathFkEnd);			// Foot
	InOutLinks.append(PathIkHandle);
	InOutLinks.append(PathPoleVector);

	// Additional attributes
	twist = DataBlock.inputValue(inTwistAttr).asDouble();
	softness = DataBlock.inputValue(inSoftnessAttr).asDouble();
	fkIk = DataBlock.inputValue(inFkIkAttr).asDouble();

	LimbLength = GetLimbLength();

	return MS::kSuccess;
}


double Ik2bSolver::GetLimbLength()
{
	/* Calculates the limb length. */
	MPoint pFkStart = (FnFkStart.rotatePivot(MSpace::kWorld));
	MPoint pFkMid = (FnFkMid.rotatePivot(MSpace::kWorld));
	MPoint pFkEnd = (FnFkEnd.rotatePivot(MSpace::kWorld));

	return pFkStart.distanceTo(pFkMid) + pFkMid.distanceTo(pFkEnd);
}


void Ik2bSolver::GetFkTransforms()
{
	// Position
	PosFkStart = FnFkStart.rotatePivot(MSpace::kWorld);
	PosFkMid = FnFkMid.rotatePivot(MSpace::kWorld);
	PosFkEnd = FnFkEnd.rotatePivot(MSpace::kWorld);
	PosFkHandle = PosFkEnd;
	PosFkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);

	// Rotations
	FnFkStart.getRotation(QuatFkStart, MSpace::kWorld);
	FnFkMid.getRotation(QuatFkMid, MSpace::kWorld);
	FnFkEnd.getRotation(QuatFkEnd, MSpace::kWorld);

	// Init ik quats to get vectors and orients etc to prevent pops and flips on the ik
	QuatIkStart = QuatFkStart;
	QuatIkMid = QuatFkMid;
	QuatIkEnd = QuatFkEnd;
}


void Ik2bSolver::GetIkTransforms()
{
	// Position
	PosIkHandle = FnIkHandle.rotatePivot(MSpace::kWorld);
	PosIkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);
}


MVector Ik2bSolver::GetPoleVectorPosition(MVector& PosStart, MVector& PosMid, MVector& PosEnd)
{
	/* Calculates the perfect pole vector position for ik solving.

	From Greg's Hendrix tutorial https://www.youtube.com/watch?v=bB_HL1tBVHY

	*/
	MVector VecStartEnd(PosEnd - PosStart);
	MVector VecMidEnd(PosEnd - PosMid);

	double ValScale = (VecStartEnd * VecMidEnd) / (VecStartEnd * VecStartEnd);
	MVector VecProjection = (VecStartEnd * ValScale) + PosStart;
	double LenLimb = (PosMid - PosStart).length() + VecMidEnd.length();

	return (PosMid - VecProjection).normal() * LenLimb + PosMid;
}


void Ik2bSolver::BlendFkIk()
{
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


bool Ik2bSolver::TimeChanged(MAnimControl& AnimCtrl, MTime& TimeCached, MTime& TimeCurrent)
{
	/* Checks wheter or not time has changed.

	Playback / scrubbing / time change
	if (AnimCtrl.isPlaying() or AnimCtrl.isScrubbing() or TimeCached != TimeCurrent)

	Args:
		AnimCtrl (MAnimControl&): Animation control instance to check isPlaying and isSrubbing.
		TimeCached (MTimge&): Time that has been cached - ex. previous frame.
		TimeCurrent (MTimge&): Current time / frame.

	Return:
		bool: True if time has changed, false if it didn't.

	*/
	if (AnimCtrl.isPlaying() || AnimCtrl.isScrubbing() || TimeCached != TimeCurrent)
	{
		return true;
	}

	return false;
}


MStatus Ik2bSolver::Solve(MDagPathArray& InOutLinks)
{
	/* */
	MStatus status;

	GetFkTransforms();

	SolveLimb(InOutLinks);

	// Cache time change
	TimeCached = TimeCurrent;

	return MS::kSuccess;
}


bool Ik2bSolver::SolveLimb(MDagPathArray& InOutLinks)
{
	/* Solves the limb. 

	Main fk / ik routing method.

	Args:
		InOutLinks (MDagPathArray&): Array with path to the input transforms.

	*/
	if (TimeChanged(AnimCtrl, TimeCached, TimeCurrent))	{
		// Solve for playback and all other possible cases - just solve something
		if (fkIk == 0.0) {
			SolveFk();
		}
		if (fkIk > 0.0 && fkIk < 100.0) {
			SolveBlendedIk();
		}
		if (fkIk == 100.0) {
			SolveIk();
		}
	}	else {
		// Editing
		MGlobal::getActiveSelectionList(__selList);
		if (__selList.hasItem(InOutLinks[3]) || __selList.hasItem(InOutLinks[4])) {
			SolveIk();
		}	else {
			SolveFk();
		}
	}
	return true;
}


void Ik2bSolver::SolveFk()
{
	/* Set the fk transforms.

	We don't actually solve fk - it's called like this just for consistency and readability.
	The isEditing flag is reserved for editing the fk transforms where we move the pole vector by
	a constant distance (limb length) calculated from the mid transform. 

	*/
	FnPoleVector.setTranslation(GetPoleVectorPosition(PosFkStart, PosFkMid, PosFkEnd), MSpace::kWorld);

	// Set ik transforms
	FnIkHandle.setTranslation(PosFkHandle, MSpace::kWorld);
	FnIkHandle.setRotation(QuatFkEnd, MSpace::kWorld);
}


void Ik2bSolver::SolveBlendedIk()
{
	/* So kind of does what the name says but not really.
	*/
	MStatus status;

	SolveTwoBoneIk();

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


void Ik2bSolver::SolveIk()
{

	// Neat optimization though i couldn't get the single joint solve to work properley without flips
	SolveTwoBoneIk();

	// Get chain length
	// GetLimbLength();

	// if (RootTargetDistance >= LimbLength)
	// {
	// 	SolveStraightLimb();
	// }
	// else
	// {
	// 	SolveTwoBoneIk();
	// }

	// Set fk rotations
	FnFkStart.setRotation(QuatIkStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatIkMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatIkEnd, MSpace::kWorld);
}


void Ik2bSolver::SolveStraightLimb()
{
	MVector FkEndLocation = FnFkEnd.rotatePivot(MSpace::kWorld);
	MVector FkMidLocation = FnFkMid.rotatePivot(MSpace::kWorld);
	MVector FkStartLocation = FnFkStart.rotatePivot(MSpace::kWorld);
	MVector IkHandleLocation = FnIkHandle.rotatePivot(MSpace::kWorld);
	MVector PoleVectorLocation = FnPoleVector.rotatePivot(MSpace::kWorld);

	MVector PoleVector = makeNonZero(PoleVectorLocation - FkStartLocation).normal();
	MVector Direction = makeNonZero(IkHandleLocation - FkStartLocation).normal();

	// compute cross products
	// MVector dir = (PosFkMid - (PosFkStart + (ac * ((startMidVec) * ac)))).normal();

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


void Ik2bSolver::SolveTwoBoneIk()
	// CHAD VERNON BASE
	// https://theorangeduck.com/page/simple-two-joint
{
	MStatus status;

	GetIkTransforms();

	// makeNonZero approach would rather be for testing,
	// Vector from start to mid fk
	MVector startMidVec = makeNonZero(PosFkMid - PosFkStart);
	// Vector from mid to end fk
	MVector midEndVec = makeNonZero(PosFkMid - PosFkEnd);
	// Vector from start to ik handle
	MVector startIkVec = makeNonZero(PosIkHandle - PosFkStart);
	// Pole vector - vector
	MVector poleVectorVec = makeNonZero(PosFkPoleVector - PosFkStart);

	MVector startEndVec = makeNonZero(PosFkEnd - PosFkStart);
	MVector midStartVec = makeNonZero(PosFkStart - PosFkMid);
	MVector endMidVec = makeNonZero(PosFkEnd - PosFkMid);

	// Lengths
	double startMidLen = startMidVec.length();
	double midEndLen = midEndVec.length();
	double startIkLen = startIkVec.length();
	double limbLength = startMidLen + midEndLen;
	
	double eps = 0.0001;
	

	// Soften the edge if required
	if (softness > 0.0) {startIkLen = softenIk(startIkLen, startMidLen, midEndLen, limbLength, softness);}


	double ac_ab_0 = acos(clamp((startEndVec).normal() * (startMidVec).normal(), -1.0, 1.0));
	double ba_bc_0 = acos(clamp((midStartVec).normal() * (endMidVec).normal(), -1.0, 1.0));
	double ac_at_0 = acos(clamp((startEndVec).normal() * (startIkVec).normal(), -1.0, 1.0));

	//midEndLen -> lcb
	//startMidLen -> lab
	//startIkLen - > lat
	double lat = clamp(startIkLen, eps, limbLength - eps);
	
	double ac_ab_1 = acos(clamp((midEndLen * midEndLen - startMidLen * startMidLen - lat * lat) / (-2 * startMidLen * lat), -1.0, 1.0));
	double ba_bc_1 = acos(clamp((lat * lat - startMidLen * startMidLen - midEndLen * midEndLen) / (-2 * startMidLen * midEndLen), -1.0, 1.0));
	

	MVector ac = (startEndVec).normal();
	
	MVector d = (PosFkMid - (PosFkStart + (ac * ((startMidVec) * ac)))).normal();

	MVector axis0 = ((startEndVec) ^ d).normal();
	MVector axis1 = (startEndVec ^ startIkVec).normal();

	MQuaternion r0(ac_ab_1 - ac_ab_0, axis0);
	MQuaternion r1(ba_bc_1 - ba_bc_0, axis0);
	MQuaternion r2(ac_at_0, axis1);

	MVector n1 = ((startEndVec) ^ (startMidVec)).normal().rotateBy(r0).rotateBy(r2);
	MVector n2 = ((startIkVec) ^ (poleVectorVec)).normal();
	MQuaternion r3 = n1.rotateTo(n2);
	
	// Rotation cross vectors and twist
	MQuaternion QuatTwist(twist, startIkVec);

	// Start rotation
	QuatIkStart *= r0 * r2 * r3;
	// QuatIkStart *= QuatTwist * r0 * r2 * r3;
	
	// Mid rotation
	FnFkMid.getRotation(QuatIkMid, MSpace::kWorld);
	QuatIkMid *= r1;
	QuatIkMid *= r0 * r2 * r3;

	// End rotation
	FnIkHandle.getRotation(QuatIkEnd, MSpace::kWorld);
}


MStatus Ik2bSolver::UpdateOutput(const MPlug& Plug, MDataBlock& DataBlock)
{	
	/* Sets the outputs and data block clean.

	Args:
		Plug (MPlug&): Plug representing the attribute that needs to be recomputed.
		DataBlock (MDataBlock&): Data block containing storage for the node's attributes.

	Returns:
		status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
			during the operation.

	*/
	MStatus status;

	MDataHandle DhOutUpdate = DataBlock.outputValue(AttrOutUpdate, &status);
	DhOutUpdate.set3Double(0.0, 0.0, 0.0);
	DhOutUpdate.setClean();

	DataBlock.setClean(Plug);

	return MS::kSuccess;
}


MStatus Ik2bSolver::compute(const MPlug& plug, MDataBlock& dataBlock)
{
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
	status = ParseDataBlock(dataBlock, InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Solve the limb
	status = Solve(InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Set the output and data block clean
	status = UpdateOutput(plug, dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}


MStatus Ik2bSolver::setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs)
{
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
	)
	{
		affectedPlugs.append(MPlug(SelfObj, AttrOutUpdate));
	}

	return MS::kSuccess;
}


void Ik2bSolver::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const
{
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


void Ik2bSolver::postConstructor()
{
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
