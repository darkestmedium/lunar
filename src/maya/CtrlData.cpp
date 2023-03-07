#include "Ctrl.h"
#include "CtrlData.h"
#include "ShapesDefinition.h"



void CtrlData::getPlugs(const MObject& obj)
{
	/* Get all the necessary data from the attributes of the locator.

	Args:
		obj (MObject &): Object passed to query the attrbutes from

	*/
	float tx = MPlug(obj, Ctrl::localPositionX).asFloat();
	float ty = MPlug(obj, Ctrl::localPositionY).asFloat();
	float tz = MPlug(obj, Ctrl::localPositionZ).asFloat();

	float rx = MPlug(obj, Ctrl::localRotateX).asFloat();
	float ry = MPlug(obj, Ctrl::localRotateY).asFloat();
	float rz = MPlug(obj, Ctrl::localRotateZ).asFloat();

	float sx = MPlug(obj, Ctrl::localScaleX).asFloat();
	float sy = MPlug(obj, Ctrl::localScaleY).asFloat();
	float sz = MPlug(obj, Ctrl::localScaleZ).asFloat();

	MEulerRotation eulerRot(rx, ry, rz);
	this->matLocalShape = eulerRot.asMatrix();
	this->matLocalShape.matrix[0][0] *= sx;
	this->matLocalShape.matrix[0][1] *= sx;
	this->matLocalShape.matrix[0][2] *= sx;

	this->matLocalShape.matrix[1][0] *= sy;
	this->matLocalShape.matrix[1][1] *= sy;
	this->matLocalShape.matrix[1][2] *= sy;

	this->matLocalShape.matrix[2][0] *= sz;
	this->matLocalShape.matrix[2][1] *= sz;
	this->matLocalShape.matrix[2][2] *= sz;

	this->matLocalShape.matrix[3][0] = tx;
	this->matLocalShape.matrix[3][1] = ty;
	this->matLocalShape.matrix[3][2] = tz;

	MFnDependencyNode thisFn(obj);
	fillShape = MPlug(obj, Ctrl::fillShapeAttr).asBool();
	bDrawline = MPlug(obj, Ctrl::attrInDrawLine).asBool();
	fillColor = MColor(
		thisFn.findPlug("overrideColorR", false).asFloat(),
		thisFn.findPlug("overrideColorG", false).asFloat(),
		thisFn.findPlug("overrideColorB", false).asFloat(),
		MPlug(obj, Ctrl::fillTransparencyAttr).asFloat()
	);
	lineWidth = MPlug(obj, Ctrl::lineWidthAttr).asFloat();
}


