#rom xml.etree.ElementTree import Element
from . settings import Settings
from . ui_functions import UIFunctions
from qt_core import *

from pathlib import Path
import glob
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_bottom.ui"))


class AppBuilderBottom(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		settings = Settings('ui')
		self.settings = settings
		
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(size.width()-400, 160)
		self.move(399, size.height()-200)
		
		
		#self.ui.move(399, -1)
		#self.setWindowFlag(Qt.WindowStaysOnBottomHint)
		
		self.loadThemesButtons()
	
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
		app_theme_settings = Settings('theme')
		app_theme_settings.items['default_theme'] = name
		#app_theme_settings.items['theme'] = app_theme_settings.items['themes'][name]
		app_theme_settings.serialize()
		#
		#builder_theme_settings = Settings('builder_theme')
		#builder_theme_settings.items['theme'] = app_theme_settings.items['themes'][name]
		#builder_theme_settings.serialize()
		#
		#self.parent.showMessage("info", "Load Theme", f"Theme {name} loaded!",2)
		self.parent.reload_app()


	def connectThemeButtons(self):
		for button in self.findChildren(QAbstractButton):
			if button.metaObject().className() == "QPushButton": 
				button.clicked.connect(self.loadSavedTheme)

	def loadThemesButtons(self):
		self.scrollFrame.hide()
		for childframe in self.scrollFrame.findChildren(QFrame):
			childframe.deleteLater()

		i = 0
		for file_path in glob.glob("app/gui/resources/imgs/themes/*.png"):
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