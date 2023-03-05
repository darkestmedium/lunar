# Built-in imports

# Third-party imports
from maya import cmds

# Custom imports



def connectSourceAndSaveAnimNew(pTransform, pSrcT, pSrcR, forcePairBlendCreation):
	"""Python override of the global proc connectSourceAndSaveAnimNew()

	If nodes already has sources, create a pairblend to preserve the animation.

	Note: 
		pairBlends are just supporting T and R, not S, anim on S will be lost if $pSrcS is set.

	Args:
		pTransform (string): The transform for which the pairBlend node will be created.
		pSrcT (string):	State2SK nodes output translation attribute.
		pSrcR (string): State2SK nodes output rotation attribute.
		forcePairBlendCreation (int): Whether or not we want to force creation of the pairBlend node.

	"""
	nbSrc = 0

	if forcePairBlendCreation:
		for attr in ["translate", "translateX", "translateY", "translateZ", "rotate",	"rotateX", "rotateY", "rotateZ"]:
			connections = cmds.listConnections(f"{pTransform}.{attr}", destination=False, source=True)
			if connections:	nbSrc += len(connections)

	if forcePairBlendCreation or nbSrc:
		animatableAttributes = [attr.split('.')[-1] for attr in cmds.listAnimatable(pTransform)]

		pairBlend = cmds.pairBlend(node=pTransform, attribute=animatableAttributes)

		if pSrcT != "":
			cmds.connectAttr(pSrcT, f"{pairBlend}.inTranslate2")

		if pSrcR != "":
			cmds.connectAttr(pSrcR, f"{pairBlend}.inRotate2")

		cmds.setAttr(f"{pairBlend}.weight", True)
		cmds.setAttr(f"{pairBlend}.currentDriver", True)

	else:
		if pSrcT != "":
			if cmds.getAttr(f"{pTransform}.translateX", lock=True) == 0: cmds.connectAttr(f"{pSrcT}x", f"{pTransform}.translateX")
			if cmds.getAttr(f"{pTransform}.translateY", lock=True) == 0: cmds.connectAttr(f"{pSrcT}y", f"{pTransform}.translateY")
			if cmds.getAttr(f"{pTransform}.translateZ", lock=True) == 0: cmds.connectAttr(f"{pSrcT}z", f"{pTransform}.translateZ")

		if pSrcR != "":
			if cmds.getAttr(f"{pTransform}.translateX", lock=True) == 0: cmds.connectAttr(f"{pSrcR}x", f"{pTransform}.rotateX")
			if cmds.getAttr(f"{pTransform}.translateY", lock=True) == 0: cmds.connectAttr(f"{pSrcR}y", f"{pTransform}.rotateY")
			if cmds.getAttr(f"{pTransform}.translateZ", lock=True) == 0: cmds.connectAttr(f"{pSrcR}z", f"{pTransform}.rotateZ")

