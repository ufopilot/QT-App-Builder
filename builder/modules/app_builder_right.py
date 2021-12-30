from .app_builder_message import AppBuilderMessage
from .app_builder_save_theme import AppBuilderSaveTheme
from .app_builder_create_app import AppBuilderCreateApp

from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_right.ui"))


class AppBuilderRight(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
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
		self.apps_path = apps_path
		self.app_name = app_name
		self.setupUi(self)
		self.builder_settings = None
		
	def setup(self):
		self.themeSaver = AppBuilderSaveTheme(self, self.ui)
		self.appCreator = AppBuilderCreateApp(self, self.ui)
		self.message_box = AppBuilderMessage(self)
		self.initFormControl()
		self.resize_window()
		#self.parent.setStyle(self, "right")
		self.show()
		#self.parent.unfade(self)

	def resize_window(self):
		screen = QApplication.primaryScreen()
		self.size = screen.size()
		self.resize(
			self.builder_settings.items['right']['width'] 
			+ 
			1, 
			self.size.height()
			-
			self.builder_settings.items['right']['bottom']
			-
			self.builder_settings.items['right']['top']
		)
		self.move(
			self.size.width()
			-
			self.builder_settings.items['right']['width']
			-
			1, 
			self.builder_settings.items['right']['top']
		)

	def initFormControl(self):
		self.saveCurrentTheme.setCheckable(True)
		self.saveCurrentTheme.setToolTip("Save current style as theme")
		self.saveCurrentTheme.setCursor(QCursor(Qt.PointingHandCursor))
		self.saveCurrentTheme.clicked.connect(self.save_current_theme)
		self.saveCurrentTheme.enterEvent = lambda x: self.highlighter(self.saveCurrentTheme, "enter")
		self.saveCurrentTheme.leaveEvent = lambda x: self.highlighter(self.saveCurrentTheme, "leave")
		self.add_icon(self.saveCurrentTheme, "ei.css")


		self.saveAppBuilder.setToolTip('Save all changes')
		self.saveAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
		self.saveAppBuilder.clicked.connect(self.parent.saveAll)
		self.saveAppBuilder.enterEvent = lambda x: self.highlighter(self.saveAppBuilder, "enter")
		self.saveAppBuilder.leaveEvent = lambda x: self.highlighter(self.saveAppBuilder, "leave")
		self.add_icon(self.saveAppBuilder, "mdi.content-save-all-outline")

		self.reloadApp.setToolTip('Reload App')
		self.reloadApp.setCursor(QCursor(Qt.PointingHandCursor))
		self.reloadApp.clicked.connect(self.parent.reload_app)
		self.add_icon(self.reloadApp, "mdi.reload")

		self.createNewApp.setCheckable(True)
		self.createNewApp.setToolTip('Create new app from template')
		self.createNewApp.setCursor(QCursor(Qt.PointingHandCursor))
		self.createNewApp.clicked.connect(self.create_new_app)
		self.createNewApp.enterEvent = lambda x: self.highlighter(self.createNewApp, "enter")
		self.createNewApp.leaveEvent = lambda x: self.highlighter(self.createNewApp, "leave")
		
		self.add_icon(self.createNewApp, "mdi.new-box")

		self.compileApp.setCheckable(True)
		self.compileApp.setToolTip('Build selectedb app')
		self.compileApp.setCursor(QCursor(Qt.PointingHandCursor))
		#self.compileApp.clicked.connect(self.create_new_app)
		self.add_icon(self.compileApp, "ph.buildings-bold")
		
		#self.setAppsPath.setCheckable(True)
		self.setAppsPath.setToolTip('Set applications path ')
		self.setAppsPath.setCursor(QCursor(Qt.PointingHandCursor))
		self.setAppsPath.clicked.connect(self.parent.setAppsPath)
		self.setAppsPath.enterEvent = lambda x: self.highlighter(self.setAppsPath, "enter")
		self.setAppsPath.leaveEvent = lambda x: self.highlighter(self.setAppsPath, "leave")
		self.add_icon(self.setAppsPath, "mdi.folder-table-outline")
		
	def add_icon(self, btn, icon_name):
		if 'icons_color' in self.builder_settings.items:
			if self.builder_settings.items['icons_color'] != "":
				icon_color = self.builder_settings.items['icons_color']
			else:
				icon_color = "white"

		icon = qta.icon(icon_name, color=icon_color)
		btn.setIcon(icon)
		btn.setIconSize(QSize(40, 40))

	def save_current_theme(self):
		if self.builder_settings.items['selected_app'] == "":
			self.message_box.notify("warning", "Save Settings", "No App selected!")
			timer=QTimer.singleShot(2000, lambda: self.message_box.close())
			self.sender().toggle()
			return
		
		if self.themeSaver.isVisible():
			return 
		if not self.saveCurrentTheme.isChecked():
			return
		
		self.themeSaver.show()
		   
	def take_screenshot(self, name=None):
		screen = QApplication.primaryScreen()
		screenshot = screen.grabWindow(
				QApplication.desktop().winId(), 
				self.ui.pos().x(), 
				self.ui.pos().y(), 
				self.ui.width(), 
				self.ui.height()
			)
		screenshot.save(f'{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/{name}.png', 'png')
		theme_settings = Settings('theme', self.apps_path, self.app_name)
		theme_settings.items['themes'][name] = theme_settings.items['theme']
		theme_settings.serialize()
		self.parent.builder_bottom.loadThemesButtons()

	def create_new_app(self):
		btn = self.sender()
		if self.appCreator.isVisible():
			return

		if not btn.isChecked():
			return
	
		self.appCreator.show()
	
	def highlighter(self, btn, e): 
		btn_name = btn.objectName()
		if btn_name == "setAppsPath":
			if e == "enter":
				self.parent.builder_center_header.apps_path.setStyleSheet("color: orange")
			else:
				self.parent.builder_center_header.apps_path.setStyleSheet("color: white")               
		if btn_name == "createNewApp":
			if e == "enter":
				self.parent.builder_center.scrollArea.setStyleSheet("QScrollArea{border-bottom: 1px solid cyan}")
			else:
				self.parent.builder_center.scrollArea.setStyleSheet("QScrollArea{border: 0px solid cyan}")               
		if btn_name == "saveCurrentTheme":
			if e == "enter":
				self.parent.builder_bottom.themes_label.setStyleSheet("color: orange")
	
			else:
				self.parent.builder_bottom.themes_label.setStyleSheet("color: white")
		if btn_name == "saveAppBuilder":
			if e == "enter":
				self.parent.builder_left.setStyleSheet("#BuilderLeft QTabBar::tab{color: orange}")
	
			else:
				self.parent.builder_left.setStyleSheet("#BuilderLeft QTabBar::tab{color: white}")
	