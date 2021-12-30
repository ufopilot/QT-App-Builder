
from qt_core import *
from builder.template_app.gui.content import *
from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions

class Panel1(QWidget):
	_lastcontent = None
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		settings = Settings("theme")
		self.theme_settings = settings.items
		menu_settings = Settings('menu')
		self.menu_data = menu_settings.items
		self.setupMenu()
		
		if not self.settings['panel1']['visible']:
			self.ui.panel1.parent().hide()
		else:
			self.resizePanel()

	def resizePanel(self):
		self.ui.parentPanel1.setMinimumSize(QSize(self.settings['panel1']['maximum'], 0))
		self.ui.parentPanel1.setMaximumSize(QSize(self.settings['panel1']['maximum'], 16777215))

	def setupMenu(self):
		self.ui.menuTree.setFocusPolicy(Qt.NoFocus)
		sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ui.menuTree.sizePolicy().hasHeightForWidth())
		self.ui.menuTree.setSizePolicy(sizePolicy)
		self.ui.menuTree.setHeaderLabels(['Navigation', 'icon'])
		self.ui.menuTree.setHeaderHidden(True);
		self.ui.menuTree.setAnimated(True)
		self.ui.menuTree.setColumnHidden(2, True)
		
		self.ui.menuTree.setColumnWidth(0,self.settings['panel1']['maximum']-90)
		self.ui.menuTree.setColumnWidth(1,5)
		#self.ui.menuTree.header().setDefaultSectionSize(0)
	  	#self.tree.expandAll()
		self.ui.menuTree.setCursor(Qt.PointingHandCursor)
		self.build_menu(data=self.menu_data, parent=self.ui.menuTree)
		self.ui.menuTree.itemClicked.connect(self.onItemClicked)

	@Slot(QTreeWidgetItem, int)	
	def onItemClicked(self, item, col):
		icon_color = self.theme_settings['theme']['panel1']['icons']
		if item.text(2) != None and item.text(2) != "":	
			# open menu link in content panel
			# call target class
			targetPageClass = item.text(2)
			# test if widgetClass exists 
			try:
				var = eval(targetPageClass)()
			except NameError:
				print(targetPageClass, "is not defined")
				return
			
			if self._lastcontent != None:
				self.ui.panel3.findChild(QWidget, self._lastcontent).hide()
			
			cachedWidget = self.ui.panel3.findChild(QWidget, targetPageClass)
			if cachedWidget:
				cachedWidget.show()
			else:
				self.ui.contentWidget  = eval(targetPageClass)(self.ui.panel3)
				self.ui.contentWidget .setObjectName(f"{targetPageClass}")
				sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
				sizePolicy.setHorizontalStretch(0)
				sizePolicy.setVerticalStretch(0)
				sizePolicy.setHeightForWidth(self.ui.contentWidget .sizePolicy().hasHeightForWidth())
				self.ui.contentWidget .setSizePolicy(sizePolicy)
				self.ui.contentWidget .setLayoutDirection(Qt.LeftToRight)
				self.ui.contentLayout.addWidget(self.ui.contentWidget )
			self._lastcontent = targetPageClass
		else:
			# collapse/expand
			if item.isExpanded():
				icon = qta.icon("fa.chevron-right", color=icon_color)
				item.setIcon(1, icon)
				
				if item.text(3) != "":
					try:
						icon = qta.icon(item.text(3), color=icon_color)
						item.setIcon(0, icon)
					except:
						item.setIcon(0, QIcon())

					
				self.ui.menuTree.collapseItem(item)
			else:
				icon = qta.icon("fa.chevron-down", color=icon_color)
				item.setIcon(1, icon)
				#self.ui.menuTree.collapseAll()
				if item.text(4) != "":
					try:
						icon = qta.icon(item.text(4), color=icon_color)
						item.setIcon(0, icon)
					except:
						item.setIcon(0, QIcon())
					
				self.ui.menuTree.expandItem(item)
				
	def build_menu(self, data=None, parent=None):
		icon_color = self.theme_settings['theme']['panel1']['icons']
		for menu_item in data:
			tree_item = QTreeWidgetItem(parent)
			tree_item.setText(0, menu_item['name'])
		
			if type(menu_item['icon']) == dict:
				try:
					icon = qta.icon(menu_item['icon']['collapsed'], color=icon_color)
					tree_item.setIcon(0, icon)
				except:
					tree_item.setIcon(0, QIcon())
				#tree_item.setIcon(0, QIcon(UIFunctions().set_svg_icon(menu_item['icon']['collapsed'], self.theme_settings['colors']['content_icon_color'])))
				tree_item.setText(3, menu_item['icon']['collapsed'])
				tree_item.setText(4, menu_item['icon']['expanded'])
			else:
				try:
					icon = qta.icon(menu_item['icon'], color=icon_color)
					tree_item.setIcon(0, icon)
				except:
					tree_item.setIcon(0, QIcon())
				
				#tree_item.setIcon(0, QIcon(UIFunctions().set_svg_icon(menu_item['icon'], self.theme_settings['colors']['content_icon_color'])))

			if "children" in menu_item:
				icon = qta.icon("fa.chevron-right", color=icon_color)
				tree_item.setIcon(1, icon)
				#tree_item.setIcon(1, QIcon(UIFunctions().set_svg_icon("chevron-right.svg", self.theme_settings['colors']['content_icon_color'])))
				self.build_menu(data=menu_item['children'], parent=tree_item)
			else:
				tree_item.setText(2, menu_item['widget'])
				if "start" in menu_item:
					self.onItemClicked(tree_item, 0)

	