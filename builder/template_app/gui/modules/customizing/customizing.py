from qt_core import *
from app.gui.content import *
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions
import re

class Customizing(QWidget):
	_init = True
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.ui = parent
		self.settings = Settings('ui')
		self.loadCustomValues()
		for checkox in self.ui.findChildren(QAbstractButton):
			if "customize" in checkox.objectName():
				checkox.setCursor(QCursor(Qt.PointingHandCursor))
				checkox.stateChanged.connect(self.state_changed)

	def loadCustomValues(self):
		for panel in ("panel1", "panel2", "panel4", "panel5"):
			toggle = self.settings.items[panel]['toggle']
			show_onstart = self.settings.items[panel]['show_onstart']
			if panel == "panel1":
				self.ui.customizePanel1Showonstart.setChecked(show_onstart)
				self.ui.customizePanel1Toggling.setChecked(toggle)
			if panel == "panel2":
				self.ui.customizePanel2Showonstart.setChecked(show_onstart)
				self.ui.customizePanel2Toggling.setChecked(toggle)
			if panel == "panel3":
				self.ui.customizePanel3Showonstart.setChecked(show_onstart)
				self.ui.customizePanel3Toggling.setChecked(toggle)
			if panel == "panel5":
				self.ui.customizePanel5Showonstart.setChecked(show_onstart)
				self.ui.customizePanel5Toggling.setChecked(toggle)

	def state_changed(self, int):
		checkbox = self.sender()
		strings = re.sub( r"([A-Z])", r" \1", checkbox.objectName()).split()
		if strings[2] == "Toggling":
			self.settings.items[strings[1].lower()]['toggle'] = checkbox.isChecked()
		if strings[2] == "Showonstart":
			self.settings.items[strings[1].lower()]['show_onstart'] = checkbox.isChecked()
		self.settings.serialize()