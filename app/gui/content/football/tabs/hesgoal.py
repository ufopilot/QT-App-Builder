import os
import webbrowser
import pyperclip
import requests
from bs4 import BeautifulSoup
from qt_core import *
from app.gui.content.football.ui_functions import *

Gen_Class, Base_Class = loadUiType(resource_path("gui/content/football/tabs/hesgoal.ui"))


class HesgoalTab(Base_Class, Gen_Class):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.url = "http://www.hesgoal.com/"
		self.refreshbutton.clicked.connect(self.scrapper)

		#self.gamestable.doubleClicked.connect(self.OpenLink)
		#self.header = self.gamestable.horizontalHeader()

		#self.scrapper()
		self.gamestable.verticalHeader().setVisible(False)
		self.gamestable.setAlternatingRowColors(True)

	def draw_table(self):
		self.model = QtGui.QStandardItemModel(5, 3)
		self.model.setHorizontalHeaderLabels(['Title', 'Description', 'Link'])
		self.gamestable.doubleClicked.connect(self.OpenLink)
		self.gamestable.installEventFilter(self)

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.ContextMenu and source is self.gamestable:
			cmenu = QtWidgets.QMenu()
			openAction = cmenu.addAction("Open Stream")
			copyAction = cmenu.addAction("Copy Link")
			action = cmenu.exec_(self.mapToGlobal(event.pos()))
			if action == openAction:
				index = (self.gamestable.selectionModel().currentIndex())
				link = index.sibling(index.row(), 2).data()
				self.show_stream(link)

			if action == copyAction:
				index = (self.gamestable.selectionModel().currentIndex())
				link = index.sibling(index.row(), 2).data()
				pyperclip.copy(link)

			#if cmenu.exec_(event.globalPos()):
			#	#item = source.itemAt(event.pos())
			#	index = (self.gamestable.selectionModel().currentIndex())
			#	Link = index.sibling(index.row(), 2).data()
			#	print(Link)
			return True
		return super().eventFilter(source, event)

	def set_tabele_filter(self):
		# filter proxy model
		self.filter_proxy_model = QtCore.QSortFilterProxyModel()
		self.filter_proxy_model.setSourceModel(self.model)
		self.filter_proxy_model.setFilterKeyColumn(2)  # third column

		self.hesgoaledit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
		self.gamestable.setModel(self.filter_proxy_model)

	def set_table_header(self):
		self.header = self.gamestable.horizontalHeader()
		self.header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		self.header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		self.header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

	def scrapper(self):
		# cleat LineEdit Filter
		self.hesgoaledit.clear()
		# clear QTableView
		self.gamestable.setModel(None)

		self.draw_table()
		self.set_tabele_filter()
		self.set_table_header()

		response = requests.get(self.url)
		html = BeautifulSoup(response.text, 'html.parser')
		games_html = html.find_all('div', class_="file file_index")
		#games = list()
		#self.gamestable.setRowCount(0);
		row = 0
		for game in games_html:
			game_infos = game.find_all('p')
			title = game_infos[0].a.text
			link = game_infos[0].a.get('href')
			desc = game_infos[1].text
			#title = QtGui.QIcon("activity.svg")
			self.model.setItem(row, 0, QtGui.QStandardItem(title))
			self.model.setItem(row, 1, QtGui.QStandardItem(desc))
			self.model.setItem(row, 2, QtGui.QStandardItem(link))
			row += 1

	def OpenLink(self):
		# read third-cell value.
		index = (self.gamestable.selectionModel().currentIndex())
		#index.row()
		#index.column()
		value = index.sibling(index.row(), 2).data()
		# open link
		self.show_stream(value)

	def show_stream(self, value):
		response = requests.get(value)
		html = BeautifulSoup(response.text, 'html.parser')
		frames_html = html.find_all('iframe')
		for frame in frames_html:
			link = frame.get('src')
			if link.startswith('//'):
				link = 'http:'+link
			webbrowser.open(link)
			break

# retranslateUi


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	w = HesgoalTab()
	w.show()
	sys.exit(app.exec_())
