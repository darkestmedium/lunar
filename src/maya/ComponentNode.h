#pragma once

// System includes
#include <math.h>
#include <cassert>
#include <memory>
#include <unordered_map>
#include <atomic>

#include <maya/MUserData.h>
#include <maya/MMatrix.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MColor.h>
#include <maya/MDistance.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MGlobal.h>
#include <maya/MDagMessage.h>
#include <maya/MEvaluationNode.h>
#include <maya/MEventMessage.h>
#include <maya/MEvaluationManager.h>
#include <maya/MEvaluationNode.h>
#include <maya/MDagModifier.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>

// Function sets
#include <maya/MFnEnumAttribute.h>

// Viewport 2.0 includes
#include <maya/MDrawRegistry.h>
#include <maya/MPxGeometryOverride.h>
#include <maya/MShaderManager.h>
#include <maya/MHWGeometry.h>
#include <maya/MHWGeometryUtilities.h>

// Proxies
#include <maya/MPxTransform.h>
#include <maya/MPxCommand.h>
#include <maya/MPxSurfaceShape.h>
#include <maya/MPxDrawOverride.h>

// Lunar
#include "../maya/api/Utils.h"
#include "../maya/api/LMText.h"

#include "../maya/api/LMAttribute.h"




//-------------------------------------------------------------------------------------------------
//
// Component Transform Node definition
//
//-------------------------------------------------------------------------------------------------


class ComponentNode : public MPxTransform {
	/* Component Node - transform instance with a custom type_name. */
public:
	// Class attributes
	static const MString type_name;
	static const MTypeId type_id;
	static const MString type_drawdb;
	static const MString type_drawid;

	// Node attributes

	MObject self_object;

	// Constructors
	ComponentNode()
		: MPxTransform()
	{};
	// Destructors
	virtual ~ComponentNode() override {};

	// Class Methods
	static void * 	creator() {return new ComponentNode();};
	static MStatus	initialize() {return MS::kSuccess;};
	virtual void 		postConstructor() override;

	void 					  getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const override;
	SchedulingType  schedulingType() const override {return SchedulingType::kParallel;}

};


// Class attributes
const MString ComponentNode::type_name 		= "component";
const MTypeId ComponentNode::type_id 			= 0x9000001;
const MString ComponentNode::type_drawdb	= "drawdb/geometry/animation/component";
const MString ComponentNode::type_drawid	= "componentPlugin";


void ComponentNode::postConstructor() {
	self_object=thisMObject();
	MFnDependencyNode fn_this(self_object);

	fn_this.findPlug("shear", false).setLocked(true);
	// fn_this.findPlug("rotateAxis", false).setLocked(true);
}


void ComponentNode::getCacheSetup(const MEvaluationNode& evalNode, MNodeCacheDisablingInfo& disablingInfo, MNodeCacheSetupInfo& cacheSetupInfo, MObjectArray& monitoredAttributes) const {
	/* Disables Cached Playback support by default.

	Built-in locators all enable Cached Playback by default, but plug-ins have to
	explicitly enable it by overriding this method.
	This method should be overridden to enable Cached Playback by default for custom locators.

	Args:
		evalNode (MEvaluationNode&): This node's evaluation node, contains animated plug information
		disablingInfo (MNodeCacheDisablingInfo&): Information about why the node disables caching to be reported to the user
		cacheSetup (MNodeCacheSetupInfo&): Preferences and requirements this node has for caching
		monitoredAttribures (MObjectArray&): Attributes impacting the behavior of this method that will be monitored for change

	*/
	MPxTransform::getCacheSetup(evalNode, disablingInfo, cacheSetupInfo, monitoredAttributes);
	assert(!disablingInfo.getCacheDisabled());
	cacheSetupInfo.setPreference(MNodeCacheSetupInfo::kWantToCacheByDefault, true);
}




//-------------------------------------------------------------------------------------------------
//
// Component Transform Node definition
//
//-------------------------------------------------------------------------------------------------


class ComponentCmd : public MPxCommand {
public:
	enum CommandMode {kCommandCreate, kCommandHelp};
	CommandMode command;

	// Public Data
	static const char* command_name;

	// Command's Flags
	static const char* fs_name;
	static const char* fl_name;
	static const char* fs_parent;
	static const char* fl_parent;
	static const char* fs_lock_attributes;
	static const char* fl_lock_attributes;
	static const char* fs_help;
	static const char* fl_help;

	MString name;
	MString parent;
	bool lock_attributes;

	// Constructors
	ComponentCmd()
 		: MPxCommand()
		, name(ComponentNode::type_name)
		, lock_attributes(false)
		, command(kCommandCreate)
	{};

	// Inherited Public Methods
	static void* creator() {return new ComponentCmd();}
	virtual bool isUndoable() const override {return command == kCommandCreate;}
	static MSyntax syntaxCreator();

	virtual MStatus doIt(const MArgList& argList) override;
	virtual MStatus redoIt() override;
	virtual MStatus undoIt() override;

	MStatus parseArguments(const MArgList& argList);

private:
	MObject self_object;
	MDagPath self_dp;

	MSelectionList list_sel;
	MDagModifier mod_dag;
};


