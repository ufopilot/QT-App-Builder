#rom xml.etree.ElementTree import Element
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./app/gui/modules/app_builder/app_builder_bottom.ui"))


class AppBuilderBottom(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		settings = Settings('ui')
		self.settings = settings
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(size.width()-400, 200)
		self.move(399, size.height()-200)
		#self.ui.move(399, -1)
		#self.setWindowFlag(Qt.WindowStaysOnBottomHint)
		
		
			
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderBottom()
	w.show()
	sys.exit(app.exec())
