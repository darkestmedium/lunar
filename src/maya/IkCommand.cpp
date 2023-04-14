#include "Ik2bSolver.h"
#include "IkCommand.h"



// Public Data
const char* IkCommand::commandName = "ik";

// Command's Flags
const char* IkCommand::nameFlagShort = "-n";
const char* IkCommand::nameFlagLong = "-name";

// Pole Vector Flags
const char* IkCommand::fkStartFlagShort = "-fks";
const char* IkCommand::fkStartFlagLong = "-fkStart";
const char* IkCommand::fkMidFlagShort = "-fkm";
const char* IkCommand::fkMidFlagLong = "-fkMid";
const char* IkCommand::fkEndFlagShort = "-fke";
const char* IkCommand::fkEndFlagLong = "-fkEnd";
const char* IkCommand::ikHandleFlagShort = "-ikh";
const char* IkCommand::ikHandleFlagLong = "-ikHandle";
const char* IkCommand::poleVectorFlagShort = "-pv";
const char* IkCommand::poleVectorFlagLong = "-poleVector";

// Local position flags
const char* IkCommand::helpFlagShort = "-h";
const char* IkCommand::helpFlagLong = "-help";



MSyntax IkCommand::syntaxCreator() {
	/* Creates the command's syntax object and returns it.

	Returns:
		syntax (MSyntax): Command's syntax object

	*/
	MSyntax sytnax;

	// Main flags
	sytnax.addFlag(nameFlagShort, nameFlagLong, MSyntax::kString);

	// Ik flags
	sytnax.addFlag(fkStartFlagShort, fkStartFlagLong, MSyntax::kString);
	sytnax.addFlag(fkMidFlagShort, fkMidFlagLong, MSyntax::kString);
	sytnax.addFlag(fkEndFlagShort, fkEndFlagLong, MSyntax::kString);
	sytnax.addFlag(ikHandleFlagShort, ikHandleFlagLong, MSyntax::kString);
	sytnax.addFlag(poleVectorFlagShort, poleVectorFlagLong, MSyntax::kString);

	// Visual flags	
	sytnax.addFlag(helpFlagShort, helpFlagLong, MSyntax::kBoolean);

	sytnax.setObjectType(MSyntax::kSelectionList, 0, 1);
	sytnax.useSelectionAsDefault(true);

	return sytnax;
}


