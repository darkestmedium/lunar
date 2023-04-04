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

// Function Sets
#include <maya/MFnMatrixAttribute.h>
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
#include <maya/MPxLocatorNode.h>
#include <maya/MPxDrawOverride.h>

// Custom
#include "api/Utils.h"
#include "api/LMAttribute.h"




// Node
class MetaDataNode : public MPxLocatorNode {
public:
	// Node Data
	static const MString typeName;
	static const MTypeId typeId;
	static const MString drawDbClassification;
	static const MString drawRegistrationId;

	// Node's Input Attributes
	static MObject AttrText;
	static MObject AttrTextPositionX;
	static MObject AttrTextPositionY;
	static MObject AttrTextSize;
	static MObject AttrTextColor;
	// Nodes's Output Attributes
	static MObject AttrOutUpdate;

	MObject SelfObj;

	// Constructors
	MetaDataNode()
		: MPxLocatorNode()
	{};
	// Destructors
	~MetaDataNode() override {};

	// Public methods - overrides
	static void* creator() {return new MetaDataNode();}
	static MStatus initialize();
	void getCacheSetup(
		const MEvaluationNode& evalNode,
		MNodeCacheDisablingInfo& disablingInfo,
		MNodeCacheSetupInfo& cacheSetupInfo,
		MObjectArray& monitoredAttributes
	) const override;
	void postConstructor() override;
	SchedulingType schedulingType() const override {return SchedulingType::kParallel;}
};



// User data
class MetaDataNodeData : public MUserData {
public:
	MString Text;
	MPoint TextPosition;
	int TextSize;
	MColor TextColor;

	// Constructors
	MetaDataNodeData() 
		: MUserData()
	{};  // Don't delete after draw
	// Destructor
	virtual ~MetaDataNodeData() override {};
};



// Draw override
class MetaDataNodeDrawOverride : public MHWRender::MPxDrawOverride {
public:
	// Constructors
	MetaDataNodeDrawOverride(const MObject& Object)
		: MHWRender::MPxDrawOverride(Object, nullptr)
	{};
	// Destructors
	virtual ~MetaDataNodeDrawOverride() override {};

	static MHWRender::MPxDrawOverride* creator(const MObject& Object) {return new MetaDataNodeDrawOverride(Object);}
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
};