from qt_core import *

class FileSystemView(QWidget):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		dir_path =  r'D:'
		dirPath = r'D:'
		
		self.model = QFileSystemModel()
		self.model.setRootPath(dir_path)
		self.tree =  QTreeView()
		self.tree.setModel(self.model)
		self.tree.setRootIndex(self.model.index(dirPath))
		self.tree.setColumnWidth(0, 250)
		self.tree.setAlternatingRowColors(True)
		#QAbstractItemView::alternatingRowColors() 
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.addWidget(self.tree)
		self.setLayout(self.layout)
