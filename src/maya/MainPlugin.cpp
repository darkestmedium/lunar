#include "Ctrl.h"
#include "CtrlDrawOverride.h"
#include "CtrlCommand.h"
#include "Ik2bSolver.h"
#include "IkCommand.h"
#include "FootRollSolver.h"
#include "MetaDataNode.h"
#include "MetaDataCmd.h"
#include "TwistSolver.h"

// Function Sets
#include <maya/MFnPlugin.h>




// Callback variables
static MCallbackIdArray callbackIds;
static MCallbackId afterNewCallbackId;
static MCallbackId afterOpenCallbackId;

static MCallbackId afterSaveSetMetaDataNodeCbId;



void setMelConfig(void*) {
	/* Sets the selection priority for locators to 999. */
	MGlobal::executeCommandOnIdle("cycleCheck -e 0");
	MGlobal::executeCommandOnIdle("selectPriority -locator 999");
}

static void onSceneSaved(void* clientData) {

	MGlobal::executePythonCommand("import lunar.maya.LunarMaya as lm");
	MGlobal::executePythonCommand("lm.LMMetaData().setFromSceneName()");

}



MStatus initializePlugin(MObject obj) {
	// Plugin variables
	const char* author = "Lunatics";
	const char* version = "0.3.1";
	const char* requiredApiVersion = "Any";

	MStatus status;
	MFnPlugin pluginFn(obj, author, version, requiredApiVersion);

	// Register Controller node
	status = pluginFn.registerNode(
		Ctrl::typeName,
		Ctrl::typeId,
		Ctrl::creator,
		Ctrl::initialize,
		MPxLocatorNode::kLocatorNode,
		&Ctrl::drawDbClassification
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Register Controller draw override
	status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
		Ctrl::drawDbClassification,
		Ctrl::drawRegistrationId,
		CtrlDrawOverride::creator
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Register Controller command
	status = pluginFn.registerCommand(
		CtrlCommand::commandName,
		CtrlCommand::creator,
		CtrlCommand::syntaxCreator
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Register Ik2bSolver node
	status = pluginFn.registerNode(
		Ik2bSolver::typeName,
		Ik2bSolver::typeId,
		Ik2bSolver::creator,
		Ik2bSolver::initialize,
		MPxNode::kDependNode
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Register ik command
	status = pluginFn.registerCommand(
		IkCommand::commandName,
		IkCommand::creator,
		IkCommand::syntaxCreator
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Register MetaData node
	status = pluginFn.registerNode(
		MetaDataNode::typeName,
		MetaDataNode::typeId,
		MetaDataNode::creator,
		MetaDataNode::initialize,
	 	MPxLocatorNode::kLocatorNode,
	 	&MetaDataNode::drawDbClassification
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Register MetaData draw override
	status = MHWRender::MDrawRegistry::registerDrawOverrideCreator(
		MetaDataNode::drawDbClassification,
		MetaDataNode::drawRegistrationId,
		MetaDataNodeDrawOverride::creator
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Register MetaData command
	status = pluginFn.registerCommand(
		MetaDataCmd::commandName,
		MetaDataCmd::creator,
		MetaDataCmd::syntaxCreator
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Register FootRoll node
	status = pluginFn.registerNode(
		FootRollSolver::typeName,
		FootRollSolver::typeId,
		FootRollSolver::creator,
		FootRollSolver::initialize,
		MPxNode::kDependNode
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Register TwistSolver node
	status = pluginFn.registerNode(
		TwistSolver::typeName,
		TwistSolver::typeId,
		TwistSolver::creator,
		TwistSolver::initialize,
		MPxNode::kDependNode
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	if (MGlobal::mayaState() == MGlobal::kInteractive) {
		// Register callback to set selection priority on locators to 999
		setMelConfig(NULL);

		afterNewCallbackId = MSceneMessage::addCallback(MSceneMessage::kAfterNew, setMelConfig, NULL, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		callbackIds.append(afterNewCallbackId);

		afterOpenCallbackId = MSceneMessage::addCallback(MSceneMessage::kAfterOpen, setMelConfig, NULL, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		callbackIds.append(afterOpenCallbackId);
	
		afterSaveSetMetaDataNodeCbId = MSceneMessage::addCallback(MSceneMessage::kBeforeSave, onSceneSaved, NULL, &status);
		CHECK_MSTATUS_AND_RETURN_IT(status);
		callbackIds.append(afterSaveSetMetaDataNodeCbId);

		// // Creates the maya main menu items
		// MGlobal::executePythonCommandOnIdle("from lunar.maya.resources.scripts.ctrlMainMenu import CtrlMainMenu");
		// MGlobal::executePythonCommandOnIdle("CtrlMainMenu().createMenuItems()");
	}

	return status;
}



MStatus uninitializePlugin(MObject obj) {
	MStatus status;
	MFnPlugin pluginFn(obj);

	MMessage::removeCallbacks(callbackIds);

	// Deregister TwistSolver
	status = pluginFn.deregisterNode(TwistSolver::typeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Deregister Footroll Node
	status = pluginFn.deregisterNode(FootRollSolver::typeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Deregister MetaData command
	status = pluginFn.deregisterCommand(IkCommand::commandName);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Deregister MetaData draw override
	status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(
		MetaDataNode::drawDbClassification,
		MetaDataNode::drawRegistrationId
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Deregister MetaDataNode
	status = pluginFn.deregisterNode(MetaDataNode::typeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Deregister IkCommand
	status = pluginFn.deregisterCommand(IkCommand::commandName);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Deregister Ik2Solver
	status = pluginFn.deregisterNode(Ik2bSolver::typeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Deregister Controller command
	status = pluginFn.deregisterCommand(CtrlCommand::commandName);
	CHECK_MSTATUS_AND_RETURN_IT(status);
	// Deregister Controller draw override
	status = MHWRender::MDrawRegistry::deregisterDrawOverrideCreator(
		Ctrl::drawRegistrationId,
		Ctrl::drawDbClassification
	);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// Deregister Controller node
	status = pluginFn.deregisterNode(Ctrl::typeId);
	CHECK_MSTATUS_AND_RETURN_IT(status);

	// // Deletes the maya main menu items
	// if (MGlobal::mayaState() == MGlobal::kInteractive)
	// {
	// MGlobal::executePythonCommandOnIdle("CtrlMainMenu().deleteMenuItems()");
	// }

	return status;
}
