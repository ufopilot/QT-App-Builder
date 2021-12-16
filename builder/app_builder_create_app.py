#rom xml.etree.ElementTree import Element
from .settings import Settings
from .ui_functions import UIFunctions
from qt_core import *
import shutil
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_create_app.ui"))


class AppBuilderCreateApp(Base_Class, Gen_Class):
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
		self.lineEdit.returnPressed.connect(self.accept)
		
	def accept(self):
		if self.lineEdit.text().strip() != "":
			self.close()
			self.parent.createNewApp.toggle()
			app_name = self.lineEdit.text()
			# create app 
			#######################################
			if not os.path.exists(f"apps/{app_name}"):
				#os.makedirs(f"apps/{app_name}")
				shutil.copytree('builder/template_app', f'apps/{app_name}', dirs_exist_ok=True)
			else:
				# show message
				print(f"{app_name} already exists!")
			#QTimer.singleShot(200, lambda: self.parent.take_screenshot(self.lineEdit.text()))
			
		
	def reject(self):
		self.parent.createNewApp.toggle()
		self.close()
			
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderCreateApp()
	w.show()
	sys.exit(app.exec())
