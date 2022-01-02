from qt_core import *

from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
import re

class ThemeBuilder(QWidget):
	_init = True
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
		super(self.__class__, self).__init__(parent)
		#############################################################
		# Initial
		#############################################################
		self.ui = ui
		self.parent = parent
		self.apps_path = apps_path
		self.app_name = app_name
		self.ui_settings = None
		self.theme_settings = None
		self.builder_settings = None
		self.initial = False
		self.reset = False

	def setup(self):

		if 'icons_color' in self.builder_settings.items:
			if self.builder_settings.items['icons_color'] != "":
				icon_color = self.builder_settings.items['icons_color']
			else:
				icon_color = "white"
				
		for frame in self.parent.builder_left.Theming.findChildren(QFrame):
			try:
				label1 = frame.findChildren(QLabel)[0]
				label2 = frame.findChildren(QLabel)[1]
				btn = frame.findChild(QPushButton)
				if label1.parent().parent().objectName() != "theming_font":
					label1.setProperty("type", 1)
					label2.setProperty("type", "color_label")
				icon = qta.icon("fa.pencil", color=icon_color)
				btn.setIcon(icon)
			except:
				pass
		self.parent.builder_left.changeSelectedFont.insertItem(0, "")
		self.parent.builder_left.changeSelectedFont.setCurrentIndex(0)
	
	
	def refresh(self):
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		self.ui_settings = Settings('ui', apps_path=self.apps_path, app_name=self.app_name)
		
		valcount = self.countValues()
		progress_step = 100 / valcount
		
		for button in self.parent.builder_left.Theming.findChildren(QPushButton):
			button_name = button.objectName()
			if "colorPicker" in button_name:
				button.setCursor(QCursor(Qt.PointingHandCursor))
				try:
					button.clicked.disconnect() 
				except:
					pass
				button.clicked.connect(self.open_color_picker)

		for combo in self.parent.builder_left.Theming.findChildren(QComboBox):
			combo.setCursor(QCursor(Qt.PointingHandCursor))
			if "changeSelectedColor" in combo.objectName():
				#self.fillColorsCombo(combo)
				try:
					combo.currentTextChanged.disconnect()
				except:
					pass 
				combo.currentTextChanged.connect(self.handleColorPressed)
			if "changeSelectedFont" in combo.objectName():
				#self.fillColorsCombo(combo)
				try:
					combo.currentTextChanged.disconnect()
				except:
					pass 
				combo.currentTextChanged.connect(self.handleFontFamily)
		for spin in (self.parent.builder_left.selectedTextSize, self.parent.builder_left.selectedTitleSize):
			try:
				spin.valueChanged.disconnect()
			except:
				pass 
			spin.valueChanged.connect(self.handleFontSize)

		i = 0
		for area in (
				"titlebar",
				"panel1",
				"panel2",
				"panel3",
				"panel4",
				"panel5",
				"footerbar",
				"dividers"
			):
			
			widget = self.parent.findChild(QWidget, f"theming_{area}")
		
			for key, value in self.theme_settings.items['theme'][area].items():
				try:
					i += 1
					regex = QRegExp("^{}_.*$".format(key))

					subwidget = widget.findChildren(QFrame, regex)[0]
					combo = subwidget.findChild(QComboBox)
					combo.clear()
					combo.addItem(value)
					combo.setCurrentIndex(0)
					self.parent.loadingProgress.setValue(i*progress_step)
				except:
					pass

		font_name = self.theme_settings.items['theme']['font']['family']
		index = self.parent.builder_left.changeSelectedFont.findText(font_name, Qt.MatchFixedString)
		if index >= 0:
			self.parent.builder_left.changeSelectedFont.setCurrentIndex(index)
		
		self.parent.builder_left.selectedTitleSize.setValue(self.theme_settings.items['theme']['font']['title_size'])
		self.parent.builder_left.selectedTextSize.setValue(self.theme_settings.items['theme']['font']['text_size'])
		
		self.initial = False

		#	if any(key in button_name for key in List3):
		#		button.stateChanged.connect(self.changeBarIconsColor)

	
	def loadThemeColors(self):
		self.initial = True
		
		theme_name = self.builder_settings.items['selected_theme']
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		
		if theme_name == "" or theme_name == "no-theme":
			selectedTheme = self.theme_settings.items['theme']
		else: 
			selectedTheme = self.theme_settings.items['themes'][theme_name]

		i = 0
		for area in (
				"titlebar",
				"panel1",
				"panel2",
				"panel3",
				"panel4",
				"panel5",
				"footerbar",
				"dividers"
			):
			
			widget = self.parent.findChild(QWidget, f"theming_{area}")
			for key, value in selectedTheme[area].items():
				try:
					i += 1
					regex = QRegExp("^{}_.*$".format(key))

					subwidget = widget.findChildren(QFrame, regex)[0]
					combo = subwidget.findChild(QComboBox)
					combo.clear()
					combo.addItem(value)
					combo.setCurrentIndex(0)
					#self.parent.loadingProgress.setValue(i*progress_step)
				except:
					pass
		try:
			font_name = selectedTheme['font']['family']
			index = self.parent.changeSelectedFont.findText(font_name, Qt.MatchFixedString)
			if index >= 0:
				self.parent.changeSelectedFont.setCurrentIndex(index)
		except:
			pass
		self.parent.builder_left.selectedTitleSize.setValue(selectedTheme['font']['title_size'])
		self.parent.builder_left.selectedTextSize.setValue(selectedTheme['font']['text_size'])
		
		self.initial = False

	def countValues(self):
		i = 1
		for area in (
				"titlebar",
				"panel1",
				"panel2",
				"panel3",
				"panel4",
				"panel5",
				"footerbar",
				"dividers"
			):
			for key, value in self.theme_settings.items['theme'][area].items():
				i += 1
		return i

	def open_color_picker(self):
		
		#settings = Settings('builder')
		if self.builder_settings.items['selected_app'] == "":
			return
		
		btn = self.sender()
		genre = btn.parent().objectName().split('_')[0] 
		area = btn.parent().parent().objectName().split('_')[1]	
		# select color
		color = QColorDialog.getColor()
		if not color.isValid():
			return 
		
		# fill label
		for label in btn.parent().findChildren(QLabel): 
			if "selectedColor" in label.objectName():
				#label.setStyleSheet(f"background: {color.name()}; border: 2px solid teal;border-radius: 12px; max-width: 24px; max-height: 24px")	
				label.setStyleSheet(f"background: {color.name()}")	

		# add alternative colors to combobox
		combo = btn.parent().findChild(QComboBox)
		combo.clear()
		combo.addItem(color.name())
		#color = button.palette().color(QPalette.Background).name()
		color_list = []
		#color_list.append(color.name())
		qcolor = QColor(color.name())
		color_list.append(qcolor.darker(15).name())
		color_list.append(qcolor.darker(30).name())
		color_list.append(qcolor.darker(45).name())
		color_list.append(qcolor.darker(60).name())
		color_list.append(qcolor.darker(75).name())
		color_list.append(qcolor.darker(90).name())
		color_list.append(color.name())
		color_list.append(qcolor.darker(115).name())
		color_list.append(qcolor.darker(130).name())
		color_list.append(qcolor.darker(145).name())
		color_list.append(qcolor.darker(160).name())
		color_list.append(qcolor.darker(175).name())
		color_list.append(qcolor.darker(190).name())
		
		model = combo.model()
		color_list = list(dict.fromkeys(color_list))
		for row, color in enumerate(color_list):
			combo.addItem(color.title())
			model.setData(model.index(row, 0), QColor(color), Qt.BackgroundRole)
		combo.addItem("")

	def handleColorPressed(self):
		if self.builder_settings.items['selected_app'] == "":
			return

		el = self.sender()
		color = el.currentText() 
		
		label = el.parent().findChildren(QLabel)[1]
		if self.reset:
			label.setStyleSheet(f"background: transparent")
		else:
			label.setStyleSheet(f"background: {color}")
		
		if self.initial:
			return  
		
		genre = el.parent().objectName().split('_')[0] 
		area = el.parent().parent().objectName().split('_')[1]

		theme_name = self.builder_settings.items['selected_theme']
		if theme_name != "":
			target = self.theme_settings.items['themes'][theme_name]
		else:
			theme_name = None
			target = self.theme_settings.items['theme']
			
		target[area][genre] = color
		
		#self.theme_settings.serialize()
		self.reloadStyle(theme_name)
	
	def handleFontFamily(self):
		if self.builder_settings.items['selected_app'] == "":
			return

		el = self.sender()
		font = el.currentText() 
		theme_name = self.builder_settings.items['selected_theme']
		if theme_name != "":
			target = self.theme_settings.items['themes'][theme_name]
		else:
			theme_name = None
			target = self.theme_settings.items['theme']
		target['font']['family'] = font
		#self.theme_settings.serialize()
		self.reloadStyle(theme_name)
	
	def handleFontSize(self, value):
		if self.builder_settings.items['selected_app'] == "":
			return
		
		el = self.sender()
		if "Title" in el.objectName():
			genre = "title_size"
		else:
			genre = "text_size"

		theme_name = self.builder_settings.items['selected_theme']
		if theme_name != "":
			target = self.theme_settings.items['themes'][theme_name]
		else:
			theme_name = None
			target = self.theme_settings.items['theme']
		target['font'][genre] = value
		#self.theme_settings.serialize()
		self.reloadStyle(theme_name)

	def setInitFalse(self):
		self._init = False

	def getAppThemeCss(self, theme_name=None):
		regex = r"\w+\(([^\)]+)\)"
		with open(UIFunctions().resource_path(f'{self.apps_path}/{self.app_name}/gui/assets/style/base.qss'), "r", encoding='utf-8') as reader:
			base_stylesheet = reader.read().replace("{","{{").replace("}","}}")
			base_stylesheet = re.sub(regex, '{\\1}', base_stylesheet)
			
			if theme_name == None:
				theme = self.theme_settings.items['theme']
			else:
				theme = self.theme_settings.items['themes'][theme_name]
			formated_stylesheet = base_stylesheet.format(**theme)
			return formated_stylesheet

	def reloadStyle(self, theme_name):
		stylesheet = self.getAppThemeCss(theme_name)
		self.ui.centralwidget.setStyleSheet(stylesheet)
		
	def component(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return  strings[1].lower()
		
	def typos(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return strings[0].lower()
	
		
		
		
	