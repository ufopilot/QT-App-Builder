from qt_core import *
from . sidegrip import SideGrip

class WindowResizer(QMainWindow):
	_gripSize = 8
	def __init__(self, parent):
		QMainWindow.__init__(self, parent)
		
		self.sideGrips = [
			SideGrip(self, Qt.LeftEdge), 
			SideGrip(self, Qt.TopEdge), 
			SideGrip(self, Qt.RightEdge), 
			SideGrip(self, Qt.BottomEdge), 
		]
		# corner grips should be "on top" of everything, otherwise the side grips
		# will take precedence on mouse events, so we are adding them *after*;
		# alternatively, widget.raise_() can be used
		self.cornerGrips = [QSizeGrip(self) for i in range(4)]
		self.cornerGrips[0].setStyleSheet("background: transparent;")
		self.cornerGrips[1].setStyleSheet("background: transparent;")
		self.cornerGrips[2].setStyleSheet("background: transparent;")
		self.cornerGrips[3].setStyleSheet("background: transparent;")

	@property
	def gripSize(self):
		return self._gripSize

	def setGripSize(self, size):
		if size == self._gripSize:
			return
		self._gripSize = max(2, size)
		self.updateGrips()

	def updateGrips(self):
		#self.setContentsMargins(*[self.gripSize] * 4)
		#self.setStyleSheet("background: #000")
		
		outRect = self.rect()
		
		# an "inner" rect used for reference to set the geometries of size grips
		inRect = outRect.adjusted(self.gripSize, self.gripSize,
			-self.gripSize, -self.gripSize)
		
		# top left
		self.cornerGrips[0].setGeometry(
			QRect(outRect.topLeft(), inRect.topLeft()))
		# top right
		self.cornerGrips[1].setGeometry(
			QRect(outRect.topRight(), inRect.topRight()).normalized())
		# bottom right
		self.cornerGrips[2].setGeometry(
			QRect(inRect.bottomRight(), outRect.bottomRight()))
		# bottom left
		self.cornerGrips[3].setGeometry(
			QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

		# left edge
		self.sideGrips[0].setGeometry(
			0, inRect.top(), self.gripSize, inRect.height())
		
		# top edge
		self.sideGrips[1].setGeometry(
			inRect.left(), 0, inRect.width(), self.gripSize)
		# right edge
		self.sideGrips[2].setGeometry(
			inRect.left() + inRect.width(), 
			inRect.top(), self.gripSize, inRect.height())
		# bottom edge
		self.sideGrips[3].setGeometry(
			self.gripSize, inRect.top() + inRect.height(), 
			inRect.width(), self.gripSize)

		[grip.raise_() for grip in self.sideGrips + self.cornerGrips]

	def resizeEvent(self, event):
		QMainWindow.resizeEvent(self, event)
		self.updateGrips()
	