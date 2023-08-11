// ==========================================================================
// Copyright 2019 Autodesk, Inc.  All rights reserved.
// Use of this software is subject to the terms of the Autodesk license agreement
// provided at the time of installation or download, or which otherwise
// accompanies this software in either electronic or hard copy form.
// ==========================================================================
#pragma once

// System includes
#include <math.h>
#include <cassert>
#include <memory>
#include <unordered_map>
#include <atomic>

#include <maya/MUserData.h>
#include <maya/MMatrix.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MColor.h>
// #include <maya/MFnPlugin.h>
#include <maya/MDistance.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MGlobal.h>
#include <maya/MDagMessage.h>
#include <maya/MEvaluationManager.h>
#include <maya/MEvaluationNode.h>
#include <maya/MEventMessage.h>

// Function sets
#include <maya/MFnEnumAttribute.h>

// Viewport 2.0 includes
#include <maya/MDrawRegistry.h>
#include <maya/MPxGeometryOverride.h>
#include <maya/MShaderManager.h>
#include <maya/MHWGeometry.h>
#include <maya/MHWGeometryUtilities.h>

// Proxies
#include <maya/MPxTransform.h>
#include <maya/MPxTransformationMatrix.h>
#include <maya/MPxSurfaceShape.h>
#include <maya/MPxDrawOverride.h>

// Lunar
#include "../maya/api/Utils.h"
#include <../maya/api/LMText.h>

#include "../maya/api/LMAttribute.h"





//-------------------------------------------------------------------------------------------------
//
// Ctrl Transform Node definition
//
//-------------------------------------------------------------------------------------------------

class CtrlNode : public MPxTransform {
	/* Clean transform instance with a custom type_name. */
public:
	// Class attributes
	static const MString type_name;
	static const MTypeId type_id;
	static const MString type_drawdb;
	static const MString type_drawid;

	// Node attributes
	// static MObject size;
	static MObject local_position, local_positionX, local_positionY, local_positionZ;
	static MObject local_rotate, local_rotateX, local_rotateY, local_rotateZ;
	static MObject local_scale, local_scaleX, local_scaleY, local_scaleZ;

	static MObject attr_line_width;
	static MObject attr_shape_indx;

	static MObject attrInDrawLine;
	static Attribute attrInDrawLineTo;

	static MObject attr_draw_solver_mode;
	static MObject attr_solver_mode_size;
	static MObject attr_solver_mode_positionX, attr_solver_mode_positionY, attr_solver_mode_positionZ, attr_solver_mode_position;
	static MObject attrInText;

	static MObject attrInFkIk;
	static MObject attr_has_dynamic_attributes;

	// Use only on dynamic ctrl like fk / ik blending or pole vectors
	bool has_dynamic_attributes;

	MObject self_object;
	MDagPath self_path;

	// Constructors
	CtrlNode()
		: MPxTransform()
		, has_dynamic_attributes(false)
	{};
	// Destructors
	virtual ~CtrlNode() override {};

	// Class Methods
	static void * 	creator() {return new CtrlNode();};
	static MStatus	initialize();
	virtual void postConstructor() override;
	
	MStatus setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) override;
	void getCacheSetup(const MEvaluationNode& evalNode,	MNodeCacheDisablingInfo& disablingInfo,	MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const override;
	SchedulingType schedulingType() const override {return SchedulingType::kParallel;}
	
	bool isBounded() const override {return true;};
	virtual MBoundingBox boundingBox() const override;

private:
	// CtrlDrawOverride*	ptrCtrlDrawOverride;				// The node we are rendering
};




//-------------------------------------------------------------------------------------------------
//
// Ctrl Draw Override definition
//
//-------------------------------------------------------------------------------------------------

class CtrlUserData : public MUserData {
public:
	MMatrix 			mat_local;
	MBoundingBox 	bbox;
	MMatrix 			mat_pv;
	MPoint 				pos_draw_pv_to;
	

	short 				shape_indx;
	unsigned int 	prio_depth;
	MPointArray 	list_vertecies;
	MPointArray 	list_lines;
	float 				line_width;
	MColor 				col_wireframe;

	// Fk Ik state
	MObject objDrawLineTo;
	MMatrix matTo;
	double fkIk;
	bool bDrawline;

	bool draw_solver_mode;
	unsigned int solver_mode_size;
	MPoint pos_solver_mode;
	MString str_solver_mode;

	// Constructors
	CtrlUserData()
		: MUserData(false)
		// , line_width(2)
	{};

	// Destructor
	virtual ~CtrlUserData() override {};

	virtual void get_plugs(const MObject& object);
	virtual void get_shape(const MObject& object, const MDagPath& dp_object, MMatrix matrix);
	virtual void get_bbox(const MObject& object, const MDagPath& dp_object, MMatrix matrix);
	virtual void get_text(const MObject& object);
};




class CtrlDrawOverride : public MHWRender::MPxDrawOverride {
private:


public:
	// Destructor
	virtual ~CtrlDrawOverride() override 	{
		ptrCtrlNode = NULL; 
		if (fModelEditorChangedCbId != 0) {
			MMessage::removeCallback(fModelEditorChangedCbId);
			fModelEditorChangedCbId = 0;
		}
	};

	// Public Methods
	static MHWRender::MPxDrawOverride* creator(const MObject& obj) {return new CtrlDrawOverride(obj);}
	virtual MHWRender::DrawAPI supportedDrawAPIs() const override {return MHWRender::kAllDevices;}

	virtual bool isBounded(const MDagPath& objPath, const MDagPath& cameraPath) const override {return true;}
	virtual MBoundingBox boundingBox(
		const MDagPath& objPath,
		const MDagPath& cameraPath
	) const override;

	virtual bool hasUIDrawables() const override {return true;}
	virtual MUserData* prepareForDraw(
		const MDagPath& objPath,
		const MDagPath& cameraPath,
		const MHWRender::MFrameContext& frameContext,
		MUserData* oldData
	) override;
	virtual void addUIDrawables(
		const MDagPath& objPath,
		MHWRender::MUIDrawManager& drawManager,
		const MHWRender::MFrameContext& frameContext,
		const MUserData* data
	) override;

private:
	// Constructors
	CtrlDrawOverride(const MObject& obj)
		: MHWRender::MPxDrawOverride(obj, nullptr, false)
		, ptrCtrlNode(nullptr)
	{
		fModelEditorChangedCbId = MEventMessage::addEventCallback("modelEditorChanged", OnModelEditorChanged, this);

		MStatus status;
		MFnDependencyNode fn_node(obj, &status);
		ptrCtrlNode = status ? dynamic_cast<CtrlNode*>(fn_node.userNode()) : NULL;
	};

	CtrlNode*				ptrCtrlNode;				// The node we are rendering
	MCallbackId fModelEditorChangedCbId;
	static void OnModelEditorChanged(void *clientData);
};
