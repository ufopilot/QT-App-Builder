from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
import shutil
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_left.ui"))


class AppBuilderLeft(Base_Class, Gen_Class):
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
		self.builder__window__icon.doubleClicked.connect(self.selectIcon)
		self.builder__title_bar__icon.doubleClicked.connect(self.selectIcon)
	
		self.tabWidget.tabBar().setCursor(Qt.PointingHandCursor)
		
		self.toolbox_handler()
		self.resize_window()

	def toolbox_handler(self):
		icon = qta.icon("mdi6.square-edit-outline", color="white")
		for x in range(0,8):
			self.customizingToolBox.setItemIcon(x,icon)
		
		self.customizingToolBox.currentWidget().setCursor(Qt.PointingHandCursor)

		icon = qta.icon("mdi.format-color-fill", color="white")
		for x in range(0,8):
			self.themingToolBox.setItemIcon(x,icon)

		icon = qta.icon("ei.fontsize", color="white")
		self.themingToolBox.setItemIcon(8,icon)
		 #.setCursor(Qt.PointingHandCursor)
		
	def resize_window(self):
		screen = QApplication.primaryScreen()
		
		self.size = screen.size()
		self.move(
			self.builder_settings.items['left']['left'], 
			self.builder_settings.items['left']['top']
		)
		self.resize(
			self.builder_settings.items['left']['width'], 
			self.size.height()
			-
			self.builder_settings.items['left']['bottom']
			-
			self.builder_settings.items['left']['top']
		)
		

		
	def selectIcon(self):
		lineedit = self.sender()
		if self.builder_settings.items['selected_app'] == "":
			return
		dialog = QFileDialog(self)
		dialog.setWindowTitle('Choose an icon')
		dialog.setNameFilter('(*.png *.ico)')
		dialog.setDirectory(self.builder_settings.items['apps_path'])
		dialog.setFileMode(QFileDialog.ExistingFile)  
		dialog.setOption(QFileDialog.DontUseNativeDialog, True)
		#dialog.setOption(QFileDialog.ShowDirsOnly, True)
		dialog.move(
			round(self.parent.size.width()/2 - dialog.rect().width()/2), round(self.parent.size.height()/2 - dialog.rect().height()/2)
		)

		if dialog.exec_() == QDialog.Accepted:
			names = dialog.selectedFiles()
			try:
				iconfile = os.path.abspath(names[0])
				filename  = os.path.basename(iconfile)
				if self.copy_selected_icon_to_app(iconfile, filename):
					app_dir = os.path.basename(self.builder_settings.items['apps_path'])
					app_dir = f"{app_dir}/{self.builder_settings.items['selected_app']}"
					lineedit.setText(f"{app_dir}/gui/resources/imgs/{filename}")
			except:
				pass
	
	def copy_selected_icon_to_app(self, iconfile, filename):
		try:
			shutil.copyfile(iconfile, f"{self.builder_settings.items['apps_path']}/{self.builder_settings.items['selected_app']}/gui/resources/imgs/{filename}")
			return True
		except:
			return False

	def initFormControl(self):
		for spinbox in self.Customizing.findChildren(QSpinBox):
			spinbox.setMaximum(4000)
		
		for button in self.Customizing.findChildren(QAbstractButton):
			if button.metaObject().className() == "AnimatedCheck" or button.metaObject().className() == "QCheckBox": 
				button.setCursor(QCursor(Qt.PointingHandCursor))
				button.stateChanged.connect(self.changeCheckboxState)

		for lineedit in self.Customizing.findChildren(QLineEdit):
			if "__title" in  lineedit.objectName():
				lineedit.textEdited.connect(self.changeTitle)
		
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
					bar = eval(f"self.ui.mainHeader")
					if element.isChecked():
						bar.show()
					else:		
						bar.hide()

				elif "footer_bar" in name:
					bar = eval(f"self.ui.mainFooter")
					if element.isChecked():
						bar.show()
					else:		
						bar.hide()
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

	