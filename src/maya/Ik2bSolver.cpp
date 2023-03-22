#include "Ik2bSolver.h"


// Public Data
const MString Ik2bSolver::typeName = "ik2bSolver";
const MTypeId Ik2bSolver::typeId = 0x0066674;

// Node's Input Attributes
Attribute Ik2bSolver::inFkStartAttr;
Attribute Ik2bSolver::inFkMidAttr;
Attribute Ik2bSolver::inFkEndAttr;
Attribute Ik2bSolver::inIkHandleAttr;

MObject Ik2bSolver::attrInPvX;
MObject Ik2bSolver::attrInPvY;
MObject Ik2bSolver::attrInPvZ;
MObject Ik2bSolver::attrInPv;

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

	attrInPvX = nAttr.create("poleVectorX", "pvX", MFnNumericData::kDouble, 0.0);
	attrInPvY = nAttr.create("poleVectorY", "pvY", MFnNumericData::kDouble, 0.0);
	attrInPvZ = nAttr.create("poleVectorZ", "pvZ", MFnNumericData::kDouble, 0.0);
	attrInPv = nAttr.create("poleVector", "pv", attrInPvX, attrInPvY, attrInPvZ);

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
		inIkHandleAttr,	attrInPv,
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
	posInPoleVector = MVector(dataBlock.inputValue(attrInPvX).asDouble(), dataBlock.inputValue(attrInPvY).asDouble(),	dataBlock.inputValue(attrInPvZ).asDouble());

	// Start fk controller
	MDagPath pathFkStart;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(inFkStartAttr).attribute()), pathFkStart);
	if (status == MS::kSuccess) {
		FnFkStart.setObject(pathFkStart);
	} else {
		return MS::kFailure;
	}
	// Mid fk controller
	MDagPath pathFkMid;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(inFkMidAttr).attribute()), pathFkMid);
	if (status == MS::kSuccess) {
		FnFkMid.setObject(pathFkMid);
	} else {
		return MS::kFailure;
	}
	// End fk controller
	MDagPath pathFkEnd;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(inFkEndAttr).attribute()), pathFkEnd);
	if (status == MS::kSuccess) {
		FnFkEnd.setObject(pathFkEnd);
	} else {
		return MS::kFailure;
	}
	// Ik handle
	MDagPath pathIkHandle;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(inIkHandleAttr).attribute()), pathIkHandle);
	if (status == MS::kSuccess) {
		FnIkHandle.setObject(pathIkHandle);
	} else {
		return MS::kFailure;
	}
	// Pole vector
	MDagPath pathPoleVector;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(attrInPv).attribute()), pathPoleVector);
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

	return MS::kSuccess;
}


void Ik2bSolver::getFkTransforms() {
	// Position
	PosFkStart = FnFkStart.rotatePivot(MSpace::kWorld);
	FnFkStart.getRotation(QuatFkStart, MSpace::kWorld);

	PosFkMid = FnFkMid.rotatePivot(MSpace::kWorld);
	FnFkMid.getRotation(QuatFkMid, MSpace::kWorld);

	PosFkEnd = FnFkEnd.rotatePivot(MSpace::kWorld);
	FnFkEnd.getRotation(QuatFkEnd, MSpace::kWorld);

	PosFkHandle = PosFkEnd;
	FnIkHandle.getRotation(QuaFkHandle, MSpace::kWorld);

	if (bIsPoleVectorConnected) {PosFkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);}
	else {
		PosIkPoleVector = posInPoleVector + PosIkStart;
	}
}


void Ik2bSolver::getIkTransforms() {
	// Position
	PosIkStart = FnFkStart.rotatePivot(MSpace::kWorld);
	FnFkStart.getRotation(QuatIkStart, MSpace::kWorld);

	PosIkMid = FnFkMid.rotatePivot(MSpace::kWorld);
	FnFkMid.getRotation(QuatIkMid, MSpace::kWorld);

	PosIkEnd = FnFkEnd.rotatePivot(MSpace::kWorld);
	FnFkEnd.getRotation(QuatIkEnd, MSpace::kWorld);

	PosIkHandle = FnIkHandle.rotatePivot(MSpace::kWorld);
	FnIkHandle.getRotation(QuatIkHandle, MSpace::kWorld);

	if (bIsPoleVectorConnected) {PosIkPoleVector = FnPoleVector.rotatePivot(MSpace::kWorld);}
	else {
		// MGlobal::displayWarning(MString("vecInX ") + std::to_string(posInPoleVector.x).c_str());
		// MGlobal::displayWarning(MString("vecInX ") + std::to_string(posInPoleVector.y).c_str());
		// MGlobal::displayWarning(MString("vecInY ") + std::to_string(posInPoleVector.z).c_str());

		PosIkPoleVector = posInPoleVector + PosIkStart;

		// MGlobal::displayWarning(MString("vecOutX ") + std::to_string(PosIkPoleVector.x).c_str());
		// MGlobal::displayWarning(MString("vecOutX ") + std::to_string(PosIkPoleVector.y).c_str());
		// MGlobal::displayWarning(MString("vecOutY ") + std::to_string(PosIkPoleVector.z).c_str());
	}
}


