#rom xml.etree.ElementTree import Element
from builder.app_builder_save_theme import AppBuilderSaveTheme
from builder.app_builder_create_app import AppBuilderCreateApp

from . settings import Settings
from . ui_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_right.ui"))


class AppBuilderRight(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		settings = Settings('ui')
		self.settings = settings
		
		screen = QApplication.primaryScreen()
		self.size = screen.size()
		self.resize(50, self.size.height()-200)
		self.move(self.size.width()-50, 0)
		#self.ui.move(399, -1)
		
		self.themeSaver = AppBuilderSaveTheme(self, self.ui)
		self.appCreator = AppBuilderCreateApp(self, self.ui)


		self.initFormControl()

	def initFormControl(self):
		#exitActIcon = QtGui.QIcon("./icons/outline-exit_to_app-24px.svg")
 		#exitAct = QtWidgets.QAction(exitActIcon, "Exit", self)
		#exitAct.setShortcut("Ctrl+Q")
		#exitAct.triggered.connect(QtWidgets.qApp.quit)
		#self.toolbar = self.addToolBar("Exit")
		#self.toolbar.addAction(exitAct)
		#self.toolbar.setIconSize(QtCore.QSize(128, 128)) # <---

		self.closeAppBuilder.setToolTip('Close App-Builder')
		self.closeAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
		self.closeAppBuilder.clicked.connect(self.parent.window().close)
		self.add_icon(self.closeAppBuilder, "fa5.window-close")

		self.saveCurrentTheme.setCheckable(True)
		self.saveCurrentTheme.setToolTip("Save current style as theme")
		self.saveCurrentTheme.setCursor(QCursor(Qt.PointingHandCursor))
		self.saveCurrentTheme.clicked.connect(self.save_current_theme)
		self.add_icon(self.saveCurrentTheme, "fa5.save")


		self.saveAppBuilder.setToolTip('Save all changes')
		self.saveAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
		self.saveAppBuilder.clicked.connect(self.parent.saveAll)
		self.add_icon(self.saveAppBuilder, "mdi.content-save-all-outline")

		self.reloadApp.setToolTip('Reload App')
		self.reloadApp.setCursor(QCursor(Qt.PointingHandCursor))
		self.reloadApp.clicked.connect(self.parent.reload_app)
		self.add_icon(self.reloadApp, "mdi.reload")

		self.createNewApp.setCheckable(True)
		self.createNewApp.setToolTip('Create new app')
		self.createNewApp.setCursor(QCursor(Qt.PointingHandCursor))
		self.createNewApp.clicked.connect(self.create_new_app)
		self.add_icon(self.createNewApp, "mdi.new-box")

		

		self.closeAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
		
	def add_icon(self, btn, icon_name):
		icon = qta.icon(icon_name, color="cyan")
		#icon = QIcon()
		#icon.addFile(f"builder/icons/cyan/{icon_name}.svg", QSize(), QIcon.Normal, QIcon.Off)
		btn.setIcon(icon)
		btn.setIconSize(QSize(24, 24))

	def save_current_theme(self):
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
		screenshot.save(f'app/gui/resources/imgs/themes/{name}.png', 'png')
		
		builder_theme_settings = Settings('builder_theme')
		app_theme_settings = Settings('theme')
		app_theme_settings.items['themes'][name] = builder_theme_settings.items['theme']
		app_theme_settings.serialize()
		self.parent.builder_bottom.loadThemesButtons()

	def create_new_app(self):
		btn = self.sender()
		if self.appCreator.isVisible():
			return

		if not btn.isChecked():
			return
	
		self.appCreator.show()
		

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderRight()
	w.show()
	sys.exit(app.exec())
