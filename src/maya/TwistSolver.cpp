#include "TwistSolver.h"


// #include <maya/MAngle.h>
// #include <maya/MAnimControl.h>
// #include <maya/MArrayDataBuilder.h>
// #include <maya/MDagPath.h>
// #include <maya/MDataBlock.h>
// #include <maya/MDataHandle.h>
// #include <maya/MFnAnimCurve.h>
// #include <maya/MFnCompoundAttribute.h>
// #include <maya/MFnEnumAttribute.h>
// #include <maya/MFnMatrixAttribute.h>
// #include <maya/MFnNumericAttribute.h>
// #include <maya/MFnPlugin.h>
// #include <maya/MFnUnitAttribute.h>
// #include <maya/MGlobal.h>
// #include <maya/MMatrix.h>
// #include <maya/MPlug.h>
// #include <maya/MPlugArray.h>
// #include <maya/MPxNode.h>
// #include <maya/MQuaternion.h>
// #include <maya/MRampAttribute.h>
// #include <maya/MTransformationMatrix.h>
// #include <maya/MVector.h>
// #include <maya/MTypeId.h>



// ---------------------------------------------------------------------
// main
// ---------------------------------------------------------------------

// Public Data
const MString TwistSolver::typeName = "twistSolver";
const MTypeId TwistSolver::typeId = 0x0066677;

MObject TwistSolver::active;
MObject TwistSolver::autoRegulate;
MObject TwistSolver::axis;
MObject TwistSolver::extend;
MObject TwistSolver::inputMatrix;
MObject TwistSolver::invertTwist;
MObject TwistSolver::offset;
MObject TwistSolver::poseVector;
MObject TwistSolver::regulationAngle;
MObject TwistSolver::restMatrix;
MObject TwistSolver::reverseSegments;
MObject TwistSolver::scale;
MObject TwistSolver::segmentBlend;
MObject TwistSolver::transformIndex;
MObject TwistSolver::twist;
MObject TwistSolver::twistInput;
MObject TwistSolver::twistReference;
MObject TwistSolver::twistSegmentOut;
MObject TwistSolver::useCurve;
MObject TwistSolver::segmentCount;




