import posixpath
from qt_core import *
from . ui_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("gui/content/football/main.ui"))

class FootballWidget(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.tabscontent.setCurrentIndex(0)
		##########################################################################################
		# Read Settings
		##########################################################################################
		self.config = read_config()
		change_tabs_direction(self, self.config['tabs_position'])
	
	
if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	w = FootballWidget()
	w.show()
	sys.exit(app.exec_())


# https://7asry.yalla-shoot.today/
# https://extra.yalla-shoot-7sry.com/
# https://fel3arda.xyz
# https://hd.live-yalla-shoot.com/
# https://kol7sry.news
# kooora365 	https://kooora365.com
# koraonline 	https://kora-online.tv
# https://kora.yalla-shoot.plus/
# https://today.yalla-shoot-7asry.com/
# https://yalla-shoot.com
# https://yalla-shoot.us
# https://yallashoot-news.com

# https://online.yalla-shoot-new.com/
# https://7sry.yalla-shoot-arabia.com/
# https://hd.yalla-shoot.io/
# https://plus.yalla-shoot-kora.com/
# https://www.yalla-shoot7sry.com/
# https://www.as-goal.com:2053/m/
# https://king-shoot.tv:2096/ar/
# https://livehd7.vip/yalla-shooot-today/
# https://goll.koooora-live.com/