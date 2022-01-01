#rom xml.etree.ElementTree import Element
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
import shutil	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_save_theme.ui"))

class AppBuilderCloneTheme(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setStyle()
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(400, 50)
		self.move(size.width()/2, size.height()/2)
		#self.setStyleSheet("min-width: 200px;")
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)	
		self.lineEdit.returnPressed.connect(self.accept)

		self.apps_path = None
		self.app_name = None
		self.theme = None
		self.img = None
		
	def accept(self):
		if self.lineEdit.text().strip() != "":
			self.close()
		target = self.lineEdit.text().strip()
		try:
			shutil.copy(self.img, f"{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/{target}.png")
		except:
			pass

		theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		
		theme_settings.items['themes'][target] = theme_settings.items['themes'][self.theme]
		theme_settings.serialize()
		self.parent.loadThemesButtons()
			
		
	def reject(self):
		self.close()
	
	def setStyle(self):
		with open(f"builder/style/app_builder_theme_saver.qss") as f:
			stylesheet = f.read()
			self.setStyleSheet(stylesheet)
			
