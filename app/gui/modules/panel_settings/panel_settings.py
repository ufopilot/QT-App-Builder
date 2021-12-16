from qt_core import *
from app.gui.functions.ui_functions import UIFunctions
from app.gui.functions.settings import Settings


Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./app/gui/uis/panel_settings.ui"))

class PanelSettings(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		##########################################################################################
		# Init
		##########################################################################################
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)

		#self.ui = parent
		
		# LOAD SETTINGS
		# ///////////////////////////////////////////////////////////////
		settings = Settings('ui')
		self.settings = settings.items

		effect = QGraphicsDropShadowEffect(self.frame, enabled=False, blurRadius=5)
		self.frame.setGraphicsEffect(effect)
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(15)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 150))
		# add the shadow object to the frame
		self.frame.raise_()
		self.frame.setGraphicsEffect(self.shadow)

		UIFunctions().setGuiStyle("dialog", "dark", self.frame)

		self.buttonBox.accepted.connect(self.ok_callback)
		self.buttonBox.rejected.connect(self.cancel_callback)
		

	def ok_callback(self):
		print("OK")
	
		self.close()

	def cancel_callback(self):
		print("Cancel")
		self.close()		