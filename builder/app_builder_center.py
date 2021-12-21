#rom xml.etree.ElementTree import Element
from . settings import Settings
from . ui_functions import UIFunctions
from qt_core import *

	
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
		self.resize(size.width()-464, size.height()-200)
		self.move(399, 0)	
	
		if self.builder_settings.items['apps_path'].strip() == "":
			self.setAppsPath()

		self.searchApps()
	
	def setAppsPath(self):
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.Directory)  # ExistingFile
		dialog.setOption(QFileDialog.DontUseNativeDialog, True)
		dialog.setOption(QFileDialog.ShowDirsOnly, True)
		nMode = dialog.exec_()
		names = dialog.selectedFiles()
		self.builder_settings.items['apps_path'] = os.path.abspath(names[0])
		self.builder_settings.serialize()
		
		
	def searchApps(self):
		apps_path = self.builder_settings.items['apps_path']

		

		if not os.path.isdir(apps_path):
			return
		
		for button in self.myApps.findChildren(QPushButton):
			button.deleteLater()

		btn = QPushButton(self.myApps)
		btn.setObjectName(f"template_app")
		btn.setText(f"Template APP")
		btn.setCursor(QCursor(Qt.PointingHandCursor))
		btn.setStyleSheet("font-size: 20px")
		btn.setMinimumSize(QSize(0, 170))
		btn.clicked.connect(lambda: self.loadApp("template_app"))
		self.myAppsLayout.addWidget(btn, 0, 0, 1, 1)
		
		i = 0; j = 1
		for app_name in os.listdir(apps_path):
			if not os.path.isdir(os.path.join(apps_path, app_name)):
				continue
			btn = QPushButton(self.myApps)
			btn.setObjectName(f"{app_name}")
			btn.setText(f"{app_name}")
			btn.setCursor(QCursor(Qt.PointingHandCursor))
			btn.setStyleSheet("font-size: 20px")
			btn.setMinimumSize(QSize(0, 170))
			btn.clicked.connect(lambda: self.loadApp(app_name))
			self.myAppsLayout.addWidget(btn, i, j, 1, 1)

			j += 1
			if j == 4: i += 1; j = 0
	
	def loadApp(self, app_name):
		self.progressBar.show()
		QTimer.singleShot(100, lambda: self.parent.loadApp(app_name))
		
		

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	app.setStyle("fusion")
	w = AppBuilderCenter()
	w.show()
	sys.exit(app.exec())
