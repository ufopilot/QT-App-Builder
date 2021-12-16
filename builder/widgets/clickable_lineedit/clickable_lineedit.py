from qt_core import *

class ClickableQLineEdit(QLineEdit):
    #clicked= Signal()
    doubleClicked = Signal()
    def __init__(self,widget):
        super().__init__(widget)
    
    
    #def mousePressEvent(self,QMouseEvent):
    #    self.doubleClicked.emit()

    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonDblClick:
            self.doubleClicked.emit()
        return super().event(event)