MStatus Ik2bSolver::solveLimb(MDagPathArray& InOutLinks) {
	/* Solves the limb. 

	Main fk / ik routing method. 

	Args:
		InOutLinks (MDagPathArray&): Array with path to the input transforms.

	*/
	// Editing
	if (!LMAnimControl::timeChanged(ctrlAnim, timeCached, timeCurrent)) {
		if (LMGLobal::currentToolIsTransformContext()) {
			MGlobal::getActiveSelectionList(listSel);
			// If selection has any fk ctrl, solve fk
			if (listSel.hasItem(InOutLinks[0]) || listSel.hasItem(InOutLinks[1]) || listSel.hasItem(InOutLinks[2])) {
				solveFk();
			} else {
				solveIk();
			}
			return MS::kSuccess;
		}
	}
	// Solve for playback and all other possible cases - just solve something
	if (fkIk == 0.0) {
		solveFk();
	}	else if (fkIk > 0.0 && fkIk < 100.0) {
		solveFkIk();
	} else if (fkIk == 100.0) {
		solveIk();
	}
	return MS::kSuccess;
}


void Ik2bSolver::solveFk() {
	/* Set the fk transforms.

	We don't actually solve fk - it's called like this just for consistency and readability.
	The isEditing flag is reserved for editing the fk transforms where we move the pole vector by
	a constant distance (limb length) calculated from the mid transform. 

	*/
	getFkTransforms();

	FnIkHandle.setTranslation(PosFkHandle, MSpace::kWorld);
	FnIkHandle.setRotation(QuatFkEnd, MSpace::kWorld);

	if (bIsPoleVectorConnected) {
		FnPoleVector.setTranslation(LMRigUtils::getPvPosition(PosFkStart, PosFkMid, PosFkEnd), MSpace::kWorld);
	}
}


void Ik2bSolver::solveIk() {
	/* Calculates the ik solution for a two bone limb.
	*/
	getIkTransforms();

	LMSolve::twoBoneIk(PosIkStart, PosIkMid, PosIkEnd, PosIkHandle, PosIkPoleVector, twist, softness, QuatIkStart, QuatIkMid);

	// Set fk rotations
	FnFkStart.setRotation(QuatIkStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatIkMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatIkHandle, MSpace::kWorld);
}


void Ik2bSolver::blendFkIk() {
	// because we want to use 0 - 100 in the channel box, yeah i know :|
	double ScaledWeight = fkIk * 0.01;

	QuatOutStart = slerp(QuatFkStart, QuatIkStart, ScaledWeight);
	QuatOutMid = slerp(QuatFkMid, QuatIkMid, ScaledWeight);
	QuatOutEnd = slerp(QuatFkEnd, QuatIkEnd, ScaledWeight);
	QuatOutHandle = slerp(QuatFkEnd, QuatIkHandle, ScaledWeight);
	// so this still is an issue since it's a bit off from the fk end ctrl pos, maybe we just snap to it
	PosOutHandle = Lerp(PosFkHandle, PosIkHandle, ScaledWeight);
	PosOutPoleVector = Lerp(PosFkPoleVector, PosIkPoleVector, ScaledWeight);
}


void Ik2bSolver::solveFkIk() {
	/* So kind of does what the name says but not really.
	*/
	getFkTransforms();
	getIkTransforms();

	LMSolve::twoBoneIk(PosIkStart, PosIkMid, PosIkEnd, PosIkHandle, PosIkPoleVector, twist, softness, QuatIkStart, QuatIkMid);

	blendFkIk();

	// Set rotations
	FnFkStart.setRotation(QuatOutStart, MSpace::kWorld);
	FnFkMid.setRotation(QuatOutMid, MSpace::kWorld);
	FnFkEnd.setRotation(QuatOutEnd, MSpace::kWorld);
	FnIkHandle.setRotation(QuatOutHandle, MSpace::kWorld);

	// Sync the ik ctrl to the fk end bone due to differences in fk / ik blending
	FnIkHandle.setTranslation(PosOutHandle, MSpace::kWorld);
	FnPoleVector.setTranslation(PosOutPoleVector, MSpace::kWorld);
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

	// MDagPathArray InOutLinks;
	status = parseDataBlock(dataBlock, InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = solveLimb(InOutLinks);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = updateOutput(plug, dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Cache time change
	timeCached = timeCurrent;

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
		|| plugBeingDirtied == attrInPv
		|| plugBeingDirtied == inTwistAttr
		|| plugBeingDirtied == inSoftnessAttr
		|| plugBeingDirtied == inFkIkAttr
		|| plugBeingDirtied == AttrInTime
	)	{
		affectedPlugs.append(MPlug(objSelf, AttrOutUpdate));
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
	objSelf = thisMObject();
}