MStatus TwistSolver::initialize() {
	//
	// MFnEnumAttribute
	//

	MFnEnumAttribute eAttr;

	axis = eAttr.create("axis", "ax", 0);
	eAttr.addField("X", 0);
	eAttr.addField("Y", 1);
	eAttr.addField("Z", 2);

	//
	// MFnNumericAttribute
	//

	MFnNumericAttribute nAttr;

	active = nAttr.create("active", "ac", MFnNumericData::kBoolean);
	nAttr.setKeyable(true);
	nAttr.setDefault(true);

	segmentCount = nAttr.create("segmentCount", "sc", MFnNumericData::kLong);
	nAttr.setKeyable(true);
	nAttr.setMin(1);
	nAttr.setDefault(1);

	invertTwist = nAttr.create("invertTwist", "it", MFnNumericData::kBoolean);
	nAttr.setKeyable(true);
	nAttr.setDefault(false);

	offset = nAttr.create("offset", "of", MFnNumericData::kDouble);
	nAttr.setKeyable(true);
	nAttr.setDefault(0.0);
	nAttr.setSoftMin(-90.0);
	nAttr.setSoftMax(90.0);

	scale = nAttr.create("scale", "s", MFnNumericData::kDouble);
	nAttr.setKeyable(true);
	nAttr.setDefault(1.0);
	nAttr.setSoftMin(0.0);
	nAttr.setSoftMax(2.0);

	reverseSegments = nAttr.create("reverseSegments", "rs", MFnNumericData::kBoolean);
	nAttr.setKeyable(true);
	nAttr.setDefault(false);

	useCurve = nAttr.create("useCurve", "uc", MFnNumericData::kBoolean);
	nAttr.setKeyable(true);
	nAttr.setDefault(false);

	extend = nAttr.create("extend", "ext", MFnNumericData::kBoolean);
	nAttr.setKeyable(false);
	nAttr.setHidden(true);
	nAttr.setDefault(true);

	poseVector = nAttr.create("poseVector", "pv", MFnNumericData::k3Double);
	nAttr.setHidden(true);

	autoRegulate = nAttr.create("autoRegulate", "ar", MFnNumericData::kBoolean);
	nAttr.setKeyable(true);
	nAttr.setDefault(true);

	regulationAngle = nAttr.create("regulationAngle", "ra", MFnNumericData::kDouble);
	nAttr.setKeyable(false);
	nAttr.setHidden(false);
	nAttr.setDefault(45.0);

	transformIndex = nAttr.create("transformIndex", "tid", MFnNumericData::kLong);
	nAttr.setKeyable(true);
	nAttr.setMin(0);
	nAttr.setDefault(0);

	//
	// MFnUnitAttribute
	//

	MFnUnitAttribute uAttr;

	twist = uAttr.create("twist", "tw", MFnUnitAttribute::kAngle);
	uAttr.setKeyable(false);
	uAttr.setDefault(0.0);

	twistSegmentOut = uAttr.create("twistSegmentOut", "tso", MFnUnitAttribute::kAngle);
	uAttr.setKeyable(false);
	uAttr.setArray(true);
	uAttr.setUsesArrayDataBuilder(true);

	twistInput = uAttr.create("twistInput", "ti", MFnUnitAttribute::kAngle);
	uAttr.setKeyable(false);
	uAttr.setArray(true);
	uAttr.setUsesArrayDataBuilder(true);

	twistReference = uAttr.create("twistReference", "tr", MFnUnitAttribute::kAngle);
	uAttr.setKeyable(false);
	uAttr.setHidden(true);
	uAttr.setDefault(0.0);

	//
	// MFnMatrixAttribute
	//

	MFnMatrixAttribute mAttr;

	inputMatrix = mAttr.create("inputMatrix", "im");
	mAttr.setHidden(true);

	restMatrix = mAttr.create("restMatrix", "rm");
	mAttr.setHidden(true);

	//
	// MRampAttribute
	//

	MRampAttribute rAttr;

	segmentBlend = rAttr.createCurveRamp("segmentBlend", "sb");

	// -----------------------------------------------------------------
	// add attributes (order matters)
	// -----------------------------------------------------------------

	addAttribute(active);
	addAttribute(inputMatrix);
	addAttribute(restMatrix);
	addAttribute(axis);
	addAttribute(twist);
	addAttribute(segmentCount);
	addAttribute(invertTwist);
	addAttribute(offset);
	addAttribute(scale);
	addAttribute(reverseSegments);
	addAttribute(useCurve);
	addAttribute(segmentBlend);
	addAttribute(twistSegmentOut);
	addAttribute(extend);
	addAttribute(poseVector);
	addAttribute(twistInput);
	addAttribute(transformIndex);
	addAttribute(twistReference);
	addAttribute(autoRegulate);
	addAttribute(regulationAngle);

	// -----------------------------------------------------------------
	// affects
	// -----------------------------------------------------------------

	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(active));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(axis));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(extend));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(inputMatrix));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(invertTwist));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(offset));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(restMatrix));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(reverseSegments));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(scale));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(segmentBlend));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(segmentCount));
	CHECK_MSTATUS_AND_RETURN_IT(affectsOutput(useCurve));

	return MS::kSuccess;
}


MStatus TwistSolver::affectsOutput(MObject &attr) {
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(attr, TwistSolver::twist));
	CHECK_MSTATUS_AND_RETURN_IT(attributeAffects(attr, TwistSolver::twistSegmentOut));

	return MStatus::kSuccess;
}

