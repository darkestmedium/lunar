#include "Ik2bSolver.h"


// Public Data
const MString Ik2bSolver::typeName = "ik2bSolver";
const MTypeId Ik2bSolver::typeId = 0x0066674;

// Node's Input Attributes
Attribute Ik2bSolver::attrInFkStart;
Attribute Ik2bSolver::attrInFkMid;
Attribute Ik2bSolver::attrInFkEnd;
Attribute Ik2bSolver::attrInIkHandle;

MObject Ik2bSolver::attrInPvX;
MObject Ik2bSolver::attrInPvY;
MObject Ik2bSolver::attrInPvZ;
MObject Ik2bSolver::attrInPv;

Attribute Ik2bSolver::attrInTwist;
MObject Ik2bSolver::attrInSoftness;
MObject Ik2bSolver::attrInFkIk;
MObject Ik2bSolver::attrInTime;
// Nodes's Output Attributes
Attribute Ik2bSolver::attrOutUpdateX;
Attribute Ik2bSolver::attrOutUpdateY;
Attribute Ik2bSolver::attrOutUpdateZ;
Attribute Ik2bSolver::attrOutUpdate;

MObject Ik2bSolver::attrInDirty;
MObject Ik2bSolver::attrOutDirty;


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
	createAttribute(attrInFkStart, "fkStart", DefaultValue<MMatrix>());
	createAttribute(attrInFkMid, "fkMid", DefaultValue<MMatrix>());
	createAttribute(attrInFkEnd, "fkEnd", DefaultValue<MMatrix>());
	createAttribute(attrInIkHandle, "ikHandle", DefaultValue<MMatrix>());

	attrInPvX = nAttr.create("poleVectorX", "pvX", MFnNumericData::kDouble, 0.0);
	attrInPvY = nAttr.create("poleVectorY", "pvY", MFnNumericData::kDouble, 0.0);
	attrInPvZ = nAttr.create("poleVectorZ", "pvZ", MFnNumericData::kDouble, 0.0);
	attrInPv = nAttr.create("poleVector", "pv", attrInPvX, attrInPvY, attrInPvZ);

	createAttribute(attrInTwist, "twist", DefaultValue<double>());

	attrInSoftness = nAttr.create("softness", "sfns", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(10.0);

	attrInFkIk = nAttr.create("fkIk", "fkik", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	uAttr.setReadable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(100.0);

	attrInTime = uAttr.create("inTime", "itm", MFnUnitAttribute::kTime);
	uAttr.setKeyable(true);
	uAttr.setReadable(false);

	// Output attributes
	attrOutUpdateX = nAttr.create("updateX", "updX", MFnNumericData::kDouble, 0.0);
	attrOutUpdateY = nAttr.create("updateY", "updY", MFnNumericData::kDouble, 0.0);
	attrOutUpdateZ = nAttr.create("updateZ", "updZ", MFnNumericData::kDouble, 0.0);
	attrOutUpdate = nAttr.create("update", "upd", attrOutUpdateX, attrOutUpdateY, attrOutUpdateZ);


	attrInDirty = nAttr.create("inDirty", "idirt", MFnNumericData::kDouble, 1.0);
	attrOutDirty = nAttr.create("dirty", "dirt", MFnNumericData::kDouble, 0.0);

	// Add attributes
	addAttributes(
		attrInFkStart, attrInFkMid,	attrInFkEnd,
		attrInIkHandle,	attrInPv,
		attrInTwist, attrInSoftness, attrInFkIk,
		attrInTime,
		attrOutUpdate,
		attrInDirty,
		attrOutDirty
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
	if (plug == attrOutUpdate) {
		return true;
	}
	return MPxNode::isPassiveOutput(plug);
}


MStatus Ik2bSolver::parseDataBlock(MDataBlock& dataBlock) {
	/* Parse the data block and get all inputs.
	 *
	 * We're getting the mObj from the .attribute() instead of a numeric data type like double in
	 * order to retrieve the MFnTransform for the input controllers - this also triggers the input as
	 * dirty. All of Maya's solvers get the world position from the .rotatePivot() method.
	 * 
	 */
	MStatus status;

	isDirty = dataBlock.inputValue(attrInDirty).asDouble(),

	// Ask for time value to force refresh on the node
	timeCurrent = dataBlock.inputValue(attrInTime, &status).asTime();
	// Asking for the actuall matrix input helps refreshing the rig if there are no anim curves
	matInFkStart = dataBlock.inputValue(attrInFkStart).asMatrix();
	matInFkMid = dataBlock.inputValue(attrInFkMid).asMatrix();
	matInFkEnd = dataBlock.inputValue(attrInFkEnd).asMatrix();
	matInIkHandle = dataBlock.inputValue(attrInIkHandle).asMatrix();
	posInPv = MVector(dataBlock.inputValue(attrInPvX).asDouble(), dataBlock.inputValue(attrInPvY).asDouble(),	dataBlock.inputValue(attrInPvZ).asDouble());

	// Start fk controller
	status = LMPlugin::parseTransformInput(dataBlock, fnFkStart, objSelf, attrInFkStart);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Mid fk controller
	status = LMPlugin::parseTransformInput(dataBlock, fnFkMid, objSelf, attrInFkMid);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// End fk controller
	status = LMPlugin::parseTransformInput(dataBlock, fnFkEnd, objSelf, attrInFkEnd);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Ik handle
	status = LMPlugin::parseTransformInput(dataBlock, fnIkHandle, objSelf, attrInIkHandle);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Pole vector
	MDagPath pathPv;
	status = MDagPath::getAPathTo(LMAttribute::getSourceObjFromPlug(objSelf, dataBlock.inputValue(attrInPv).attribute()), pathPv);
	if (status == MS::kSuccess) {
		fnPv.setObject(pathPv);
		bIsPvConnected = true;
	} else {
		fnPv.setObject(MObject::kNullObj);
		bIsPvConnected = false;
		// Get fk start parent
		MDagPath pathRoot;
		status = MDagPath::getAPathTo(fnFkStart.parent(0), pathRoot);
		if (status == MS::kSuccess) {
			fnRoot.setObject(pathRoot);
		} else {
			fnRoot.setObject(MObject::kNullObj);
		}
	}

	// Additional attributes
	twist = MAngle(dataBlock.inputValue(attrInTwist).asDouble(), MAngle::uiUnit());
	softness = dataBlock.inputValue(attrInSoftness).asDouble();
	fkIk = dataBlock.inputValue(attrInFkIk).asDouble();

	return MS::kSuccess;
}


void Ik2bSolver::getFkTransforms() {
	// Position
	posFkStart = fnFkStart.rotatePivot(MSpace::kWorld);
	fnFkStart.getRotation(quatFkStart, MSpace::kWorld);

	posFkMid = fnFkMid.rotatePivot(MSpace::kWorld);
	fnFkMid.getRotation(quatFkMid, MSpace::kWorld);

	posFkEnd = fnFkEnd.rotatePivot(MSpace::kWorld);
	fnFkEnd.getRotation(quatFkEnd, MSpace::kWorld);

	posFkHandle = posFkEnd;
	fnIkHandle.getRotation(quatFkHandle, MSpace::kWorld);

	if (bIsPvConnected) {posFkPv = fnPv.rotatePivot(MSpace::kWorld);}
	else {
		posFkRoot = fnRoot.rotatePivot(MSpace::kWorld);
		posFkPv = posInPv * fnRoot.dagPath().exclusiveMatrix() + posFkRoot;}
}


void Ik2bSolver::getIkTransforms() {
	// Position
	posIkStart = fnFkStart.rotatePivot(MSpace::kWorld);
	fnFkStart.getRotation(quatIkStart, MSpace::kWorld);

	posIkMid = fnFkMid.rotatePivot(MSpace::kWorld);
	fnFkMid.getRotation(quatIkMid, MSpace::kWorld);

	posIkEnd = fnFkEnd.rotatePivot(MSpace::kWorld);
	fnFkEnd.getRotation(quatIkEnd, MSpace::kWorld);

	posIkHandle = fnIkHandle.rotatePivot(MSpace::kWorld);
	fnIkHandle.getRotation(quatIkHandle, MSpace::kWorld);

	if (bIsPvConnected) {posIkPv = fnPv.rotatePivot(MSpace::kWorld);}
	else {
		// we need a getPvRootPosition that will calculate the pv and multiply by the root
		posIkRoot = fnRoot.rotatePivot(MSpace::kWorld);
		posIkPv = posInPv * fnRoot.dagPath().exclusiveMatrix() + posIkRoot;}
}


MStatus Ik2bSolver::solveLimb() {
	/* Solves the limb. 

	Main fk / ik routing method. 

	Args:
		InOutLinks (MDagPathArray&): Array with path to the input transforms.

	*/
	// Editing
	if (!LMAnimControl::timeChanged(ctrlAnim, timeCached, timeCurrent)) {
		if (LMGLobal::currentToolIsTransformContext()) {
			MGlobal::getActiveSelectionList(listSel);  // If selection has any fk ctrl, solve fk
			if (listSel.hasItem(fnFkStart.dagPath()) || listSel.hasItem(fnFkMid.dagPath()) || listSel.hasItem(fnFkEnd.dagPath())) {
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

	fnIkHandle.setTranslation(posFkHandle, MSpace::kWorld);
	fnIkHandle.setRotation(quatFkEnd, MSpace::kWorld);

	if (bIsPvConnected) {fnPv.setTranslation(LMRigUtils::getPvPosition(posFkStart, posFkMid, posFkEnd), MSpace::kWorld);}
}


void Ik2bSolver::solveIk() {
	/* Calculates the ik solution for a two bone limb.
	*/
	getIkTransforms();

	LMSolve::twoBoneIk(posIkStart, posIkMid, posIkEnd, posIkHandle, posIkPv, twist, softness, bIsPvConnected, quatIkStart, quatIkMid);

	// Set fk rotations
	fnFkStart.setRotation(quatIkStart, MSpace::kWorld);
	fnFkMid.setRotation(quatIkMid, MSpace::kWorld);
	fnFkEnd.setRotation(quatIkHandle, MSpace::kWorld);
}


void Ik2bSolver::blendFkIk() {
	// because we want to use 0 - 100 in the channel box, yeah i know :|
	double ScaledWeight = fkIk * 0.01;

	quatOutStart = slerp(quatFkStart, quatIkStart, ScaledWeight);
	quatOutMid = slerp(quatFkMid, quatIkMid, ScaledWeight);
	quatOutEnd = slerp(quatFkEnd, quatIkEnd, ScaledWeight);
	quatOutHandle = slerp(quatFkEnd, quatIkHandle, ScaledWeight);
	// so this still is an issue since it's a bit off from the fk end ctrl pos, maybe we just snap to it
	posOutHandle = Lerp(posFkHandle, posIkHandle, ScaledWeight);
	posOutPv = Lerp(posFkPv, posIkPv, ScaledWeight);
}


void Ik2bSolver::solveFkIk() {
	/* So kind of does what the name says but not really.
	*/
	getFkTransforms();
	getIkTransforms();

	LMSolve::twoBoneIk(posIkStart, posIkMid, posIkEnd, posIkHandle, posIkPv, twist, softness, bIsPvConnected, quatIkStart, quatIkMid);

	blendFkIk();

	// Set rotations
	fnFkStart.setRotation(quatOutStart, MSpace::kWorld);
	fnFkMid.setRotation(quatOutMid, MSpace::kWorld);
	fnFkEnd.setRotation(quatOutEnd, MSpace::kWorld);
	fnIkHandle.setRotation(quatOutHandle, MSpace::kWorld);

	// Sync the ik ctrl to the fk end bone due to differences in fk / ik blending
	fnIkHandle.setTranslation(posOutHandle, MSpace::kWorld);
	fnPv.setTranslation(posOutPv, MSpace::kWorld);
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

	MDataHandle dhOutUpdate = dataBlock.outputValue(attrOutUpdate, &status);
	dhOutUpdate.set3Double(0.0, 0.0, 0.0);
	dhOutUpdate.setClean();

	MDataHandle dhOutDirty = dataBlock.outputValue(attrOutDirty, &status);
	dhOutDirty.setDouble(1.0);
	dhOutDirty.setClean();

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

	status = parseDataBlock(dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	status = solveLimb();
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
	if ( plugBeingDirtied == attrInFkStart
		|| plugBeingDirtied == attrInFkMid
		|| plugBeingDirtied == attrInFkEnd
		|| plugBeingDirtied == attrInIkHandle
		|| plugBeingDirtied == attrInPv
		|| plugBeingDirtied == attrInTwist
		|| plugBeingDirtied == attrInSoftness
		|| plugBeingDirtied == attrInFkIk
		|| plugBeingDirtied == attrInTime
	)	{
		affectedPlugs.append(MPlug(objSelf, attrOutUpdate));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateX));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateY));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateZ));
		affectedPlugs.append(MPlug(objSelf, attrOutDirty));
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
	/* post constructor.

	Internally maya creates two objects when a user defined node is created, the internal MObject and
	the user derived object. The association between the these two objects is not made until after the
	MPxNode constructor is called. This implies that no MPxNode member function can be called from the
	MPxNode constructor. The postConstructor will get called immediately after the constructor when it
	is safe to call any MPxNode member function.

	Reimplemented in MPxTransform, and MPxPolyTrg.

	*/
	objSelf = thisMObject();
}
