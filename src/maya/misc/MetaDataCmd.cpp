// #include "ctrl/Ctrl.h"
#include "MetaDataCmd.h"



// Public Data
const char* MetaDataCmd::commandName = "metaData";

// Command's Flags
const char* MetaDataCmd::nameFlagShort = "-n";
const char* MetaDataCmd::nameFlagLong = "-name";

const char* MetaDataCmd::textFlagShort = "-t";
const char* MetaDataCmd::textFlagLong = "-text";

const char* MetaDataCmd::textPositionFlagShort = "-tp";
const char* MetaDataCmd::textPositionFlagLong = "-textPosition";

const char* MetaDataCmd::textSizeFlagShort = "-ts";
const char* MetaDataCmd::textSizeFlagLong = "-textSize";

const char* MetaDataCmd::textColorFlagShort = "-tc";
const char* MetaDataCmd::textColorFlagLong = "-textColor";

const char* MetaDataCmd::textVisibilityFlagShort = "-tv";
const char* MetaDataCmd::textVisibilityFlagLong = "-textVisibility";

const char* MetaDataCmd::helpFlagShort = "-h";
const char* MetaDataCmd::helpFlagLong = "-help";




MSyntax MetaDataCmd::syntaxCreator() {
	/* Creates the command's syntax object and returns it.

	Returns:
		syntax (MSyntax): Command's syntax object

	*/
	MSyntax sytnax;

	// Main flags
	sytnax.addFlag(nameFlagShort, nameFlagLong, MSyntax::kString);
	sytnax.addFlag(textFlagShort, textFlagLong, MSyntax::kString);
	sytnax.addFlag(textPositionFlagShort, textPositionFlagLong, MSyntax::kUnsigned, MSyntax::kUnsigned);
	sytnax.addFlag(textSizeFlagShort, textSizeFlagLong, MSyntax::kUnsigned);
	sytnax.addFlag(textColorFlagShort, textColorFlagLong, MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);
	sytnax.addFlag(textVisibilityFlagShort, textVisibilityFlagLong, MSyntax::kBoolean);

	sytnax.addFlag(helpFlagShort, helpFlagLong, MSyntax::kBoolean);

	return sytnax;
}


