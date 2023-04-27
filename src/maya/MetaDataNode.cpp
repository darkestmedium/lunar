#include "MetaDataNode.h"


// Public Data
const MString MetaDataNode::typeName = "metaData";
const MTypeId MetaDataNode::typeId = 0x0066675;
const MString MetaDataNode::drawDbClassification = "drawdb/geometry/metaData";
const MString MetaDataNode::drawRegistrationId = "metaDataNode";

// Node's Input Attributes
MObject MetaDataNode::attrInMetaData;
MObject MetaDataNode::attrInText;
MObject MetaDataNode::attrInDisplayInViewport;

MObject MetaDataNode::AttrTextPositionX;
MObject MetaDataNode::AttrTextPositionY;
MObject MetaDataNode::AttrTextSize;
MObject MetaDataNode::AttrTextColor;

// Nodes's Output Attributes
MObject MetaDataNode::AttrOutUpdate;




MStatus MetaDataNode::initialize() {
	MStatus status;
	MFnTypedAttribute AttrTyped;
	MFnNumericAttribute attrNum;
	MFnMatrixAttribute mAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;

	// Node's Input Attributes

	/* metaData:
	-- metaData
		 | -- text
	*/
	attrInText = AttrTyped.create("text", "txt", MFnData::kString);
	attrInDisplayInViewport = attrNum.create("displayInViewport", "divp", MFnNumericData::kBoolean);
	attrInMetaData = cAttr.create("metaData", "mdat");
	cAttr.addChild(attrInText);
	cAttr.addChild(attrInDisplayInViewport);
	cAttr.setArray(true);
	cAttr.setKeyable(false);
	cAttr.setReadable(false);

	AttrTextPositionX = attrNum.create("textPositionX", "tpX", MFnNumericData::kInt, 50);
	attrNum.setKeyable(false);
	attrNum.setChannelBox(true);
	attrNum.setStorable(true);
	attrNum.setWritable(true);
	attrNum.setMin(0);
	AttrTextPositionY = attrNum.create("textPositionY", "tpY", MFnNumericData::kInt, 50);
	attrNum.setKeyable(false);
	attrNum.setChannelBox(true);
	attrNum.setStorable(true);
	attrNum.setWritable(true);
	attrNum.setMin(0);
	AttrTextSize = attrNum.create("textSize", "txts", MFnNumericData::kInt, 12);
	attrNum.setKeyable(false);
	attrNum.setChannelBox(true);
	attrNum.setStorable(true);
	attrNum.setWritable(true);
	attrNum.setMin(9);
	attrNum.setMax(22);

	AttrTextColor = attrNum.createColor("textColor", "tcol");
	attrNum.setDefault(2.0f, 2.0f, 2.0f);

	addAttributes(attrInMetaData,	AttrTextPositionX, AttrTextPositionY,	AttrTextSize,	AttrTextColor);

	return MS::kSuccess;
}


