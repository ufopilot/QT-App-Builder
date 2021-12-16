import os
import sys
import json
import webbrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from bs4 import BeautifulSoup
import requests 


def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

def read_config():
	with open(resource_path('gui/settings/ui_settings.json')) as f:
		return json.load(f)

def clear_game_layout(self):
	while self.tabcontentLayout.count():
		child = self.tabcontentLayout.takeAt(0)
		if child.widget():
			child.widget().deleteLater()

def open_game(self, idx):
    try:
        webbrowser.open(self.links[idx])
    except:
        pass

def change_tabs_direction(self, position):
		position = position.lower()
		if position == "north" or position == "top":
			self.tabscontent.setTabPosition(QtWidgets.QTabWidget.North)		
		if position == "east" or position == "right":
			self.tabscontent.setTabPosition(QtWidgets.QTabWidget.East)		
		if position == "west" or position == "left":
			self.tabscontent.setTabPosition(QtWidgets.QTabWidget.West)
		if position == "south" or position == "bottom":
			self.tabscontent.setTabPosition(QtWidgets.QTabWidget.South)		
				
		

def progress_dialog(self):
	self.dialog = QtWidgets.QProgressDialog()
	self.dialog.setFixedSize(300, 50)
	self.dialog.setAutoFillBackground(True)
	self.dialog.setWindowModality(QtCore.Qt.WindowModal)
	self.dialog.setWindowTitle('Please wait')
	self.dialog.setLabelText("Loading ...")
	self.dialog.setSizeGripEnabled(False)
	self.dialog.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
	self.dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
	self.dialog.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
	self.dialog.setModal(True)
	self.dialog.setCancelButton(None)
	self.dialog.setRange(0, 0)
	self.dialog.setMinimumDuration(0)
	self.dialog.setAutoClose(False)
	return self.dialog


def football_game_scrapper1(self):
    self.progressBar.setValue(0)
    clear_game_layout(self)
    response = requests.get(self.url)
    response.encoding = "utf-8"
    html = BeautifulSoup(response.text, 'html.parser')
    games_container = html.find("div", {"id": "today"})
    games_html = games_container.find_all('a', class_="alba_sports_events_link")
    counter = len(games_html)
    if counter == 0:
    	return
    step = 100 / counter
    pgb = 0
    row = 0
    self.links = list()
    result = "0-0"
    for game in games_html:
        try:
            team1_html = game.find('div', {'class': 'team-first'})
            team1 = team1_html.text
            flag1 = team1_html.find('img').get('src')
            team2_html = game.find('div', {'class': 'team-second'})
            team2 = team2_html.text
            flag2 = team2_html.find('img').get('src')
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


def football_game_scrapper2(self):
    self.progressBar.setValue(0)
    clear_game_layout(self)
    response = requests.get(self.url)
    response.encoding = "utf-8"
    html = BeautifulSoup(response.text, 'html.parser')
    games_html = html.find_all('div', class_="match-container")
    counter = len(games_html)
    step = 100 / counter
    pgb = 0
    row = 0
    self.links = list()
    for game in games_html:
        try:
            team1_html = game.find('div', class_="left-team")
            team1 = team1_html.find('div', class_="team-name").text
            flag1 = team1_html.find('img').get('data-src')
            #flag_data = team1_html.find('img').get('src')
            team2_html = game.find('div', class_="right-team")
            team2 = team2_html.find('div', class_="team-name").text
            flag2 = team2_html.find('img').get('data-src')
            link = game.a.get('href')
            self.links.append(link)
            channel = game.find_all('li')[0].text
            speaker = game.find_all('li')[1].text
            description = game.find_all('li')[2].text
            status = game.find('div', class_="date").text

            if status == "لم تبدأ بعد" or status == "بعد قليل":
                result = status
                time = game.find('div', id="match-time").text
            else:
                if status == "إنتهت المباراة":
                    result = game.find('div', id="result").text
                    time = status
                else:
                    time = game.find('div', id="match-time").text
                    result = "0-0"


				#if time == None:
				#	time = game.find('div', class_="date").text

			# date end / date comming
				# if date comming --> match-time
				# else result
				# status
        except:
            continue
       
        add_game(self, team1, team2, time, speaker, channel, description, link, flag1, flag2, row, result)
        pgb = pgb + step
        self.progressBar.setValue(pgb)
        row += 1
    self.progressBar.setValue(0)

