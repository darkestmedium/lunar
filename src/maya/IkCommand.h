#pragma once

#include "Ctrl.h"
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
#include <maya/MTransformationMatrix.h>
#include <maya/MFnMatrixData.h>

// Iterators
#include <maya/MItSelectionList.h>

// Proxies
#include <maya/MPxCommand.h>



class IkCommand : public MPxCommand {
public:
	enum CommandMode {kCommandCreate, kCommandHelp};
	CommandMode command;

	// Public Data
	static const char* commandName;

	// Command's Flags
	static const char* nameFlagShort;
	static const char* nameFlagLong;

	// Ik Flags
	static const char* fkStartFlagShort;
	static const char* fkStartFlagLong;
	static const char* fkMidFlagShort;
	static const char* fkMidFlagLong;
	static const char* fkEndFlagShort;
	static const char* fkEndFlagLong;
	static const char* ikHandleFlagShort;
	static const char* ikHandleFlagLong;
	static const char* poleVectorFlagShort;
	static const char* poleVectorFlagLong;

	static const char* helpFlagShort;
	static const char* helpFlagLong;

	MString name;
	bool bIsPoleVectorSet;

	MObject objIk2bSolver;
	MDagPath dpPoleVector;

	MFnTransform fnFkStart;
	MFnTransform fnFkMid;
	MFnTransform fnFkEnd;
	MFnTransform fnIkHandle;
	MFnTransform fnPoleVector;
	MFnDependencyNode fnIk2bSolver;

	MDGModifier modDg;

	// Constructors
	IkCommand()
 	: MPxCommand()
 	, command(kCommandCreate)
	, name(Ctrl::typeName)
	, bIsPoleVectorSet(false)
	{}

	// Public Methods
	static void* creator() {return new IkCommand();}
	virtual bool isUndoable() const override {return command == kCommandCreate;}
	static MSyntax syntaxCreator();
	MStatus parseArguments(const MArgList& argList);
	virtual MStatus doIt(const MArgList& argList) override;
	virtual MStatus redoIt() override;
	virtual MStatus undoIt() override;


private:
	// Private Data
	MSelectionList __selList;
	MDagPath __dp;
};