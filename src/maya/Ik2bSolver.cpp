#include "Ik2bSolver.h"


// Public Data
const MString Ik2bSolver::typeName = "ik2bSolver";
const MTypeId Ik2bSolver::typeId = 0x0066674;

// Node's Input Attributes
MObject Ik2bSolver::attrInMode;

Attribute Ik2bSolver::attrInFkStart;
Attribute Ik2bSolver::attrInFkMid;
Attribute Ik2bSolver::attrInFkEnd;
Attribute Ik2bSolver::attrInIkHandle;

MObject Ik2bSolver::attrInPvX, Ik2bSolver::attrInPvY, Ik2bSolver::attrInPvZ, Ik2bSolver::attrInPv;

Attribute Ik2bSolver::attrInTwist;
MObject Ik2bSolver::attrInSoftness;

// Nodes's Output Attributes
MObject Ik2bSolver::attrOutStartX, Ik2bSolver::attrOutStartY, Ik2bSolver::attrOutStartZ, Ik2bSolver::attrOutStart;
MObject Ik2bSolver::attrOutMidX, Ik2bSolver::attrOutMidY, Ik2bSolver::attrOutMidZ, Ik2bSolver::attrOutMid;
MObject Ik2bSolver::attrOutEndX, Ik2bSolver::attrOutEndY, Ik2bSolver::attrOutEndZ, Ik2bSolver::attrOutEnd;

MObject Ik2bSolver::attrOutFkVisibility;
MObject Ik2bSolver::attrOutIkVisibility;


Attribute Ik2bSolver::attrInJntStart;
Attribute Ik2bSolver::attrInJntMid;
Attribute Ik2bSolver::attrInJntEnd;

MObject Ik2bSolver::attrOutUpdate;




MStatus Ik2bSolver::initialize() {
	/* Node Initializer.

	This method initializes the node, and should be overridden in user-defined nodes.
	
	Returns:
		status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
			during the operation.

	*/
	MStatus status;

	// Attr function sets
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;
	MFnEnumAttribute eAttr;

	// Node's Input Attributes
	attrInMode = eAttr.create("mode", "mod");
	eAttr.addField("Fk", 0);
	eAttr.addField("Ik", 1);
	eAttr.setKeyable(true);
	eAttr.setReadable(false);
	eAttr.setStorable(true);

	createAttribute(attrInFkStart, "fkStart", DefaultValue<MMatrix>());
	createAttribute(attrInFkMid, "fkMid", DefaultValue<MMatrix>());
	createAttribute(attrInFkEnd, "fkEnd", DefaultValue<MMatrix>());
	createAttribute(attrInIkHandle, "ikHandle", DefaultValue<MMatrix>());

	attrInPvX = nAttr.create("poleVectorX", "pvX", MFnNumericData::kDouble, 0.0);
	attrInPvY = nAttr.create("poleVectorY", "pvY", MFnNumericData::kDouble, 0.0);
	attrInPvZ = nAttr.create("poleVectorZ", "pvZ", MFnNumericData::kDouble, 0.0);
	attrInPv = nAttr.create("poleVector", "pv", attrInPvX, attrInPvY, attrInPvZ);
	nAttr.setReadable(false);

	createAttribute(attrInTwist, "twist", DefaultValue<double>());

	attrInSoftness = nAttr.create("softness", "sfns", MFnNumericData::kDouble, 0.0);
	nAttr.setKeyable(true);
	nAttr.setReadable(false);
	nAttr.setStorable(true);
	nAttr.setWritable(true);
	nAttr.setMin(0.0);
	nAttr.setMax(10.0);

	createAttribute(attrInJntStart, "jntStart", DefaultValue<MMatrix>());
	createAttribute(attrInJntMid, "jntMid", DefaultValue<MMatrix>());
	createAttribute(attrInJntEnd, "jntEnd", DefaultValue<MMatrix>());

	// attrInTime = uAttr.create("inTime", "itm", MFnUnitAttribute::kTime);
	// uAttr.setKeyable(true);
	// uAttr.setReadable(false);

	// Output attributes
	attrOutStartX = uAttr.create("outputStartX", "osX", MFnUnitAttribute::kAngle, 0.0);
	attrOutStartY = uAttr.create("outputStartY", "osY", MFnUnitAttribute::kAngle, 0.0);
	attrOutStartZ = uAttr.create("outputStartZ", "osZ", MFnUnitAttribute::kAngle, 0.0);
	attrOutStart = nAttr.create("outputStart", "os", attrOutStartX, attrOutStartY, attrOutStartZ);
	nAttr.setWritable(false);

	attrOutMidX = uAttr.create("outputMidX", "omX", MFnUnitAttribute::kAngle, 0.0);
	attrOutMidY = uAttr.create("outputMidY", "omY", MFnUnitAttribute::kAngle, 0.0);
	attrOutMidZ = uAttr.create("outputMidZ", "omZ", MFnUnitAttribute::kAngle, 0.0);
	attrOutMid = nAttr.create("outputMid", "om", attrOutMidX, attrOutMidY, attrOutMidZ);
	nAttr.setWritable(false);

	attrOutEndX = uAttr.create("outputEndX", "oeX", MFnUnitAttribute::kAngle, 0.0);
	attrOutEndY = uAttr.create("outputEndY", "oeY", MFnUnitAttribute::kAngle, 0.0);
	attrOutEndZ = uAttr.create("outputEndZ", "oeZ", MFnUnitAttribute::kAngle, 0.0);
	attrOutEnd = nAttr.create("outputEnd", "oe", attrOutEndX, attrOutEndY, attrOutEndZ);
	nAttr.setWritable(false);

	attrOutFkVisibility = nAttr.create("fkVisibility", "fkVis", MFnNumericData::kBoolean, true);
	nAttr.setWritable(false);

	attrOutIkVisibility = nAttr.create("ikVisibility", "ikVis", MFnNumericData::kBoolean, false);
	nAttr.setWritable(false);

	attrOutUpdate = nAttr.create("outputUpdate", "outu", MFnNumericData::kDouble, 0.0);
	nAttr.setWritable(false);

	// Add attributes
	addAttributes(
		attrInFkStart, attrInFkMid,	attrInFkEnd, attrInIkHandle, attrInPv,
		attrInMode, attrInTwist, attrInSoftness,
		attrInJntStart, attrInJntMid, attrInJntEnd,
		attrOutStart, attrOutMid, attrOutEnd,
		attrOutFkVisibility, attrOutIkVisibility,
		attrOutUpdate
	);

	return MS::kSuccess;
}


