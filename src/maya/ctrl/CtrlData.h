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
	// Public Data
	MBoundingBox bBox;
	MMatrix matLocalShape;
	
	MObject objDrawLineTo;
	MMatrix matTo;

	MPointArray fTransformedList;
	MPointArray fLineList;
	MPointArray fTriangleList;
	MPointArray listLine;

	bool fillShape;
	bool bDrawline;
	float lineWidth;
	MColor _wfColor;
	MColor fillColor;

	MPoint _textOffset;
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
	virtual void getBBox(const MObject& obj, const MDagPath& objPath, MMatrix matrix);
	virtual void getShape(const MObject& obj, const MDagPath& pathObj, MMatrix matrix);


};
