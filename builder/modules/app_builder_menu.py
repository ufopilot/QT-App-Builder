import json
from qt_core import *
#from app.gui.content import *

from .app_builder_settings import Settings
from .app_builder_functions import UIFunctions
from ..widgets.animated_check.animated_check import AnimatedCheck



class MenuBuilder(QWidget):
	_init = True
	def __init__(self, parent=None, ui=None, apps_path=None, app_name=None):
		super(self.__class__, self).__init__(parent)
		#############################################################
		# Initial
		#############################################################
		self.ui = ui
		self.parent = parent
		self.apps_path = apps_path
		self.app_name = app_name
		self.ui_settings = None
		self.builder_settings = None
		self.theme_settings = None
		self.menu_settings = None
		self.initial = False
	
	def setup(self, init=True):
		
		#self.parent.builder_left.menuTree.setFocusPolicy(Qt.NoFocus)
		sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.parent.builder_left.menuTree.sizePolicy().hasHeightForWidth())
		self.parent.builder_left.menuTree.setSizePolicy(sizePolicy)
		self.parent.builder_left.menuTree.setHeaderLabels(['Name', 'Object', 'Children', 'Icon', '', 'Start'])
		#self.parent.builder_left.menuTree.setHeaderHidden(True); 
		#self.parent.builder_left.menuTree.setAnimated(True)
		#self.parent.builder_left.menuTree.setColumnHidden(2, True)
		
		self.parent.builder_left.menuTree.setColumnWidth(0,150)
		self.parent.builder_left.menuTree.setColumnWidth(1,100)
		self.parent.builder_left.menuTree.setColumnWidth(2,60)
		self.parent.builder_left.menuTree.setColumnWidth(3,100)
		self.parent.builder_left.menuTree.setColumnWidth(4,40)
		self.parent.builder_left.menuTree.setColumnWidth(5,40)

		self.parent.builder_left.menuTree.expandAll()
		self.parent.builder_left.menuTree.setSelectionMode(QAbstractItemView.MultiSelection)
		self.parent.builder_left.menuTree.setDragEnabled(True)
		self.parent.builder_left.menuTree.viewport().setAcceptDrops(True)
		self.parent.builder_left.menuTree.setDropIndicatorShown(True)

		# itemchanged
		self.parent.builder_left.menuTree.itemChanged[QTreeWidgetItem, int].connect(self.get_item)
		self.root = self.parent.builder_left.menuTree.invisibleRootItem()
		# Connect the contextmenu
		self.parent.builder_left.menuTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.parent.builder_left.menuTree.customContextMenuRequested.connect(self.menuContextTree)

	def refresh(self, init=True):
		self.theme_settings = Settings('theme', apps_path=self.apps_path, app_name=self.app_name)
		self.ui_settings = Settings('ui', apps_path=self.apps_path, app_name=self.app_name)
		self.menu_settings = Settings('menu', apps_path=self.apps_path, app_name=self.app_name)
		self.parent.builder_left.menuTree.clear() 
		self.drawMenu(self.menu_settings.items)
		self.parent.builder_left.menuTree.expandAll()
		
	def get_item(self, item, column):
		if  column == 2:
			if item.checkState(column) == Qt.Checked:
				item.setText(1, "")
				item.setData(5, Qt.CheckStateRole, QVariant())
				item.addChild(self.new_item("Menu Item", {"icon": "fa.circle-o", "widget":"ClassName"}))
				self.parent.builder_left.menuTree.expandAll()
			else:
				#(item.parent() or self.root).removeChild(item)
				for i in reversed(range(item.childCount())):
					item.removeChild(item.child(i))
				item.setText(1, "ClassName")
				item.setCheckState(5, Qt.Unchecked)
		if column == 3:
			try:
				icon = qta.icon(item.text(3), color="white")
				item.setIcon(4, icon)
			except:
				item.setIcon(4, QIcon())
		
		if column == 5:
			if item.checkState(column) == Qt.Checked: 
				self.uncheckAll(self.root, item, 5)
				#item.setCheckState(5, Qt.Checked)
			else:
				return

	def new_item(self, name, opt):
		item = QTreeWidgetItem()
		item.setText(0, name)
		if "widget" in opt:
			item.setText(1, opt['widget'])
		if "children" in opt:
			item.setCheckState(2, Qt.Checked)
		else:
			item.setCheckState(2, Qt.Unchecked)
			item.setCheckState(5, Qt.Unchecked)

		if "icon" in opt:
			item.setText(3, opt['icon'])
			try:
				icon = qta.icon(opt['icon'], color="white")
				item.setIcon(4, icon)
			except:
				item.setIcon(4, QIcon())

		if "start" in opt and opt['start']:
			item.setCheckState(5, Qt.Checked)
			
		item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		return item

	def drawMenu(self, dat):
		for el in dat:
			self.add(self.parent.builder_left.menuTree, el)

	def add(self, p, ch):
		k=ch['name']
		v=ch
		#for k, v in ch.items():
		item = self.new_item(k,v)
		if isinstance(p, QTreeWidget):
			p.addTopLevelItem(item)
		else:
			p.addChild(item)
		if "children" in v:
			for el in v['children']:
				self.add(item, el)	
	
	def menuContextTree(self, point):
		# Infos about the node selected.
		index = self.parent.builder_left.menuTree.indexAt(point)

		if not index.isValid():
			return

		item = self.parent.builder_left.menuTree.itemAt(point)
		name = item.text(0)  # The text of the node.

		# We build the menu.
		menu = QMenu()
		icon_color = "black"
		icon = qta.icon("mdi6.table-row-plus-after", color=icon_color)
		appendItem = menu.addAction(icon, f"Append Menu Item")
		
		icon = qta.icon("mdi6.table-row-plus-before", color=icon_color)
		prependItem = menu.addAction(icon, f"Prepend Menu Item")
		
		icon = qta.icon("fa.level-up", color=icon_color)
		moveUp = menu.addAction(icon, f"Move up")
		
		icon = qta.icon("mdi.chevron-triple-up", color=icon_color)
		moveToTop = menu.addAction(icon, f"Move to top")

		icon = qta.icon("fa.level-down", color=icon_color)
		moveDown = menu.addAction(icon, f"Move down")
		
		icon = qta.icon("mdi.chevron-triple-down", color=icon_color)
		moveToBottom = menu.addAction(icon, f"Move to bottom")
		
		menu.addSeparator()
		icon = qta.icon("mdi.close", color=icon_color)
		delete = menu.addAction(icon, f"Remove {name}")

		action = menu.exec_(self.parent.builder_left.menuTree.mapToGlobal(point))

		if action == delete:
			itemParent = item.parent() or self.root
			itemParent.removeChild(item)
		elif action == prependItem:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			c = itemParent.childCount()
			itemParent.addChild(self.new_item("Menu Item", {"icon": "fa.circle-o", "widget":"ClassName"}))
			child = itemParent.takeChild(c);
			itemParent.insertChild(index, child);
			self.parent.builder_left.menuTree.expandAll()
		elif action == appendItem:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			c = itemParent.childCount()
			itemParent.addChild(self.new_item("Menu Item", {"icon": "fa.circle-o", "widget":"ClassName"}))
			child = itemParent.takeChild(c);
			itemParent.insertChild(index+1, child);
			self.parent.builder_left.menuTree.expandAll()
			
		elif action == moveUp:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			if index == 0:
				return
			child = itemParent.takeChild(index)
			itemParent.insertChild(index-1, child)
			self.parent.builder_left.menuTree.expandAll()
		elif action == moveDown:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			if itemParent.childCount() == index+1:
				return
			child = itemParent.takeChild(index);
			itemParent.insertChild(index+1, child);
			self.parent.builder_left.menuTree.expandAll()
		elif action == moveToBottom:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			bottomIndex = itemParent.childCount()
			child = itemParent.takeChild(index);
			itemParent.insertChild(bottomIndex-1, child);
			self.parent.builder_left.menuTree.expandAll()
		elif action == moveToTop:
			itemParent = item.parent() or self.root
			index = itemParent.indexOfChild(item)
			child = itemParent.takeChild(index);
			itemParent.insertChild(0, child);
			self.parent.builder_left.menuTree.expandAll()

	def tree_to_dict(self, parent):
		childCount = parent.childCount()
		if not childCount:
			return 
		content = []
		for row in range(childCount):
			child = parent.child(row)
			li = {}
			 
			li["name"] = child.text(0)
			li["widget"] = child.text(1)
			li["icon"] = child.text(3)
			if child.checkState(5) == Qt.Checked: 
				li['start'] = True 
			if child.checkState(2) != 0:
				li["children"] = self.tree_to_dict(child)
			content.append(li)
		return content
		
	def menuToJson(self):
		self.parent.builder_left.menuTree.expandAll()
		dictionary = []

		for x in range(self.root.childCount()):
			li = {}
			#self.root.takeChild(x)
			li['name'] = self.root.child(x).text(0)
			li['widget'] = self.root.child(x).text(1)
			li['icon'] = self.root.child(x).text(3)
			if self.root.child(x).checkState(5) == Qt.Checked: 
				li['start'] = True 
			if self.root.child(x).checkState(2) != 0:
				li['children'] = self.tree_to_dict(self.root.child(x))
			dictionary.append(li)
		
		self.menu_settings.items = dictionary
		self.menu_settings.serialize()
	
	def uncheckAll(self, parent, item, col):
		childCount = parent.childCount()
		if not childCount:
			return 
		for row in range(childCount):
			child = parent.child(row)
			if child != item:
				if child.checkState(col) == Qt.Checked: 
					child.setCheckState(col, Qt.Unchecked)
			self.uncheckAll(child, item, col)
			