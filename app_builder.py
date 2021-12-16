#rom xml.etree.ElementTree import Element
from builder.app_builder_message import AppBuilderMessage
from builder.settings import Settings
from builder.ui_functions import UIFunctions
from builder.theme_builder import ThemeBuilder
from builder.app_builder_bottom import AppBuilderBottom
from builder.app_builder_right import AppBuilderRight
from builder.app_builder_center import AppBuilderCenter
from builder.template_app.main import MainWidget
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/app_builder.ui"))


class AppBuilder(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.ui = parent
		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		settings = Settings('ui')
		self.settings = settings
		
		settings = Settings('builder_theme')
		self.theme_settings = settings

		self.move(-1, -1)
		screen = QApplication.primaryScreen()
		print('Screen: %s' % screen.name())
		self.size = screen.size()
		self.resize(400, self.size.height()-40)
		#self.ui.move(399, -1)
		self.initFormControl()
		self.loadValues()
		
		self.app = MainWidget(self)
		self.app.move(435, 15)

		ThemeBuilder(self, self.app)
		
		self.builder_right = AppBuilderRight(self, self.app)
		self.builder_right.show()
		self.builder_center = AppBuilderCenter(self, self.app)
		self.builder_center.show()
		self.builder_bottom = AppBuilderBottom(self, self.app)
		self.builder_bottom.show()
		
		self.message_box = AppBuilderMessage(self, self.app)
		
		#self.app.show()


		#self.app.screen_shot()
		#self.app.setWindowFlag(Qt.WindowStaysOnTopHint)
		
		#self.loadColors()
		self.builder__window__icon.doubleClicked.connect(self.selectIcon)
		self.builder__title_bar__icon.doubleClicked.connect(self.selectIcon)
	#def loadColors(self):
	#	for el in self.findChildren(QComboBox):
	#		el.setCursor(QCursor(Qt.PointingHandCursor))
	#		if "__background" in el.objectName():
	#			print(el.objectName())
	#			self.fillColorsCombo(el)
	#			el.currentTextChanged.connect(self.handleColorPressed)
#
	#def handleColorPressed(self):
	#	color = QColorDialog.getColor()
#
	#	if color.isValid():
	#		print(color.name())
#
	#	el = self.sender()
	#	name = el.objectName()
	#	label = eval(f"self.{name}__selectedcolor")
	#	color = el.currentText() 
	#	label.setStyleSheet(f"background: {color}; border: 2px solid teal;border-radius: 12px; max-width: 24px; max-height: 24px")
#
	#def fillColorsCombo(self, combo):
	#	color_list = self.theme_settings.items["colors"]["background"]
	#	model = combo.model()
	#	for row, color in enumerate(color_list):
	#		combo.addItem(color.title())
	#		model.setData(model.index(row, 0), QColor(color), Qt.BackgroundRole)
#
#

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
						print(key, value)
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
		nr = name.split('__')[2].replace('panel', '')
		titleLabel = eval(f"self.ui.headerPanel{nr}")
		titleLabel.setText(text)
	
	def saveAll(self):
		for item in self.findChildren(QLineEdit):
			try:
				name = item.objectName()
				print(name)
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
		from my_app import MainWidget
		self.app = MainWidget(self)
		self.app.move(435, 15)
		self.app.show()

		#ThemeBuilder(self, self.app)

		#ThemeBuilder.parent = self
		#ThemeBuilder.ui = self.app

	

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilder()
	w.show()
	sys.exit(app.exec())