void CtrlData::getBBox(const MObject& obj, const MDagPath& pathObj, MMatrix matrix) 
{
	/* Gets the bounding box from the shapesDefinition.h file

	Args:
		obj (MObject &): Object passed to query the attrbutes from
		matrix (MMatrix): Matrix used to transform the bounding box

	*/
	unsigned int shapeIndex = MPlug(obj, Ctrl::shapeAttr).asInt();

	// Cube
	if (shapeIndex == 0) {
		this->bBox = MBoundingBox(
			MPoint(cubeBB[0][0], cubeBB[0][1], cubeBB[0][2]),
			MPoint(cubeBB[1][0], cubeBB[1][1], cubeBB[1][2])
		);
	// Sphere
	} else if (shapeIndex == 1) {
		this->bBox = MBoundingBox(
			MPoint(sphereBB[0][0], sphereBB[0][1], sphereBB[0][2]),
			MPoint(sphereBB[1][0], sphereBB[1][1], sphereBB[1][2])
		);
	// Cross
	} else if (shapeIndex == 2) {
		this->bBox = MBoundingBox(
			MPoint(crossBB[0][0], crossBB[0][1], crossBB[0][2]),
			MPoint(crossBB[1][0], crossBB[1][1], crossBB[1][2])
		);
	// Diamond
	} else if (shapeIndex == 3) {
		this->bBox = MBoundingBox(
			MPoint(diamondBB[0][0], diamondBB[0][1], diamondBB[0][2]),
			MPoint(diamondBB[1][0], diamondBB[1][1], diamondBB[1][2])
		);
	// Square
	} else if (shapeIndex == 4) {
		this->bBox = MBoundingBox(
			MPoint(squareBB[0][0], squareBB[0][1], squareBB[0][2]),
			MPoint(squareBB[1][0], squareBB[1][1], squareBB[1][2])
		);
	// Circle
	} else if (shapeIndex == 5) {
		this->bBox = MBoundingBox(
			MPoint(circleBB[0][0], circleBB[0][1], circleBB[0][2]),
			MPoint(circleBB[1][0], circleBB[1][1], circleBB[1][2])
		);

	// Locator
	} else if (shapeIndex == 6) {
		this->bBox = MBoundingBox(
			MPoint(nullBB[0][0], nullBB[0][1], nullBB[0][2]),
			MPoint(nullBB[1][0], nullBB[1][1], nullBB[1][2])
		);

	// Line
	} else if (shapeIndex == 7) {
		this->bBox = MBoundingBox(
			MPoint(lineBB[0][0], lineBB[0][1], lineBB[0][2]),
			MPoint(lineBB[1][0], lineBB[1][1], lineBB[1][2])
		);
	}
	this->bBox.transformUsing(matrix);

	// MMatrix matDrawLineTo = MDataHandle(MPlug(obj, Ctrl::attrInDrawLineTo).asMDataHandle()).asMatrix();
	// this->bBox.expand(MPoint(matDrawLineTo[3][0], matDrawLineTo[3][1], matDrawLineTo[3][2]));

}