MStatus TwistSolver::postConstructor_init_curveRamp(MObject &nodeObj,	MObject &rampObj, int index, float position, float value,	int interpolation) {
	MStatus status;

	MPlug rampPlug(nodeObj, rampObj);
	MPlug elementPlug = rampPlug.elementByLogicalIndex((unsigned)index, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MPlug positionPlug = elementPlug.child(0, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	status = positionPlug.setFloat(position);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MPlug valuePlug = elementPlug.child(1);
	status = valuePlug.setFloat(value);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MPlug interpolationPlug = elementPlug.child(2);
	interpolationPlug.setInt(interpolation);

	return MS::kSuccess;
}


// ---------------------------------------------------------------------
// compute
// ---------------------------------------------------------------------

MStatus TwistSolver::compute(const MPlug &plug, MDataBlock& dataBlock) {
	MStatus status = MS::kSuccess;

	MObject objSelf = this->thisMObject();

	// -----------------------------------------------------------------
	// attributes
	// -----------------------------------------------------------------

	MDataHandle autoRegulateData = dataBlock.inputValue(autoRegulate, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool regulateVal = autoRegulateData.asBool();

	MDataHandle activeData = dataBlock.inputValue(active, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool activeVal = activeData.asBool();

	MDataHandle axisData = dataBlock.inputValue(axis, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	int axisVal = axisData.asShort();

	MDataHandle extendData = dataBlock.inputValue(extend, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool extendVal = extendData.asBool();

	MDataHandle invertTwistData = dataBlock.inputValue(invertTwist, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool invertVal = invertTwistData.asBool();

	MDataHandle offsetData = dataBlock.inputValue(offset, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	double offsetVal = offsetData.asDouble();

	MDataHandle regulationAngleData = dataBlock.inputValue(regulationAngle, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	double regulationAngleVal = regulationAngleData.asDouble();

	MDataHandle reverseSegmentsData = dataBlock.inputValue(reverseSegments, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool reverseVal = reverseSegmentsData.asBool();

	MDataHandle scaleData = dataBlock.inputValue(scale, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	double scaleVal = scaleData.asDouble();

	MDataHandle segmentCountData = dataBlock.inputValue(segmentCount, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	int countVal = segmentCountData.asShort();

	MDataHandle transformIndexData = dataBlock.inputValue(transformIndex, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	int transformIndexVal = transformIndexData.asShort();

	MDataHandle twistReferenceData = dataBlock.inputValue(twistReference, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	double twistRefVal = twistReferenceData.asAngle().asDegrees();

	MDataHandle useCurveData = dataBlock.inputValue(useCurve, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	bool useCurveVal = useCurveData.asBool();

	MRampAttribute blendAttr = MRampAttribute(objSelf, segmentBlend, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MDataHandle poseDataHandle = dataBlock.inputValue(poseVector, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	double3& poseVal = poseDataHandle.asDouble3();

	// -----------------------------------------------------------------
	// plugs
	// -----------------------------------------------------------------

	MPlug matrixPlug(objSelf, TwistSolver::inputMatrix);
	MPlug twistInputPlug(objSelf, TwistSolver::twistInput);
	MPlug twistPlug(objSelf, TwistSolver::twist);
	MPlug twistReferencePlug(objSelf, TwistSolver::twistReference);

	// -----------------------------------------------------------------
	// check if the node should be computed
	// -----------------------------------------------------------------

	// Deactivate the node if the state is set to HasNoEffect.
	MDataHandle stateData = dataBlock.inputValue(state, &status);
	if (stateData.asShort() == 1)
		return status;

	// -----------------------------------------------------------------
	// get the input twist reference
	// -----------------------------------------------------------------

	MIntArray twistInputIds;

	twistInputPlug.getExistingArrayAttributeIndices(twistInputIds, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	MArrayDataHandle twistInputHandle = dataBlock.inputArrayValue(twistInput, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	unsigned int inputCount = twistInputIds.length();

	MPlug animPlug;
	bool isConnected = false;

	if (inputCount > 0)
	{
		// Check if the current transform index matches one of the
		// existing attribute ids.
		bool exists = false;
		for (unsigned int i = 0; i < inputCount; i ++)
		{
			if (twistInputIds[i] == transformIndexVal)
			{
				exists = true;
				break;
			}
		}

		if (exists)
		{
			MPlug inPlug = twistInputPlug.connectionByPhysicalIndex((unsigned)transformIndexVal);

			// If the input is animated replace the internal twist
			// reference with the twist input value.
			// This also returns the attribute on the transform node and
			// if the twist input index is actually connected.
			// This is important for setting the twist value on the
			// transform node.
			bool animated = isAnimated(inPlug, animPlug, isConnected);
			if (animated)
			{
				status = twistInputHandle.jumpToArrayElement((unsigned)transformIndexVal);
				CHECK_MSTATUS_AND_RETURN_IT(status);
				twistRefVal = twistInputHandle.inputValue().asAngle().asDegrees();
			}
		}
	}

	// -----------------------------------------------------------------
	// get the input and rest matrix dataBlock
	// -----------------------------------------------------------------

	MDataHandle matrixHandle = dataBlock.inputValue(inputMatrix, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MMatrix inputMat = matrixHandle.asMatrix();

	MDataHandle restHandle = dataBlock.inputValue(restMatrix, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	MMatrix restMat = restHandle.asMatrix();

	// -----------------------------------------------------------------
	// get the parent matrix
	// -----------------------------------------------------------------

	MPlugArray plugConn;
	matrixPlug.connectedTo(plugConn, true, false, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// cancel, if the matrix is not connected
	if (!plugConn.length())
		return status;
	MDagPath dagPath;
	MDagPath::getAPathTo(plugConn[0].node(), dagPath);
	MMatrix parentMatInv = dagPath.exclusiveMatrixInverse();

	// -----------------------------------------------------------------
	// get the quaternions
	// -----------------------------------------------------------------

	MTransformationMatrix inputTransMat = inputMat * parentMatInv;
	MQuaternion quatInput = inputTransMat.rotation();

	MTransformationMatrix restTransMat = restMat;
	MQuaternion quatRest = restTransMat.rotation();

	// -----------------------------------------------------------------
	// main calculation
	// -----------------------------------------------------------------

	MQuaternion quat;
	MVector pose(1.0, 0.0, 0.0);

	double twistVal = 0.0;

	if (activeVal)
	{
		// Build the relative quaternion.
		quat = quatInput * quatRest.conjugate();

		// The current issue with tracking the rotation is that larger
		// changes to the current orientation can lead to false results
		// due to the twist reference value which is mandatory for the
		// tracking to work. For example, setting the joint back to the
		// default pose from large rotation values usually leaves the
		// twist at 360. To reduce this problem a delta angle between
		// the current pose vector and the previous pose gets
		// calculated. Usually during animation or manual interaction
		// this angle is rather small but if rotation changes with
		// larger values occur this angle gets larger as well.
		// If the given angle (default 45 degrees) is exceeded the
		// reference value gets modified/reduced to a remainder of 180,
		// which should be sufficient in most cases.
		if (extendVal && regulateVal)
		{
			// Define the reference vector base.
			if (axisVal == 1)
				pose = MVector(0.0, 1.0, 0.0);
			else if (axisVal == 2)
				pose = MVector(0.0, 0.0, 1.0);

			// Transform the pose based on the current orientation.
			pose *= inputTransMat.asMatrix();

			// Compare with the last pose and modify the reference value
			// if needed.
			double delta = pose.angle(MVector(poseVal[0], poseVal[1], poseVal[2])) * RADTODEG;
			if (delta > regulationAngleVal)
				twistRefVal = fmod(twistRefVal, 180.0);
		}

		twistVal = getTwistAngle(quat, axisVal);
		if (invertVal)
			twistVal *= -1;

		if (extendVal)
			twistVal = trackRotation(twistVal, twistRefVal);
	}

	// -----------------------------------------------------------------
	// pass the pose value to the output
	// -----------------------------------------------------------------

	// twist
	dataBlock.outputValue(twistPlug).set(MAngle((twistVal * scaleVal) + offsetVal, MAngle::kDegrees));
	dataBlock.outputValue(twistReferencePlug).set(MAngle(twistVal, MAngle::kDegrees));

	// pose vector
	dataBlock.outputValue(poseVector).set3Double(pose.x, pose.y, pose.z);

	// Set the twist reference on the transform node.
	if (isConnected) {
		MAngle animAngle(twistVal, MAngle::kDegrees);
		animPlug.setMAngle(animAngle);
	}

	// -----------------------------------------------------------------
	// segments
	// -----------------------------------------------------------------

	// twist segment
	MArrayDataHandle twistHandle = dataBlock.outputArrayValue(twistSegmentOut);
	MArrayDataBuilder twistBuilder(&dataBlock, twistSegmentOut, (unsigned)countVal);

	// Use different cases for non-curve-based and curve-based segment.
	// Though it duplicates some parts it's easier to manage the
	// different approaches to calculate the segments.
	if (!useCurveVal) {
		double twistSubVal = twistVal * scaleVal * (1.0 / countVal);
		double twistInc = twistSubVal;
		if (reverseVal) {
			twistInc = twistVal * scaleVal;
			twistSubVal *= -1;
		}

		for (unsigned int i = 0; i < (unsigned)countVal; i ++) {
			MDataHandle twistIdHandle = twistBuilder.addElement(i);
			twistIdHandle.set(MAngle(twistInc + offsetVal, MAngle::kDegrees));
			twistHandle.set(twistBuilder);
			twistHandle.setAllClean();

			twistInc += twistSubVal;
		}
	}	else {
		float subStep = (float)(1.0 / countVal);

		for (unsigned int i = 0; i < (unsigned)countVal; i ++) {
			int stepMult = (int)(i + 1);
			if (reverseVal)
				stepMult = countVal - (int)i;

			float curveVal;
			blendAttr.getValueAtPosition(subStep * stepMult, curveVal);
			double subVal = twistVal * curveVal * scaleVal;

			MDataHandle twistIdHandle = twistBuilder.addElement(i);
			twistIdHandle.set(MAngle(subVal + offsetVal, MAngle::kDegrees));
			twistHandle.set(twistBuilder);
			twistHandle.setAllClean();
		}
	}

	dataBlock.setClean(plug);

	return MStatus::kSuccess;
}


double TwistSolver::getTwistAngle(MQuaternion quat,	int axis) {
	/* Calculate the twist angle based on the given rotate order.

	Args:
		quat (MQuaternion): The rotation quaternion.
		axis (int): The rotation axis.
	Returns:
		double: The twist angle.

	*/
	double axisComponent = quat.x;
	if (axis == 1)
		axisComponent = quat.y;
	else if (axis == 2)
		axisComponent = quat.z;

	return RADTODEG * (2.0 * atan2(axisComponent, quat.w));
}


double TwistSolver::trackRotation(double twistValue, double reference) {
	/* Return the twist value based on the given reference angle.

	Args:
		twistValue (double): The current twist value.
		reference (double): The reference angle.
	Returns:
		double: The expanded twist angle.

	*/
	// Get the relative twist based on the current angle and the last
	// angle.
	double relativeTwist = reference - twistValue;

	// Expand the angle range beyond 360 degrees based on the reference
	// value.
	int cycle = 0;
	remquo(relativeTwist, 360.0, &cycle);
	twistValue = twistValue + 360 * cycle;

	return twistValue;
}


bool TwistSolver::isAnimated(MPlug plug, MPlug& animPlug, bool& isConnected) {
	/* Return if the given plug is animated.

	Args:
		plug (MPlug): The MPlug to check for an animation.
		animPlug (MPlug&): The source MPlug of the connection.
		isConnected (bool&): Returns true, if the plug is connected.

	Returns:
		bool: True, if the given plug is animated.

	*/
	MStatus status = MS::kSuccess;
	bool animated = false;
	MPlugArray plugArray;

	// First check if the current twistInput plug is connected (to a
	// transform node)
	plug.connectedTo(plugArray, true, false, &status);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	if (plugArray.length())	{
		isConnected = true;
		animPlug = plugArray[0];

		// Check if the TwistSolver attribute on the transform node is
		// driven by an animation curve.
		plugArray[0].connectedTo(plugArray, true, false, &status);
		CHECK_MSTATUS_AND_RETURN(status, false);

		if (plugArray.length())	{
			MObject animObj = plugArray[0].node();

			if (animObj.hasFn(MFn::kAnimCurve))	{
				MFnAnimCurve animFn(animObj);

				unsigned int numKeys = animFn.numKeys();
				MTime keyTimeFirst = animFn.time(0, &status);
				CHECK_MSTATUS_AND_RETURN(status, false);
				MTime keyTimeLast = animFn.time(numKeys - 1, &status);
				CHECK_MSTATUS_AND_RETURN(status, false);

				MTime currentTime = MAnimControl::currentTime();

				if (currentTime >= keyTimeFirst && currentTime <= keyTimeLast)
					animated = true;
			}
		}
	}

	return animated;
}


void TwistSolver::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const {
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


void TwistSolver::postConstructor() {
	/* Post constructor.

	Internally maya creates two objects when a user defined node is created, the internal MObject and
	the user derived object. The association between the these two objects is not made until after the
	MPxNode constructor is called. This implies that no MPxNode member function can be called from the
	MPxNode constructor. The postConstructor will get called immediately after the constructor when it
	is safe to call any MPxNode member function.

	Reimplemented in MPxTransform, and MPxPolyTrg.

	*/
	MObject objSelf = thisMObject();

	// One entry is the least needed or the attribute editor will
	// produce an error.
	postConstructor_init_curveRamp(objSelf, segmentBlend, 0, 0.0f, 0.0f, 1);
	postConstructor_init_curveRamp(objSelf, segmentBlend, 1, 1.0f, 1.0f, 1);
}
