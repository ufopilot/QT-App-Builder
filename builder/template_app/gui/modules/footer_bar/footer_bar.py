
from qt_core import *
from app.gui.content import *
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions

class FooterBar(QWidget):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		settings = Settings('theme')
		self.theme_settings = settings.items
		
		##########################################################################################
		# footer_bar 
		##########################################################################################
		self.ui.author.setText(f"{self.settings['window']['version']} | {self.settings['window']['year']} | {self.settings['window']['author']}")
			