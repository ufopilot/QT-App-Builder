from qt_core import *
from app.gui.functions.ui_functions import *

class FileTree(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)
		
		self.treeWidget = QTreeWidget(self)
		self.treeWidget.setObjectName(u"treeWidget")
		self.treeWidget.setGeometry(QRect(10, 60, 256, 377))

		self.startDir = "D:\\"
		
		self.treeWidget.setHeaderLabels(['FileTree'])
		self.treeWidget.setColumnWidth(0,400)
		self.treeWidget.setContentsMargins(0, 0, 0, 0)
		#self.treeWidget.header().setResizeMode(0, QHeaderView.ResizeToContents)
		#self.treeWidget.header().setDefaultSectionSize(300)
		#self.treeWidget.header().setStretchLastSection(False)
		#self.treeWidget.header().setResizeMode(0, QHeaderView.Stretch)
		self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
		#self.treeWidget.setColumnCount(1)
		#self.treeWidget.setAlternatingRowColors(True)
		self.fileTree("D:\\Autoit", self.treeWidget)

	def fileTree(self, startpath, tree):
		for element in os.listdir(startpath):
			path_info = startpath + "/" + element
			parent_itm = QTreeWidgetItem(tree, [os.path.basename(element)])
			if os.path.isdir(path_info):
				self.fileTree(path_info, tree)
				parent_itm.setIcon(0, QIcon("gui/resources/icons/magenta/folder.svg"))
			else:
				parent_itm.setIcon(0, QIcon("gui/resources/icons/cyan/file.svg"))
	