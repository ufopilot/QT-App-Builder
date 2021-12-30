from qt_core import *
from builder.template_app.gui.content import *
from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions


class Panel2(QWidget):
	_init = True
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		
		####################################################
		# 
		# ################################################## 
		if self.settings['panel2']['visible']:
			self.resizePanel()
			self.setup()
		else:
			self.ui.panel2.parent().hide()
			

		
	def resizePanel(self):
		self.ui.parentPanel2.setMinimumSize(QSize(self.settings['panel2']['maximum'], 0))
		self.ui.parentPanel2.setMaximumSize(QSize(self.settings['panel2']['maximum'], 16777215))
		
	def setup(self):	
		print("in Arbreit")