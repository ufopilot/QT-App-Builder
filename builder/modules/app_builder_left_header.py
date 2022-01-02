from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
import shutil
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_left_header.ui"))


class AppBuilderLeftHeader(Base_Class, Gen_Class):
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
		self.origLeftHeaderWidth = self.builder_settings.items['left_header']['width']
		self.origLeftWidth = self.builder_settings.items['left']['width']
		self.resize_window()
		self.addLeftButtons()
		
	def resize_window(self):
		screen = QApplication.primaryScreen()
		
		self.size = screen.size()
		self.move(
			self.builder_settings.items['left_header']['left'], 
			self.builder_settings.items['left_header']['top']
		)
		self.resize(
			self.builder_settings.items['left_header']['width'], 
			self.builder_settings.items['left_header']['height']
		)
		

	def addLeftButtons(self):
		icon = qta.icon("mdi6.chevron-double-left", color="white")
		self.toggleLeft.setIcon(icon)
		self.toggleLeft.setIconSize(QSize(20, 20))
		self.toggleLeft.setCursor(QCursor(Qt.PointingHandCursor))
		self.toggleLeft.setCheckable(False)
		self.toggleLeft.clicked.connect(self.toggle_left_panel)
		self.visible = True


		icon = qta.icon("fa.gear", color="white")
		self.builderSettings.setIcon(icon)
		self.builderSettings.setIconSize(QSize(20, 20))
		self.builderSettings.setCursor(QCursor(Qt.PointingHandCursor))
		self.builderSettings.setCheckable(False)
		self.builderSettings.clicked.connect(self.config_app_builder)
		
	def config_app_builder(self):
		print(1)

	def toggle_left_panel(self):
		if self.visible:
			icon = qta.icon("mdi6.chevron-double-right", color="white")
			self.visible = False
			animate_dr = False
			self.parent.builder_settings.items['left']['width'] = self.parent.builder_settings.items['left']['minimum']
			self.parent.builder_settings.items['left_header']['width'] = self.parent.builder_settings.items['left_header']['minimum']
			self.parent.update_settings("builder")
			
		else:
			icon = qta.icon("mdi6.chevron-double-left", color="white")
			self.visible = True
			animate_dr = True
			self.parent.builder_settings.items['left_header']['width'] = self.origLeftHeaderWidth
			self.parent.builder_settings.items['left']['width'] = self.origLeftWidth
			self.parent.update_settings("builder")
		
		self.resize_window()
		self.parent.builder_left.resize_window()
		self.parent.builder_center.resize_window()
		self.parent.builder_center_header.resize_window()
		self.parent.builder_bottom.resize_window()
		self.sender().setIcon(icon)
		