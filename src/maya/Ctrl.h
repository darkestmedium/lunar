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

// Proxies
#include <maya/MPxLocatorNode.h>

// Lunar
#include "../maya/api/Utils.h"



class Ctrl : public MPxLocatorNode {
public:
	// Public Data
	static const MString typeName;
	static const MTypeId typeId;
	static const MString drawDbClassification;
	static const MString drawRegistrationId;

	// Node's Input Attributes
	static MObject localRotateX;
	static MObject localRotateY;
	static MObject localRotateZ;
	static MObject localRotate;

	static MObject shapeAttr;
	static MObject fillShapeAttr;
	static MObject fillTransparencyAttr;
	static MObject lineWidthAttr;

	static MObject attrInDrawLine;
	static Attribute attrInDrawLineTo;

	static MObject attrInDrawText;
	static MObject attrInTextPositionX;
	static MObject attrInTextPositionY;
	static MObject attrInTextPositionZ;
	static MObject attrInTextPosition;
	static MObject attrInText;

	static MObject attrInFkIk;

	MObject objSelf;
	MDagPath pathSelf;

	// Constructors
	Ctrl()
		: MPxLocatorNode() 	
	{};
	// Destructor
	virtual ~Ctrl() override {};

	// Public Methods
	static void* creator() {return new Ctrl();}
	static MStatus initialize();
	virtual bool isBounded() const override {return true;}
	virtual MBoundingBox boundingBox() const override;
	void getCacheSetup(
		const MEvaluationNode& evalNode,
		MNodeCacheDisablingInfo& disablingInfo,
		MNodeCacheSetupInfo& cacheSetupInfo,
		MObjectArray& monitoredAttributes
	) const override;
	virtual void postConstructor() override;
};
