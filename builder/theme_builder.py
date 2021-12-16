from PyQt5.QtCore import pyqtRemoveInputHook
from qt_core import *
#from app.gui.content import *

from . settings import Settings
from . ui_functions import UIFunctions
import re
from webcolors import hex_to_name


class ThemeBuilder(QWidget):
	_init = True
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = ui
		self.parent = parent

		self.ui_settings = Settings('ui')
		self.theme_settings = Settings('builder_theme')
		#self.selectColors()
		
		###self.parent.loadingProgressBar.setValue(0)

		####################################################
		# 
		# ################################################## 
		self.setup()
		###if self.ui_settings.items['panel4']['visible']:
		###	self.setup()
		###else:
		###	self.ui.panel4.parent().hide()
		###	self.ui.loadingLabel.setText("")
		###	###self.ui.loadingProgressBar.hide()
		###	QTimer.singleShot(100, self.ui.controllerButtons.EnableToggleButtons)
		
	def setup(self):
		for button in self.parent.findChildren(QPushButton):
			button_name = button.objectName()
			if "colorPicker" in button_name:
				button.setCursor(QCursor(Qt.PointingHandCursor))
				button.clicked.connect(self.open_color_picker)

		for combo in self.parent.findChildren(QComboBox):
			combo.setCursor(QCursor(Qt.PointingHandCursor))
			if "changeSelectedColor" in combo.objectName():
				#print(combo.objectName())
				#self.fillColorsCombo(combo)
				combo.currentTextChanged.connect(self.handleColorPressed)

		return 	
		QTimer.singleShot(1000, self.selectColors)
		List1 = ("HeaderColor", "FooterColor", "BorderColor", "HoverColor")
		List2 = ("First_textColor", "Second_textColor", "Third_textColor")
		List3 = ("headerDarkIcons", "headerLightIcons", "footerDarkIcons", "footerLightIcons")
		for button in self.parent.findChildren(QAbstractButton):
			button_name = button.objectName()
			button.setCursor(QCursor(Qt.PointingHandCursor))

			if "MainColor" in button_name:
				button.setCheckable(True)
				button.clicked.connect(self.getColorPalette)
		
			if "iconColor" in button_name:
				button.setCheckable(True)
				button.clicked.connect(self.changeIconsColor)
			
			if any(key in button_name for key in List1):
				button.setCheckable(True)
				button.clicked.connect(self.changeColor)

			if any(key in button_name for key in List2):
				button.setCheckable(True)
				button.clicked.connect(self.changeTextColor)
			
			if any(key in button_name for key in List3):
				button.stateChanged.connect(self.changeBarIconsColor)

	def open_color_picker(self):
		btn = self.sender()
		genre = btn.parent().objectName().split('_')[0] 
		area = btn.parent().parent().objectName().split('_')[1]
		print(area, genre)
		
		# select color
		color = QColorDialog.getColor()
		if not color.isValid():
			return 

		# fill label
		for label in btn.parent().findChildren(QLabel):
			if "selectedColor" in label.objectName():
				label.setStyleSheet(f"background: {color.name()}; border: 2px solid teal;border-radius: 12px; max-width: 24px; max-height: 24px")	
		
		# add alternative colors to combobox
		combo = btn.parent().findChild(QComboBox)
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
			#print(color.title())
			model.setData(model.index(row, 0), QColor(color), Qt.BackgroundRole)
		combo.addItem("")

	def handleColorPressed(self):
		el = self.sender()
		#name = el.objectName()
		color = el.currentText() 
		for label in el.parent().findChildren(QLabel):
			if "selectedColor" in label.objectName():
				label.setStyleSheet(f"background: {color}; border: 2px solid teal;border-radius: 12px; max-width: 24px; max-height: 24px")	

		genre = el.parent().objectName().split('_')[0] 
		area = el.parent().parent().objectName().split('_')[1]
		
		print(area, genre, color)

	def selectColors(self):
		T = 0
		D=1000
		counter=0
		backgroundColorList = self.theme_settings.items['colors']['background']
		for comp in ("header", "footer", "controller", "content"):	
			
			compString = comp+"MainColor"
			color = self.theme_settings.items['theme'][comp]['background']
			
			for button in self.parent.findChildren(QAbstractButton):
				if compString in button.objectName():
					# load background colors
					#####################################################
					regex = r"[A-z]*(\d*)"
					subst = "\\1"
					nr = re.sub(regex, subst, button.objectName(), 0, re.MULTILINE)
					#print(compString, button.objectName())#, backgroundColorList[int(nr)-1])
					try:
						button.setStyleSheet(f"background: {backgroundColorList[int(nr)-1]}")
					except:
						pass
					# get selected background
					#####################################################
					if color == button.palette().color(QPalette.Background).name():	
						QTimer.singleShot(T, button.clicked.emit)
						QTimer.singleShot(T, button.toggle)
						QTimer.singleShot(D, partial(self.selectSubColors, comp))
						
						T += 100
						D += 100
						counter +=1
						###self.ui.loadingProgressBar.setValue(counter*2)
						

			# load text colors
			#####################################################
			textColorList = self.theme_settings.items['colors']['text']
			for substr in ("First_text", "Second_text", "Third_text"):
				i = 1
				
				for textColor in textColorList:
					btn = eval(f"self.parent.{comp}{substr}Color{i}")
					btn.setStyleSheet(f"background: {textColor}") 
					i += 1
					counter +=1	
					###self.ui.loadingProgressBar.setValue(counter*2)
			
		# Load icons colors
		# ##################################################	
		nr = 1
		for key, value in self.theme_settings.items['colors']['icon_colors'].items():
			try:
				icon_btn = eval(f"self.parent.iconColor{nr}")
				nr += 1
			
				icon_btn.setStyleSheet(f"background: {key}")
			except:
				pass
		
		# Load BarIcons colors
		# ##################################################	
		# header
		for key in ("header", "footer"): 
			color = self.theme_settings.items['colors'][key+'_icon_color'].capitalize() 
			checkbox = eval(f"self.parent.{key}{color}Icons")
			checkbox.setChecked(True)

		QTimer.singleShot(D, self.setInitFalse)
		# clear loadings infos
		###self.ui.loadingLabel.setText("")
		###self.ui.loadingProgressBar.hide()
		###QTimer.singleShot(100, self.ui.controllerButtons.EnableToggleButtons)
		#self.ui.controllerButtons.EnableToggleButtons()

	def setInitFalse(self):
		self._init = False

	def selectSubColors(self, comp):
		T = 0
		if comp == "content":
			subcomps = ("Header", "Footer", "Hover", "Border")
		else:
			subcomps = ("Hover", "Border")

		for subcomp in subcomps:
			color = self.theme_settings.items['theme'][comp][subcomp.lower()]
			for i in range(1,5):
				btn = self.parent.findChild(QPushButton, f"{comp}{subcomp}Color{i}")
				if color == btn.palette().color(QPalette.Background).name():
					QTimer.singleShot(T, btn.clicked.emit)
					QTimer.singleShot(T, btn.toggle)
			T += 100		

	def getColorPalette(self):

		button = self.sender()
		name = button.objectName()
		parentFrame = button.parent().parent()
		for btn in parentFrame.findChildren(QAbstractButton):
			if btn.isChecked() and btn.objectName() != button.objectName():
				btn.toggle()

		colorList = [] 
		color = button.palette().color(QPalette.Background).name()
		qcolor = QColor(color)

		colorList.append(color)
		colorList.append(qcolor.darker(110).name())
		colorList.append(qcolor.darker(120).name())
		colorList.append(qcolor.darker(130).name())
		
		i = 0
		if self.typos(name) == "content":
			buttons = {"Header": [], "Footer": [], "Border": [], "Hover": []}
		else:
			buttons = {"Border": [], "Hover": []}
		
		for x in range (1,5):
			for tg, value in buttons.items():
				try:
					buttons[tg].append(eval(f"self.parent.{self.typos(name)}{tg}Color{x}"))
				except:
					pass
		
		for item, btns in buttons.items():
			i = 0
			for btn in btns:
				try:
					btn.setStyleSheet(f'background: {colorList[i]}')
				except:
					pass	
				i += 1
		## load text colors
		######################################################
		#textColorList = self.theme_settings.items['colors']['text']
		#for substr in ("First_text", "Second_text", "Third_text"):
		#	i = 1
		#	for textColor in textColorList:
		#		btn = eval(f"self.ui.{self.typos(name)}{substr}Color{i}")
		#		btn.setStyleSheet(f"background: {textColor}") 
		#		i += 1

		# on changing main background -> click first subcolor
		#####################################################
		if not self._init:
			for tg, value in buttons.items():
				T=100
				sub_btn = eval(f"self.parent.{self.typos(name)}{tg}Color1")
				#for sub_btn in (self.parent.headerHoverColor1, self.parent.headerBorderColor1):
				QTimer.singleShot(T, partial(self.toggleSelected, sub_btn))
				QTimer.singleShot(T, sub_btn.clicked.emit)
				T += 100
		# write theme-settings
		# ###################################################		
		self.theme_settings.items['theme'][self.typos(name)]['background'] = color
		self.theme_settings.items['theme'][self.typos(name)]['background_alternate'] = colorList[1]
		self.theme_settings.serialize()
		
		# reload stylesheet
		#####################################################
		self.reloadStyle()
		

	def changeColor(self):
		button = self.sender()
		name = button.objectName()
		parentFrame = button.parent()
		for btn in parentFrame.findChildren(QAbstractButton):
			_name = btn.objectName()
			if btn.isChecked() and _name != name:
				btn.toggle()
		color = button.palette().color(QPalette.Background).name()
		self.theme_settings.items['theme'][self.typos(name)][self.component(name)] = color
		
		self.theme_settings.serialize()
		self.reloadStyle()

	def changeTextColor(self):
		button = self.sender()
		name = button.objectName()
		parentFrame = button.parent()
		for btn in parentFrame.findChildren(QAbstractButton):
			_name = btn.objectName()
			if btn.isChecked() and _name != name:
				btn.toggle()
		color = button.palette().color(QPalette.Background).name()
		self.theme_settings.items['theme'][self.typos(name)][self.component(name)] = color
		
		self.theme_settings.serialize()
		self.reloadStyle()

	def clickSubSelected(self, button, T):
		QTimer.singleShot(T, button.clicked.emit)

	def toggleSelected(self, button):
		name = button.objectName()
		parentFrame = button.parent()
		
		for btn in parentFrame.findChildren(QAbstractButton):
			if btn.isChecked():
				btn.toggle()
		button.toggle()
	
	def changeIconsColor(self):
		button = self.sender()
		name = button.objectName()
		parentFrame = button.parent()
		for btn in parentFrame.findChildren(QAbstractButton):
			_name = btn.objectName()
			if btn.isChecked() and _name != name:
				btn.toggle()
		color = button.palette().color(QPalette.Background).name()
		color_name = hex_to_name(color)
		#print(color_name, color)
		self.theme_settings.items['colors']['content_icon_color'] = color_name
		self.theme_settings.serialize()
	
	def changeBarIconsColor(self):
		checkbox = self.sender()
		name = checkbox.objectName()
		if "Dark" in name:
			op_name = name.replace("Dark", "Light")
			this_color = "dark"
			other_color = "light"
		else:
			op_name = name.replace("Light", "Dark")
			this_color = "light"
			other_color = "dark"

		op_checkbox = eval(f"self.parent.{op_name}")

		if checkbox.isChecked():
			op_checkbox.setChecked(False)
			color = this_color

		if not checkbox.isChecked():
			op_checkbox.setChecked(True)
			color = other_color

		typos = self.typos(name).lower()
		self.theme_settings.items['colors'][typos+'_icon_color'] = color 
		self.theme_settings.serialize()

	def reloadStyle(self):
		stylesheet = UIFunctions().getAppTheme(self.theme_settings.items)
		
		#self.ui.centralwidget.setStyleSheet(stylesheet)
		self.parent.app.centralwidget.setStyleSheet(stylesheet)
	
	def component(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return  strings[1].lower()
		
	def typos(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return strings[0].lower()
	
		
		
		
	