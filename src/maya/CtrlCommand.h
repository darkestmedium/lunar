#pragma once

// System Includes
#include <string>

// Maya General Includes
#include <maya/MGlobal.h>
#include <maya/MPlug.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>
#include <maya/MSelectionList.h>
#include <maya/MDGModifier.h>
#include <maya/MDagModifier.h>
#include <maya/MTime.h>
#include <maya/MAnimControl.h>
#include <maya/MString.h>
#include <maya/MDagModifier.h>

// Function Sets
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>

// Iterators
#include <maya/MItSelectionList.h>

// Proxies
#include <maya/MPxCommand.h>

// Lunar
#include "Ctrl.h"
#include "../maya/api/Utils.h"
#include "../maya/api/LMAttribute.h"
#include "../maya/api/LMObject.h"



class CtrlCommand : public MPxCommand {
public:
	enum CommandMode {kCommandCreate, kCommandHelp};
	CommandMode command;

	// Public Data
	static const char* commandName;

	// Command's Flags
	static const char* nameFlagShort;
	static const char* nameFlagLong;

	static const char* parentFlagShort;
	static const char* parentFlagLong;

	static const char* translateToFlagShort;
	static const char* translateToFlagLong;

	static const char* rotatetToFlagShort;
	static const char* rotatetToFlagLong;

	static const char* localPositionFlagShort;
	static const char* localPositionFlagLong;

	static const char* localRotateFlagShort;
	static const char* localRotateFlagLong;
	
	static const char* localScaleFlagShort;
	static const char* localScaleFlagLong;

	// Visual flags
	static const char* shapeFlagShort;
	static const char* shapeFlagLong;

	static const char* fillShapeFlagShort;
	static const char* fillShapeFlagLong;

	static const char* drawLineFlagShort;
	static const char* drawLineFlagLong;

	static const char* drawTextFlagShort;
	static const char* drawTextFlagLong;

	static const char* textPositionFlagShort;
	static const char* textPositionFlagLong;

	static const char* fillTransparencyFlagShort;
	static const char* fillTransparencyFlagLong;

	static const char* lineWidthFlagShort;
	static const char* lineWidthFlagLong;

	static const char* colorFlagShort;
	static const char* colorFlagLong;

	static const char* lockShapeAttributesFlagShort;
	static const char* lockShapeAttributesFlagLong;

	static const char* hideOnPlaybackFlagShort;
	static const char* hideOnPlaybackFlagLong;

	static const char* helpFlagShort;
	static const char* helpFlagLong;

	MString name;
	MString parent;

	bool bTranslateTo;
	bool bRotateTo;
	MString strTranslateTo;
	MString strRotateTo;

	MVector localPosition;
	MVector localRotate;
	MVector localScale;
	MVector textPosition;

	MString strColor;
	MColor colorOverride;

	short indxShape;
	bool bFillShape;
	bool bDrawLine;
	bool bDrawText;
	double fillTransparency;
	double lineWidth;
	bool bLockShapeAttributes;
	bool bHideOnPlayback;

	// Constructors
	CtrlCommand()
 		: MPxCommand()
		, name(Ctrl::typeName)
		, bTranslateTo(false)
		, bRotateTo(false)
 		, localPosition(0.0, 0.0, 0.0)
 		, localRotate(0.0, 0.0, 0.0)
 		, localScale(1.0, 1.0, 1.0)
 		, indxShape(0)
 		, bFillShape(true)
 		, bDrawLine(false)
 		, bDrawText(false)
 		, textPosition(0.0, 0.0, 0.0)
 		, fillTransparency(0.25)
 		, lineWidth(1.0)
		, strColor("yellow")
		, colorOverride(1.0, 1.0, 0.25)
		, bLockShapeAttributes(false)
		, bHideOnPlayback(false)
		, command(kCommandCreate)
	{};

	// Public Methods
	static void* creator() {return new CtrlCommand();}
	virtual bool isUndoable() const override {return command == kCommandCreate;}
	static MSyntax syntaxCreator();

	virtual MStatus doIt(const MArgList& argList) override;
	virtual MStatus redoIt() override;
	virtual MStatus undoIt() override;

	MStatus parseArguments(const MArgList& argList);

private:
	// Private Method
	// MStatus getDagPathFromString(MString& objectName, MDagPath& path);

	// Private Data
	MObject objThisTransform;
	MDagPath dpThisTransform;
	MObject objThisShape;

	MDagPath dpTargetTranslation;
	MDagPath dpTargetRotation;
	MVector posTarget;
	MQuaternion rotTarget;

	MSelectionList listSelection;
	MDagModifier modDag;
};