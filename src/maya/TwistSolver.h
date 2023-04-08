#pragma once

// ---------------------------------------------------------------------
//
//  TwistSolver.cpp
//
//  Created by ingo on 10/10/16.
//  Copyright (c) 2021 Ingo Clemens. All rights reserved.
//
// ---------------------------------------------------------------------

// ---------------------------------------------------------------------
// MIT License
//
// Copyright (c) 2021 Ingo Clemens, brave rabbit
// TwistSolver is under the terms of the MIT License
//
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the
// "Software"), to deal in the Software without restriction, including
// without limitation the rights to use, copy, modify, merge, publish,
// distribute, sublicense, and/or sell copies of the Software, and to
// permit persons to whom the Software is furnished to do so, subject to
// the following conditions:
//
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
// CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
// SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// Author: Ingo Clemens    www.braverabbit.com
// ---------------------------------------------------------------------

// System Includes
#include <cmath>
#include <string.h>
#include <iostream>
#include <cassert>
#include <map>
#include <vector>
#include <set>

// Maya General Includes
#include <maya/MGlobal.h>
#include <maya/MAnimControl.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MMatrix.h>
#include <maya/MAngle.h>
#include <maya/MQuaternion.h>
#include <maya/MEulerRotation.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MString.h>
#include <maya/MDataHandle.h>
#include <maya/MSelectionList.h>
#include <maya/MRampAttribute.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MArrayDataBuilder.h>

// Function Sets
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MFnToolContext.h>
#include <maya/MFnAnimCurve.h>
// #include <maya/MFnCompoundAttribute.h>
#include <maya/MFnEnumAttribute.h>
// #include <maya/MFnMatrixAttribute.h>
// #include <maya/MFnNumericAttribute.h>
// #include <maya/MFnPlugin.h>
// #include <maya/MFnUnitAttribute.h>

// Iterators

// Proxies
#include <maya/MPxNode.h>

// Lunar
#include "../maya/api/LMAttribute.h"
#include "../maya/api/LMGlobal.h"
#include "../maya/api/LMAnimControl.h"
#include "../maya/api/LMSolve.h"
#include "../maya/api/LMRigUtils.h"
#include "../maya/api/LMPlugin.h"
#include "../maya/api/Utils.h"
#include "../maya/api/MathUtility.h"

const float RADTODEG = (float)(180 / M_PI);




class TwistSolver : public MPxNode {
public:
	// Public Data
	static const MString typeName;
	static const MTypeId typeId;

	// Attributes
	static MObject active;
	static MObject axis;
	static MObject inputMatrix;
	static MObject invertTwist;
	static MObject offset;
	static MObject restMatrix;
	static MObject reverseSegments;
	static MObject scale;
	static MObject segmentBlend;
	static MObject segmentCount;
	static MObject twist;
	static MObject twistSegmentOut;
	static MObject useCurve;

	// Rotation tracking
	static MObject autoRegulate;
	static MObject extend;
	static MObject poseVector;
	static MObject regulationAngle;
	static MObject transformIndex;
	static MObject twistInput;
	static MObject twistReference;

	MObject objSelf;

	// Constructors
	TwistSolver()
		: MPxNode()
	{};
	// Destructors
	virtual ~TwistSolver() override {};

	static void* creator() {return new TwistSolver();}
	static MStatus initialize();
	virtual MStatus compute(const MPlug& plug, MDataBlock& dataBlock) override;
	// MStatus setDependentsDirty(const MPlug& plugBeingDirtied, MPlugArray& affectedPlugs) override;
	void getCacheSetup(const MEvaluationNode& evalNode,	MNodeCacheDisablingInfo& disablingInfo,	MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const override;
	void postConstructor() override;
	SchedulingType schedulingType() const override {return SchedulingType::kParallel;}

	MStatus postConstructor_init_curveRamp(MObject& nodeObj, MObject& rampObj, int index,	float position, float value, int interpolation);
	double getTwistAngle(MQuaternion quat, int axis);
	double trackRotation(double value, double reference);
	bool isAnimated(MPlug plug,	MPlug &animPlug, bool &isConnected);

private:
	static MStatus affectsOutput(MObject &attr);
};