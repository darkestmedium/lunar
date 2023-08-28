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
	if (argData.isFlagSet(helpFlagShort))	{
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
	if (argData.isFlagSet(nameFlagShort))	{
		name = argData.flagArgumentString(nameFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Flag
	if (argData.isFlagSet(textFlagShort))	{
		text = argData.flagArgumentString(textFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Position Flag
	if (argData.isFlagSet(textPositionFlagShort))	{
		textPosition.x = argData.flagArgumentInt(textPositionFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textPosition.y = argData.flagArgumentInt(textPositionFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Color Flag
	if (argData.isFlagSet(textPositionFlagShort))	{
		textColor.r = argData.flagArgumentDouble(textColorFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textColor.g = argData.flagArgumentDouble(textColorFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		textColor.b = argData.flagArgumentDouble(textColorFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Text Visibility Flag
	if (argData.isFlagSet(textVisibilityFlagShort))	{
		textVisibility = argData.flagArgumentBool(textVisibilityFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	return MS::kSuccess;
}


MStatus MetaDataCmd::doIt(const MArgList& argList) {
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
		obj_metadata = dagMod.createNode(MetaDataNode::type_name, MObject::kNullObj);
		if (name != MetaDataNode::type_name) {dagMod.renameNode(obj_metadata, name);}
	}

	return redoIt();
}


MStatus MetaDataCmd::redoIt() {
	/* Command's redoIt method.

	This method should do the actual work of the command based on the internal class data only.	Internal class data should be set in the doIt method.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/

	// Command create mode
	if (command == kCommandCreate) {
		MStatus status;

		status = dagMod.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		MFnDependencyNode fn_metadata(obj_metadata);
		// MFnDependencyNode fnShape(objShape);
		// TRANSFORM NODE
		MPlug plugTranslateX = fn_metadata.findPlug("translateX", false);
		LMAttribute::lockAndHideAttr(plugTranslateX);
		MPlug plugTranslateY = fn_metadata.findPlug("translateY", false);
		LMAttribute::lockAndHideAttr(plugTranslateY);
		MPlug plugTranslateZ = fn_metadata.findPlug("translateZ", false);
		LMAttribute::lockAndHideAttr(plugTranslateZ);
		MPlug plugRotateX = fn_metadata.findPlug("rotateX", false);
		LMAttribute::lockAndHideAttr(plugRotateX);
		MPlug plugRotateY = fn_metadata.findPlug("rotateY", false);
		LMAttribute::lockAndHideAttr(plugRotateY);
		MPlug plugRotateZ = fn_metadata.findPlug("rotateZ", false);
		LMAttribute::lockAndHideAttr(plugRotateZ);
		MPlug plugScaleX = fn_metadata.findPlug("scaleX", false);
		LMAttribute::lockAndHideAttr(plugScaleX);
		MPlug plugScaleY = fn_metadata.findPlug("scaleY", false);
		LMAttribute::lockAndHideAttr(plugScaleY);
		MPlug plugScaleZ = fn_metadata.findPlug("scaleZ", false);
		LMAttribute::lockAndHideAttr(plugScaleZ);
		// MPlug plugVisibility = fn_metadata.findPlug("visibility", false);
		// LMAttribute::lockAndHideAttr(plugVisibility);

		// Sets the plugs values based on the flag arguments
		MPlug plugMetaData(obj_metadata, MetaDataNode::attrInMetaData);
		// Get first plug in array
		MPlug plugText0 = plugMetaData.elementByPhysicalIndex(0).child(0);
		plugText0.setValue(text);

		MPlug plugTextPositionX(obj_metadata, MetaDataNode::AttrTextPositionX);
		plugTextPositionX.setValue(textPosition.x);
		MPlug plugTextPositionY(obj_metadata, MetaDataNode::AttrTextPositionY);
		plugTextPositionY.setValue(textPosition.y);

		MPlug plugTextSize(obj_metadata, MetaDataNode::AttrTextSize);
		plugTextSize.setInt(textSize);

		MPlug plugTextColor(obj_metadata, MetaDataNode::AttrTextColor);
		MPlug plugTextColorR = plugTextColor.child(0);
		plugTextColorR.setValue(textColor.r);
		MPlug plugTextColorG = plugTextColor.child(1);
		plugTextColorG.setValue(textColor.g);
		MPlug plugTextColorB = plugTextColor.child(2);
		plugTextColorB.setValue(textColor.b);

		MPlug plugTextVisbility(obj_metadata, MetaDataNode::visibility);
		plugTextVisbility.setValue(textVisibility);

		// Sets command's output result in mel / python
		clearResult();
		setResult(fn_metadata.name());
		// appendToResult(fnShape.name());
	}

	return MS::kSuccess;
}


MStatus MetaDataCmd::undoIt() {
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