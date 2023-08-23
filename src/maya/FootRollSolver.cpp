#include "FootRollSolver.h"


// Public Data
const MString FootRollSolver::typeName = "footRollSolver";
const MTypeId FootRollSolver::typeId = 0x0066676;

// Node's Input Attributes
Attribute FootRollSolver::attrInBall;
Attribute FootRollSolver::attrInAnkle;
MObject FootRollSolver::attrInHeelX;
MObject FootRollSolver::attrInHeelY;
MObject FootRollSolver::attrInHeelZ;
MObject FootRollSolver::attrInHeel;
MObject FootRollSolver::attrInToeX;
MObject FootRollSolver::attrInToeY;
MObject FootRollSolver::attrInToeZ;
MObject FootRollSolver::attrInToe;

Attribute FootRollSolver::attrInRoll;
Attribute FootRollSolver::attrInBendLimitAngle;
Attribute FootRollSolver::attrInToeLimitAngle;
MObject FootRollSolver::attrInTime;

// Nodes's Output Attributes
Attribute FootRollSolver::attrOutUpdateX;
Attribute FootRollSolver::attrOutUpdateY;
Attribute FootRollSolver::attrOutUpdateZ;
Attribute FootRollSolver::attrOutUpdate;


MStatus FootRollSolver::initialize() {
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

	// Node's Input Attributes
	createAttribute(attrInBall, "ball", DefaultValue<MMatrix>());
	createAttribute(attrInAnkle, "ankle", DefaultValue<MMatrix>());

	attrInHeelX = nAttr.create("heelX", "helX", MFnNumericData::kDouble, 0.0);
	attrInHeelY = nAttr.create("heelY", "helY", MFnNumericData::kDouble, 0.0);
	attrInHeelZ = nAttr.create("heelZ", "helZ", MFnNumericData::kDouble, 0.0);
	attrInHeel = nAttr.create("heel", "hel", attrInHeelX, attrInHeelY, attrInHeelZ);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);

	attrInToeX = nAttr.create("toeX", "toeX", MFnNumericData::kDouble, 0.0);
	attrInToeY = nAttr.create("toeY", "toeY", MFnNumericData::kDouble, 0.0);
	attrInToeZ = nAttr.create("toeZ", "toeZ", MFnNumericData::kDouble, 0.0);
	attrInToe = nAttr.create("toe", "toe", attrInToeX, attrInToeY, attrInToeZ);
	nAttr.setKeyable(true);
	nAttr.setStorable(true);
	nAttr.setWritable(true);

	createAttribute(attrInRoll, "roll", DefaultValue<double>());
	createAttribute(attrInBendLimitAngle, "bendLimitAngle", DefaultValue<double>());
	createAttribute(attrInToeLimitAngle, "toeLimitAngle", DefaultValue<double>());

	attrInTime = uAttr.create("inTime", "itm", MFnUnitAttribute::kTime);
	uAttr.setKeyable(true);
	uAttr.setReadable(false);

	// Output attributes
	attrOutUpdateX = nAttr.create("updateX", "updX", MFnNumericData::kDouble, 0.0);
	attrOutUpdateY = nAttr.create("updateY", "updY", MFnNumericData::kDouble, 0.0);
	attrOutUpdateZ = nAttr.create("updateZ", "updZ", MFnNumericData::kDouble, 0.0);
	attrOutUpdate = nAttr.create("update", "upd", attrOutUpdateX, attrOutUpdateY, attrOutUpdateZ);

	// Add attributes
	addAttributes(
		attrInBall, attrInAnkle, attrInHeel, attrInToe,
		attrInRoll, attrInBendLimitAngle, attrInToeLimitAngle, attrInTime,
		attrOutUpdate
	);

	return MS::kSuccess;
}


bool FootRollSolver::isPassiveOutput(const MPlug& plug) const {
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
	if (plug == attrOutUpdate) {return true;}
	return MPxNode::isPassiveOutput(plug);
}


