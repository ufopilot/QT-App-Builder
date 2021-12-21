from qt_core import *
from builder.template_app.gui.content.content_functions import *
	
Gen_Class, Base_Class = loadUiType(resource_path("builder/template_app/gui/content/tabs/main.ui"))


class TabsWest(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.tabWidget.setTabPosition(QTabWidget.West)
		self.pageTitle.setText("Tab Position West")		