MStatus Ik2bSolver::parseDataBlock(MDataBlock& dataBlock) {
	/* Parse the data block and get all inputs.
	
	We're getting the mObj from the .attribute() instead of a numeric data type like double in
	order to retrieve the MFnTransform for the input controllers - this also triggers the input as
	dirty. All of Maya's solvers get the world position from the .rotatePivot() method.

	*/
	MStatus status;

	mode = dataBlock.inputValue(attrInMode).asShort();
	if (mode == 0) {
		bFkVisibility = true;
		bIkVisibility = false;
	} else if (mode == 1) {
		bFkVisibility = false;
		bIkVisibility = true;
	}

	// // Ask for time value to force refresh on the node
	// timeCurrent = dataBlock.inputValue(attrInTime, &status).asTime();
	// Asking for the actuall matrix input helps refreshing the rig if there are no anim curves
	// mtrnInStart = dataBlock.inputValue(attrInFkStart).asMatrix();
	// mtrnInMid = dataBlock.inputValue(attrInFkMid).asMatrix();
	// matInFkEnd = dataBlock.inputValue(attrInFkEnd).asMatrix();
	matInFkStart = dataBlock.inputValue(attrInFkStart).asMatrix();
	matInFkMid = dataBlock.inputValue(attrInFkMid).asMatrix();
	matInFkEnd = dataBlock.inputValue(attrInFkEnd).asMatrix();
	matInIkHandle = dataBlock.inputValue(attrInIkHandle).asMatrix();
	posInPv = MVector(dataBlock.inputValue(attrInPvX).asDouble(), dataBlock.inputValue(attrInPvY).asDouble(),	dataBlock.inputValue(attrInPvZ).asDouble());

	// In controllers
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnFkStart, attrInFkStart));
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnFkMid, attrInFkMid));
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnFkEnd, attrInFkEnd));
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnIkHandle, attrInIkHandle));

	// Out joints
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnOutStart, attrInJntStart));
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnOutMid, attrInJntMid));
	CHECK_MSTATUS_AND_RETURN_IT(LMPlugin::parseTransformInput(dataBlock, objSelf, fnOutEnd, attrInJntEnd));

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
	uiUnitAngle = MAngle::uiUnit();
	twist = MAngle(dataBlock.inputValue(attrInTwist).asDouble(), uiUnitAngle);
	softness = dataBlock.inputValue(attrInSoftness).asDouble();

	return MS::kSuccess;
}


