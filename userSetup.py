# Built-in imports

# Third-Party imports
from maya import cmds
import maya.mel as mel

# # VS Code
cmds.commandPort(name="localhost:20230", sourceType="mel")

cmds.loadPlugin("mlunar")

mel.eval('loadNewShelf "shelf_Bambaa_Animation.mel";')