MStatus MetaDataCmd::parseArguments(const MArgList &argList) {
	/* Parses the commands's flag arguments.

	Args:
		argList (MArglist): List of arguments passed to the command.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	MArgDatabase argData(syntax(), argList);

	// Display Help
	if (argData.isFlagSet(helpFlagShort))
	{
		command = kCommandHelp;
		MString helpStr;
		helpStr += "Flags:\n";
		helpStr += "   -n    -name                 String       Name of the metadata node to create.\n";
		helpStr += "   -t    -text                 String       Text that will be displayed int he viewport.\n";
		helpStr += "   -tp   -textPosition         Int, Int     Text position, viewports' lower left corner is (0, 0).\n";
		helpStr += "   -ts   -textSize             Int          Font size - between 9 and 32, the default is 12.\n";
		helpStr += "   -tc   -textColor	           Double3      Color of the text.\n";
		helpStr += "   -tv   -textVisibility       Bool         Visibility of the text.\n";
		helpStr += "   -h    -help                 N/A          Display this text.\n";
		MGlobal::displayInfo(helpStr);
		return MS::kSuccess;
	}

	// Name Flag
	if (argData.isFlagSet(nameFlagShort))
	{
		name = argData.flagArgumentString(nameFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Flag
	if (argData.isFlagSet(textFlagShort))
	{
		text = argData.flagArgumentString(textFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Position Flag
	if (argData.isFlagSet(textPositionFlagShort))
	{
		textPosition.x = argData.flagArgumentInt(textPositionFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textPosition.y = argData.flagArgumentInt(textPositionFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Color Flag
	if (argData.isFlagSet(textPositionFlagShort))
	{
		textColor.r = argData.flagArgumentDouble(textColorFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textColor.g = argData.flagArgumentDouble(textColorFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textColor.b = argData.flagArgumentDouble(textColorFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Visibility Flag
	if (argData.isFlagSet(textVisibilityFlagShort))
	{
		textVisibility = argData.flagArgumentBool(textVisibilityFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	return MS::kSuccess;
}


MStatus MetaDataCmd::objExists(MString& objectName)
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


MStatus MetaDataCmd::getDagPathFromString(MString& objectName, MDagPath& path)
{
	MStatus status;
	MSelectionList selectionList;

	status = selectionList.add(objectName);
	if (status == MS::kSuccess)	{
		selectionList.getDagPath(0, path);
		if (path.hasFn(MFn::kTransform) == true) {
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


MStatus MetaDataCmd::doIt(const MArgList& argList)
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
	if (command == kCommandCreate)
	{
		objTransform = dagMod.createNode("transform", MObject::kNullObj);
		objShape = dagMod.createNode(MetaDataNode::typeName, objTransform);

		// If name equals to "metaData" rename only the transform node as the shape node will be
		// renamed in the rigController.RigController::postConstructor method.
		if (name == MetaDataNode::typeName)
		{
			dagMod.renameNode(objTransform, name);
		}
		else
		{
			dagMod.renameNode(objTransform, name);
			dagMod.renameNode(objShape, name + "Shape");
		}
	}
	return redoIt();
}


MStatus MetaDataCmd::redoIt()
{
	/* Command's redoIt method.

	This method should do the actual work of the command based on the internal class data only.	Internal class data should be set in the doIt method.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/

	// Command create mode
	if (command == kCommandCreate)
	{
		MStatus status;

		status = dagMod.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		MFnDependencyNode fnTransform(objTransform);
		MFnDependencyNode fnShape(objShape);
		// TRANSFORM NODE
		lockHideAttribute(fnTransform.findPlug("translateX", false));
		lockHideAttribute(fnTransform.findPlug("translateY", false));
		lockHideAttribute(fnTransform.findPlug("translateZ", false));
		lockHideAttribute(fnTransform.findPlug("rotateX", false));
		lockHideAttribute(fnTransform.findPlug("rotateY", false));
		lockHideAttribute(fnTransform.findPlug("rotateZ", false));
		lockHideAttribute(fnTransform.findPlug("scaleX", false));
		lockHideAttribute(fnTransform.findPlug("scaleY", false));
		lockHideAttribute(fnTransform.findPlug("scaleZ", false));
		lockHideAttribute(fnTransform.findPlug("visibility", false));


		// SHAPE NODE
		// Sets the plugs values based on the flag arguments
		MPlug plugText(objShape, MetaDataNode::AttrText);
		plugText.setValue(text);

		MPlug plugTextPositionX(objShape, MetaDataNode::AttrTextPositionX);
		plugTextPositionX.setValue(textPosition.x);
		MPlug plugTextPositionY(objShape, MetaDataNode::AttrTextPositionY);
		plugTextPositionY.setValue(textPosition.y);

		MPlug plugTextSize(objShape, MetaDataNode::AttrTextSize);
		plugTextSize.setInt(textSize);

		MPlug plugTextColor(objShape, MetaDataNode::AttrTextColor);
		MPlug plugTextColorR = plugTextColor.child(0);
		plugTextColorR.setValue(textColor.r);
		MPlug plugTextColorG = plugTextColor.child(1);
		plugTextColorG.setValue(textColor.g);
		MPlug plugTextColorB = plugTextColor.child(2);
		plugTextColorB.setValue(textColor.b);

		MPlug plugTextVisbility(objShape, MetaDataNode::visibility);
		plugTextVisbility.setValue(textVisibility);

		// Sets command's output result in mel / python
		clearResult();
		appendToResult(fnTransform.name());
		appendToResult(fnShape.name());
	}

	return MS::kSuccess;
}


MStatus MetaDataCmd::undoIt()
{
	/* Command's undoIt method.

	This method should undo the work done by the redoIt method based on the internal class data only.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	// Restore the initial state
	status = dagMod.undoIt();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}


MStatus MetaDataCmd::lockHideAttribute(MPlug plug)
{
	/* Locks and hides the given plug from the channelbox.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	plug.setLocked(true);
	plug.setKeyable(false);
	plug.setChannelBox(false);

	return MS::kSuccess;
}