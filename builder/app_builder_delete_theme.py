#rom xml.etree.ElementTree import Element
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_delete_theme.ui"))

class AppBuilderDeleteTheme(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(400, 50)
		self.move(size.width()/2, size.height()/2)
		#self.setStyleSheet("min-width: 200px;")
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)	
		self.img = None
		self.theme = None
		self.app_name = None
		self.apps_path = None

	def accept(self):
		
		theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		try:
			del theme_settings.items["themes"][self.theme]
			theme_settings.serialize()
		except:
			pass

		if os.path.exists(self.img):
			try:
				os.remove(self.img)
			except:
				pass

		self.parent.loadThemesButtons()
		self.close()
		
	def reject(self):
		self.close()
			
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderDeleteTheme()
	w.show()
	sys.exit(app.exec())
