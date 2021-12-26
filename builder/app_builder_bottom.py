#rom xml.etree.ElementTree import Element
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

from pathlib import Path
import glob
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_bottom.ui"))


class AppBuilderBottom(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent
		self.apps_path = apps_path
		self.app_name = app_name
		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		#settings = Settings('ui')
		#self.settings = settings
		settings = Settings('builder')
		self.builder_settings = settings
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(size.width()-self.builder_settings.items['left_width']+1, self.builder_settings.items['bottom_height'])
		self.move(self.builder_settings.items['left_width']-1, size.height()-self.builder_settings.items['bottom_height'])
		
		
		#self.ui.move(399, -1)
		#self.setWindowFlag(Qt.WindowStaysOnBottomHint)
		
		self.loadThemesButtons()

		self.themes_label.setStyleSheet("min-width: 40px;max-width: 40px; border-right: 1px solid rgb(49, 54, 72); font-size: 16px;")
	
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
		
		theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
	
		theme_settings.items['default_theme'] = name

		#app_theme_settings.items['theme'] = app_theme_settings.items['themes'][name]
		theme_settings.serialize()
		
		#
		#builder_theme_settings = Settings('builder_theme')
		#builder_theme_settings.items['theme'] = app_theme_settings.items['themes'][name]
		#builder_theme_settings.serialize()
		#
		#self.parent.showMessage("info", "Load Theme", f"Theme {name} loaded!",2)
		
		self.setSelectedTheme(name)
		
		self.parent.reload_app()

	def setSelectedTheme(self, name=""):
		settings = Settings('builder')
		settings.items['selected_theme'] = name
		settings.serialize()
		self.parent.builder_center.selected_theme.setText(f"Theme: {name}")
	
	def connectThemeButtons(self):
		for button in self.findChildren(QAbstractButton):
			if button.metaObject().className() == "QPushButton": 
				button.clicked.connect(self.loadSavedTheme)
	
	def clearThemesButtons(self):
		for childframe in self.scrollFrame.findChildren(QFrame):
			childframe.deleteLater()

	def loadThemesButtons(self):
		self.scrollFrame.hide()
		self.clearThemesButtons()

		i = 0
		for file_path in glob.glob(f"{self.apps_path}/{self.app_name}/gui/resources/imgs/themes/*.png"):
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
			label = QLabel(frame)
			label.setObjectName(u"label")
			label.setText(name)
			label.setStyleSheet("padding: 5px;")
			layout.addWidget(label)
			pushButton = QPushButton(frame)
			pushButton.setObjectName(f"{name}")
			pushButton.setCursor(QCursor(Qt.PointingHandCursor))
			pushButton.setCheckable(True)
			pushButton.setToolTip(f"Load {name} Theme")
			icon = QIcon()
			icon.addFile(f"{file_path}", QSize(), QIcon.Normal, QIcon.Off)
			pushButton.setIcon(icon)
			pushButton.setIconSize(QSize(158, 113))

			layout.addWidget(pushButton)
			self.innerLayout.addWidget(frame, 0, Qt.AlignTop)
			i += 1
		self.scrollFrame.show()
		self.connectThemeButtons()

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderBottom()
	w.show()
	sys.exit(app.exec())
