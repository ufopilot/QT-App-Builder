from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_message.ui"))


class AppBuilderMessage(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(400, 50)
		self.move(size.width()-400, size.height()-150)
	
	def notify(self, msg_type, title, message):
		self.title.setText(title)
		self.message.setText(message)
		if msg_type == "info":
			icon = qta.icon("fa.info-circle", color="#17a2b8")
		if msg_type == "warning":
			icon = qta.icon("fa.warning", color="#ffc107")
		if msg_type == "danger" or msg_type == "error":
			icon = qta.icon("ei.error-alt", color="#dc3545")
		if msg_type == "success":
			icon = qta.icon("fa.check-circle", color="#28a745")

		self.icon.setIcon(icon)
		self.icon.setIconSize(QSize(50, 50))
		self.show()
