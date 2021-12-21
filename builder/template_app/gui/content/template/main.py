#from main import UIFunctions
from qt_core import *
from builder.template_app.gui.content.content_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("builder/template_app/gui/content/template/main.ui"))

class TemplatePage(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)

	
