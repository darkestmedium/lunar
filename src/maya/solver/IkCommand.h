#pragma once

#include "../ctrl/Ctrl.h"
// #include "Utils.h"

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



class IkCommand : public MPxCommand 
{
public:
	enum CommandMode {kCommandCreate, kCommandHelp};
	// Constructors
 IkCommand()
 	: MPxCommand()
	, __name(Ctrl::typeName)
 	, __command(kCommandCreate)
	// __translateTo(false),
	// __rotateTo(false),
	// __side("center")
{}

	// Public Methods
	static void* creator() {return new IkCommand();}
	virtual bool isUndoable() const override {return __command == kCommandCreate;}
	static MSyntax syntaxCreator();

	virtual MStatus doIt(const MArgList& argList) override;
	virtual MStatus redoIt() override;
	virtual MStatus undoIt() override;

	// Public Data
	static const char* commandName;

	// Command's Flags
	static const char* nameFlagShort;
	static const char* nameFlagLong;

	static const char* parentFlagShort;
	static const char* parentFlagLong;

	// Ik Flags
	static const char* fkStartFlagShort;
	static const char* fkStartFlagLong;

	static const char* fkMidFlagShort;
	static const char* fkMidFlagLong;

	static const char* fkEndFlagShort;
	static const char* fkEndFlagLong;

	static const char* poleVectorFlagShort;
	static const char* poleVectorFlagLong;


	// Visual flags
	static const char* helpFlagShort;
	static const char* helpFlagLong;

private:
	// Private Methods

	MStatus objExists(MString& objectName);
	MStatus getDagPathFromString(MString& objectName, MDagPath& path);
	MStatus parseArguments(const MArgList& argList);

	// Private Data
	CommandMode __command;

	MObject __ObjIk2bSolver;

	MObject __ObjFkStart;
	MObject __ObjFkMid;
	MObject __ObjFkEnd;
	MObject __ObjPoleVector;


	MString __name;
	MString __parent;

	MSelectionList __selList;
	MDagModifier __DgMod;
	MDagPath __dp;
};
