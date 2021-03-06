#rom xml.etree.ElementTree import Element
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_save_theme.ui"))

class AppBuilderSaveTheme(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setStyle()
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(400, 50)
		self.move(size.width()/2, size.height()/2)
		#self.setStyleSheet("min-width: 200px;")
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)	
		self.lineEdit.returnPressed.connect(self.accept)
		self.hide()
		
	def accept(self):
		if self.lineEdit.text().strip() != "":
			self.close()
			self.parent.saveCurrentTheme.toggle()
			QTimer.singleShot(200, lambda: self.parent.take_screenshot(self.lineEdit.text()))
			
		
	def reject(self):
		self.parent.saveCurrentTheme.toggle()
		self.close()

	def setStyle(self):
		with open(f"builder/style/app_builder_theme_saver.qss") as f:
			stylesheet = f.read()
			self.setStyleSheet(stylesheet)

