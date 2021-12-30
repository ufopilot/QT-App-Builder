from builder.modules.app_builder_delete_app import AppBuilderDeleteApp
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

		
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_center_header.ui"))

class AppBuilderCenterHeader(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		#############################################################
		# Flags
		#############################################################
		self.setWindowFlag(Qt.FramelessWindowHint)
		#############################################################
		# Initial
		#############################################################
		self.ui = ui
		self.parent = parent
		self.setupUi(self)
		self.builder_settings = None
		self.app = None
		self.app_name = None
		
	def setup(self):
		if self.builder_settings.items['apps_path'].strip() == "":
			self.parent.setAppsPath()
		self.resize_window()

	def resize_window(self):
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(
			size.width()
			-
			self.builder_settings.items['left_header']['width']
			- 
			self.builder_settings.items['right']['width'] 
			- 
			self.builder_settings.items['center_header']['right'], 
			self.builder_settings.items['center_header']['height']
		)
		self.move(
			self.builder_settings.items['left_header']['width']
			+
			self.builder_settings.items['center_header']['left'], 
			self.builder_settings.items['center_header']['top'], 
		)

	def setSelectedApp(self, name=""):
		self.selected_app.setText(f"App: {name}")
