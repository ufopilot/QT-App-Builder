from qt_core import *
from app.gui.content import *
from app.gui.functions.settings import Settings
from app.gui.functions.ui_functions import UIFunctions


class Panel5(QWidget):
	_init = True
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = parent
		self.ui_settings = Settings('ui')
		
		
		####################################################
		# 
		# ################################################## 
		if self.ui_settings.items['panel5']['visible']:
			self.setup()
		else:
			self.ui.panel5.parent().hide()
			
	def setup(self):	
		print("in Arbreit")