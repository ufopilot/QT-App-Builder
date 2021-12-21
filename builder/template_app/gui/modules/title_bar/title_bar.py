
from qt_core import *
from builder.template_app.gui.content import *
from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions

class TitleBar(QWidget):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		settings = Settings('theme')
		self.theme_settings = settings.items
		#self.icon = QIcon()
		self.icon_color = self.theme_settings['theme']['titlebar']['icons']
		
		self.ui.appTitle.setText(self.settings['window']['app_name'])
		self.ui.appDescription.setText(self.settings['window']['description'])
		self.ui.appLogo.setPixmap(QPixmap(UIFunctions().resource_path(self.settings['window']['icon'])))
		
		if  not self.settings['window']['frameless']:
			self.ui.windowicons.hide()
		else:
			icon = qta.icon("msc.chrome-maximize", color=self.icon_color)
			self.ui.maximizewindow.setIcon(icon)
			icon = qta.icon("msc.chrome-close", color=self.icon_color)
			self.ui.closewindow.setIcon(icon)
			icon = qta.icon("msc.chrome-minimize", color=self.icon_color)
			self.ui.minimizewindow.setIcon(icon)
			
		
		self.ui.maximizewindow.clicked.connect(self.icon_maximize_restore)		
		self.ui.minimizewindow.clicked.connect(self.ui.window().showMinimized)
		self.ui.closewindow.clicked.connect(self.ui.window().close)
		self.ui.appDescription.mouseDoubleClickEvent = self.dbclick_maximize_restore

	def icon_maximize_restore(self):
		self.ui.window().showMaximized
		button = self.sender()
		
		if self.ui.window().isMaximized():
			icon = qta.icon("msc.chrome-maximize", color=self.icon_color)
			button.setIcon(icon)
			self.ui.window().showNormal()
		else:
			icon = qta.icon("msc.chrome-restore", color=self.icon_color)
			button.setIcon(icon)
			self.ui.window().showMaximized()
			

	def dbclick_maximize_restore(self, event=None):
		if self.settings['window']['frameless']:
			QTimer.singleShot(0, self.ui.maximizewindow.clicked.emit)
			