// Public Data
const char* ComponentCmd::command_name = "component";

// Command's Flags
const char* ComponentCmd::fs_name = "-n";
const char* ComponentCmd::fl_name = "-name";
const char* ComponentCmd::fs_parent = "-p";
const char* ComponentCmd::fl_parent = "-parent";
const char* ComponentCmd::fs_lock_attributes = "-la";
const char* ComponentCmd::fl_lock_attributes = "-lockAttributes";
const char* ComponentCmd::fs_help = "-h";
const char* ComponentCmd::fl_help = "-help";



MSyntax ComponentCmd::syntaxCreator() {
	/* Creates the command's syntax object and returns it.

	Returns:
		syntax (MSyntax): Command's syntax object

	*/
	MSyntax sytnax;

	// Main flags
	sytnax.addFlag(fs_name, fl_name, MSyntax::kString);
	sytnax.addFlag(fs_parent, fl_parent, MSyntax::kString);
	sytnax.addFlag(fs_lock_attributes, fl_lock_attributes, MSyntax::kBoolean);
	sytnax.addFlag(fs_help, fl_help, MSyntax::kBoolean);

	sytnax.setObjectType(MSyntax::kSelectionList, 0, 1);
	sytnax.useSelectionAsDefault(true);

	return sytnax;
}


MStatus ComponentCmd::parseArguments(const MArgList &argList) {
	/* Parses the commands's flag arguments.

	Args:
		argList (MArglist): List of arguments passed to the command.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	MArgDatabase argData(syntax(), argList);
	argData.getObjects(list_sel);

	// Display Help
	if (argData.isFlagSet(fs_help))	{
		command = kCommandHelp;
		MString strHelp;
		strHelp += "Flags:\n";
		strHelp += "   -n     -name                 String     Name of the rig controller to create.\n";
		strHelp += "   -p     -parent               String     Name of the object that will be the parent.\n";
		strHelp += "   -la    -lockAttributes       String     Whether or not to lock the transform attributes.\n";
		strHelp += "   -h     -help                 N/A        Display this text.\n";
		MGlobal::displayInfo(strHelp);
		return MS::kSuccess;
	}
	// Name Flag
	if (argData.isFlagSet(fs_name))	{
		name = argData.flagArgumentString(fs_name, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Parent Flag
	if (argData.isFlagSet(fs_parent)) {
		list_sel.add(argData.flagArgumentString(fs_parent, 0, &status));
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}
	// Lock shape attributes
	if (argData.isFlagSet(fs_lock_attributes)) {
		lock_attributes = argData.flagArgumentBool(fs_lock_attributes, 0, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
	}

	return MS::kSuccess;
}


MStatus ComponentCmd::doIt(const MArgList& argList) {
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
		self_object = mod_dag.createNode(ComponentNode::type_name, MObject::kNullObj);
		if (name != ComponentNode::type_name) {mod_dag.renameNode(self_object, name);}
		// Parent under the transform node if the selection is not empty and / or parent was specified
		int numItems = list_sel.length();
		if (numItems == 1) {
			MObject parent_object;
			list_sel.getDependNode(0, parent_object);
			mod_dag.reparentNode(self_object, parent_object);
		}	else if (numItems == 2)	{
			MObject parent_object;
			list_sel.getDependNode(1, parent_object);
			mod_dag.reparentNode(self_object, parent_object);
		}
	}

	return redoIt();
}


MStatus ComponentCmd::redoIt() {
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
		MDagPath::getAPathTo(self_object, self_dp);
		MFnTransform fn_transform(self_dp);

		status = mod_dag.doIt();
		CHECK_MSTATUS_AND_RETURN_IT(status);

		// TRANSFORM NODE
		// if (bTranslateTo == true) {fn_transform.setTranslation(posTarget, MSpace::kWorld);}
		// if (bRotateTo == true) {fn_transform.setRotation(rotTarget, MSpace::kWorld);}
	
		// MPlug plug_has_dynamic_attributes = fn_transform.findPlug("hasDynamicAttributes", false);
		// plug_has_dynamic_attributes.setValue(has_dynamic_attributes);

		// Lock shape attributes
		if (lock_attributes == true) {	
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::translate);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::rotate);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::scale);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::shear);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::rotateAxis);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::rotateOrder);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::inheritsTransform);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::offsetParentMatrix);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::rotateQuaternion);
			LMAttribute::lockAndHideAttr(self_object, ComponentNode::visibility);
		}

		// Set hide on playback
		// fn_transform.findPlug("hideOnPlayback", false).setValue(bHideOnPlayback);

		// Sets command's output result in mel / python
		clearResult();
		setResult(fn_transform.name());
		// appendToResult(fn_transform.name());
	}

	return MS::kSuccess;
}


MStatus ComponentCmd::undoIt() {
	/* Command's undoIt method.

	This method should undo the work done by the redoIt method based on the internal class data only.

	Returns:
		status code (MStatus): kSuccess if the command was successful, kFailure if an error occured
			during the command.

	*/
	MStatus status;

	// Restore the initial state
	status = mod_dag.undoIt();
	CHECK_MSTATUS_AND_RETURN_IT(status);

	return MS::kSuccess;
}

