from PyQt5.QtCore import pyqtRemoveInputHook
from qt_core import *
#from app.gui.content import *

from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from .widgets.animated_check.animated_check import AnimatedCheck
import re
from webcolors import hex_to_name


class MenuBuilder(QWidget):
	_init = True
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
		super(self.__class__, self).__init__(parent)
		
		self.ui = ui
		self.parent = parent

		self.apps_path = apps_path
		self.app_name = app_name

		#self.ui_settings = Settings('ui')
		self.ui_settings = None
		self.theme_settings = None
		self.menu_settings = None
		self.initial = False
	
	def setup(self):
		
		self.parent.menuTree.setFocusPolicy(Qt.NoFocus)
		sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.parent.menuTree.sizePolicy().hasHeightForWidth())
		self.parent.menuTree.setSizePolicy(sizePolicy)
		self.parent.menuTree.setHeaderLabels(['Name', 'Object', 'Children', 'icon'])
		#self.parent.menuTree.setHeaderHidden(True);
		#self.parent.menuTree.setAnimated(True)
		#self.parent.menuTree.setColumnHidden(2, True)
		
		#self.parent.menuTree.setColumnWidth(0,200)
		#self.parent.menuTree.setColumnWidth(1,5)
		
		#self.parent.menuTree.header().setDefaultSectionSize(0)
	  	#self.tree.expandAll()
		
		#self.parent.menuTree.setCursor(Qt.PointingHandCursor)
		
		#self.build_menu(data=self.menu_data, parent=self.parent.menuTree)
		#self.parent.menuTree.itemClicked.connect(self.onItemClicked)
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		self.ui_settings = Settings('ui', apps_path=self.apps_path, app_name=self.app_name)
		self.menu_settings = Settings('menu', apps_path=self.apps_path, app_name=self.app_name)
		
		self.build_menu(data=self.menu_settings.items, parent=self.parent.menuTree)

	def build_menu(self, data=None, parent=None):
		
		#icon_color = self.theme_settings['theme']['panel1']['icons']
		icon_color = "white"
		for menu_item in data:
			tree_item = QTreeWidgetItem(parent)
			tree_item.setFlags(tree_item.flags() | Qt.ItemIsEditable)
			tree_item.setText(0, menu_item['name'])
			#tree_item.setText(3, menu_item['icon'])
			
			if type(menu_item['icon']) == dict:
				#icon = qta.icon(menu_item['icon']['collapsed'], color=icon_color)
				#tree_item.setIcon(0, icon)
				#tree_item.setText(3, menu_item['icon']['collapsed'])
				#tree_item.setText(4, menu_item['icon']['expanded'])
				tree_item.setText(3, f"{menu_item['icon']['collapsed']}|{menu_item['icon']['expanded']}")
			else:
				#icon = qta.icon(menu_item['icon'], color=icon_color)
				#tree_item.setIcon(0, icon)
				tree_item.setText(3, menu_item['icon'])
				
			if "children" in menu_item:
				#icon = qta.icon("fa.chevron-right", color=icon_color)
				#tree_item.setIcon(1, icon)
				#tree_item.setText(2, "Y")
				tree_item.setCheckState(2, Qt.Checked)
				self.build_menu(data=menu_item['children'], parent=tree_item)
			else:
				tree_item.setText(1, menu_item['widget'])
				#tree_item.setText(2, "N")
				tree_item.setCheckState(2, Qt.Unchecked)
				#tree_item.setText(2, menu_item['widget'])
				#if "start" in menu_item:
				#	self.onItemClicked(tree_item, 0)

	def setup2(self):
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		self.ui_settings = Settings('ui', apps_path=self.apps_path, app_name=self.app_name)
		self.menu_settings = Settings('menu', apps_path=self.apps_path, app_name=self.app_name)
		#print(self.menu_settings.items)
		
		#self.parent.menuItem_1.deleteLater()
		#self.parent.menuItem_2.deleteLater()
		#self.parent.menuLayout.setParent(None)
		#self.parent.menuLayout = QFormLayout(self.parent.menuWidget)
		#self.parent.menuLayout.setObjectName(u"menuLayout")
		#for i in reversed(range(self.parent.menuLayout.count())): 
		#	self.parent.menuLayout.itemAt(i).widget().deleteLater()
		#	print("delete")
		#	
		for item in self.parent.Menu.findChildren(QWidget):
			if "menuItem_" in item.objectName():
				print("delete", item.objectName())
				item.deleteLater()

		i = 0
		for item in self.menu_settings.items:
			print(item['name'])
			self.addMenuItem(i, item['name'], item['icon'])
			i += 1

	def addMenuItem(self, i, name, icon):
		menuItem = QWidget(self.parent.Menu)
		
		menuItem.setObjectName(u"menuItem_{i}")
		menuItem.setMaximumSize(QSize(16777215, 122))
		gridLayout = QGridLayout(menuItem)
		gridLayout.setObjectName(u"gridLayout")
		# Name
		label_name = QLabel(menuItem)
		label_name.setText("Name")
		label_name.setObjectName(u"label_name")
		gridLayout.addWidget(label_name, 0, 0, 1, 1)
		itemName = QLineEdit(menuItem)
		itemName.setObjectName(f"menu_name")
		itemName.setText(f"{name}")
		gridLayout.addWidget(itemName, 0, 1, 1, 2)
		# Icon
		label_icon = QLabel(menuItem)
		label_icon.setText("Icon")
		label_icon.setObjectName(u"label_icon")
		gridLayout.addWidget(label_icon, 1, 0, 1, 1)
		itemIcon = QLineEdit(menuItem)
		itemIcon.setObjectName(u"menu_icon")
		itemIcon.setText(f"{icon}")
		gridLayout.addWidget(itemIcon, 1, 1, 1, 2)
		#Widget
		label_widget = QLabel(menuItem)
		label_widget.setText("Object")
		label_widget.setObjectName(u"label_widget")
		gridLayout.addWidget(label_widget, 2, 0, 1, 1)
		itemWidget = QLineEdit(menuItem)
		itemWidget.setObjectName(u"menu_object")
		itemWidget.setText(f"{name}")
		gridLayout.addWidget(itemWidget, 2, 1, 1, 2)
		# Children
		label_children = QLabel(menuItem)
		label_children.setObjectName(u"label_children")
		label_children.setText(f"Children")
		gridLayout.addWidget(label_children, 3, 0, 1, 1)
		enableChildren = AnimatedCheck(menuItem)
		enableChildren.setObjectName(u"menu_enableChildren")
		gridLayout.addWidget(enableChildren, 3, 1, 1, 1)
		addChild = QPushButton(menuItem)
		addChild.setObjectName(u"menu_addChild")
		addChild.setText(u"addChild")
		gridLayout.addWidget(addChild, 3, 2, 1, 1)

		
		self.parent.menuLayout.addWidget(menuItem, 0, Qt.AlignTop)
		#self.parent.menuLayout.addWidget(menuItem, 0, Qt.AlignTop)
		
			
		
		
	