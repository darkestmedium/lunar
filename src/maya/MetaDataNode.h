#pragma once

// System Includes
#include <string>
#include <sstream>
#include <cassert>

// Maya General Includes
#include <maya/MGlobal.h>
#include <maya/MCallbackIdArray.h>
#include <maya/MSceneMessage.h>
#include <maya/MDagPath.h>
#include <maya/MMatrix.h>
#include <maya/MPlug.h>
#include <maya/MPoint.h>
#include <maya/MDataHandle.h>
#include <maya/MAnimControl.h>
#include <maya/MDrawRegistry.h>
#include <maya/MStringArray.h>
#include <maya/MEventMessage.h>

// Function Sets
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnData.h>
#include <maya/MFnDagNode.h>

// Iterators

// Viewport 2.0 Includes
#include <maya/MDrawRegistry.h>
#include <maya/MUserData.h>

// Proxies
#include <maya/MPxTransform.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MPxDrawOverride.h>

// Custom
#include "api/Utils.h"
#include "api/LMAttribute.h"




// Node
// class MetaDataNode : public MPxLocatorNode {
class MetaDataNode : public MPxTransform {
public:
	// Node Data
	static const MString type_name;
	static const MTypeId type_id;
	static const MString type_drawdb;
	static const MString type_drawid;

	// Node's Input Attributes
	static MObject attrInMetaData;
	static MObject attrInText;
	static MObject attrInDisplayInViewport;

	static MObject AttrTextPositionX;
	static MObject AttrTextPositionY;
	static MObject AttrTextSize;
	static MObject AttrTextColor;
	// Nodes's Output Attributes
	static MObject AttrOutUpdate;

	MObject self_object;

	// Constructors
	MetaDataNode()
		: MPxTransform()
	{};
	// Destructors
	virtual ~MetaDataNode() override {};

	// Public methods - overrides
	static void* 		creator() {return new MetaDataNode();}
	static MStatus	initialize();
	virtual void 		postConstructor() override;

	MStatus 				setDependentsDirty(const MPlug& plug, MPlugArray& affectedPlugs) override;
	void 						getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const override;
	SchedulingType 	schedulingType() const override {return SchedulingType::kParallel;}

	// bool 						isBounded() const override {return true;};
};



// User data
class MetaDataNodeData : public MUserData {
public:
	// MPlug arrayMetaData;
	unsigned int countMetaData;
	
	std::vector<MString> vectorText;
	MPoint TextPosition;
	int TextSize;
	MColor TextColor;

	// Constructors
	MetaDataNodeData() 
		: MUserData(false)
	{};  // Don't delete after draw
	// Destructor
	virtual ~MetaDataNodeData() override {};

	void getText(const MObject& obj);
};



// Draw override
class MetaDataDrawOverride : public MHWRender::MPxDrawOverride {
public:
	// Destructors
	virtual ~MetaDataDrawOverride() override 	{
		ptr_metadata = NULL; 
		if (fModelEditorChangedCbId != 0) {
			MMessage::removeCallback(fModelEditorChangedCbId);
			fModelEditorChangedCbId = 0;
		}
	};

	static MHWRender::MPxDrawOverride* creator(const MObject& Object) {return new MetaDataDrawOverride(Object);}
	virtual MHWRender::DrawAPI supportedDrawAPIs() const override {return MHWRender::kAllDevices;}
	virtual bool hasUIDrawables() const override {return true;}
	virtual void addUIDrawables(
		const MDagPath& objPath,
		MHWRender::MUIDrawManager& drawManager, 
		const MHWRender::MFrameContext& frameContext,
		const MUserData* data
	) override;
	virtual MUserData* prepareForDraw(
		const MDagPath& objPath,
		const MDagPath& cameraPath,
		const MHWRender::MFrameContext& frameContext,
		MUserData* oldData
	) override;

private:
	// Constructors
	MetaDataDrawOverride(const MObject& obj)
		: MHWRender::MPxDrawOverride(obj, nullptr, false)
		, ptr_metadata(nullptr)
	{
		fModelEditorChangedCbId = MEventMessage::addEventCallback("modelEditorChanged", OnModelEditorChanged, this);
		MStatus status;
		MFnDependencyNode fn_node(obj, &status);
		ptr_metadata = status ? dynamic_cast<MetaDataNode*>(fn_node.userNode()) : NULL;
	};

	MetaDataNode*	ptr_metadata;						// The node we are rendering
	MCallbackId 	fModelEditorChangedCbId;
	static void 	OnModelEditorChanged(void *clientData);

};
