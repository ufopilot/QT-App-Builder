import importlib
import sys

from PyQt5.sip import transferback
from builder.modules.app_builder_center_header import AppBuilderCenterHeader
from builder.modules.app_builder_left import AppBuilderLeft
from builder.modules.app_builder_left_header import AppBuilderLeftHeader
from builder.modules.app_builder_menu import MenuBuilder
from builder.modules.app_builder_message import AppBuilderMessage
from builder.modules.app_builder_settings import Settings
from builder.modules.app_builder_functions import UIFunctions
from builder.modules.app_builder_themeing import ThemeBuilder
from builder.modules.app_builder_bottom import AppBuilderBottom
from builder.modules.app_builder_right import AppBuilderRight
from builder.modules.app_builder_center import AppBuilderCenter

from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_main.ui"))


class AppBuilder(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.ui = parent
		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setWindowOpacity(0)
		
		############################################################
		# Load Settings
		############################################################
		self.builder_settings = self.load_settings("builder")
		# ------------------------------	
		# clear selected app in settings
		# ------------------------------
		self.builder_settings.items['selected_app'] = ""
		self.builder_settings.serialize()
		############################################################
		# resizer
		############################################################
		screen = QApplication.primaryScreen()
		self.size = screen.size()
		############################################################
		# Titlebar
		############################################################
		# ------------------------------
		# close button
		# ------------------------------
		icon = qta.icon("msc.chrome-close", color="white")
		self.closeBtn.setCursor(QCursor(Qt.PointingHandCursor))
		self.closeBtn.clicked.connect(self.window().close)
		self.closeBtn.setIcon(icon)
		# ------------------------------
		# minimize button
		# ------------------------------
		icon = qta.icon("msc.chrome-minimize", color="white")
		self.minimizeBtn.setCursor(QCursor(Qt.PointingHandCursor))
		#self.minimizeBtn.clicked.connect(self.window().showMinimized)
		self.minimizeBtn.clicked.connect(lambda : self.setStyle(self, "main"))
		self.minimizeBtn.setIcon(icon)
		############################################################
		# initial
		############################################################
		self.app = None
		self.app_name = None
		# ------------------------------
		# left
		# ------------------------------
		self.builder_left = AppBuilderLeft(self, self.app)
		self.builder_left.builder_settings = self.builder_settings
		self.builder_left.setup()
		#self.fadeIn(self.builder_left)
		# ------------------------------
		# left Header
		# ------------------------------
		self.builder_left_header = AppBuilderLeftHeader(self, self.app)
		self.builder_left_header.builder_settings = self.builder_settings
		self.builder_left_header.setup()
		# ------------------------------
		# right
		# ------------------------------
		self.builder_right = AppBuilderRight(self, self.app)
		self.builder_right.builder_settings = self.builder_settings
		self.builder_right.setup()
		# ------------------------------
		# center Header
		# ------------------------------
		self.builder_center_header = AppBuilderCenterHeader(self, self.app)
		self.builder_center_header.builder_settings = self.builder_settings
		self.builder_center_header.setup()
		# ------------------------------
		# center
		# ------------------------------
		self.builder_center = AppBuilderCenter(self, self.app)
		self.builder_center.builder_settings = self.builder_settings
		self.builder_center.setup()
		self.loadingProgress = self.builder_center.progressBar
		#self.fadeIn(self.builder_center)
		# ------------------------------
		# bottom
		# ------------------------------
		self.builder_bottom = AppBuilderBottom(self, self.app)
		self.builder_bottom.builder_settings = self.builder_settings
		self.builder_bottom.setup()
		# ------------------------------
		# Helpers  --> move ist to left
		# ------------------------------
		self.theme_builder = ThemeBuilder(self, self.app)
		self.theme_builder.builder_settings = self.builder_settings
		self.theme_builder.setup()

		self.menu_builder = MenuBuilder(self, self.app)
		self.menu_builder.builder_settings = self.builder_settings
		self.menu_builder.setup()
		# ------------------------------
		# MessagesBox
		# ------------------------------
		self.message_box = AppBuilderMessage(self)
		##############################################################
		# load style
		##############################################################
		self.setStyle(self, "main")
		
		
		self.showMaximized()
		time.sleep(1)
		self.setWindowOpacity(1)
	

	def load_settings(self, type):
		settings = Settings(type)
		return settings

	def setStyle(self, win, area):
		with open(f"builder/style/app_builder_{area}.qss") as f:
			stylesheet = f.read()
			win.setStyleSheet(stylesheet)
	
	def setAppsPath(self):
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.Directory)  # ExistingFile
		dialog.setOption(QFileDialog.DontUseNativeDialog, True)
		dialog.setOption(QFileDialog.ShowDirsOnly, True)
		
		dialog.move(
			round(self.size.width()/2 - dialog.rect().width()/2), round(self.size.height()/2 - dialog.rect().height()/2)
		)
		if dialog.exec_() == QDialog.Accepted:
			names = dialog.selectedFiles()
			if names:
				apps_path = os.path.abspath(names[0])
				self.builder_settings.items['apps_path'] = apps_path
				self.builder_settings.serialize()
				self.update_settings("builder")
				self.builder_center_header.apps_path.setText(f"Path: {apps_path}")
				self.builder_center.searchApps(apps_path)

	def saveAll(self):
		if self.builder_settings.items['selected_app'] == "":
			self.message_box.notify("warning", "Save Settings", "No App selected!")
			timer=QTimer.singleShot(2000, lambda: self.message_box.close())
			return
		
		for item in self.builder_left.Customizing.findChildren(QLineEdit):
			try:
				name = item.objectName()
				comp = name.split('__')[1]
				key = name.split('__')[2]
				self.settings.items[comp][key] = item.text()
			except:
				pass

		for item in self.builder_left.Customizing.findChildren(QSpinBox):
			try:
				name = item.objectName()
				comp = name.split('__')[1]
				key = name.split('__')[2]
				self.settings.items[comp][key] = int(item.text())
			except:
				pass
		
		for item in self.builder_left.Customizing.findChildren(QCheckBox):
			try:
				name = item.objectName()
				comp = name.split('__')[1]
				key = name.split('__')[2]
				self.settings.items[comp][key] = item.isChecked()
			except:
				pass
		self.settings.serialize()
		self.menu_builder.menuToJson()
		self.showMessage("info", "Save all changes", "App-Settings successfully saved!")
	
	def showMessage(self, typos, title, message, time=3):
		self.message_box.notify(typos, title, message)

		timer=QTimer.singleShot(time*1000, lambda: self.message_box.close())
		
	def loadApp(self, app_name):
		self.app_name = app_name
		
		if app_name == "template_app":
			apps_path = "builder"
		else:
			apps_path = self.builder_settings.items['apps_path']

		
		settings = Settings('ui', apps_path=apps_path, app_name=app_name)
		self.settings = settings
		self.builder_left.settings = settings
		theme_settings = Settings('theme', apps_path=apps_path, app_name=app_name)
		theme_settings.items['default_theme'] = ""
		theme_settings.serialize()

		self.builder_left.app_name = self.app_name
		self.builder_left.apps_path = apps_path

		self.builder_left.initFormControl()
		self.builder_left.loadValues()
		# select app
		if app_name == "template_app":
			from builder.template_app.template_main import MainWidget
			self.app = MainWidget(self)
		else:
			try: 		
				sys.path.append(os.path.join(os.path.abspath(apps_path), app_name))
				cls = getattr(importlib.import_module(f"{app_name}_main"), 'MainWidget')
				self.cls = cls
				self.app = cls(self)
			except:
				return
		self.builder_settings.items['selected_app'] = app_name
		self.builder_settings.items['selected_theme'] = ""
		self.update_settings("builder")
		#self.builder_settings.serialize()
		
		self.ui = self.app
		##################################################
		# move app to center
		##################################################
		self.move_app_to_center()
		##################################################
		self.app.show()
		
		self.app.closewindow.clicked.connect(self.closeApp)
	
		#self.builder_right.app = self.app
		self.builder_left.ui = self.app
		# ThemeBuilder
		self.theme_builder.ui = self.app
		self.theme_builder.apps_path = apps_path
		self.theme_builder.app_name = app_name
		self.theme_builder.initial = True
		self.theme_builder.refresh()
		# MenuBuilder
		self.menu_builder.ui = self.app
		self.menu_builder.apps_path = apps_path
		self.menu_builder.app_name = app_name
		self.menu_builder.refresh(init=False)
		# init actions on RightPanel
		self.builder_right.ui = self.app
		self.builder_right.apps_path = apps_path
		self.builder_right.app_name = app_name
		# init actions on CenterPanel
		self.builder_center.ui = self.app
		# init actions on BottomPanel
		self.builder_bottom.ui = self.app
		self.builder_bottom.apps_path = apps_path
		self.builder_bottom.app_name = app_name
		self.builder_bottom.loadThemesButtons()
		
		self.loadingProgress.hide()
		self.loadingProgress.setValue(0)
		
	def reload_app(self):
		if self.builder_settings.items['selected_app'] == "":
			self.message_box.notify("warning", "Reload App", "No App selected!")
			timer=QTimer.singleShot(2000, lambda: self.message_box.close())
			return

		self.app.close()
		self.theme_builder.loadThemeColors()
		if self.app_name == "template_app":
			from builder.template_app.template_main import MainWidget
			self.app = MainWidget(self)
		else:
			self.app = self.cls(self)
		
		self.theme_builder.ui = self.app

		##################################################
		# move app to center
		##################################################
		self.move_app_to_center()
		##################################################
		self.app.closewindow.clicked.connect(self.closeApp)
		self.app.show()
	
	def move_app_to_center(self):
		self.app.move(
			self.builder_settings.items['left']['width'] 
			+ 
			self.builder_settings.items['app']['left'], 
			self.builder_settings.items['center']['top']+10 
		)
	def update_settings(self, type):
		if type == "builder":
			self.builder_left.builder_settings = self.builder_settings
			self.builder_bottom.builder_settings = self.builder_settings
			self.builder_center.builder_settings = self.builder_settings
			self.builder_right.builder_settings = self.builder_settings
			self.theme_builder.builder_settings = self.builder_settings

	def closeApp(self):
		self.builder_settings.items['selected_theme'] = ""
		self.builder_settings.items['selected_app'] = ""
		# update builder settings
		self.update_settings("builder")

		self.theme_builder.initial = True
		self.theme_builder.reset = True
		
		for combo in self.builder_left.Theming.findChildren(QComboBox):
			if combo.objectName() != "changeSelectedFont":
				combo.clear()
		
		for label in self.builder_left.Theming.findChildren(QLabel):
			if "selectedColor" in label.objectName():
				label.setStyleSheet("background: transparent")

		for edit in self.builder_left.Customizing.findChildren(QLineEdit):
			edit.setText("")
		
		for edit in self.builder_left.Customizing.findChildren(QSpinBox):
			edit.setValue(0)
		
		for check in self.builder_left.Customizing.findChildren(QCheckBox):
			check.setChecked(False)

		self.builder_left.menuTree.clear() 
		
		for btn in self.builder_center.myApps.findChildren(QPushButton):
			btn.setEnabled(True)

		for spin in (self.builder_left.selectedTextSize, self.builder_left.selectedTitleSize):
			spin.setValue(0)
		
		self.builder_left.changeSelectedFont.setCurrentIndex(0)
		
		self.theme_builder.initial = False
		self.theme_builder.reset = False
		self.builder_center.setSelectedApp()
		self.builder_bottom.setSelectedTheme()
		self.builder_bottom.clearThemesButtons()

	def fadeOut(self, widget):
		self.effect = QGraphicsOpacityEffect()
		widget.setGraphicsEffect(self.effect)

		self.animation = QPropertyAnimation(self.effect, b"opacity")
		self.animation.setDuration(1000)
		self.animation.setStartValue(1)
		self.animation.setEndValue(0)
		self.animation.start()

	def fadeIn(self, widget):
		effect = QGraphicsOpacityEffect()
		widget.setGraphicsEffect(effect)

		animation = QPropertyAnimation(effect, b"opacity")
		animation.setDuration(1000)
		animation.setStartValue(0)
		animation.setEndValue(1)
		animation.start()
	
	def fadeAllIn(self):
		group = QParallelAnimationGroup(self)
        #group.addAnimation(geometry_animation)
        #group.addAnimation(opacity_animation)
        #group.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
	#
	#def fadeOut(self, w):
	#	for i in range(10):
	#		i = i / 10
	#		w.setWindowOpacity(1 - i)
	#		time.sleep(0.05)
	#	self.close()
#
	#def fadeIn(self, w):
	#	for i in range(10):
	#		i = i / 10
	#		w.setWindowOpacity(0 + i)
	#		time.sleep(0.1)
	#	w.setWindowOpacity(1)
		

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilder()
	#w.showMaximized()
	sys.exit(app.exec())
