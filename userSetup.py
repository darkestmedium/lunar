# Built-in imports

# Third-Party imports
from maya import cmds
from maya import mel
import maya.OpenMaya as om

# Third-Pary dependencies


cmds.loadPlugin("mlunar")



def guiUserSetup():
	"""User setup for gui mode.
	"""
	# VS Code
	cmds.commandPort(name="localhost:20230", sourceType="mel")


if (om.MGlobal.mayaState() == om.MGlobal.kInteractive): guiUserSetup()
