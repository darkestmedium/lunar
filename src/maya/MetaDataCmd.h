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

#include "MetaDataNode.h"
// Lunar
#include "../maya/api/Utils.h"



class MetaDataCmd : public MPxCommand 
{
public:
	enum CommandMode {kCommandCreate, kCommandHelp};
	CommandMode command;

	static const char* commandName;

	// Command's Flags
	static const char* nameFlagShort;
	static const char* nameFlagLong;

	static const char* textFlagShort;
	static const char* textFlagLong;
	
	static const char* textPositionFlagShort;
	static const char* textPositionFlagLong;

	static const char* textSizeFlagShort;
	static const char* textSizeFlagLong;

	static const char* textColorFlagShort;
	static const char* textColorFlagLong;

	static const char* textVisibilityFlagShort;
	static const char* textVisibilityFlagLong;

	static const char* helpFlagShort;
	static const char* helpFlagLong;
	
	MString name;
	MString text;
	MVector textPosition;
	unsigned int textSize;
	MColor textColor;
	bool textVisibility;
	
	MObject objTransform;
	MObject objShape;

	// Constructors
	MetaDataCmd()
 		: MPxCommand()
		, name(MetaDataNode::typeName)
		, textPosition(100.0, 100.0, 0.0)
		, textSize(12)
		, textColor(2.0, 2.0, 2.0)
		, textVisibility(true)
 		, command(kCommandCreate)
	{};

	// Public Methods
	static void* creator() {return new MetaDataCmd();}
	virtual bool isUndoable() const override {return command == kCommandCreate;}
	static MSyntax syntaxCreator();

	virtual MStatus doIt(const MArgList& argList) override;
	virtual MStatus redoIt() override;
	virtual MStatus undoIt() override;

	MStatus parseArguments(const MArgList& argList);

private:
	// Private Methods
	MSelectionList selList;
	MDagModifier dagMod;
};
