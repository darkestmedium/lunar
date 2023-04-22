#include "Ctrl.h"
#include "CtrlCommand.h"



// Public Data
const char* CtrlCommand::commandName = "ctrl";

// Command's Flags
const char* CtrlCommand::nameFlagShort = "-n";
const char* CtrlCommand::nameFlagLong = "-name";

const char* CtrlCommand::parentFlagShort = "-p";
const char* CtrlCommand::parentFlagLong = "-parent";

const char* CtrlCommand::translateToFlagShort = "-tt";
const char* CtrlCommand::translateToFlagLong = "-translateTo";

const char* CtrlCommand::rotatetToFlagShort = "-rt";
const char* CtrlCommand::rotatetToFlagLong = "-rotateTo";

const char* CtrlCommand::localPositionFlagShort = "-lp";
const char* CtrlCommand::localPositionFlagLong = "-localPosition";

const char* CtrlCommand::localRotateFlagShort = "-lr";
const char* CtrlCommand::localRotateFlagLong = "-localRotate";

const char* CtrlCommand::localScaleFlagShort = "-ls";
const char* CtrlCommand::localScaleFlagLong = "-localScale";

const char* CtrlCommand::shapeFlagShort = "-sh";
const char* CtrlCommand::shapeFlagLong = "-shape";

const char* CtrlCommand::fillShapeFlagShort = "-fs";
const char* CtrlCommand::fillShapeFlagLong = "-fillShape";

const char* CtrlCommand::drawLineFlagShort = "-dl";
const char* CtrlCommand::drawLineFlagLong = "-drawLine";

const char* CtrlCommand::drawFkIkStateFlagShort = "-dfi";
const char* CtrlCommand::drawFkIkStateFlagLong = "-drawFkIkState";

const char* CtrlCommand::fkIkStatePositionFlagShort = "-fis";
const char* CtrlCommand::fkIkStatePositionFlagLong = "-fkIkStatePosition";

const char* CtrlCommand::fillTransparencyFlagShort = "-ft";
const char* CtrlCommand::fillTransparencyFlagLong = "-fillTransparency";

const char* CtrlCommand::lineWidthFlagShort = "-lw";
const char* CtrlCommand::lineWidthFlagLong = "-lineWidth";

const char* CtrlCommand::colorFlagShort = "-cl";
const char* CtrlCommand::colorFlagLong = "-color";

const char* CtrlCommand::lockShapeAttributesFlagShort = "-lsa";
const char* CtrlCommand::lockShapeAttributesFlagLong = "-lockShapeAttributes";

const char* CtrlCommand::hideOnPlaybackFlagShort = "-hop";
const char* CtrlCommand::hideOnPlaybackFlagLong = "-hideOnPlayback";

const char* CtrlCommand::helpFlagShort = "-h";
const char* CtrlCommand::helpFlagLong = "-help";




MSyntax CtrlCommand::syntaxCreator() {
	/* Creates the command's syntax object and returns it.

	Returns:
		syntax (MSyntax): Command's syntax object

	*/
	MSyntax sytnax;

	// Main flags
	sytnax.addFlag(nameFlagShort, nameFlagLong, MSyntax::kString);
	sytnax.addFlag(parentFlagShort, parentFlagLong, MSyntax::kString);

	sytnax.addFlag(translateToFlagShort, translateToFlagLong, MSyntax::kString);
	sytnax.addFlag(rotatetToFlagShort, rotatetToFlagLong, MSyntax::kString);

	// Local flags
	sytnax.addFlag(localPositionFlagShort, localPositionFlagLong, MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);
	sytnax.addFlag(localRotateFlagShort, localRotateFlagLong, MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);
	sytnax.addFlag(localScaleFlagShort, localScaleFlagLong, MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);

	// Visual flags
	sytnax.addFlag(shapeFlagShort, shapeFlagLong, MSyntax::kString);
	sytnax.addFlag(fillShapeFlagShort, fillShapeFlagLong, MSyntax::kBoolean);
	sytnax.addFlag(drawLineFlagShort, drawLineFlagLong, MSyntax::kBoolean);
	sytnax.addFlag(fillTransparencyFlagShort, fillTransparencyFlagLong, MSyntax::kDouble);
	sytnax.addFlag(lineWidthFlagShort, lineWidthFlagLong, MSyntax::kDouble);
	sytnax.addFlag(colorFlagShort, colorFlagLong, MSyntax::kString);

	sytnax.addFlag(drawFkIkStateFlagShort, drawFkIkStateFlagLong, MSyntax::kBoolean);
	sytnax.addFlag(fkIkStatePositionFlagShort, fkIkStatePositionFlagLong, MSyntax::kDouble, MSyntax::kDouble, MSyntax::kDouble);

	sytnax.addFlag(lockShapeAttributesFlagShort, lockShapeAttributesFlagLong, MSyntax::kBoolean);
	sytnax.addFlag(hideOnPlaybackFlagShort, hideOnPlaybackFlagLong, MSyntax::kBoolean);
	
	sytnax.addFlag(helpFlagShort, helpFlagLong, MSyntax::kBoolean);

	sytnax.setObjectType(MSyntax::kSelectionList, 0, 1);
	sytnax.useSelectionAsDefault(true);

	return sytnax;
}


