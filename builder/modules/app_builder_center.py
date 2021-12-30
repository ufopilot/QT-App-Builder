from builder.modules.app_builder_delete_app import AppBuilderDeleteApp
from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *

		
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_center.ui"))

class AppBuilderCenter(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		#############################################################
		# Flags
		#############################################################
		self.setWindowFlag(Qt.FramelessWindowHint)
		#############################################################
		# Initial
		#############################################################
		self.ui = ui
		self.parent = parent
		self.setupUi(self)
		self.builder_settings = None
		self.app = None
		self.app_name = None
		
	def setup(self):
		self.progressBar.setValue(0)
		self.progressBar.hide()
		self.appRemover = AppBuilderDeleteApp(self, self.ui)
		if self.builder_settings.items['apps_path'].strip() == "":
			self.parent.setAppsPath()
		self.searchApps()
		self.resize_window()

	def resize_window(self):
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(
			size.width()
			-
			self.builder_settings.items['left']['width']
			- 
			self.builder_settings.items['right']['width'] 
			- 
			self.builder_settings.items['center']['right'], 
			size.height()
			-
			self.builder_settings.items['bottom']['height'] 
			- 
			self.builder_settings.items['center']['bottom']
			-
			self.builder_settings.items['center']['top']
		)
		self.move(
			self.builder_settings.items['left']['width']
			+
			self.builder_settings.items['center']['left'], 
			self.builder_settings.items['center']['top'], 
		)

	def removeApp(self):
		builder_settings = Settings("builder")
		apps_path = builder_settings.items['apps_path']
		if apps_path == "":
			return 
		el = self.sender()
		app_name = el.objectName().replace("remove_", "")	
		
		self.appRemover.apps_path = apps_path
		self.appRemover.app_name = app_name
		self.appRemover.show()
		

	def searchApps(self, apps_path=None):
		if apps_path == None:
			apps_path = self.builder_settings.items['apps_path']
			self.parent.builder_center_header.apps_path.setText(f"Path: {apps_path}")
	
		if not os.path.isdir(apps_path):
			return
		
		for button in self.myApps.findChildren(QPushButton):
			button.deleteLater()

		icon_color = self.builder_settings.items['icons_color']
		remove_icon = qta.icon("fa.trash", color=icon_color)

		
		i = 0; j = 0;

		folders = os.listdir(apps_path)
		
		if len(folders) == 1:
			mx = 4
		elif len(folders) == 2:
			mx = 2
		else:
			mx = 1

		folders.insert(0,"template_app")
		for app_name in folders:
			print(app_name)
			if app_name != "template_app":
				if not os.path.isdir(os.path.join(apps_path, app_name)):
					continue
				if not os.path.isfile(os.path.join(apps_path, app_name, "app_builder.meta")):
					continue

			frame = QFrame()
			frame.setObjectName(u"frame")
			#frame.setMaximumSize(QSize(194, 16777215))
			frame.setFrameShape(QFrame.StyledPanel)
			frame.setFrameShadow(QFrame.Raised)
			layout = QVBoxLayout(frame)
			layout.setSpacing(0)
			layout.setObjectName(u"layout")
			layout.setContentsMargins(9, 9, 9, 9)
			layout.setSpacing(10)

			#layout.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

			btn = QPushButton(frame)
			btn.setObjectName(f"{app_name}")
			btn.setText(f"{app_name}")
			btn.setCursor(QCursor(Qt.PointingHandCursor))
			btn.setStyleSheet("font-size: 20px")
			btn.setMinimumSize(QSize(0, 170))
			btn.setToolTip(f"Open App: {app_name}")
			btn.clicked.connect(self.loadApp)
			
			layout.addWidget(btn)

			
			
			if app_name == "template_app":
				btn.setText(f"Template App")
				j = 3
				#layout.addWidget(icon)
				self.myAppsLayout.addWidget(frame, 0, 0, 1, 4)

			else:
				icon = QPushButton(frame)
				icon.setObjectName(f"remove_{app_name}")
				icon.setFlat(True)
				icon.setIconSize(QSize(30, 30))
				icon.setProperty("type", "btn_app_mini")
				icon.setCursor(QCursor(Qt.PointingHandCursor))
				icon.setToolTip(f"Delete App: {app_name}")
				icon.setIcon(remove_icon)
				icon.clicked.connect(self.removeApp)

			#icon.setStyleSheet("border: none;")
				layout.addWidget(icon)
				self.myAppsLayout.addWidget(frame, i, j, 1, 1)
			
			j += 1
			if j == 4: i += 1; j = 0
	
	def loadApp(self):
		btn = self.sender()
		app_name = btn.objectName()
		self.setSelectedApp(app_name)
		self.progressBar.show()
		for btn in self.myApps.findChildren(QPushButton):
			btn.setEnabled(False)
		QTimer.singleShot(100, lambda: self.parent.loadApp(app_name))

	def setSelectedApp(self, name=""):
		self.parent.builder_center_header.selected_app.setText(f"App: {name}")
	