MStatus IkCommand::parseArguments(const MArgList& argList) {
	/* Parses the commands's flag arguments.

	Args:
		argList (MArglist): List of arguments passed to the command.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	MArgDatabase argData(syntax(), argList);
	argData.getObjects(__selList);

	// Display Help
	if (argData.isFlagSet(helpFlagShort))	{
		command = kCommandHelp;
		MString helpStr;
		helpStr += "Flags:\n";
		helpStr += "   -n    -name                 String     Name of the ik solver node to be created.\n";
		helpStr += "   -fks  -fkStart              String     Name of the fk start transform input.\n";
		helpStr += "   -fkm  -fkMid                String     Name of the fk mid transform input.\n";
		helpStr += "   -fke  -fkEnd                String     Name of the fk end transform input.\n";
		helpStr += "   -ikh  -ikHandle             String     Name of the ik handle transform input.\n";
		helpStr += "   -pv   -poleVector           String     Name of the pole vector transform input (optional).\n";
		helpStr += "   -h    -help                 N/A        Display this text.\n";
		MGlobal::displayInfo(helpStr);
		return MS::kSuccess;
	}

	// Name Flag
	if (argData.isFlagSet(nameFlagShort))	{
		name = argData.flagArgumentString(nameFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	// FkStart Flag
	if (argData.isFlagSet(fkStartFlagShort)) {
		MDagPath dpFkStart;
		status = LMObject::getDagPathFromString(argData.flagArgumentString(fkStartFlagShort, 0, &status), dpFkStart);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fnFkStart.setObject(dpFkStart);
	} else {
		MGlobal::displayError("fkStart flag is required.");
		return MS::kFailure;
	}

	// FkMid Flag
	if (argData.isFlagSet(fkMidFlagShort)) {
		MDagPath dpFkMid;
		status = LMObject::getDagPathFromString(argData.flagArgumentString(fkMidFlagShort, 0, &status), dpFkMid);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fnFkMid.setObject(dpFkMid);
	} else {
		MGlobal::displayError("fkMid flag is required.");
		return MS::kFailure;
	}

	// FkEnd Flag
	if (argData.isFlagSet(fkEndFlagShort)) {
		MDagPath dpFkEnd;
		status = LMObject::getDagPathFromString(argData.flagArgumentString(fkEndFlagShort, 0, &status), dpFkEnd);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fnFkEnd.setObject(dpFkEnd);
	} else {
		MGlobal::displayError("fkEnd flag is required.");
		return MS::kFailure;
	}

	// IkHandle Flag
	if (argData.isFlagSet(ikHandleFlagShort)) {
		MDagPath dpIkHandle;
		status = LMObject::getDagPathFromString(argData.flagArgumentString(ikHandleFlagShort, 0, &status), dpIkHandle);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fnIkHandle.setObject(dpIkHandle);
	} else {
		MGlobal::displayError("ikHandle flag is required.");
		return MS::kFailure;
	}

	// PoleVector Flag
	if (argData.isFlagSet(poleVectorFlagShort)) {
		MString strPoleVector = argData.flagArgumentString(poleVectorFlagShort, 0, &status);
		if (strPoleVector != "") {
			status = LMObject::getDagPathFromString(strPoleVector, dpPoleVector);
			CHECK_MSTATUS_AND_RETURN_IT(status);
			fnPoleVector.setObject(dpPoleVector);
			bIsPoleVectorSet = true;
		}
	} else {
		fnPoleVector.setObject(MObject::kNullObj);
		bIsPoleVectorSet = false;
	}

	return MS::kSuccess;
}


MStatus IkCommand::doIt(const MArgList& argList) {
	/* Command's doIt method.

	This method should perform a command by setting up internal class data and then	calling the
	redoIt method.

	The actual action performed by the command should be done in the redoIt method.	This is a pure
	virtual method, and must be overridden in derived classes.

	Args:
		argList (MArgList): List of arguments passed to the command.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	status = parseArguments(argList);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Command create mode
	if (command == kCommandCreate) {
		// Solver node creation
		objIk2bSolver = modDg.createNode(Ik2bSolver::typeName);
		if (name == Ik2bSolver::typeName)	{
			modDg.renameNode(objIk2bSolver, name);
		}	else {
			modDg.renameNode(objIk2bSolver, name + Ik2bSolver::typeName);
		}
		// Get function sets
		fnIk2bSolver.setObject(objIk2bSolver);

		// Get input plugs
		MPlug plugOutFkStartWorldMatrix0 = fnFkStart.findPlug("worldMatrix", false).elementByLogicalIndex(0);
		MPlug plugOutFkMidWorldMatrix0 = fnFkMid.findPlug("worldMatrix", false).elementByLogicalIndex(0);
		MPlug plugOutFkEndWorldMatrix0 = fnFkEnd.findPlug("worldMatrix", false).elementByLogicalIndex(0);
		MPlug plugOutIkHandleWorldMatrix0 = fnIkHandle.findPlug("worldMatrix", false).elementByLogicalIndex(0);
		
		MPlug plugInFkStartRotPivot = fnFkStart.findPlug("rotatePivot", false);
		MPlug plugInFkMidRotPivot = fnFkMid.findPlug("rotatePivot", false);
		MPlug plugInFkEndRotPivot = fnFkEnd.findPlug("rotatePivot", false);
		MPlug plugInIkHandleRotPivot = fnIkHandle.findPlug("rotatePivot", false);
	
		// Get solver input plugs
		MPlug plugInFkStart = fnIk2bSolver.findPlug("fkStart", false);
		MPlug plugInFkMid = fnIk2bSolver.findPlug("fkMid", false);
		MPlug plugInFkEnd = fnIk2bSolver.findPlug("fkEnd", false);
		MPlug plugInIkHandle = fnIk2bSolver.findPlug("ikHandle", false);
		MPlug plugInPoleVector = fnIk2bSolver.findPlug("poleVector", false);

		// Connect matrix plugs
		modDg.connect(plugOutFkStartWorldMatrix0, plugInFkStart);
		modDg.connect(plugOutFkMidWorldMatrix0, plugInFkMid);
		modDg.connect(plugOutFkEndWorldMatrix0, plugInFkEnd);
		modDg.connect(plugOutIkHandleWorldMatrix0, plugInIkHandle);
	

		// Pole vector plugs
		if (bIsPoleVectorSet) {
			MPlug plugPoleVectorTranslate = fnPoleVector.findPlug("translate", false);
			MPlug plugPoleVectorRotPivot = fnIkHandle.findPlug("rotatePivot", false);

			// Get poleVectorShape
			dpPoleVector.extendToShape();
			MFnDependencyNode fnPoleVectorShape = dpPoleVector.node();
			MPlug plugPoleVectorDrawLineTo = fnPoleVectorShape.findPlug("drawLineTo", false);
			
			modDg.connect(plugPoleVectorTranslate, plugInPoleVector);
			// modDg.connect(plugOutUpdate, plugPoleVectorRotPivot);
			// modDg.connect(plugOutFkMidWorldMatrix0, plugPoleVectorDrawLineTo);
		}

		// // Connect time node
		// LMScene::connectSceneTime(objIk2bSolver, "inTime", modDg);
	}

	return redoIt();
}


MStatus IkCommand::redoIt() {
	/* Command's redoIt method.

	This method should do the actual work of the command based on the internal class data only.	Internal class data should be set in the doIt method.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/

	// Command create mode
	if (command == kCommandCreate) {
		MStatus status;

		status = modDg.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		if (!bIsPoleVectorSet) {
			MPlug plugInPoleVectorX = fnIk2bSolver.findPlug("poleVectorX", false);
			MPlug plugInPoleVectorY = fnIk2bSolver.findPlug("poleVectorY", false);
			MPlug plugInPoleVectorZ = fnIk2bSolver.findPlug("poleVectorZ", false);

			MVector posFkStart = fnFkStart.rotatePivot(MSpace::kWorld);
			MVector posFkMid = fnFkMid.rotatePivot(MSpace::kWorld);
			MVector posFkEnd = fnFkEnd.rotatePivot(MSpace::kWorld);
			MVector posPoleVector = LMRigUtils::getPvPosition(posFkStart, posFkMid, posFkEnd, "local");

			plugInPoleVectorX.setValue(posPoleVector.x);
			plugInPoleVectorY.setValue(posPoleVector.y);
			plugInPoleVectorZ.setValue(posPoleVector.z);
		}

		// Sets command's output result in mel / python
		clearResult();
		appendToResult(fnIk2bSolver.name());
	}

	return MS::kSuccess;
}


MStatus IkCommand::undoIt() {
	/* Command's undoIt method.

	This method should undo the work done by the redoIt method based on the internal class data only.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	// Restore the initial state
	status = modDg.undoIt();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}

