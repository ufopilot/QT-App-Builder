from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_loading.ui"))


class AppBuilderLoading(Base_Class, Gen_Class):
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
	
	def loading(self, title="Loading ..."):
		self.title.setText(title)
		self.show()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderLoading()
	w.show()
	sys.exit(app.exec())
