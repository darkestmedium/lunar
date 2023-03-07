#pragma once

#include "CtrlData.h"

// System Includes
#include <vector>

// Maya General Includes
#include <maya/M3dView.h>
#include <maya/MBoundingBox.h>
#include <maya/MUserData.h>
#include <maya/MColor.h>
#include <maya/MPointArray.h>
#include <maya/MEulerRotation.h>

// Viewport 2.0 Includes
#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>
#include <maya/MDrawContext.h>
#include <maya/MHWGeometryUtilities.h>

// Proxies
#include <maya/MPxDrawOverride.h>



class CtrlDrawOverride : public MHWRender::MPxDrawOverride
{
private:
	// Constructors
	CtrlDrawOverride(const MObject& obj): MHWRender::MPxDrawOverride(obj, nullptr) {};

public:
	// Destructor
	virtual ~CtrlDrawOverride() override {};

	// Public Methods
	static MHWRender::MPxDrawOverride* creator(const MObject& obj) {return new CtrlDrawOverride(obj);}
	virtual MHWRender::DrawAPI supportedDrawAPIs() const override {return MHWRender::kAllDevices;}

	virtual bool isBounded(const MDagPath& objPath, const MDagPath& cameraPath) const override {return true;}
	virtual MBoundingBox boundingBox(
		const MDagPath& objPath,
		const MDagPath& cameraPath
	) const override;

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
