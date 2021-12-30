from qt_core import *
from builder.template_app.gui.content import *
from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions


class Panel5(QWidget):
	_init = True
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		
		
		####################################################
		# 
		# ################################################## 
		if self.settings['panel5']['visible']:
			self.resizePanel()
			self.setup()

		else:
			self.ui.panel5.parent().hide()

	def resizePanel(self):
		self.ui.parentPanel5.setMinimumSize(QSize(0, self.settings['panel5']['maximum']))
		self.ui.parentPanel5.setMaximumSize(QSize(16777215, self.settings['panel5']['maximum']))

	def setup(self):	
		print("in Arbreit")