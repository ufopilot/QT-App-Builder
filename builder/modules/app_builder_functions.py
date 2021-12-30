
from qt_core import *
import re

class UIFunctions():
	def __init__(self):
		super().__init__()
		
	def resource_path(self, relative_path):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, relative_path)
		return os.path.join(os.path.abspath("."), relative_path)
	# SET SVG ICON
	# ///////////////////////////////////////////////////////////////
	def set_svg_icon(self, icon_name, color="white"):
		app_path = os.path.abspath(os.getcwd())
		folder = self.resource_path(f"app/gui/resources/icons/{color}/")
		path = os.path.join(app_path, folder)
		icon = os.path.normpath(os.path.join(path, icon_name))
		return icon
	# SET SVG IMAGE
	# ///////////////////////////////////////////////////////////////
	def set_svg_image(self, icon_name):
		app_path = os.path.abspath(os.getcwd())
		folder = self.resource_path("app/gui/resources/images/svg")
		path = os.path.join(app_path, folder)
		icon = os.path.normpath(os.path.join(path, icon_name))
		return icon
	# SET IMAGE
	# ///////////////////////////////////////////////////////////////
	def set_image(self, image_name):
		app_path = os.path.abspath(os.getcwd())
		folder = self.resource_path("app/gui/resources/images/png/")
		path = os.path.join(app_path, folder)
		image = os.path.normpath(os.path.join(path, image_name))
		return image
	
	def QIcon_from_svg(self, icon, color='white'):
		img = QPixmap(self.set_svg_icon(icon))
		qp = QPainter(img)
		qp.setCompositionMode(QPainter.CompositionMode_SourceIn)
		qp.fillRect( img.rect(), QColor(color) )
		qp.end()
		return QIcon(img)

	def getAppTheme(self, theme_settings=None, apps_path=None, app_name=None, theme_name=None):
		regex = r"\w+\(([^\)]+)\)"
		with open(UIFunctions().resource_path(f'{apps_path}/{app_name}/gui/assets/style/base.qss'), "r", encoding='utf-8') as reader:
			base_stylesheet = reader.read().replace("{","{{").replace("}","}}")
			base_stylesheet = re.sub(regex, '{\\1}', base_stylesheet)
			if theme_name == None:
				theme = theme_settings['theme']
			else:
				theme = theme_settings['themes'][theme_name]
			formated_stylesheet = base_stylesheet.format(**theme)
			return formated_stylesheet
			