void Ik2bSolver::getFkTransforms() {

	posFkStart = fnFkStart.rotatePivot(MSpace::kWorld);
	fnFkStart.getRotation(quatFkStart, MSpace::kWorld);

	posFkMid = fnFkMid.rotatePivot(MSpace::kWorld);
	fnFkMid.getRotation(quatFkMid, MSpace::kWorld);

	posFkMid = fnFkEnd.rotatePivot(MSpace::kWorld);
	fnFkEnd.getRotation(quatFkEnd, MSpace::kWorld);

}


void Ik2bSolver::getIkTransforms() {

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
		posIkPv = posInPv * fnRoot.dagPath().exclusiveMatrix() + posIkRoot;
	}
}


MStatus Ik2bSolver::solveLimb() {
	/* Solves the limb. 

	Main fk / ik routing method. 

	*/
	if (mode == 0) {solveFk();}

	if (mode == 1) {solveIk();}

	return MS::kSuccess;
}


bool Ik2bSolver::solveFk() {
	/* Set the fk transforms.

	We don't actually solve fk - it's called like this just for consistency and readability.
	The isEditing flag is reserved for editing the fk transforms where we move the pole vector by
	a constant distance (limb length) calculated from the mid transform. 

	*/
	// getFkTransforms();

	fnFkStart.getRotation(quatFkStart, MSpace::kWorld);
	fnFkMid.getRotation(quatFkMid, MSpace::kWorld);
	fnFkEnd.getRotation(quatFkEnd, MSpace::kWorld);

	// fnOutStart.getRotation(quatOutStart, MSpace::kWorld);
	// fnOutMid.getRotation(quatOutMid, MSpace::kWorld);
	// fnOutEnd.getRotation(quatOutEnd, MSpace::kWorld);

	// quatOutStart = slerp(quatOutStart, quatFkStart, 1);
	// quatOutMid = slerp(quatOutMid, quatFkMid, 1);
	// quatOutEnd = slerp(quatOutEnd, quatFkEnd, 1);

	fnOutStart.setRotation(quatFkStart, MSpace::kWorld);
	fnOutMid.setRotation(quatFkMid, MSpace::kWorld);
	fnOutEnd.setRotation(quatFkEnd, MSpace::kWorld);

	// quatOutStart = quatFkStart;
	// quatOutMid = quatFkMid;
	// quatOutEnd = quatFkEnd;

	fnOutStart.getRotation(quatOutStart, MSpace::kTransform);
	fnOutMid.getRotation(quatOutMid, MSpace::kTransform);
	fnOutEnd.getRotation(quatOutEnd, MSpace::kTransform);

	return true;
}


bool Ik2bSolver::solveIk() {
	/* Calculates the ik solution for a two bone limb.
	*/
	getIkTransforms();

	LMSolve::twoBoneIk(posIkStart, posIkMid, posIkEnd, posIkHandle, posIkPv, twist, softness, bIsPvConnected, quatIkStart, quatIkMid);

	// Lame as f@ck but maybe i will fix it one-day :)
	// Apply the rotations to the output joints world -> local
	fnOutStart.setRotation(quatIkStart, MSpace::kWorld);
	fnOutMid.setRotation(quatIkMid, MSpace::kWorld);
	fnOutEnd.setRotation(quatIkHandle, MSpace::kWorld);
	// Get the output rotations in local space because joint chain
	fnOutStart.getRotation(quatOutStart, MSpace::kTransform);
	fnOutMid.getRotation(quatOutMid, MSpace::kTransform);
	fnOutEnd.getRotation(quatOutEnd, MSpace::kTransform);

	return true;
}


void Ik2bSolver::blendFkIk() {
	// because we want to use 0 - 100 in the channel box, yeah i know :|
	double ScaledWeight = mode * 0.01;

	quatOutStart = slerp(quatFkStart, quatIkStart, ScaledWeight);
	quatOutMid = slerp(quatFkMid, quatIkMid, ScaledWeight);
	quatOutEnd = slerp(quatFkEnd, quatIkEnd, ScaledWeight);
	quatOutHandle = slerp(quatFkEnd, quatIkHandle, ScaledWeight);
	// so this still is an issue since it's a bit off from the fk end ctrl pos, maybe we just snap to it
	// posOutHandle = Lerp(posFkHandle, posIkHandle, ScaledWeight);
	// posOutPv = Lerp(posFkPv, posIkPv, ScaledWeight);
}