void MetaDataNode::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const {
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


void MetaDataNode::postConstructor() {
	/* Post constructor.

	Internally maya creates two objects when a user defined node is created, the internal MObject and
	the user derived object. The association between the these two objects is not made until after the
	MPxNode constructor is called. This implies that no MPxNode member function can be called from the
	MPxNode constructor. The postConstructor will get called immediately after the constructor when it
	is safe to call any MPxNode member function.

	Reimplemented in MPxTransform, and MPxPolyTrg.

	*/
	SelfObj = thisMObject();

	MFnDependencyNode FnShape(SelfObj);
	FnShape.setName(MetaDataNode::typeName + "Shape");

	MPlug PlugVisibility(SelfObj, MetaDataNode::visibility);
	PlugVisibility.setChannelBox(true);

	MPlug plugLocalPositionX(SelfObj, MetaDataNode::localPositionX);
	MPlug plugLocalPositionY(SelfObj, MetaDataNode::localPositionY);
	MPlug plugLocalPositionZ(SelfObj, MetaDataNode::localPositionZ);
	MPlug plugLocalScaleX(SelfObj, MetaDataNode::localScaleX);
	MPlug plugLocalScaleY(SelfObj, MetaDataNode::localScaleY);
	MPlug plugLocalScaleZ(SelfObj, MetaDataNode::localScaleZ);

	LMAttribute::lockAndHideAttr(plugLocalPositionX);
	LMAttribute::lockAndHideAttr(plugLocalPositionY);
	LMAttribute::lockAndHideAttr(plugLocalPositionZ);
	LMAttribute::lockAndHideAttr(plugLocalScaleX);
	LMAttribute::lockAndHideAttr(plugLocalScaleY);
	LMAttribute::lockAndHideAttr(plugLocalScaleZ);
}


void MetaDataNodeData::getText(const MObject& obj) {
	/*Gets the string array from metaData attribute
	*/

	MPlug arrayMetaData = MPlug(obj, MetaDataNode::attrInMetaData);
	countMetaData = arrayMetaData.numElements();
	vectorText.clear();
	if (countMetaData > 0) {
		for (unsigned int i = 0; i < countMetaData; ++i) {
			bool displayText = arrayMetaData.elementByPhysicalIndex(i).child(1).asBool();
			if (displayText) {
				vectorText.push_back(arrayMetaData.elementByPhysicalIndex(i).child(0).asString());
			}
		}
		std::reverse(vectorText.begin(), vectorText.end());
	}
}


MUserData* MetaDataNodeDrawOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath, const MHWRender::MFrameContext& frameContext, MUserData* oldData) {
	/* Called by Maya whenever the object is dirty and needs to update for draw.

	Any data needed from the Maya dependency graph must be retrieved and cached in this
	stage. It is invalid to pull data from the Maya dependency graph in the draw callback
	method and Maya may become unstable if that is attempted.

	Implementors may allow Maya to handle the data caching by returning a pointer to the
	data from this method. The pointer must be to a class derived from MUserData. This
	same pointer will be passed to the draw callback. On subsequent draws, the pointer
	will also be passed back into this method so that the data may be modified and reused
	instead of reallocated. If a different pointer is returned Maya will delete the old
	data. If the cache should not be maintained between draws, set the delete after use
	flag on the user data and Maya will delete it in a certain stage depending on whether
	the draw callback exists. If exists, the user data will be deleted after both
	addUIDrawables() and the draw callback are called; otherwise, the user data will be
	deleted immediately after addUIDrawables() is called. In all cases, the lifetime and
	ownership of the user data is handled by Maya and the user cshould not try to delete
	the data themselves. Data caching occurs per-instance of the associated DAG object.
	The lifetime of the user data can be longer than the associated node, instance or
	draw override. Due to internal caching, the user data can be deleted after an
	arbitrary long time. One should therefore be careful to not access stale objects from
	the user data destructor. If it is not desirable to allow Maya to handle data caching,
	simply return NULL in this method and ignore the user data parameter in the draw
	callback method.

	Args:
		objPath (MDagPath&): The path to the object being drawn
		cameraPath (MDagPath&): The path to the camera that is being used to draw
		frameContext (MHWRender::MFrameContext&): Frame level context information
		oldData (MUserData*) Data cached by the previous draw of the instance

	Returns:
		MUserData*: Pointer to data to be passed to the draw callback method

	*/
	MStatus status;

	MetaDataNodeData* data = dynamic_cast<MetaDataNodeData*>(oldData);
	MObject ObjNode = objPath.node(&status);

	if (!data) {data=new MetaDataNodeData;}

	data->getText(ObjNode);

	data->TextSize = MPlug(ObjNode, MetaDataNode::AttrTextSize).asInt();
	data->TextPosition = MPoint(
		MPlug(ObjNode, MetaDataNode::AttrTextPositionX).asInt(),
		MPlug(ObjNode, MetaDataNode::AttrTextPositionY).asInt() - 20
	);
	MPlug PlugColor(ObjNode, MetaDataNode::AttrTextColor);
	data->TextColor = MColor(
		PlugColor.child(0).asFloat(),
		PlugColor.child(1).asFloat(),
		PlugColor.child(2).asFloat()
	);

	return data;
}


void MetaDataNodeDrawOverride::addUIDrawables(const MDagPath& objPath, MHWRender::MUIDrawManager& drawManager, const MHWRender::MFrameContext& frameContext, const MUserData* data) {
	/* Provides access to the MUIDrawManager, which can be used to queue up operations to draw simple
	UI shapes like lines, circles, text, etc.

	This method will only be called when this override is dirty and its hasUIDrawables()
	is overridden to return true. This method is called after prepareForDraw() and carries
	the same restrictions on the sorts of operations it can perform.

	Args:
		objPath (MDagPath&): The path to the object being drawn.
		drawManager (MHWRender::MUIDrawManager&): The UI draw manager, it can be used to draw some simple
			geometry including text.
		frameContext (MHWRender::MFrameContext&): Frame level context information.
		data (MUserData*): Data cached by prepareForDraw().

	*/
	MetaDataNodeData* pMetaDataNodeData = (MetaDataNodeData*)data;
	if (!pMetaDataNodeData) {return;}

	drawManager.beginDrawable(MHWRender::MUIDrawManager::kNonSelectable);

	drawManager.setColor(pMetaDataNodeData->TextColor);
	drawManager.setFontSize(pMetaDataNodeData->TextSize);

	// Render text if string array is not empty
	if (pMetaDataNodeData->vectorText.size() > 0 ) {
		for (unsigned int i = 0; i < pMetaDataNodeData->vectorText.size(); ++i) {
			drawManager.text2d(
				pMetaDataNodeData->TextPosition += MPoint(0, 20, 0),
				pMetaDataNodeData->vectorText[i],
				MUIDrawManager::kLeft
			);
		}
	}

	drawManager.endDrawable();
}