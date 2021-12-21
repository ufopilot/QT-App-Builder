import importlib
import sys
from builder.app_builder_message import AppBuilderMessage
from builder.settings import Settings
from builder.ui_functions import UIFunctions
from builder.theme_builder import ThemeBuilder
from builder.app_builder_bottom import AppBuilderBottom
from builder.app_builder_right import AppBuilderRight
from builder.app_builder_center import AppBuilderCenter

from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/app_builder.ui"))


class AppBuilder(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.ui = parent
		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		#settings = Settings('ui')
		#self.settings = settings
		self.cls = None
		self.settings = None

		settings = Settings('builder_theme')
		self.theme_settings = settings

		settings = Settings('builder')
		self.builder_settings = settings

		self.move(-1, -1)
		screen = QApplication.primaryScreen()
		print('Screen: %s' % screen.name())
		self.size = screen.size()
		self.resize(400, self.size.height()-40)
		
		self.app = None
		self.app_name = None
		self.builder_right = AppBuilderRight(self, self.app)
		self.builder_right.show()
		self.builder_center = AppBuilderCenter(self, self.app)
		self.builder_center.show()
		self.loadingProgress = self.builder_center.progressBar
		self.builder_bottom = AppBuilderBottom(self, self.app)
		self.builder_bottom.show()
		self.theme_builder = ThemeBuilder(self, self.app)
		self.message_box = AppBuilderMessage(self)
		
		self.builder__window__icon.doubleClicked.connect(self.selectIcon)
		self.builder__title_bar__icon.doubleClicked.connect(self.selectIcon)

	def setAppsPath(self):
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.Directory)  # ExistingFile
		dialog.setOption(QFileDialog.DontUseNativeDialog, True)
		dialog.setOption(QFileDialog.ShowDirsOnly, True)
		nMode = dialog.exec_()
		names = dialog.selectedFiles()
		self.builder_settings.items['apps_path'] = os.path.abspath(names[0])
		self.builder_settings.serialize()
	
	
	def loadApp(self, app_name):
		
		self.app_name = app_name
		
		#btn = self.sender()
		#app_name = btn.objectName()
		
		#self.ui.move(399, -1)
		if app_name == "template_app":
			apps_path = "builder"
		else:
			apps_path = self.builder_settings.items['apps_path']

		#with open(os.path.join(apps_path, app_name, "gui/settings/ui_settings.json"), "r", encoding='utf-8') as reader:
		#	self.settings = json.loads(reader.read())
		
		settings = Settings('ui', apps_path=apps_path, app_name=app_name)
		self.settings = settings
		
		self.initFormControl()
		self.loadValues()
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
		self.builder_settings.serialize()
		
		self.ui = self.app
		self.app.move(435, 15)
		self.app.show()
		#self.builder_right.app = self.app
		self.theme_builder.ui = self.app
		self.theme_builder.apps_path = apps_path
		self.theme_builder.app_name = app_name
		
		self.theme_builder.setup()
		
		self.builder_right.ui = self.app
		self.builder_right.apps_path = apps_path
		self.builder_right.app_name = app_name
		

		self.builder_center.ui = self.app
		
		self.builder_bottom.ui = self.app
		self.builder_bottom.apps_path = apps_path
		self.builder_bottom.app_name = app_name
		 
		self.builder_bottom.loadThemesButtons()
		self.loadingProgress.hide()
		self.loadingProgress.setValue(0)

	def selectIcon(self):
		lineedit = self.sender()

		i = 0
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(os.path.basename(fileName))
		lineedit.setText(os.path.basename(fileName))	

	def initFormControl(self):
		for spinbox in (self.builder__window__minimum_width, 
						self.builder__window__minimum_height, 
						self.builder__window__initial_width, 
						self.builder__window__initial_height,
						self.builder__panel1__minimum,
						self.builder__panel1__maximum,
						self.builder__panel2__minimum,
						self.builder__panel2__maximum,
						self.builder__panel4__minimum,
						self.builder__panel4__maximum,
						self.builder__panel5__minimum,
						self.builder__panel5__maximum,
						):
			spinbox.setMaximum(3000)
		
		for button in self.findChildren(QAbstractButton):
			if button.metaObject().className() == "AnimatedCheck" or button.metaObject().className() == "QCheckBox": 
				button.setCursor(QCursor(Qt.PointingHandCursor))
				button.stateChanged.connect(self.changeCheckboxState)
	
		for titleEdit in (
							self.builder__panel1__title, 
							self.builder__panel2__title, 
							self.builder__panel3__title,
							self.builder__panel4__title,
							self.builder__panel5__title
						):
			titleEdit.textEdited.connect(self.changeTitle)
	


	def loadValues(self):
		for component in (
			"window", 
			"title_bar", 
			"footer_bar", 
			"panel1",
			"panel2",
			"panel3",
			"panel4",
			"panel5"
			):
			for key, value in self.settings.items[component].items():
				try:
					el = eval(f"self.builder__{component}__{key}") 
					widgetType = el.metaObject().className()
					if widgetType == "QLineEdit" or widgetType == "ClickableQLineEdit":
						el.setText(str(value))
					elif widgetType == "AnimatedCheck" or widgetType == "QCheckBox":
						el.setChecked(value)
					elif widgetType == "QSpinBox":
						el.setValue(int(value))
					elif widgetType == "QComboBox":
						index = el.findText(value, Qt.MatchFixedString)
						if index >= 0:
							el.setCurrentIndex(index)

				except:
					pass
				
	def changeCheckboxState(self):
		try:
			element = self.sender()	
			name = element.objectName()
			panelName = name.split('__')[1]

			if "visible" in name:
				if "title_bar" in name:
					print("titlebar")
				elif "footer_bar" in name:
					print("footer_bar")
				else:
					panel = eval(f"self.ui.{panelName}").parent()	
					if element.isChecked():
						panel.show()
					else:		
						panel.hide()
		except:
			pass
	
	def changeTitle(self, text):

		element = self.sender()
		name = element.objectName()	
		nr = name.split('__')[1].replace('panel', '')

		titleLabel = eval(f"self.ui.headerPanel{nr}")
		titleLabel.setText(text)
	
	def saveAll(self):
		for item in self.findChildren(QLineEdit):
			try:
				name = item.objectName()
				comp = name.split('__')[1]
				key = name.split('__')[2]
				print(comp, key, item.text(), type(item.text()))
				self.settings.items[comp][key] = item.text()
			except:
				pass

		for item in self.findChildren(QSpinBox):
			try:
				name = item.objectName()
				print(name)
				comp = name.split('__')[1]
				key = name.split('__')[2]
				print(comp, key, item.text(), type(item.text()))
				self.settings.items[comp][key] = int(item.text())
			except:
				pass
		
		for item in self.findChildren(QCheckBox):
			try:
				name = item.objectName()
				print(name)
				comp = name.split('__')[1]
				key = name.split('__')[2]
				print(comp, key, item.isChecked())
				self.settings.items[comp][key] = item.isChecked()
			except:
				pass
		self.settings.serialize()
		self.showMessage("info", "Save all changes", "App-Settings successfully saved!")
	
	def showMessage(self, typos, title, message, time=3):
		self.message_box.notify(typos, title, message)

		timer=QTimer.singleShot(time*1000, lambda: self.message_box.close())
		
	def reload_app(self):
		self.app.close()
		if self.app_name == "template_app":
			from builder.template_app.template_main import MainWidget
			self.app = MainWidget(self)
		else:
			self.app = self.cls(self)
		self.app.move(435, 15)
		self.app.show()
	
	

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilder()
	w.show()
	sys.exit(app.exec())
