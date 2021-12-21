import webbrowser
import requests
from functools import partial
from bs4 import BeautifulSoup
from qt_core import *


from builder.template_app.gui.content.football.ui_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("gui/content/football/tabs/kooora365.ui"))

class Kooora365Tab(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.url = "https://kooora365.com"
		self.refreshbutton.clicked.connect(partial(football_game_scrapper1, self))
		clear_game_layout(self)

	def mousePressEvent(self, event):
		pass
