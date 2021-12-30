#rom xml.etree.ElementTree import Element
import shutil
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_delete_app.ui"))

class AppBuilderDeleteApp(Base_Class, Gen_Class):
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

		self.app_name = None
		self.apps_path = None
		
	def accept(self):
		try:
			print(os.path.join(self.apps_path, self.app_name))
			if os.path.exists(os.path.join(self.apps_path, self.app_name)):
				shutil.rmtree(os.path.join(self.apps_path, self.app_name))
			
		except:
			pass	
		self.parent.searchApps(self.apps_path)
		self.close()
		
	def reject(self):
		self.close()