void CtrlData::getShape(const MObject& obj, const MDagPath& pathObj, MMatrix matrix) {
	/* Get the points for each line and triangle used for drawing the shape.

	Do not reorder the triangle append order since it will flip normals.

	Args:
		obj (MObject &): Object passed to query the attrbutes from
		matrix (MMatrix): Matrix used to transform the line points

	*/
	MStatus status;

	unsigned int shapeIndex = MPlug(obj, Ctrl::shapeAttr).asInt();

	this->fTransformedList.clear();
	this->fLineList.clear();
	this->fTriangleList.clear();
	this->listLine.clear();

	if (shapeIndex == 0) {  // Cube
		for (int i=0; i<cubeCount; i++) {
			fTransformedList.append(
				MPoint(listPointsCube[i][0], listPointsCube[i][1], listPointsCube[i][2]) * matrix
			);
		}
		// Top Quad
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[0]);
		// Side Lines
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[7]);
		// Bottom Quad
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[4]);
		if (fillShape) {
			// Top Quad
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[0]);
			// Right Quad
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[0]);
			// Front Quad
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[0]);
			// Back Quad
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[6]);
			// Left Quad
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[6]);
			// Bottom Quad
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[6]);
		}

	} else if (shapeIndex == 1) {	 // Sphere
		for (int i=0; i<sphereCount; i++) {
			fTransformedList.append(
				MPoint(listPointsSphere[i][0], listPointsSphere[i][1], listPointsSphere[i][2]) * matrix
			);
		}
		// Top square
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[0]);
		// Top lines
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[6]);

		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[8]);

		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[8]);
		fLineList.append(fTransformedList[8]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[10]);

		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[4]);
		// Side Lines
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[12]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[8]);
		fLineList.append(fTransformedList[16]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[19]);
		// Bottom lines
		fLineList.append(fTransformedList[20]);
		fLineList.append(fTransformedList[12]);
		fLineList.append(fTransformedList[12]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[20]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[14]);

		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[16]);

		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[16]);
		fLineList.append(fTransformedList[16]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[18]);

		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[12]);

		// Bottom square
		fLineList.append(fTransformedList[20]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[20]);
		if (fillShape) {
			// Top quad
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[0]);
			// Top triangles
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[5]);

			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[0]);

			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[7]);

			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[1]);

			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[9]);

			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[2]);

			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[11]);

			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[3]);
			// Side triangles
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[4]);

			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[5]);

			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[6]);

			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[7]);

			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[8]);

			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[9]);

			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[10]);

			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[11]);
			// Bottom triangles
			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[12]);

			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[20]);

			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[14]);

			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[21]);

			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[16]);

			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[22]);

			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[18]);

			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[23]);
			// Bottom Quad
			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[20]);
		}

	} else if (shapeIndex == 2) {  	// Cross
		for (int i=0; i<crossCount; i++) {
			fTransformedList.append(
				MPoint(listPointsCross[i][0], listPointsCross[i][1], listPointsCross[i][2]) * matrix
			);
		}
		// Base upper square
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[0]);
		// Base side lines
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[7]);
		// Base bottom square
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[4]);
		// Top pillar
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[8]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[8]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[9]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[10]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[11]);
		fLineList.append(fTransformedList[8]);
		// Right pillar
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[12]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[12]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[13]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[14]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[15]);
		fLineList.append(fTransformedList[12]);
		// Back pillar
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[16]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[16]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[17]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[18]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[19]);
		fLineList.append(fTransformedList[16]);
		// Left pillar
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[20]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[20]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[21]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[22]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[23]);
		fLineList.append(fTransformedList[20]);
		// Front pillar
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[24]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[25]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[26]);
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[27]);
		fLineList.append(fTransformedList[24]);
		fLineList.append(fTransformedList[25]);
		fLineList.append(fTransformedList[25]);
		fLineList.append(fTransformedList[26]);
		fLineList.append(fTransformedList[26]);
		fLineList.append(fTransformedList[27]);
		fLineList.append(fTransformedList[27]);
		fLineList.append(fTransformedList[24]);
		// Bottom pillar
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[28]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[29]);
		fLineList.append(fTransformedList[6]);
		fLineList.append(fTransformedList[30]);
		fLineList.append(fTransformedList[7]);
		fLineList.append(fTransformedList[31]);
		fLineList.append(fTransformedList[28]);
		fLineList.append(fTransformedList[29]);
		fLineList.append(fTransformedList[29]);
		fLineList.append(fTransformedList[30]);
		fLineList.append(fTransformedList[30]);
		fLineList.append(fTransformedList[31]);
		fLineList.append(fTransformedList[31]);
		fLineList.append(fTransformedList[28]);
		if (fillShape) {
			// Top pillar
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[8]);

			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[9]);

			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[10]);

			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[11]);

			fTriangleList.append(fTransformedList[8]);
			fTriangleList.append(fTransformedList[9]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[10]);
			fTriangleList.append(fTransformedList[11]);
			fTriangleList.append(fTransformedList[8]);
			// Right Pillar
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[12]);

			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[13]);

			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[14]);

			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[15]);

			fTriangleList.append(fTransformedList[12]);
			fTriangleList.append(fTransformedList[13]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[14]);
			fTriangleList.append(fTransformedList[15]);
			fTriangleList.append(fTransformedList[12]);
			// Back pillar
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[17]);

			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[17]);

			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[18]);

			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[19]);

			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[19]);
			fTriangleList.append(fTransformedList[16]);
			fTriangleList.append(fTransformedList[17]);
			fTriangleList.append(fTransformedList[18]);
			fTriangleList.append(fTransformedList[19]);
			// Left pillar
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[20]);

			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[22]);

			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[22]);

			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[23]);

			fTriangleList.append(fTransformedList[20]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[23]);
			fTriangleList.append(fTransformedList[21]);
			fTriangleList.append(fTransformedList[22]);
			fTriangleList.append(fTransformedList[23]);
			// Front Pillar
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[24]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[25]);
			fTriangleList.append(fTransformedList[24]);

			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[26]);
			fTriangleList.append(fTransformedList[25]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[26]);

			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[27]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[27]);
			fTriangleList.append(fTransformedList[26]);

			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[27]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[24]);
			fTriangleList.append(fTransformedList[27]);

			fTriangleList.append(fTransformedList[24]);
			fTriangleList.append(fTransformedList[25]);
			fTriangleList.append(fTransformedList[27]);
			fTriangleList.append(fTransformedList[25]);
			fTriangleList.append(fTransformedList[26]);
			fTriangleList.append(fTransformedList[27]);
			// Bottom pillar
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[28]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[28]);
			fTriangleList.append(fTransformedList[29]);

			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[29]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[29]);
			fTriangleList.append(fTransformedList[30]);

			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[6]);
			fTriangleList.append(fTransformedList[30]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[30]);
			fTriangleList.append(fTransformedList[31]);
	
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[7]);
			fTriangleList.append(fTransformedList[31]);
			fTriangleList.append(fTransformedList[31]);
			fTriangleList.append(fTransformedList[28]);
			fTriangleList.append(fTransformedList[4]);

			fTriangleList.append(fTransformedList[30]);
			fTriangleList.append(fTransformedList[29]);
			fTriangleList.append(fTransformedList[28]);
			fTriangleList.append(fTransformedList[28]);
			fTriangleList.append(fTransformedList[31]);
			fTriangleList.append(fTransformedList[30]);
		}
	} else if (shapeIndex == 3) {  	// Diamond
		for (int i=0; i<diamondCount; i++) {
			fTransformedList.append(
				MPoint(listPointsDiamond[i][0], listPointsDiamond[i][1], listPointsDiamond[i][2]) * matrix
			);
		}
		// Top lines 
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[4]);
		// Planar lines
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[4]);
		fLineList.append(fTransformedList[1]);
		// Bottom lines
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[5]);
		fLineList.append(fTransformedList[4]);
		if (fillShape) {
			// Top triangles
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[1]);
			// Bottom triangles
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[4]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[5]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[4]);
		}

	} else if (shapeIndex == 4) {  	// Square
		for (int i=0; i<squareCount; i++) {
			fTransformedList.append(
				MPoint(listPointsSquare[i][0], listPointsSquare[i][1], listPointsSquare[i][2]) * matrix
			);
		}
		fLineList.append(fTransformedList[0]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[1]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[2]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[3]);
		fLineList.append(fTransformedList[0]);
		if (fillShape) {
			fTriangleList.append(fTransformedList[0]);
			fTriangleList.append(fTransformedList[1]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[2]);
			fTriangleList.append(fTransformedList[3]);
			fTriangleList.append(fTransformedList[0]);
		}

	} else if (shapeIndex == 5) {  	// Circle
		for (int i=0; i<circleCount; i++) {
			fTransformedList.append(
				MPoint(listPointsCircle[i][0], listPointsCircle[i][1], listPointsCircle[i][2]) * matrix
			);
		}
		for (int i=1; i<=circleCount-2; i++) {
			fLineList.append(fTransformedList[i]);
			fLineList.append(fTransformedList[i+1]);
		}
		if (fillShape) {
			for (int i=1; i<=circleCount-2; i++) {
				fTriangleList.append(fTransformedList[0]);
				fTriangleList.append(fTransformedList[i]);
				fTriangleList.append(fTransformedList[i+1]);
			}
		}
	} else if (shapeIndex == 6) {  	// Locator
		for (int i=0; i<nullCount; i++) {
			fLineList.append(MPoint(listPointsNull[i][0], listPointsNull[i][1], listPointsNull[i][2]) * matrix);
		}
	} else if (shapeIndex == 7) {  	// Line
		fLineList.append(MPoint(listPointsLine[0][0], listPointsLine[0][1], listPointsLine[0][2]) * matrix);
		fLineList.append(MPoint(listPointsLine[1][0], listPointsLine[1][1], listPointsLine[1][2]) * matrix);
	}

	// Draw line for pole vectors
	if (bDrawline) { 
		MMatrix matDrawLineTo = MDataHandle(MPlug(obj, Ctrl::attrInDrawLineTo).asMDataHandle()).asMatrix();
		listLine.append(MPoint() * matrix);
		listLine.append(MPoint(matDrawLineTo[3][0], matDrawLineTo[3][1], matDrawLineTo[3][2]) * pathObj.exclusiveMatrixInverse());
	}
}