MStatus CtrlCommand::parseArguments(const MArgList &argList) {
	/* Parses the commands's flag arguments.

	Args:
		argList (MArglist): List of arguments passed to the command.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	MArgDatabase argData(syntax(), argList);
	argData.getObjects(listSelection);

	// Display Help
	if (argData.isFlagSet(helpFlagShort))	{
		command = kCommandHelp;
		MString strHelp;
		strHelp += "Flags:\n";
		strHelp += "   -n     -name                 String     Name of the rig controller to create.\n";
		strHelp += "   -p     -parent               String     Name of the object that will be the parent.\n";
		strHelp += "   -tt    -translateTo	        String     Name of the object that the controller will be translated to.\n";
		strHelp += "   -rt    -rotateTo             String     Name of the object that the controller will be rotated to.\n";
		strHelp += "   -lp    -localPosition        Double3    Local Position of the controller.\n";
		strHelp += "   -lr    -localRotate          Double3    Local Rotate of the controller.\n";
		strHelp += "   -ls    -localScale           Double3    Local Scale of the controller.\n";
		strHelp += "   -sh    -shape                String     Shape to be drawn: 'cube' 'sphere' cross' 'diamond' 'square' 'circle' 'locator' 'none'.\n";
		strHelp += "   -fs    -fillShape            Bool       Whether or not you want to render the solid shape or just the outline.\n";
		strHelp += "   -dl    -drawLine             Bool       Whether or not you want to display a line from the object center to a target.\n";
		strHelp += "   -dfis  -drawFkIkState        Bool       Whether or not you want to display te fk / ik  state.\n";
		strHelp += "   -fisp  -fkIkStatePosition    Double3    Local Position of the fk / ik state.\n";
		strHelp += "   -ft    -fillTransparency     Double     Controls the transparency of the fill shape.\n";
		strHelp += "   -fw    -lineWidth            Double     Controls the line width of the outline.\n";
		strHelp += "   -cl    -color                String     Viewport display color of the controller: 'lightyellow' 'yellow' 'lightorange' 'orange' 'lightblue' 'blue' 'magenta' 'green'.\n";
		strHelp += "   -lsa   -lockShapeAttributes  Bool       Locks all the shpae attributes on the shape node after creation.\n";
		strHelp += "   -hop   -hideOnPlayback       Bool       Wheter or not to hide the ctrl shapes on playback.\n";
		strHelp += "   -h     -help                 N/A        Display this text.\n";
		MGlobal::displayInfo(strHelp);
		return MS::kSuccess;
	}
	// Name Flag
	if (argData.isFlagSet(nameFlagShort))	{
		name = argData.flagArgumentString(nameFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Parent Flag
	if (argData.isFlagSet(parentFlagShort)) {
		listSelection.add(argData.flagArgumentString(parentFlagShort, 0, &status));
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// TranslateTo Flag
	if (argData.isFlagSet(translateToFlagShort)) {
		strTranslateTo = argData.flagArgumentString(translateToFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (strTranslateTo != "") {
			bTranslateTo = true;
			status = LMObject::getDagPathFromString(strTranslateTo, dpTargetTranslation);
			if (status == MS::kSuccess) {
				MFnTransform targetFn(dpTargetTranslation);
				posTarget = targetFn.getTranslation(MSpace::kWorld);
			}	else {
				return MS::kFailure;
			}
		}
	}
	// RotateTo Flag
	if (argData.isFlagSet(rotatetToFlagShort)) {
		strRotateTo = argData.flagArgumentString(rotatetToFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (strRotateTo != "") {
			bRotateTo = true;
			status = LMObject::getDagPathFromString(strRotateTo, dpTargetRotation);
			if (status == MS::kSuccess)	{
				MFnTransform targetFn(dpTargetRotation);
				targetFn.getRotation(rotTarget, MSpace::kWorld);
			}	else {
				return MS::kFailure;
			}
		}
	}
	// Local Position Flag
	if (argData.isFlagSet(localPositionFlagShort)) {
		localPosition.x = argData.flagArgumentDouble(localPositionFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localPosition.y = argData.flagArgumentDouble(localPositionFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localPosition.z = argData.flagArgumentDouble(localPositionFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Local Rotate Flag
	if (argData.isFlagSet(localRotateFlagShort)) {
		localRotate.x = argData.flagArgumentDouble(localRotateFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localRotate.y = argData.flagArgumentDouble(localRotateFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localRotate.z = argData.flagArgumentDouble(localRotateFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Local Scale Flag
	if (argData.isFlagSet(localScaleFlagShort))	{
		localScale.x = argData.flagArgumentDouble(localScaleFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localScale.y = argData.flagArgumentDouble(localScaleFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		localScale.z = argData.flagArgumentDouble(localScaleFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Shape Flag
	if (argData.isFlagSet(shapeFlagShort)) {
		MString strShape = argData.flagArgumentString(shapeFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (strShape == "cube")	{
			indxShape = 0;
		} else if (strShape == "sphere") {
			indxShape = 1;
		}	else if (strShape == "cross") {
			indxShape = 2;
		} else if (strShape == "diamond") {
			indxShape = 3;
		} else if (strShape == "square") {
			indxShape = 4;
		}	else if (strShape == "circle") {
			indxShape = 5;
		} else if (strShape == "locator") {
			indxShape = 6;
		} else if (strShape == "line") {
			indxShape = 7;
		} else if (strShape == "none") {
			indxShape = 8;
		}	else {
			indxShape = 0;
		}
	}
	// Fill Shape Flag
	if (argData.isFlagSet(fillShapeFlagShort)) {
		bFillShape = argData.flagArgumentBool(fillShapeFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Draw Line Flag
	if (argData.isFlagSet(drawLineFlagShort)) {
		bDrawLine = argData.flagArgumentBool(drawLineFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Draw Fk Ik State Flag
	if (argData.isFlagSet(drawFkIkStateFlagShort)) {
		bDrawFkIkState = argData.flagArgumentBool(drawFkIkStateFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Fk Ik State Position Flag
	if (argData.isFlagSet(fkIkStatePositionFlagShort)) {
		fkIkStatePosition.x = argData.flagArgumentDouble(fkIkStatePositionFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fkIkStatePosition.y = argData.flagArgumentDouble(fkIkStatePositionFlagShort, 1, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		fkIkStatePosition.z = argData.flagArgumentDouble(fkIkStatePositionFlagShort, 2, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Fill Transparency Flag
	if (argData.isFlagSet(fillTransparencyFlagShort)) {
		fillTransparency = argData.flagArgumentDouble(fillTransparencyFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Line Width Flag
	if (argData.isFlagSet(lineWidthFlagShort)) {
		lineWidth = argData.flagArgumentDouble(lineWidthFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Color Flag
	if (argData.isFlagSet(colorFlagShort)) {
		strColor = argData.flagArgumentString(colorFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		if (strColor == "lightyellow")	{
			colorOverride.r = 1.0; colorOverride.g = 1.0; colorOverride.b = 0.25;
		} else if (strColor == "yellow") {
			colorOverride.r = 1.0; colorOverride.g = 0.6;	colorOverride.b = 0.1;
		} else if (strColor == "lightorange") {
			colorOverride.r = 1.0; colorOverride.g = 0.467;	colorOverride.b = 0.2;
		} else if (strColor == "orange") {
			colorOverride.r = 0.8; colorOverride.g = 0.25; colorOverride.b = 0.05;
		}	else if (strColor == "lightblue")	{
			colorOverride.r = 0.4; colorOverride.g = 0.8; colorOverride.b = 1.0;
		}	else if (strColor == "blue") {
			colorOverride.r = 0.05;	colorOverride.g = 0.25; colorOverride.b = 0.8;
		}	else if (strColor == "magenta") {
			colorOverride.r = 0.6; colorOverride.g = 0.2; colorOverride.b = 0.4;
		}	else if (strColor == "green") {
			colorOverride.r = 0.2;	colorOverride.g = 0.8; colorOverride.b = 0.4;
		}
	}
	// Lock shape attributes
	if (argData.isFlagSet(lockShapeAttributesFlagShort)) {
		bLockShapeAttributes = argData.flagArgumentBool(lockShapeAttributesFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Hide shapes on playback
	if (argData.isFlagSet(hideOnPlaybackFlagShort))	{
		bHideOnPlayback = argData.flagArgumentBool(hideOnPlaybackFlagShort, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	return MS::kSuccess;
}



MStatus CtrlCommand::doIt(const MArgList& argList) {
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
		objThisTransform = modDag.createNode("transform", MObject::kNullObj);
		objThisShape = modDag.createNode(Ctrl::typeName, objThisTransform);
		// If __name equals to "rigController" rename only the transform node as the shape node will be
		// renamed in the rigController.RigController::postConstructor method.
		if (name == Ctrl::typeName)	{
			modDag.renameNode(objThisTransform, name);
		}	else {
			modDag.renameNode(objThisTransform, name);
			modDag.renameNode(objThisShape, name + "Shape");
		}
		// Parent under the transform node if the selection is not empty and / or parent was specified
		int numItems = listSelection.length();
		if (numItems == 1) {
			MObject parentObj;
			listSelection.getDependNode(0, parentObj);
			modDag.reparentNode(objThisTransform, parentObj);
		}	else if (numItems == 2)	{
			MObject parentObj;
			listSelection.getDependNode(1, parentObj);
			modDag.reparentNode(objThisTransform, parentObj);
		}
	}

	return redoIt();
}


MStatus CtrlCommand::redoIt() {
	/* Command's redoIt method.

	This method should do the actual work of the command based on the internal class data only.	Internal class data should be set in the doIt method.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	// Command create mode
	if (command == kCommandCreate) {
		MStatus status;
		// We need to init the MFnTransform with a dag path, mobjects do not work with transformations
		// even if the object has a MFn::kTransform
		MDagPath::getAPathTo(objThisTransform, dpThisTransform);
		MFnTransform transformFn(dpThisTransform);
		MFnDependencyNode shapeFn(objThisShape);

		status = modDag.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		{	// TRANSFORM NODE
			if (bTranslateTo == true) {
				transformFn.setTranslation(posTarget, MSpace::kWorld);
			}
			if (bRotateTo == true) {
				transformFn.setRotation(rotTarget, MSpace::kWorld);
			}
		}

		{ // SHAPE NODE
			// Sets the plugs values based on the flag arguments
			MPlug plugShape = shapeFn.findPlug("shape", false);
			plugShape.setShort(indxShape);

			// Sets local position values
			MPlug plugLocalPositionX = shapeFn.findPlug("localPositionX", false);
			plugLocalPositionX.setValue(localPosition.x);
			MPlug plugLocalPositionY = shapeFn.findPlug("localPositionY", false);
			plugLocalPositionY.setValue(localPosition.y);
			MPlug plugLocalPositionZ = shapeFn.findPlug("localPositionZ", false);
			plugLocalPositionZ.setValue(localPosition.z);

			// Sets local rotate values
			MPlug plugLocalRotateX = shapeFn.findPlug("localRotateX", false);
			plugLocalRotateX.setValue(radians(localRotate.x));
			MPlug plugLocalRotateY = shapeFn.findPlug("localRotateY", false);
			plugLocalRotateY.setValue(radians(localRotate.y));
			MPlug plugLocalRotateZ = shapeFn.findPlug("localRotateZ", false);
			plugLocalRotateZ.setValue(radians(localRotate.z));

			// Sets local scale values
			MPlug plugLocalScaleX = shapeFn.findPlug("localScaleX", false);
			plugLocalScaleX.setValue(localScale.x);
			MPlug plugLocalScaleY = shapeFn.findPlug("localScaleY", false);
			plugLocalScaleY.setValue(localScale.y);
			MPlug plugLocalScaleZ = shapeFn.findPlug("localScaleZ", false);
			plugLocalScaleZ.setValue(localScale.z);

			// Visual flags
			MPlug plugFillShape = shapeFn.findPlug("fillShape", false);
			plugFillShape.setValue(bFillShape);

			MPlug plugDrawLine = shapeFn.findPlug("drawLine", false);
			plugDrawLine.setValue(bDrawLine);

			// Fk Ik State
			MPlug plugDrawFkIkState = shapeFn.findPlug("drawFkIkState", false);
			plugDrawFkIkState.setValue(bDrawFkIkState);
			MPlug plugFkIkStatePosition = shapeFn.findPlug("fkIkStatePosition", false);

			MPlug plugFkIkStatePositionX = shapeFn.findPlug("fkIkStatePositionX", false);
			plugFkIkStatePositionX.setValue(fkIkStatePosition.x);
			MPlug plugFkIkStatePositionY = shapeFn.findPlug("fkIkStatePositionY", false);
			plugFkIkStatePositionY.setValue(fkIkStatePosition.y);
			MPlug plugFkIkStatePositionZ = shapeFn.findPlug("fkIkStatePositionZ", false);
			plugFkIkStatePositionZ.setValue(fkIkStatePosition.z);

			MPlug plugInFkIk = shapeFn.findPlug("fkIk", false);

			MPlug plugFillTransparency = shapeFn.findPlug("fillTransparency", false);
			plugFillTransparency.setValue(fillTransparency);

			MPlug plugLineWidth = shapeFn.findPlug("lineWidth", false);
			plugLineWidth.setValue(lineWidth);

			// Set color
			MPlug plugOverrideColorR = shapeFn.findPlug("overrideColorR", false);
			plugOverrideColorR.setValue(colorOverride.r);
			MPlug plugOverrideColorG = shapeFn.findPlug("overrideColorG", false);
			plugOverrideColorG.setValue(colorOverride.g);
			MPlug plugOverrideColorB = shapeFn.findPlug("overrideColorB", false);
			plugOverrideColorB.setValue(colorOverride.b);

			// Lock shape attributes
			if (bLockShapeAttributes == true) {
				// optimize with a for loop and MPlugArray
				// Local position
				LMAttribute::lockAndHideAttr(plugLocalPositionX);
				LMAttribute::lockAndHideAttr(plugLocalPositionY);
				LMAttribute::lockAndHideAttr(plugLocalPositionZ);
				// Local rotate
				LMAttribute::lockAndHideAttr(plugLocalRotateX);
				LMAttribute::lockAndHideAttr(plugLocalRotateY);
				LMAttribute::lockAndHideAttr(plugLocalRotateZ);
				// Local scale
				LMAttribute::lockAndHideAttr(plugLocalScaleX);
				LMAttribute::lockAndHideAttr(plugLocalScaleY);
				LMAttribute::lockAndHideAttr(plugLocalScaleZ);
				// Shape attrs
				LMAttribute::lockAndHideAttr(plugShape);
				LMAttribute::lockAndHideAttr(plugFillShape);
				LMAttribute::lockAndHideAttr(plugDrawLine);

				LMAttribute::lockAndHideAttr(plugDrawFkIkState);
				LMAttribute::lockAndHideAttr(plugFkIkStatePosition);
				// LMAttribute::lockAndHideAttr(plugFkIkStatePositionY);
				// LMAttribute::lockAndHideAttr(plugFkIkStatePositionZ);

				LMAttribute::lockAndHideAttr(plugFillTransparency);
				LMAttribute::lockAndHideAttr(plugLineWidth);

				LMAttribute::lockAndHideAttr(plugInFkIk);
			}
		}
		// Set hide on playback
		MPlug plugHideOnPlayback = shapeFn.findPlug("hideOnPlayback", false);
		plugHideOnPlayback.setValue(bHideOnPlayback);

		// Sets command's output result in mel / python
		clearResult();
		appendToResult(transformFn.name());
		appendToResult(shapeFn.name());
	}

	return MS::kSuccess;
}


MStatus CtrlCommand::undoIt() {
	/* Command's undoIt method.

	This method should undo the work done by the redoIt method based on the internal class data only.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	// Restore the initial state
	status = modDag.undoIt();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}
