from . settings import Settings
from . ui_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_message.ui"))


class AppBuilderMessage(Base_Class, Gen_Class):
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
	
	def notify(self, msg_type, title, message):
		self.title.setText(title)
		self.message.setText(message)
		self.icon.setPixmap(QPixmap(f"builder/imgs/{msg_type}.png"))
		self.show()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderMessage()
	w.show()
	sys.exit(app.exec())
