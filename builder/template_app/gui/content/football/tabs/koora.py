import webbrowser
from functools import partial
import requests
from bs4 import BeautifulSoup
from qt_core import *

from app.gui.content.football.ui_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("gui/content/football/tabs/koora.ui"))


class KooraTab(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.url = "https://kooora4lives.com:2096/m2/"
		clear_game_layout(self)
		self.refreshbutton.clicked.connect(partial(football_game_scrapper2, self))
		