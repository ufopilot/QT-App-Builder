import os
import webbrowser
import cloudscraper
from functools import partial
import requests

from bs4 import BeautifulSoup
from qt_core import *
from app.gui.content.football.ui_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("gui/content/football/tabs/livehd.ui"))

class LivehdTab(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.url = "https://livehd7.live:2096/"
		self.refreshbutton.clicked.connect(self.scrapper)
		clear_game_layout(self)

	def scrapper(self):
		self.progressBar.setValue(0)
		clear_game_layout(self)

		try:
			scraper = cloudscraper.create_scraper()
			response = scraper.get(self.url).text
			html = BeautifulSoup(response, 'html.parser')
			games_container = html.find("div", {"id": "today"})
			games_html = games_container.find_all('a', class_="alba_sports_events_link")
			counter = len(games_html)
		except:
			return

		step = 100/counter
		pgb = 0

		row = 0
		result = "0-0"

		self.links = list()

		for game in games_html:
			try:
				team1_html = game.find('div', {'class': 'team-first'})
				team1 = team1_html.text
				flag1 = team1_html.find('img')
				flag1 = flag1.get('src')
				team2_html = game.find('div', {'class': 'team-second'})
				team2 = team2_html.text
				flag2 = team2_html.find('img')
				flag2 = flag2.get('src')
				time = game.find('div', {'class': 'matchTime'}).text

				link = game.get('href')
				self.links.append(link)
				channel = game.find('span', {'class': 'tv'}).text
				speaker = game.find('span', {'class': 'mic'}).text
				description = game.find('span', {'class': 'cup'}).text

			except:
				continue


			add_game(self, team1, team2, time, speaker, channel, description, link, flag1, flag2, row, result)
			pgb = pgb + step
			self.progressBar.setValue(pgb)

			row += 1
		self.progressBar.setValue(0)
