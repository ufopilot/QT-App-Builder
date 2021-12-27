from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from qt_core import *
import shutil
		
	
Gen_Class, Base_Class = loadUiType(UIFunctions().resource_path("./builder/uis/app_builder_center.ui"))

class AppBuilderCenter(Base_Class, Gen_Class):
	def __init__(self, parent=None, ui=None):
		super(self.__class__, self).__init__(parent)
		self.ui = ui
		self.parent = parent

		settings = Settings('builder')
		self.builder_settings = settings

		self.setupUi(self)
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.progressBar.setValue(0)
		self.progressBar.hide()
		screen = QApplication.primaryScreen()
		size = screen.size()
		self.resize(size.width()-self.builder_settings.items['left_width']-self.builder_settings.items['right_width'], size.height()-self.builder_settings.items['bottom_height'])
		self.move(self.builder_settings.items['left_width']-1, 0)	
	
		if self.builder_settings.items['apps_path'].strip() == "":
			self.parent.setAppsPath()

		self.searchApps()
	
	def removeApp(self):
		builder_settings = Settings("builder")
		apps_path = builder_settings.items['apps_path']
		if apps_path == "":
			return 
		el = self.sender()
		app_name = el.objectName().replace("remove_", "")	
		
		
		try:
			print(os.path.join(apps_path, app_name))
			if os.path.exists(os.path.join(apps_path, app_name)):
				shutil.rmtree(os.path.join(apps_path, app_name))
		except:
			pass	
		self.searchApps()

	def searchApps(self, apps_path=None):
		if apps_path == None:
			apps_path = self.builder_settings.items['apps_path']
			self.apps_path.setText(f"Path: {apps_path}")
	
		if not os.path.isdir(apps_path):
			return
		
		for button in self.myApps.findChildren(QPushButton):
			button.deleteLater()

		icon_color = self.builder_settings.items['icons_color']
		remove_icon = qta.icon("fa.trash", color=icon_color)

		
		i = 0; j = 0

		folders = os.listdir(apps_path)
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

			icon = QPushButton(frame)
			icon.setObjectName(f"remove_{app_name}")
			icon.setFlat(True)
			icon.setIconSize(QSize(30, 30))
			
			if app_name == "template_app":
				btn.setText(f"Template App")
			else:
				icon.setProperty("type", "btn_app_mini")
				icon.setCursor(QCursor(Qt.PointingHandCursor))
				icon.setToolTip(f"Delete App: {app_name}")
				icon.setIcon(remove_icon)
				icon.clicked.connect(self.removeApp)

			icon.setStyleSheet("border: none;")
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
		settings = Settings('builder')
		settings.items['selected_app'] = name
		settings.serialize()
		self.selected_app.setText(f"App: {name}")
	
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderCenter()
	w.show()
	sys.exit(app.exec())
