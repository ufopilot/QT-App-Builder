#rom xml.etree.ElementTree import Element
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions
from . theme_builder import ThemeBuilder
from . app_builder_bottom import AppBuilderBottom
from . app_builder_right import AppBuilderRight

from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./app/gui/modules/app_builder/app_builder.ui"))


class AppBuilder(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.ui = parent
		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		settings = Settings('ui')
		self.settings = settings
		
		self.move(-1, -1)
		screen = QApplication.primaryScreen()
		print('Screen: %s' % screen.name())
		size = screen.size()
		self.resize(400, size.height()-40)
		self.ui.move(399, -1)
		self.initFormControl()
		self.loadValues()
		ThemeBuilder(self, self.ui)
		self.builder_bottom = AppBuilderBottom(self, self.ui)
		self.builder_bottom.show()
		self.builder_right = AppBuilderRight(self, self.ui)
		self.builder_right.show()
		#self.setWindowFlag(Qt.WindowStaysOnBottomHint)
		
	def initFormControl(self):
		self.closeAppBuilder.setToolTip('Close App-Builder')
		self.saveAppBuilder.setToolTip('Save all changes')
		self.closeAppBuilder.clicked.connect(self.window().close)
		self.saveAppBuilder.clicked.connect(self.saveAll)
		self.closeAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
		self.saveAppBuilder.setCursor(QCursor(Qt.PointingHandCursor))
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
					if widgetType == "QLineEdit":
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
		print("save")
		
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
		#msg = QMessageBox.information(self, "App-Builder", "App-Settings successfully saved!")
			
		self.notify("info", "App-Builder", "App-Settings successfully saved!", 2)

	def notify(self,tipo,event,detail='',time=5):
		dia=QMessageBox(self)
		
		timer=QTimer.singleShot(time*1000,dia.accept)
		# dia=QtGui.QDialog(self)
		dia.setText(event)
		dia.setInformativeText(detail)
		# dia.setDetailedText(detail)
		dia.setWindowModality(0)
		dia.setWindowOpacity(.8)
		dia.setStandardButtons(QMessageBox.NoButton)
		if tipo=='error':
			dia.setStyleSheet(".QMessageBox{background:rgba(250,30,10,255);color:#fff}QLabel{background:transparent;color:#fff}")
			dia.setIcon(QMessageBox.Critical)
		elif tipo=='info':
			dia.setStyleSheet(".QMessageBox{background:rgba(30,30,10,255);color:#fff}QLabel{background:transparent;color:#fff}")	
			dia.setIcon(QMessageBox.Information)
		elif tipo=='warning':
			dia.setStyleSheet(".QMessageBox{background:rgba(255,200,0,255);color:#fff}QLabel{background:transparent;color:#fff}")	
			dia.setIcon(QMessageBox.Warning)
		elif tipo=='exit':	
			dia.setStyleSheet(".QMessageBox{background:rgba(0,128,0,255);color:#fff}QLabel{background:transparent;color:#fff}")	
			dia.setIcon(QMessageBox.Information)
			
		dia.move(150,100)
		# dia.addWidget(QLabel(event))
		dia.setWindowFlags(dia.windowFlags()|Qt.FramelessWindowHint)
		dia.show()
		
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilder()
	w.show()
	sys.exit(app.exec())