MStatus FootRollSolver::parseDataBlock(MDataBlock& dataBlock) {
	/* Parse the data block and get all inputs.	*/
	MStatus status;

	// Ask for time value to force refresh on the node
	timeCurrent = dataBlock.inputValue(attrInTime, &status).asTime();
	// Asking for the actuall matrix input helps refreshing the rig if there are no anim curves
	matInAnkle = dataBlock.inputValue(attrInAnkle).asMatrix();
	matInBall = dataBlock.inputValue(attrInBall).asMatrix();
	posHeel = MVector(dataBlock.inputValue(attrInHeelX).asDouble(), dataBlock.inputValue(attrInHeelY).asDouble(),	dataBlock.inputValue(attrInHeelZ).asDouble());
	posToe = MVector(dataBlock.inputValue(attrInToeX).asDouble(), dataBlock.inputValue(attrInToeY).asDouble(),	dataBlock.inputValue(attrInToeZ).asDouble());

	// Ankle
	status = LMPlugin::parseTransformInput(dataBlock, objSelf, fnAnkle, attrInAnkle);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Ball
	status = LMPlugin::parseTransformInput(dataBlock, objSelf, fnBall, attrInBall);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Additional attributes
	MAngle::Unit uiAngleUnit = MAngle::uiUnit();
	roll = MAngle(dataBlock.inputValue(attrInRoll).asDouble(), uiAngleUnit);
	bendLimitAngle = MAngle(dataBlock.inputValue(attrInBendLimitAngle).asDouble(), uiAngleUnit);
	toeLimitAngle = MAngle(dataBlock.inputValue(attrInToeLimitAngle).asDouble(), uiAngleUnit);

	return MS::kSuccess;
}


MStatus FootRollSolver::solve() {
	/* Solves the node.
	*/
	MStatus status;

	// get heel location
	MVector posAnkle = fnAnkle.rotatePivot(MSpace::kWorld);
	MVector vecAnkleHeel = posAnkle - posHeel;

	// get ankle vector position
	// MGlobal::displayWarning(MString("roll: ") + std::to_string(roll.asRadians()).c_str());

	// heel - anklke pos = rotate pivot
	MQuaternion quatRoll(roll.asRadians(), MVector().zAxis);
	MQuaternion quatAnkle;
	fnAnkle.getRotation(quatAnkle, MSpace::kTransform);

	quatAnkle *= quatRoll;

	// set rotate pivot
	fnAnkle.setRotation(quatAnkle, MSpace::kTransform);

	// rotate by vector

	return MS::kSuccess;
}


MStatus FootRollSolver::updateOutput(const MPlug& plug, MDataBlock& dataBlock) {	
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

	dataBlock.setClean(plug);

	return MS::kSuccess;
}


MStatus FootRollSolver::compute(const MPlug& plug, MDataBlock& dataBlock) {
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
	status = parseDataBlock(dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// solve the node
	status = solve();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Set the output and data block clean
	status = updateOutput(plug, dataBlock);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Cache position and time
	timeCached = timeCurrent;

	return MS::kSuccess;
}


MStatus FootRollSolver::setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) {
	/* Sets the relation between attributes and marks the specified plugs dirty.

	Args:
		plugBeingDirtied (&MPlug): Plug which is being set dirty by Maya.
		affectedPlugs (&MPlugArray): The programmer should add any plugs which they want to set dirty
			to this list.

	*/
	if ( plugBeingDirtied == attrInBall
		|| plugBeingDirtied == attrInToe
		|| plugBeingDirtied == attrInAnkle
		|| plugBeingDirtied == attrInHeel
		|| plugBeingDirtied == attrInHeelX
		|| plugBeingDirtied == attrInHeelY
		|| plugBeingDirtied == attrInHeelZ
		|| plugBeingDirtied == attrInRoll
		|| plugBeingDirtied == attrInBendLimitAngle
		|| plugBeingDirtied == attrInToeLimitAngle
		|| plugBeingDirtied == attrInTime
	)	{
		affectedPlugs.append(MPlug(objSelf, attrOutUpdate));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateX));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateY));
		affectedPlugs.append(MPlug(objSelf, attrOutUpdateZ));
	}

	return MS::kSuccess;
}


void FootRollSolver::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const {
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


void FootRollSolver::postConstructor() {
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