def add_game(self, team1, team2, time, speaker, channel, description, link, flag1, flag2, row, result):
	self.row = QtWidgets.QWidget(self.scrollAreaWidgetContents)
	self.row.setObjectName(u"row")
	self.row.setMinimumSize(QtCore.QSize(0, 150))
	self.row.setMaximumSize(QtCore.QSize(16777215, 16777215))
	self.row.setLayoutDirection(QtCore.Qt.RightToLeft)
	self.row.setStyleSheet(u"")
	self.gridLayout = QtWidgets.QGridLayout(self.row)
	self.gridLayout.setObjectName(u"gridLayout")
	self.time = QtWidgets.QLabel(self.row)
	self.time.setObjectName(u"time")
	self.time.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.time, 2, 1, 1, 1)
	self.team2_text = QtWidgets.QLabel(self.row)
	self.team2_text.setObjectName(u"team2_text")
	self.team2_text.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.team2_text, 2, 2, 1, 1)
	self.speaker = QtWidgets.QLabel(self.row)
	self.speaker.setObjectName(u"speaker")
	self.speaker.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.speaker, 6, 1, 1, 1)
	self.team1_text = QtWidgets.QLabel(self.row)
	self.team1_text.setObjectName(u"team1_text")
	self.team1_text.setLayoutDirection(QtCore.Qt.RightToLeft)
	self.team1_text.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.team1_text, 2, 0, 1, 1)
	self.tv = QtWidgets.QLabel(self.row)
	self.tv.setObjectName(u"tv")
	self.tv.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.tv, 6, 2, 1, 1)
	self.genre = QtWidgets.QLabel(self.row)
	self.genre.setObjectName(u"genre")
	self.genre.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.genre, 6, 0, 1, 1)
	#self.line = QtWidgets.QFrame(self.row)
	#self.line.setObjectName(u"line")
	#self.line.setFrameShape(QtWidgets.QFrame.HLine)
	#self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
	#
	#self.gridLayout.addWidget(self.line, 5, 0, 1, 3)
	self.result = QtWidgets.QLabel(self.row)
	self.result.setObjectName(u"result")
	self.result.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.result, 1, 1, 1, 1)
	self.team1_flag = QtWidgets.QLabel(self.row)
	self.team1_flag.setObjectName(u"team1_flag")
	self.team1_flag.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.team1_flag, 1, 2, 1, 1)
	self.team2_flag = QtWidgets.QLabel(self.row)
	self.team2_flag.setObjectName(u"team2_flag")
	self.team2_flag.setAlignment(QtCore.Qt.AlignCenter)
	self.gridLayout.addWidget(self.team2_flag, 1, 0, 1, 1)
	exec(f"self.button_{row} = QtWidgets.QPushButton(self.row)")
	exec(f'self.button_{row}.setObjectName(u"button_{row}")')
	exec(f'self.button_{row}.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))')
	exec(f"self.button_{row}.clicked.connect(partial(open_game, self,  {row}))")
	exec(f"self.gridLayout.addWidget(self.button_{row}, 4, 0, 1, 3)")
	self.tabcontentLayout.addWidget(self.row)
	# add uitranslation
	self.time.setText(QtCore.QCoreApplication.translate("Tab", f"{time}", None))
	self.team2_text.setText(QtCore.QCoreApplication.translate("Tab", f"{team1}", None))
	self.speaker.setText(QtCore.QCoreApplication.translate("Tab", f"{speaker}", None))
	self.team1_text.setText(QtCore.QCoreApplication.translate("Tab", f"{team2}", None))
	self.tv.setText(QtCore.QCoreApplication.translate("Tab", f"{channel}", None))
	self.genre.setText(QtCore.QCoreApplication.translate("Tab",f"{description}",None))
	self.result.setText(QtCore.QCoreApplication.translate("Tab", f"{result}", None))
	exec(f'self.button_{row}.setText(QtCore.QCoreApplication.translate("Tab", u"Open", None))')
	try:
		image = QtGui.QImage()
		image.loadFromData(requests.get(flag1).content)
		self.team1_flag.setPixmap(QtGui.QPixmap(image).scaledToWidth(50))
	except:
		pass
	try:
		image = QtGui.QImage()
		image.loadFromData(requests.get(flag2).content)
		self.team2_flag.setPixmap(QtGui.QPixmap(image).scaledToWidth(50))
	except:
		pass

#class Loader(QtCore.QObject):
#	def __init__(self, parent=None):
#		super().__init__(parent)
#		manager = QtNetwork.QNetworkAccessManager()
#		manager.finished.connect(self.onFinished)
#		self._manager = manager
#
#	def start(self, url, label):
#		self._url = url
#		self._label = label
#		self.request()
#
#	def request(self):
#		manager = self._manager
#		req = QtNetwork.QNetworkRequest(QtCore.QUrl(self._url))
#		res = manager.get(req)
#
#	def onFinished(self, reply):
#		data = reply.readAll()
#		pixmap = QtGui.QPixmap()
#		pixmap.loadFromData(data)
#		self._label.setPixmap(pixmap)
#		QtCore.QTimer.singleShot(100, self.request)
#