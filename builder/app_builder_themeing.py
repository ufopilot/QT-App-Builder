from PyQt5.QtCore import pyqtRemoveInputHook
from qt_core import *
#from app.gui.content import *

from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
import re
from webcolors import hex_to_name

class Worker(QRunnable):
	def __init__(self, widget, settings, progress):
		super().__init__()
		self.widget = widget
		self.settings = settings
		self.progress = progress

	def run(self):
		
		self.progress.hide()

class ThemeBuilder(QWidget):
	_init = True
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = ui
		self.parent = parent

		self.apps_path = apps_path
		self.app_name = app_name

		self.ui_settings = None
		self.theme_settings = None
		settings = Settings('builder')
		self.builder_settings = settings

		self.initial = False
		self.reset = False

		self.addProps()

	def addProps(self):

		if 'icons_color' in self.builder_settings.items:
			if self.builder_settings.items['icons_color'] != "":
				icon_color = self.builder_settings.items['icons_color']
			else:
				icon_color = "white"
				
		for frame in self.parent.Theming.findChildren(QFrame):
			try:
				label1 = frame.findChildren(QLabel)[0]
				label2 = frame.findChildren(QLabel)[1]
				btn = frame.findChild(QPushButton)

				label1.setProperty("type", 1)
				label2.setProperty("type", "color_label")
				icon = qta.icon("fa.pencil", color=icon_color)
				btn.setIcon(icon)
			except:
				pass

	def setup(self):
		#threadCount = QThreadPool.globalInstance().maxThreadCount()
		#pool = QThreadPool.globalInstance()
		settings = Settings('builder')
		self.builder_settings = settings
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		self.ui_settings = Settings('ui', apps_path=self.apps_path, app_name=self.app_name)
		
		valcount = self.countValues()
		progress_step = 100 / valcount
		
		for button in self.parent.Theming.findChildren(QPushButton):
			button_name = button.objectName()
			if "colorPicker" in button_name:
				button.setCursor(QCursor(Qt.PointingHandCursor))
				try:
					button.clicked.disconnect() 
				except:
					pass
				button.clicked.connect(self.open_color_picker)

		for combo in self.parent.Theming.findChildren(QComboBox):
			combo.setCursor(QCursor(Qt.PointingHandCursor))
			if "changeSelectedColor" in combo.objectName():
				#self.fillColorsCombo(combo)
				try:
					combo.currentTextChanged.disconnect()
				except:
					pass 
				combo.currentTextChanged.connect(self.handleColorPressed)
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
			#worker = Worker(widget, self.theme_settings.items['theme'][area], eval(f"self.parent.{area}_progressBar"))
			#pool.start(worker)
			
			
			#print(widget.objectName())

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

		self.initial = False

		#	if any(key in button_name for key in List3):
		#		button.stateChanged.connect(self.changeBarIconsColor)

	def loadThemeColors(self):
		self.initial = True
		
		theme_name = self.builder_settings.items['selected_theme']
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		
		if theme_name == "" or theme_name == "no-theme":
			colors = self.theme_settings.items['theme']
		else: 
			colors = self.theme_settings.items['themes'][theme_name]

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
			for key, value in colors[area].items():
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
		
		settings = Settings('builder')
		if settings.items['selected_app'] == "":
			print("#### aus1111")
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
		
		self.theme_settings.serialize()
		self.reloadStyle(theme_name)
		
	def setInitFalse(self):
		self._init = False

	def reloadStyle(self, theme_name):
		stylesheet = UIFunctions().getAppTheme(self.theme_settings.items, self.apps_path, self.app_name, theme_name)
		self.ui.centralwidget.setStyleSheet(stylesheet)
		
	def component(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return  strings[1].lower()
		
	def typos(self, name):
		strings = re.sub( r"([A-Z])", r" \1", name).split()
		return strings[0].lower()
	
		
		
		
	