#include "Ik2bSolver.h"
#include "IkCommand.h"



// Public Data
const char* IkCommand::commandName = "ik";

// Command's Flags
const char* IkCommand::nameFlagShort = "-n";
const char* IkCommand::nameFlagLong = "-name";

const char* IkCommand::parentFlagShort = "-p";
const char* IkCommand::parentFlagLong = "-parent";

// Pole Vector Flags
const char* IkCommand::fkStartFlagShort = "-fs";
const char* IkCommand::fkStartFlagLong = "-fkStart";
const char* IkCommand::fkMidFlagShort = "-fm";
const char* IkCommand::fkMidFlagLong = "-fkMid";
const char* IkCommand::fkEndFlagShort = "-fe";
const char* IkCommand::fkEndFlagLong = "-fkEnd";
const char* IkCommand::poleVectorFlagShort = "-pv";
const char* IkCommand::poleVectorFlagLong = "-poleVector";

// Local position flags
const char* IkCommand::helpFlagShort = "-h";
const char* IkCommand::helpFlagLong = "-help";



MSyntax IkCommand::syntaxCreator()
{
	/* Creates the command's syntax object and returns it.

	Returns:
		syntax (MSyntax): Command's syntax object

	*/
	MSyntax sytnax;

	// Main flags
	sytnax.addFlag(nameFlagShort, nameFlagLong, MSyntax::kString);

	// Ik flags
	sytnax.addFlag(fkStartFlagShort, fkStartFlagLong, MSyntax::kString);
	sytnax.addFlag(fkMidFlagShort, fkStartFlagLong, MSyntax::kString);
	sytnax.addFlag(fkEndFlagShort, fkEndFlagLong, MSyntax::kString);
	sytnax.addFlag(poleVectorFlagShort, poleVectorFlagLong, MSyntax::kString);

	// Visual flags	
	sytnax.addFlag(helpFlagShort, helpFlagLong, MSyntax::kBoolean);

	sytnax.setObjectType(MSyntax::kSelectionList, 0, 1);
	sytnax.useSelectionAsDefault(true);

	return sytnax;
}


MStatus IkCommand::parseArguments(const MArgList &argList)
{
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
	if (argData.isFlagSet(helpFlagShort))
	{
		__command = kCommandHelp;
		MString helpStr;
		helpStr += "Flags:\n";
		helpStr += "   -n    -name                 String     Name of the ik solver node to be created.\n";
		helpStr += "   -h    -help                 N/A        Display this text.\n";
		MGlobal::displayInfo(helpStr);
		return MS::kSuccess;
	}

	// Name Flag
	if (argData.isFlagSet(nameFlagShort))
	{
		__name = argData.flagArgumentString(nameFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	// FkStart Flag
	if (argData.isFlagSet(fkStartFlagShort))
	{
		__name = argData.flagArgumentString(fkStartFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	// Parent Flag
	// if (argData.isFlagSet(parentFlagShort))
	// {
	// 	__selList.add(argData.flagArgumentString(parentFlagShort, 0, &status));
	// 	CHECK_MSTATUS_AND_RETURN_IT(status);
	// }

	return MS::kSuccess;
}


MStatus IkCommand::objExists(MString& objectName)
{
	MStatus status;
	MSelectionList selList;

	status = selList.add(objectName);

	if (status == MS::kSuccess)
	{
		return MS::kSuccess;
	}

	return MS::kFailure;
}


MStatus IkCommand::getDagPathFromString(MString& objectName, MDagPath& path)
{
	MStatus status;
	MSelectionList selectionList;

	status = selectionList.add(objectName);
	if (status == MS::kSuccess)
	{
		selectionList.getDagPath(0, path);
		if (path.hasFn(MFn::kTransform) == true)
		{
			return MS::kSuccess;
		}
		else
		{
			MGlobal::displayError("Given '" + objectName + "' is not a transform node.");
		}
	}
	else
	{
		MGlobal::displayError("Given '" + objectName + "' does not exist.");
	}
	return MS::kFailure;
}


MStatus IkCommand::doIt(const MArgList& argList)
{
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
	if (__command == kCommandCreate)
	{
		__ObjIk2bSolver = __DgMod.createNode(Ik2bSolver::typeName);

		if (__name == Ik2bSolver::typeName)
		{
			__DgMod.renameNode(__ObjIk2bSolver, __name);
		}
		else
		{
			__DgMod.renameNode(__ObjIk2bSolver, __name + Ik2bSolver::typeName);
		}

		MFnDependencyNode FnIk2bSolver(__ObjIk2bSolver);

		

		// Parent under the transform node if the selection is not empty and / or parent was specified
		// int numItems = __selList.length();
		// if (numItems == 1) 
		// {
		// 	MObject parentObj;
		// 	__selList.getDependNode(0, parentObj);
		// 	__DagMod.reparentNode(__thisTransformObj, parentObj);
		// }
		// else if (numItems == 2)
		// {
		// 	MObject parentObj;
		// 	__selList.getDependNode(1, parentObj);
		// 	__DagMod.reparentNode(__thisTransformObj, parentObj);
		// }
	}

	return redoIt();
}


MStatus IkCommand::redoIt()
{
	/* Command's redoIt method.

	This method should do the actual work of the command based on the internal class data only.	Internal class data should be set in the doIt method.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/

	// Command create mode
	if (__command == kCommandCreate)
	{
		MStatus status;
		// We need to init the MFnTransform with a dag path, mobjects do not work with transformations
		// even if the object has a MFn::kTransform
		////__dp.getAPathTo(__thisTransformObj, __thisTransformDp);
		//MFnTransform transformFn(__thisTransformDp);
		MFnDependencyNode FnIk2bSolver(__ObjIk2bSolver);

		status = __DgMod.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);


		// Sets command's output result in mel / python
		clearResult();
		appendToResult(FnIk2bSolver.name());
	}

	return MS::kSuccess;
}


MStatus IkCommand::undoIt()
{
	/* Command's undoIt method.

	This method should undo the work done by the redoIt method based on the internal class data only.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	// Restore the initial state
	status = __DgMod.undoIt();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}

