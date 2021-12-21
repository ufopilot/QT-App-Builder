#rom xml.etree.ElementTree import Element
from builder.app_builder_center import AppBuilderCenter
from builder.app_builder_message import AppBuilderMessage
from .settings import Settings
from .ui_functions import UIFunctions
from qt_core import *
import shutil
import fileinput
from pathlib import Path

Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_create_app.ui"))


class AppBuilderCreateApp(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent
		settings = Settings('builder')
		self.builder_settings = settings

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(400, 50)
		self.move(size.width()/2, size.height()/2)
		#self.setStyleSheet("min-width: 200px;")
		self.message_box = AppBuilderMessage(self)
		

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
			if not os.path.exists(os.path.join(self.builder_settings.items['apps_path'], app_name)):
				#os.makedirs(f"apps/{app_name}")
				shutil.copytree('builder/template_app', os.path.join(self.builder_settings.items['apps_path'], app_name), dirs_exist_ok=True)
				
				apps_path_base = os.path.basename(self.builder_settings.items['apps_path'])
				
				for file_path in Path(os.path.join(self.builder_settings.items['apps_path'], app_name)).rglob('*.py'):
					with open(file_path, 'r') as file :
						filedata = file.read()
					
					filedata = filedata.replace("from builder.template_app.", f"from {apps_path_base}.{app_name}.")
					#filedata = filedata.replace("./app/gui", f"{apps_path_base}/{app_name}/gui")
					filedata = filedata.replace("builder/template_app/gui", f"{apps_path_base}/{app_name}/gui")
					
					with open(file_path, 'w') as file:
						file.write(filedata)
				print("py files done")
				
				for file_path in Path(os.path.join(self.builder_settings.items['apps_path'], app_name)).rglob('*.ui'):
					with open(file_path, 'r', encoding='UTF8') as file :
						filedata = file.read()
					
					filedata = filedata.replace("from builder.template_app.", f"from {apps_path_base}.{app_name}.")
					filedata = filedata.replace("builder/template_app/gui", f"{apps_path_base}/{app_name}/gui")
					
					with open(file_path, 'w', encoding='UTF8') as file:
						file.write(filedata)
				print("ui files done")

				# mv main.py to {app_name}_main.py
				os.rename(
					os.path.join(self.builder_settings.items['apps_path'], app_name, "template_main.py"), 
					os.path.join(self.builder_settings.items['apps_path'], app_name, f"{app_name}_main.py")
					)
					
				print("app created")
				self.message_box.notify("info", "Create APP", f"{app_name} successfully created!")
				timer=QTimer.singleShot(3000, lambda: self.message_box.close())
				print("load from creator")
				self.parent.parent.builder_center.searchApps()
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
