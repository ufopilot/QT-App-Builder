from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions
from qt_core import *


class SetStyle(QWidget):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		settings = Settings('theme')
		self.theme_settings = settings.items
		stylesheet = UIFunctions().getAppTheme(self.theme_settings, self.theme_settings['default_theme'])
		self.ui.centralwidget.setStyleSheet(stylesheet)
		effect = QGraphicsDropShadowEffect(self.ui.mainFrame, enabled=False, blurRadius=5)
		self.ui.mainFrame.setGraphicsEffect(effect)
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(15)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 150))
		# add the shadow object to the frame
		self.ui.mainFrame.raise_()
		self.ui.mainFrame.setGraphicsEffect(self.shadow)

	