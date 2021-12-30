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
		self.origWidth = self.builder_settings.items['left_header']['width']
		self.minWidth = 39
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
		icon = qta.icon("ei.indent-right", color="white")
		self.toggleLeft.setIcon(icon)
		self.toggleLeft.setIconSize(QSize(20, 20))
		self.toggleLeft.setCursor(QCursor(Qt.PointingHandCursor))
		self.toggleLeft.setCheckable(False)
		self.toggleLeft.clicked.connect(self.toggle_left_panel)
		self.visible = True

	def toggle_left_panel(self):
		if self.visible:
			icon = qta.icon("ei.indent-left", color="white")
			self.visible = False
			self.parent.builder_settings.items['left']['width'] = self.minWidth
			self.parent.builder_settings.items['left_header']['width'] = self.minWidth
			self.parent.update_settings("builder")
			
		else:
			icon = qta.icon("ei.indent-right", color="white")
			self.visible = True
			self.parent.builder_settings.items['left_header']['width'] = self.origWidth
			self.parent.builder_settings.items['left']['width'] = self.origWidth
			self.parent.update_settings("builder")
		
		self.resize_window()
		self.parent.builder_left.resize_window()
		self.parent.builder_center.resize_window()
		self.parent.builder_center_header.resize_window()
		self.parent.builder_bottom.resize_window()
		self.sender().setIcon(icon)
		
		
		
		#self.tabWidget.hide()
		#self.Theming.hide()
		#self.Customizing.hide()
		#self.Menu.hide()

		#self.leftHeader.setMaximumSize(QSize(30, 16777215))
		#self.resize(10, self.size.height()-38)
		
		
		#self.animation = QPropertyAnimation(self.window(), bytes("minimumWidth", encoding='utf-8'))
		#self.animation.setDuration(300)
		#self.animation.setStartValue(300)
		#self.animation.setEndValue(40)
		#self.animation.setEasingCurve(QEasingCurve.InOutQuart)
		#self.animation.start()
			