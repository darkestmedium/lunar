#include "Ctrl.h"
#include "CtrlData.h"



// Public Data
const MString Ctrl::typeName("ctrl");
const MTypeId Ctrl::typeId(0x0066673);
const MString Ctrl::drawDbClassification("drawdb/geometry/ctrl");
const MString Ctrl::drawRegistrationId("ctrlNode");

// Nodes' Input Attributes
MObject Ctrl::localRotateX;
MObject Ctrl::localRotateY;
MObject Ctrl::localRotateZ;
MObject Ctrl::localRotate;

MObject Ctrl::shapeAttr;
MObject Ctrl::fillShapeAttr;
MObject Ctrl::fillTransparencyAttr;
MObject Ctrl::lineWidthAttr;

MObject Ctrl::attrInDrawLine;
Attribute Ctrl::attrInDrawLineTo;

MObject Ctrl::attrInDrawText;
MObject Ctrl::attrInTextPositionX;
MObject Ctrl::attrInTextPositionY;
MObject Ctrl::attrInTextPositionZ;
MObject Ctrl::attrInTextPosition;

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

	localRotateX = uAttr.create("localRotateX", "lrx", MFnUnitAttribute::kAngle, 0.0);
	localRotateY = uAttr.create("localRotateY", "lry", MFnUnitAttribute::kAngle, 0.0);
	localRotateZ = uAttr.create("localRotateZ", "lrz", MFnUnitAttribute::kAngle, 0.0);
	localRotate = nAttr.create("localRotate", "lr", localRotateX, localRotateY, localRotateZ);
	uAttr.setStorable(true);
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


	attrInDrawText = nAttr.create("drawText", "dt", MFnNumericData::kBoolean, false);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	attrInTextPositionX = nAttr.create("textPositionX", "tpx", MFnNumericData::kDouble, 0.0);
	attrInTextPositionY = nAttr.create("textPositionY", "tpy", MFnNumericData::kDouble, 0.0);
	attrInTextPositionZ = nAttr.create("textPositionZ", "tpz", MFnNumericData::kDouble, 0.0);
	attrInTextPosition = nAttr.create("textPosition", "tp", attrInTextPositionX, attrInTextPositionY, attrInTextPositionZ);
	nAttr.setStorable(true);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);

	attrInFkIk = nAttr.create("inFkIk", "ifi", MFnNumericData::kDouble);
	nAttr.setStorable(true);
	nAttr.setKeyable(false);
	nAttr.setChannelBox(true);



	// Add attributes
	addAttributes(
		localRotate, shapeAttr,	fillShapeAttr, fillTransparencyAttr, lineWidthAttr,
		attrInDrawLine, attrInDrawLineTo,
		attrInDrawText, attrInTextPosition,
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
