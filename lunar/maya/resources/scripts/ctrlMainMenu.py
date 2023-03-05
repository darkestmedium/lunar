# Built-in imports
import logging
import string

# Third-party imports
from maya import cmds
from maya import mel



menuName = "Ctrl"
logger = logging.getLogger(menuName) 



class MainMenu():
	"""Class for creating user-defined menu items in the maya main menu."""


	# GUI	
	menuItems = []


	def createMenuItems(self) -> bool:
		"""Adds custom menu items in the maya main menu.

		Must be overridden in the derived class.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		return False


	def displayOptionBox(self, *args, **kwargs):
		"""Displays the option box window for the command.
		
		Must be overridden in the derived class.

		"""
		pass


	def applyAndCloseButton(self, *args, **kwargs):
		"""Calls the doIt method and closes the option box window by saving the values."""
		self.doIt()
		mel.eval('saveOptionBoxSize')
		self.closeOptionBox()


	def closeOptionBox(self, *args, **kwargs):
		"""Closes the option box window."""
		mel.eval('hideOptionBox')


	def resetToDefaults(self, *args, **kwargs):
		"""Resets the settings to default ones.

		Must be overridden in the derived class.

		"""
		pass


	def getCreateCommandKwargs(self, *args, **kwargs) -> dict:
		"""Gets the moduleTemplate command arguments.

		The arguments are queried eiter from the option box widgets or the saved option 
		variables. If the widgets exist, their values will be saved to the option variables.

		Must be overridden in the derived class.

		Returns:
			dict: Dictionary of the kwargs to the moduleTemplate command.

		"""
		pass


	def doIt(self, *args, **kwargs) -> bool:
		"""Wrapper method for the main menu item.

		Must be overridden in the derived class.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		return False


	def deleteMenuItems(self) -> bool:
		"""Deletes custom menu items in the maya main menu.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if self.menuItems:
			for item in self.menuItems:
				cmds.deleteUI(item, menuItem=True)

			self.menuItems.clear()

			logger.debug(f"Successfully deleted '{menuName}' item from main menu.")
			return True

		logger.debug(f"'{menuName}' menu item not found, nothing to delete.")
		return False



class CtrlMainMenu(MainMenu):
	"""Derived class for the shakeNode plugin for creating user-defined menu items in the maya main menu.

	"""


	# Widgets
	_ctrlNameWidget = 'ctrlName'
	_ctrlParentWidget = 'ctrlParent'
	_ctrlLocalScaleWidget = 'ctrlLocalScale'
	_ctrlShapeWidget = 'ctrlShape'
	_ctrlFillShapeWidget = 'ctrlFillShape'
	_ctrlFillTransparencyWidget = 'ctrlFillTransparency'
	_ctrlLineWidthWidget = 'ctrlLineWidth'


	def createMenuItems(self):
		"""Wrapper method for the main menu item.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the
				operation.

		"""
		if not self.menuItems:
			menu = "mainRigSkeletonsMenu"
			mel.eval(f"ChaSkeletonsMenu MayaWindow|{menu};")
			
			# Rig Controller
			shakeNodeItem = cmds.menuItem(
				parent=menu,
				insertAfter="createSkeletonItem",
				label=menuName,
				image="ctrl.png",
				command=self.doIt,
				sourceType="python",
			)

			# Rig Controller Option Box
			shakeNodeOptBox = cmds.menuItem(
				parent=menu,
				insertAfter=shakeNodeItem,
				command=self.displayOptionBox,
				optionBox=True,
			)

			self.menuItems.append(shakeNodeItem)
			self.menuItems.append(shakeNodeOptBox)

			return True

		logger.debug(f"'{menuName}' menu item already exists.")
		return False


	def displayOptionBox(self, *args, **kwargs):
		"""Displays the option box window for the command."""

		layout = mel.eval('getOptionBox')
		cmds.setParent(layout)
		cmds.columnLayout(adjustableColumn=True)

		mel.eval(f'setOptionBoxTitle("{menuName} Options")')
		mel.eval('setOptionBoxCommandName("ctrl")')

		for widget in [self._ctrlNameWidget]:
			try: cmds.deletUI(widget, control=True)
			except:	pass

		# Rig Controller Name
		cmds.textFieldGrp(
			self._ctrlNameWidget,
			label='Name',
			text=cmds.optionVar(query=self._ctrlNameWidget),
		)

		# Rig Controller Parent
		cmds.textFieldGrp(
			self._ctrlParentWidget,
			label='Parent',
			text=cmds.optionVar(query=self._ctrlParentWidget),
		)

		# Rig Controller Local Scale
		cmds.floatSliderGrp(
			self._ctrlLocalScaleWidget,
			label='Local Scale',
			field=True,
			minValue=0.001,
			fieldMinValue=0.001,
			value=cmds.optionVar(query=self._ctrlLocalScaleWidget),
			step=0.001,
			precision=3.0,
		)

		# Rig Controller Shape 
		# ctrlShape = cmds.optionVar(query=self._ctrlShapeWidget)
		# print(f"SHAPE ENUM VALUE {ctrlShape}")
		# cmds.attrEnumOptionMenuGrp(
		# 	self._ctrlShapeWidget,
		# 	label='Shape',
		# 	enumeratedItem=[
		# 		(0, 'Cube'),
		# 		(1, 'Sphere'),
		# 		(2, 'Cross'),
		# 		(3, 'Diamond'),
		# 		(4, 'Square'),
		# 		(5, 'Circle'),
		# 		(6, 'Locator'),
		# 	]
		# )

		# Rig Controller Fill Shape
		# ctrlShape = cmds.optionVar(query=self._ctrlFillShapeWidget)
		# print(f"Fill SHAPE ENUM VALUE {ctrlShape}")
		# cmds.attrEnumOptionMenuGrp(
		# 	self._ctrlFillShapeWidget,
		# 	label='Fill Shape',
		# 	enumeratedItem=[
		# 		(0, 'Off'),
		# 		(1, 'On'),
		# 	]
		# 	value1=cmds.optionVar(query=self._ctrlFillShapeWidget)
		# )

		# Rig Controller Fill Transparency 
		cmds.floatSliderGrp(
			self._ctrlFillTransparencyWidget,
			label='Fill Transparency',
			field=True,
			minValue=0.1,
			fieldMinValue=0.1,
			maxValue=1.0,
			fieldMaxValue=1.0,
			value=cmds.optionVar(query=self._ctrlFillTransparencyWidget),
			step=0.01,
			precision=2,
		)

		# Rig Controller Line Width
		cmds.floatSliderGrp(
			self._ctrlLineWidthWidget,
			label='Line Width',
			field=True,
			minValue=0.5,
			fieldMinValue=0.5,
			maxValue=5.0,
			fieldMaxValue=5.0,
			value=cmds.optionVar(query=self._ctrlLineWidthWidget),
			step=0.1,
			precision=1,
		)

		# Action Buttons
		applyAndCloseButton = mel.eval('getOptionBoxApplyAndCloseBtn')
		cmds.button(applyAndCloseButton, edit=True, command=self.applyAndCloseButton)

		applyButton = mel.eval('getOptionBoxApplyBtn')
		cmds.button(applyButton, edit=True, command=self.doIt)

		closeButton = mel.eval('getOptionBoxCloseBtn')
		cmds.button(closeButton, edit=True, command=self.closeOptionBox)

		# Buttons in the menu only accepts MEL
		resetButton = mel.eval('getOptionBoxResetBtn')
		cmds.button(resetButton, edit=True,
		 	command='python("from ctrlMainMenu import ctrlMainMenu; ctrlMainMenu().resetToDefaults()")'
		)

		# Buttons in the menu only accepts MEL
		saveButton = mel.eval('getOptionBoxSaveBtn')
		cmds.button(saveButton,	edit=True,
		 	command='python("from ctrlMainMenu import ctrlMainMenu; ctrlMainMenu().getCreateCommandKwargs()")'
		)

		mel.eval('showOptionBox')


	def getCreateCommandKwargs(self, *args, **kwargs) -> dict:
		"""Gets the moduleTemplate command arguments.

		The arguments are queried eiter from the option box widgets or the saved option
		variables. If the widgets exist, their values will be saved to the option variables.

		Returns:
			dict: Dictionary of the kwargs to the moduleTemplate command.

		"""
		args = {}

		# Ctrl Name
		if cmds.textFieldGrp(self._ctrlNameWidget, exists=True):
			args['name'] = cmds.textFieldGrp(self._ctrlNameWidget, query=True, text=True)
			cmds.optionVar(stringValue=(self._ctrlNameWidget, args['name']))
		else:
			args['name'] = cmds.optionVar(query=self._ctrlNameWidget) or 'ctrl'

		# Ctrl Parent
		if cmds.textFieldGrp(self._ctrlParentWidget, exists=True):
			args['parent'] = cmds.textFieldGrp(self._ctrlParentWidget, query=True, text=True)
			cmds.optionVar(stringValue=(self._ctrlParentWidget, args['parent']))
		else:
			args['parent'] = cmds.optionVar(query=self._ctrlParentWidget) or ''

		# Ctrl Local Scale
		if cmds.floatSliderGrp(self._ctrlLocalScaleWidget, exists=True):
			args['localScale'] = cmds.floatSliderGrp(self._ctrlLocalScaleWidget, query=True, value=True)
			cmds.optionVar(floatValue=(self._ctrlLocalScaleWidget, args['localScale']))
		else:
			args['localScale'] = cmds.optionVar(query=self._ctrlLocalScaleWidget) or 1.0

		# Ctrl Shape
		# if cmds.attrEnumOptionMenuGrp(self._ctrlShapeWidget, exists=True):
		# 	args['shape'] = cmds.attrEnumOptionMenuGrp(self._ctrlShapeWidget, query=True)
		# 	cmds.optionVar(intValue=(self._ctrlShapeWidget, args['shape']))
		# 	cmds.optionVar(stringValue=(self._ctrlShapeWidget, args['shape']))
		# else:
		# 	args['shape'] = cmds.optionVar(query=self._ctrlShapeWidget) or (0, 'Cube')

		# Ctrl Fill Shape
		# if cmds.attrEnumOptionMenuGrp(self._ctrlFillShapeWidget, exists=True):
		# 	args['fillShape'] = cmds.attrEnumOptionMenuGrp(self._ctrlFillShapeWidget, query=True)
		# 	cmds.optionVar(stringValue=(self._ctrlFillShapeWidget, args['fillShape']))
		# else:
		# 	args['fillShape'] = cmds.optionVar(query=self._ctrlFillShapeWidget) or 'On'

		# Ctrl Fill Transparency
		if cmds.floatSliderGrp(self._ctrlFillTransparencyWidget, exists=True):
			args['fillTransparency'] = cmds.floatSliderGrp(self._ctrlFillTransparencyWidget, query=True, value=True)
			cmds.optionVar(floatValue=(self._ctrlFillTransparencyWidget, args['fillTransparency']))
		else:
			args['fillTransparency'] = cmds.optionVar(query=self._ctrlFillTransparencyWidget) or 0.25

		# Ctrl Line Width
		if cmds.floatSliderGrp(self._ctrlLineWidthWidget, exists=True):
			args['lineWidth'] = cmds.floatSliderGrp(self._ctrlLineWidthWidget, query=True, value=True)
			cmds.optionVar(floatValue=(self._ctrlLineWidthWidget, args['lineWidth']))
		else:
			args['lineWidth'] = cmds.optionVar(query=self._ctrlLineWidthWidget) or 1.0

		return args


	def resetToDefaults(self, *args, **kwargs):
		"""Resets the settings to default ones."""
		cmds.textFieldGrp(self._ctrlNameWidget, edit=True, text="ctrl")
		cmds.textFieldGrp(self._ctrlParentWidget, edit=True, text='')
		cmds.floatSliderGrp(self._ctrlLocalScaleWidget, edit=True, value=1.0)
		# cmds.attrEnumOptionMenuGrp(self._ctrlShapeWidget, edit=True, value=0)
		# cmds.checkBoxGrp(self._ctrlFillShapeWidget, edit=True, value1=1)
		cmds.floatSliderGrp(self._ctrlFillTransparencyWidget, edit=True, value=0.25)
		cmds.floatSliderGrp(self._ctrlLineWidthWidget, edit=True, value=1.0)


	def doIt(self, *args, **kwargs) -> bool:
		"""Wrapper method for the main menu item.

		Returns:
			bool: True if the operation was successful, False if an	error occured during the operation.

		"""
		kwargs = self.getCreateCommandKwargs()
		if cmds.ctrl(**kwargs): return True

		return False
