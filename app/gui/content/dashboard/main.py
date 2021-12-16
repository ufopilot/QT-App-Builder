from types import FunctionType
from app.gui.widgets.py_icon_button.py_icon_button import PyIconButton
from qt_core import *
from app.gui.functions.ui_functions import *
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./app/gui/content/dashboard/main.ui"))


class Dashboard(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		#self.centralwidget.setStyleSheet("background: #fff;")
		#self.icon_button_2 = PyIconButton(
        #    icon_path = UIFunctions().set_svg_icon("chevron-left.svg"),
        #    parent = self,
        #    app_parent = self.centralwidget,
        #    tooltip_text = "BTN with tooltip",
        #    width = 40,
        #    height = 40,
        #    radius = 8,
        #)

	
