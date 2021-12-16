from qt_core import *
from app.gui.content.content_functions import *
	
Gen_Class, Base_Class = loadUiType(resource_path("./app/gui/content/home/main.ui"))


class HomeWidget(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)

	
