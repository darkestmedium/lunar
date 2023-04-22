#include "Ctrl.h"
#include "CtrlData.h"



// Public Data
const MString Ctrl::typeName("ctrl");
const MTypeId Ctrl::typeId(0x0066673);
const MString Ctrl::drawDbClassification("drawdb/geometry/ctrl");
const MString Ctrl::drawRegistrationId("ctrlNode");

// Nodes' Input Attributes
MObject Ctrl::localRotateX, Ctrl::localRotateY, Ctrl::localRotateZ, Ctrl::localRotate;

MObject Ctrl::shapeAttr;
MObject Ctrl::fillShapeAttr;
MObject Ctrl::fillTransparencyAttr;
MObject Ctrl::lineWidthAttr;

MObject Ctrl::attrInDrawLine;
Attribute Ctrl::attrInDrawLineTo;

MObject Ctrl::attrInDrawFkIkState;
MObject Ctrl::attrInFkIkPositionX, Ctrl::attrInFkIkPositionY, Ctrl::attrInFkIkPositionZ, Ctrl::attrInFkIkPosition;

MObject Ctrl::attrInFkIk;


// Nodes's Output Attributes



MStatus Ctrl::initialize() {
	/* Node Initializer.

	This method initializes the node, and should be overridden in user-defined
	nodes.

	Returns:
		status code (MStatus): kSuccess if the operation was successful, kFailure if an	error occured
			during the operation

	*/
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;
	MFnTypedAttribute tAttr;
	MFnEnumAttribute eAttr;

	localRotateX = uAttr.create("localRotateX", "lrX", MFnUnitAttribute::kAngle, 0.0);
	localRotateY = uAttr.create("localRotateY", "lrY", MFnUnitAttribute::kAngle, 0.0);
	localRotateZ = uAttr.create("localRotateZ", "lrZ", MFnUnitAttribute::kAngle, 0.0);
	localRotate = nAttr.create("localRotate", "lr", localRotateX, localRotateY, localRotateZ);
	nAttr.setStorable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	shapeAttr = eAttr.create("shape", "shp");
	eAttr.addField("Cube", 0);
	eAttr.addField("Sphere", 1);
	eAttr.addField("Cross", 2);
	eAttr.addField("Diamond", 3);
	eAttr.addField("Square", 4);
	eAttr.addField("Circle", 5);
	eAttr.addField("Locator", 6);
	eAttr.addField("Line", 7);
	eAttr.addField("None", 8);
	eAttr.setKeyable(false);
	eAttr.setStorable(true);
	eAttr.setChannelBox(true);

	fillShapeAttr = nAttr.create("fillShape", "fs", MFnNumericData::kBoolean, true);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	attrInDrawLine = nAttr.create("drawLine", "dl", MFnNumericData::kBoolean, false);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	createAttribute(attrInDrawLineTo, "drawLineTo", DefaultValue<MMatrix>());

	fillTransparencyAttr = nAttr.create("fillTransparency", "ft", MFnNumericData::kDouble);
	nAttr.setMin(0.1);
	nAttr.setDefault(0.25);
	nAttr.setMax(1.0);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	lineWidthAttr = nAttr.create("lineWidth", "lw", MFnNumericData::kDouble);
	nAttr.setMin(0.5);
	nAttr.setDefault(1.0);
	nAttr.setMax(5);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);


	attrInDrawFkIkState = nAttr.create("drawFkIkState", "dfis", MFnNumericData::kBoolean, false);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	attrInFkIkPositionX = nAttr.create("fkIkStatePositionX", "fispx", MFnNumericData::kDouble, 0.0);
	attrInFkIkPositionY = nAttr.create("fkIkStatePositionY", "fispy", MFnNumericData::kDouble, 0.0);
	attrInFkIkPositionZ = nAttr.create("fkIkStatePositionZ", "fispz", MFnNumericData::kDouble, 0.0);
	attrInFkIkPosition = nAttr.create("fkIkStatePosition", "fisp", attrInFkIkPositionX, attrInFkIkPositionY, attrInFkIkPositionZ);
	nAttr.setStorable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	attrInFkIk = nAttr.create("fkIk", "fkIk", MFnNumericData::kDouble);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);
	nAttr.setMin(0.0);
	nAttr.setMax(100.0);


	// Add attributes
	addAttributes(
		localRotate,
		shapeAttr, fillShapeAttr, fillTransparencyAttr, lineWidthAttr,
		attrInDrawLine, attrInDrawLineTo,
		attrInDrawFkIkState, attrInFkIkPosition,
		attrInFkIk
	);

	return MS::kSuccess;
}


MBoundingBox Ctrl::boundingBox() const {
	/* This method should be overridden to return a bounding box for the locator.

	If this method is overridden, then MPxLocatorNode::isBounded should also be overridden
	to return true.

	Returns:
		MBoundingBox: The bounding box of the locator

	*/
	CtrlData data;

	data.getPlugs(objSelf);
	data.getBBox(objSelf, pathSelf, data.matLocalShape);

	return data.bBox;
}


void Ctrl::getCacheSetup(
	const MEvaluationNode& evalNode,
	MNodeCacheDisablingInfo& disablingInfo,
	MNodeCacheSetupInfo& cacheSetupInfo,
	MObjectArray& monitoredAttributes
	) const
{
	/*Disables Cached Playback support by default.

	Built-in locators all enable Cached Playback by default, but plug-ins have to
	explicitly enable it by overriding this method.
	This method should be overridden to enable Cached Playback by default for custom locators.

	Args:
		evalNode (MEvaluationNode&): This node's evaluation node, contains animated plug information
		disablingInfo (MNodeCacheDisablingInfo&): Information about why the node disables caching to be reported to the user
		cacheSetup (MNodeCacheSetupInfo&): Preferences and requirements this node has for caching
		monitoredAttribures (MObjectArray&): Attributes impacting the behavior of this method that will be monitored for change

	*/
	MPxLocatorNode::getCacheSetup(evalNode, disablingInfo, cacheSetupInfo, monitoredAttributes);
	assert(!disablingInfo.getCacheDisabled());
	cacheSetupInfo.setPreference(MNodeCacheSetupInfo::kWantToCacheByDefault, true);
}


void Ctrl::postConstructor() {
	/* Post constructor.

	Internally maya creates two objects when a user defined node is created, the internal
	MObject and the user derived object. The association between the these two objects is
	not made until after the MPxNode constructor is called. This implies that no MPxNode
	member function can be called from the MPxNode constructor. The postConstructor will
	get called immediately after the constructor when it is safe to call any MPxNode
	member function.

	*/
	objSelf = thisMObject();
	MDagPath::getAPathTo(objSelf, pathSelf);
	MFnDependencyNode thisFn(objSelf);
	thisFn.setName(Ctrl::typeName + "Shape");

	MPlug hideOnPlaybackPlug = thisFn.findPlug("hideOnPlayback", false);
	hideOnPlaybackPlug.setBool(1);

	// Set color
	MPlug overrideEnabledPlug = thisFn.findPlug("overrideEnabled", false);
	overrideEnabledPlug.setBool(1);
	MPlug overrideRGBColorsPlug = thisFn.findPlug("overrideRGBColors", false);
	overrideRGBColorsPlug.setBool(1);

	MPlug overrideColorR = thisFn.findPlug("overrideColorR", false);
	overrideColorR.setDouble(1.0);
	MPlug overrideColorG = thisFn.findPlug("overrideColorG", false);
	overrideColorG.setDouble(1.0);
	MPlug overrideColorB = thisFn.findPlug("overrideColorB", false);
	overrideColorB.setDouble(0.25);
}
