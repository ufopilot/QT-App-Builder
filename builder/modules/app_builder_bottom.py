#rom xml.etree.ElementTree import Element
from builder.modules.app_builder_clone_theme import AppBuilderCloneTheme
from builder.modules.app_builder_delete_theme import AppBuilderDeleteTheme
from builder.modules.app_builder_settings import Settings
from builder.modules.app_builder_functions import UIFunctions
from qt_core import *

from pathlib import Path
import glob
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_bottom.ui"))


class AppBuilderBottom(Base_Class, Gen_Class):
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
		self.theme_settings = None
		#self.setWindowFlag(Qt.WindowStaysOnBottomHint)
		
	def setup(self):
		self.themeRemover = AppBuilderDeleteTheme(self, self.ui)
		self.themeCloner = AppBuilderCloneTheme(self, self.ui)

		icon = qta.icon("mdi6.chevron-double-down", color="white")
		self.toggleBottom.setIcon(icon)
		self.toggleBottom.setIconSize(QSize(20, 20))
		self.toggleBottom.setCursor(QCursor(Qt.PointingHandCursor))
		self.toggleBottom.setCheckable(False)
		self.toggleBottom.clicked.connect(self.toggle_bottom_panel)
		self.origBottomHeight = self.parent.builder_settings.items['bottom']['height']
		self.visible = True

		self.resize_window()
		self.loadThemesButtons()

	def toggle_bottom_panel(self):
		if self.visible:
			icon = qta.icon("mdi6.chevron-double-up", color="white")
			self.visible = False
			self.parent.builder_settings.items['bottom']['height'] = self.parent.builder_settings.items['bottom']['minimum']
			self.parent.update_settings("builder")
			self.themes_label.hide()
			self.clearThemesButtons()
		else:
			icon = qta.icon("mdi6.chevron-double-down", color="white")
			self.visible = True
			animate_dr = True
			self.parent.builder_settings.items['bottom']['height'] = self.origBottomHeight
			self.parent.update_settings("builder")
			self.themes_label.show()
			self.loadThemesButtons()
		
		
		self.resize_window()
		self.parent.builder_left.resize_window()
		self.parent.builder_center.resize_window()
		self.parent.builder_center_header.resize_window()
		self.parent.builder_bottom.resize_window()
		self.sender().setIcon(icon)
	
	def resize_window(self):
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(
			size.width()
			-
			self.builder_settings.items['left']['width']
			- 
			self.builder_settings.items['right']['width'] 
			- 
			self.builder_settings.items['bottom']['right'], 
			self.builder_settings.items['bottom']['height']
		)
		self.move(
			self.builder_settings.items['left']['width']
			+
			self.builder_settings.items['bottom']['left'], 
			size.height()
			-
			self.builder_settings.items['bottom']['height']
			-
			self.builder_settings.items['bottom']['bottom']
		)

	def createScrollArea(self):
		for i in range(40):
			b = QPushButton(self.scrollFrame)
			b.setText(str(i))
			#self.scrollFrame.layout().addWidget(b)
			b.setObjectName(u"pushButton_2")

			self.innerLayout.addWidget(b)
		
	def loadSavedTheme(self):
		btn = self.sender()
		for button in self.findChildren(QAbstractButton):
			if button.metaObject().className() == "QPushButton": 
				if button.isChecked():
					button.toggle()

		
		btn.toggle()
		name = btn.objectName()
		if name == "no-theme":
			name = ""

		theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
			
		theme_settings.items['default_theme'] = name

		theme_settings.serialize()
		self.theme_settings = theme_settings
		
		self.setSelectedTheme(name)
		
		self.parent.reload_app()

	def setSelectedTheme(self, name=""):
		self.parent.builder_settings.items['selected_theme'] = name
		self.parent.update_settings("builder")
		self.parent.builder_center_header.selected_theme.setText(f"Theme: {name}")
	
	def connectThemeButtons(self):
		for button in self.findChildren(QAbstractButton):
			if button.metaObject().className() == "QPushButton": 
				if button.objectName() != "no-theme":
					button.clicked.connect(self.loadSavedTheme)
				else:
					button.clicked.connect(self.loadSavedTheme)

	def clearThemesButtons(self):
		for childframe in self.scrollFrame.findChildren(QFrame):
			childframe.deleteLater()

	def cloneTheme(self):
		btn = self.sender()
		theme = btn.objectName().replace("clone_","")
		img = f"{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/{theme}.png"
		
		if self.themeCloner.isVisible():
			return 

		self.themeCloner.img = img
		self.themeCloner.theme = theme
		self.themeCloner.app_name = self.app_name
		self.themeCloner.apps_path = self.apps_path

		self.themeCloner.show()
	

	def removeTheme(self):
		btn = self.sender()
		theme = btn.objectName().replace("remove_","")
		img = f"{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/{theme}.png"
		
		if self.themeRemover.isVisible():
			return 
		self.themeRemover.img = img
		self.themeRemover.theme = theme
		self.themeRemover.app_name = self.app_name
		self.themeRemover.apps_path = self.apps_path
		self.themeRemover.show()
		

	def loadThemesButtons(self):
		self.scrollFrame.hide()
		self.clearThemesButtons()
		icon_color = self.builder_settings.items['icons_color']
		remove_icon = qta.icon("ei.remove-circle", color=icon_color)
		clone_icon = qta.icon("fa.clone", color=icon_color)
		i = 0
		if self.app_name == None:
			return 
		
		themes_list = glob.glob(f"{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/*.png")
		themes_list.insert(0,f"builder/imgs/no-theme.png")
		for file_path in themes_list:
			name = Path(file_path).stem #.capitalize() 
			frame = QFrame(self.scrollFrame)
			frame.setObjectName(u"frame")
			frame.setMaximumSize(QSize(194, 16777215))
			frame.setFrameShape(QFrame.StyledPanel)
			frame.setFrameShadow(QFrame.Raised)
			layout = QVBoxLayout(frame)
			layout.setSpacing(0)
			layout.setObjectName(u"layout")
			layout.setContentsMargins(9, 0, 9, 30)
			headerFrame = QFrame(frame)
			headerFrame.setObjectName(u"headerFrame")
			headerFrame.setFrameShape(QFrame.StyledPanel)
			headerFrame.setFrameShadow(QFrame.Raised)

			sublayout = QHBoxLayout(headerFrame)
			sublayout.setObjectName(u"sublayout")
			#sublayout.setContentsMargins(0, 0, 0, 0)
			#sublayout.setSpacing(5)
			themeName = QLabel(headerFrame)
			themeName.setObjectName(u"label")
			themeName.setText(name)

			themeName.setStyleSheet("padding: 5px;")
			sublayout.addWidget(themeName)

			if name != "no-theme":
				#pushButton = QPushButton(headerFrame)
				#pushButton.setObjectName(u"pushButton")
				#pushButton.setMinimumSize(QSize(40, 0))
				#pushButton.setMaximumSize(QSize(40, 16777215))

				icon = QPushButton(headerFrame)
				icon.setObjectName(f"clone_{name}")
				#icon.setMinimumSize(QSize(40, 0))
				#icon.setMaximumSize(QSize(40, 16777215))

				icon.setIcon(clone_icon)
				icon.setCursor(QCursor(Qt.PointingHandCursor))
				icon.setFlat(True)
				icon.setToolTip(f"Clone Theme: {name}")
				icon.clicked.connect(self.cloneTheme)
				icon.setStyleSheet("border: none;")
				sublayout.addWidget(icon,0, Qt.AlignRight)

				icon = QPushButton(headerFrame)
				icon.setObjectName(f"remove_{name}")
				#icon.setMinimumSize(QSize(40, 0))
				#icon.setMaximumSize(QSize(40, 16777215))

				icon.setIcon(remove_icon)
				icon.setCursor(QCursor(Qt.PointingHandCursor))
				icon.setFlat(True)
				icon.setToolTip(f"Remove Theme: {name}")
				icon.clicked.connect(self.removeTheme)
				icon.setStyleSheet("border: none;")
				sublayout.addWidget(icon,0, Qt.AlignRight)
				
			layout.addWidget(headerFrame)
			pushButton = QPushButton(frame)
			pushButton.setObjectName(f"{name}")
			pushButton.setCursor(QCursor(Qt.PointingHandCursor))
			pushButton.clicked.connect(self.loadSavedTheme)
			pushButton.setCheckable(True)
			if name == "no-theme":
				pushButton.toggle()
			pushButton.setToolTip(f"Load {name} Theme")
			icon = QIcon()
			icon.addFile(f"{file_path}", QSize(), QIcon.Normal, QIcon.Off)
			pushButton.setIcon(icon)
			pushButton.setIconSize(QSize(158, 113))

			layout.addWidget(pushButton)
			self.innerLayout.addWidget(frame, 0, Qt.AlignTop)
			i += 1
		self.scrollFrame.show()
