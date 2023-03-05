# Built-in imports

# Third-party imports
import unreal as uep

# Custom imports
from lunar.abstract.fbx import AbstractFbx
# from lunar.standalone.finder import Finder


# Class instances
fbx = uep.FbxFactory()



class UnrealFbx(AbstractFbx):
	"""Unreal Editor Fbx class, inherited from AbstractFbx

		TODO:	
			Implement basic import / export anim clip from fbx from drive

	
	"""

	def importAnimation(self) -> bool:
		return False

	def exportAnimation(self) -> bool:
		return False





# if __name__ == "__main__":
# 	fbx.import
	
