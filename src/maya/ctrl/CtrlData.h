#pragma once

// System Includes
#include <vector>

// Maya General Includes
#include <maya/M3dView.h>
#include <maya/MBoundingBox.h>
#include <maya/MUserData.h>
#include <maya/MColor.h>
#include <maya/MVector.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MEulerRotation.h>

// Viewport 2.0 Includes
#include <maya/MDrawRegistry.h>
#include <maya/MPxDrawOverride.h>
#include <maya/MUserData.h>



class CtrlData : public MUserData
{
public:
	unsigned int DepthPriority;
	bool DrawInXray;
	// Constructors
	// CtrlData() : MUserData(false) {}; // Don't delete after draw
	CtrlData()
	 : MUserData()
	{};  // Don't delete after draw

	// Destructor
	virtual ~CtrlData() override {};

	// Public Methods
	virtual void getPlugs(const MObject& obj);
	virtual void getBBox(const MObject& obj, MMatrix matrix);
	virtual void getShape(const MObject& obj, MMatrix matrix);

	// Public Data
	MBoundingBox bBox;
	MMatrix matrix;

	MPointArray fTransformedList;
	MPointArray fLineList;
	MPointArray fTriangleList;

	float lineWidth;
	MColor _wfColor;
	bool fillShape;
	MColor fillColor;

	MPoint _textOffset;
};
