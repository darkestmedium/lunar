#include "CtrlDrawOverride.h"



MBoundingBox CtrlDrawOverride::boundingBox(const MDagPath& objPath, const MDagPath& cameraPath) const {
	/* Called by Maya whenever the bounding box of the drawable object is needed.

	This method should return the object space bounding box for the object to be drawn.
	Note that this method will not be called if the isBounded() method returns a value of
	false.
	Default implementation returns a huge bounding box which will never cull the object.

	Args:
		objPath (MDagPath&): The path to the object being drawn
		cameraPath (MDagPath&): The path to the camera that is being used to draw

	Returns:
		MBoundingBox: The object space bounding box of object drawn in the draw callback

	*/
	CtrlData data;
	MObject node = objPath.node();

	data.getPlugs(node);
	data.getBBox(node, objPath, data.matLocalShape);

	return data.bBox;
}


MUserData* CtrlDrawOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath, const MHWRender::MFrameContext& frameContext, MUserData* oldData) {
	/* Called by Maya whenever the object is dirty and needs to update for draw.

	Any data needed from the Maya dependency graph must be retrieved and cached in this
	stage. It is invalid to pull data from the Maya dependency graph in the draw callback
	method and Maya may become unstable if that is attempted.

	Implementors may allow Maya to handle the data caching by returning a pointer to the
	data from this method. The pointer must be to a class derived from MUserData. This
	same pointer will be passed to the draw callback. On subsequent draws, the pointer
	will also be passed back into this method so that the data may be modified and reused
	instead of reallocated. If a different pointer is returned Maya will delete the old
	data. If the cache should not be maintained between draws, set the delete after use
	flag on the user data and Maya will delete it in a certain stage depending on whether
	the draw callback exists. If exists, the user data will be deleted after both
	addUIDrawables() and the draw callback are called; otherwise, the user data will be
	deleted immediately after addUIDrawables() is called. In all cases, the lifetime and
	ownership of the user data is handled by Maya and the user cshould not try to delete
	the data themselves. Data caching occurs per-instance of the associated DAG object.
	The lifetime of the user data can be longer than the associated node, instance or
	draw override. Due to internal caching, the user data can be deleted after an
	arbitrary long time. One should therefore be careful to not access stale objects from
	the user data destructor. If it is not desirable to allow Maya to handle data caching,
	simply return NULL in this method and ignore the user data parameter in the draw
	callback method.

	Args:
		objPath (MDagPath&): The path to the object being drawn
		cameraPath (MDagPath&): The path to the camera that is being used to draw
		frameContext (MHWRender::MFrameContext&): Frame level context information
		oldData (MUserData*) Data cached by the previous draw of the instance

	Returns:
		MUserData*: Pointer to data to be passed to the draw callback method

	*/
	MStatus status;

	CtrlData* data = dynamic_cast<CtrlData*>(oldData);
	MObject objShape = objPath.node(&status);

	if (!data) {data=new CtrlData;}

	data->getPlugs(objShape);
	data->getShape(objShape, objPath, data->matLocalShape);
	data->getText(objShape);

	data->_wfColor = MHWRender::MGeometryUtilities::wireframeColor(objPath);

	// If XRay Joints Draw in XRay Mode
	if (frameContext.getDisplayStyle() & MHWRender::MFrameContext::kXrayJoint) {data->DrawInXray = true;}
	else {data->DrawInXray = false;}

	switch (MHWRender::MGeometryUtilities::displayStatus(objPath))
	{
		case MHWRender::kLead:
		case MHWRender::kActive:
		case MHWRender::kHilite:
		case MHWRender::kActiveComponent:
			data->DepthPriority = MHWRender::MRenderItem::sActiveWireDepthPriority;
			break;
		default:
			data->DepthPriority = MHWRender::MRenderItem::sDormantFilledDepthPriority;
			break;
	}

	return data;
}


void CtrlDrawOverride::addUIDrawables(const MDagPath& objPath, MHWRender::MUIDrawManager& drawManager, const MHWRender::MFrameContext& frameContext, const MUserData* data) {
	/* Provides access to the MUIDrawManager, which can be used to queue up operations
	to draw simple UI shapes like lines, circles, text, etc.

	This method will only be called when this override is dirty and its hasUIDrawables()
	is overridden to return true. This method is called after prepareForDraw() and carries
	the same restrictions on the sorts of operations it can perform.

	Args:
		objPath (MDagPath&): The path to the object being drawn
		drawManager (MHWRender::MUIDrawManager&): The UI draw manager, it can be used to
			draw some simple geometry including text
		frameContext (MHWRender::MFrameContext&): Frame level context information
		data (MUserData*) Data cached by prepareForDraw()

	*/
	CtrlData* pCtrlData = (CtrlData*)data;
	if (!pCtrlData) {return;}

	// Define selectability
	if (pCtrlData->shapeIndex == 8) {
		drawManager.beginDrawable(MHWRender::MUIDrawManager::kNonSelectable);
	} else {
		drawManager.beginDrawable();
	}

	drawManager.setDepthPriority(pCtrlData->DepthPriority);

	// If XRay Joints Draw in XRay Mode
	if (pCtrlData->DrawInXray) {drawManager.beginDrawInXray();}
	
	// Draw the fill shape
	if (pCtrlData->fillShape)	{
		drawManager.setColor(pCtrlData->fillColor);
		drawManager.mesh(MHWRender::MUIDrawManager::kTriangles, pCtrlData->fTriangleList);
	}
	// Draw the outline
	drawManager.setColor(pCtrlData->_wfColor);
	drawManager.setLineWidth(pCtrlData->lineWidth);
	drawManager.mesh(MHWRender::MUIDrawManager::kLines, pCtrlData->fLineList);
	if (pCtrlData->bDrawline) {
		drawManager.mesh(MHWRender::MUIDrawManager::kLines, pCtrlData->listLine);
	}
	// Fk Ik State
	if (pCtrlData->bDrawFkIkState) {
		drawManager.setFontSize(12);
		drawManager.text(pCtrlData->posFkIkState, pCtrlData->strFkIkState, drawManager.kCenter);
	}

	// End drawable
	if (pCtrlData->DrawInXray) {drawManager.endDrawInXray();}

	drawManager.endDrawable();
}