void Ik2bSolver::solveFkIk() {
	/* So kind of does what the name says but not really.
	*/
	getFkTransforms();
	getIkTransforms();

	LMSolve::twoBoneIk(posIkStart, posIkMid, posIkEnd, posIkHandle, posIkPv, twist, softness, bIsPvConnected, quatIkStart, quatIkMid);

	blendFkIk();

	// // Set rotations
	// fnFkStart.setRotation(quatOutStart, MSpace::kWorld);
	// fnFkMid.setRotation(quatOutMid, MSpace::kWorld);
	// fnFkEnd.setRotation(quatOutEnd, MSpace::kWorld);
	// fnIkHandle.setRotation(quatOutHandle, MSpace::kWorld);

	// Sync the ik ctrl to the fk end bone due to differences in fk / ik blending
	// fnIkHandle.setTranslation(posOutHandle, MSpace::kWorld);
	// fnPv.setTranslation(posOutPv, MSpace::kWorld);
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

	// Rotation outputs
	// MEulerRotation eulrStart;
	// fnFkStart.getRotation(eulrStart);
	MEulerRotation eulrStart = quatOutStart.asEulerRotation();
	MDataHandle dhOutStart = dataBlock.outputValue(attrOutStart, &status);
	dhOutStart.set3Double(eulrStart.x, eulrStart.y, eulrStart.z);
	dhOutStart.setClean();

	// MEulerRotation eulrMid;
	// fnFkMid.getRotation(eulrMid);
	MEulerRotation eulrMid = quatOutMid.asEulerRotation();
	MDataHandle dhOutMid = dataBlock.outputValue(attrOutMid, &status);
	dhOutMid.set3Double(eulrMid.x, eulrMid.y, eulrMid.z);
	dhOutMid.setClean();

	// MEulerRotation eulrEnd;
	// fnFkEnd.getRotation(eulrEnd);
	MEulerRotation eulrEnd = quatOutEnd.asEulerRotation();
	MDataHandle dhOutEnd = dataBlock.outputValue(attrOutEnd, &status);
	dhOutEnd.set3Double(eulrEnd.x, eulrEnd.y, eulrEnd.z);
	dhOutEnd.setClean();

	// Visibility outputs
	MDataHandle dhOutFkVisibility = dataBlock.outputValue(attrOutFkVisibility, &status);
	dhOutFkVisibility.setBool(bFkVisibility);
	dhOutFkVisibility.setClean();

	MDataHandle dhOutIkVisibility = dataBlock.outputValue(attrOutIkVisibility, &status);
	dhOutIkVisibility.setBool(bIkVisibility);
	dhOutIkVisibility.setClean();

	MDataHandle dhOutUpdate = dataBlock.outputValue(attrOutUpdate, &status);
	dhOutUpdate.setDouble(0.0);
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

	// if (plug != attrOutStart || plug != attrOutMid || plug != attrOutEnd) {return MS::kUnknownParameter;}

	CHECK_MSTATUS_AND_RETURN_IT(parseDataBlock(dataBlock));

	CHECK_MSTATUS_AND_RETURN_IT(solveLimb());

	CHECK_MSTATUS_AND_RETURN_IT(updateOutput(plug, dataBlock));

	return MS::kSuccess;
}


MStatus Ik2bSolver::setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) {
	/* Sets the relation between attributes and marks the specified plugs dirty.

	Args:
		plugBeingDirtied (&MPlug): Plug which is being set dirty by Maya.
		affectedPlugs (&MPlugArray): The programmer should add any plugs which they want to set dirty
			to this list.

	*/
	// Rotation output
	if ( plugBeingDirtied == attrInMode
		|| plugBeingDirtied == attrInFkStart
		|| plugBeingDirtied == attrInFkMid
		|| plugBeingDirtied == attrInFkEnd
		|| plugBeingDirtied == attrInIkHandle
		|| plugBeingDirtied == attrInPv
		|| plugBeingDirtied == attrInTwist
		|| plugBeingDirtied == attrInSoftness
	)	{
		affectedPlugs.append(MPlug(objSelf, attrOutStart));
		affectedPlugs.append(MPlug(objSelf, attrOutMid));
		affectedPlugs.append(MPlug(objSelf, attrOutEnd));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdate));
	}
	// Visibility output
	if (plugBeingDirtied == attrInMode)	{
		affectedPlugs.append(MPlug(objSelf, attrOutFkVisibility));
		affectedPlugs.append(MPlug(objSelf, attrOutIkVisibility));
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
