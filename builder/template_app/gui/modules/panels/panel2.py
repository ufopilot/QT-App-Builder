from qt_core import *
from builder.template_app.gui.content import *
from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions


class Panel2(QWidget):
	_init = True
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = parent
		self.ui_settings = Settings('ui')
		
		
		####################################################
		# 
		# ################################################## 
		if self.ui_settings.items['panel2']['visible']:
			self.setup()
		else:
			self.ui.panel2.parent().hide()
			
	def setup(self):	
		print("in Arbreit")