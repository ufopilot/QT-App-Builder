
from qt_core import *
from app.gui.content import *
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions

class TitleBar(QWidget):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		settings = Settings('theme')
		self.theme_settings = settings.items
		self.icon = QIcon()
        
		self.ui.appTitle.setText(self.settings['window']['app_name'])
		self.ui.appDescription.setText(self.settings['window']['description'])
		self.ui.appLogo.setPixmap(QPixmap(UIFunctions().resource_path(self.settings['window']['icon'])))
		
		if  not self.settings['window']['frameless']:
			self.ui.windowicons.hide()
		else:
			self.icon.addPixmap(QPixmap(UIFunctions().set_svg_icon("chrome-maximize.svg", self.theme_settings['colors']['header_icon_color'])))
			self.ui.maximizewindow.setIcon(self.icon)
			self.icon.addPixmap(QPixmap(UIFunctions().set_svg_icon("chrome-close.svg", self.theme_settings['colors']['header_icon_color'])))
			self.ui.closewindow.setIcon(self.icon)
			self.icon.addPixmap(QPixmap(UIFunctions().set_svg_icon("chrome-minimize.svg", self.theme_settings['colors']['header_icon_color'])))
			self.ui.minimizewindow.setIcon(self.icon)
			
		
		self.ui.maximizewindow.clicked.connect(self.icon_maximize_restore)		
		self.ui.minimizewindow.clicked.connect(self.ui.window().showMinimized)
		self.ui.closewindow.clicked.connect(self.ui.window().close)
		self.ui.appDescription.mouseDoubleClickEvent = self.dbclick_maximize_restore

	def icon_maximize_restore(self):
		self.ui.window().showMaximized
		button = self.sender()
		if self.ui.window().isMaximized():
			self.icon.addPixmap(QPixmap(UIFunctions().set_svg_icon("chrome-maximize.svg", self.theme_settings['colors']['header_icon_color'])))
			button.setIcon(self.icon)
			self.ui.window().showNormal()
		else:
			self.icon.addPixmap(QPixmap(UIFunctions().set_svg_icon("chrome-restore.svg", self.theme_settings['colors']['header_icon_color'])))
			button.setIcon(self.icon)
			self.ui.window().showMaximized()
			

	def dbclick_maximize_restore(self, event=None):
		if self.settings['custom_title_bar']:
			QTimer.singleShot(0, self.ui.maximizewindow.clicked.emit)
			