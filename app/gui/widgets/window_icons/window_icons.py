
from qt_core import *
from app.gui.functions.ui_functions import *

class WindowIcons(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        
        self.windowicons = QWidget(self)
        self.windowicons.setObjectName(u"windowicons")
        self.windowicons.setMaximumSize(QSize(100, 16777215))
        self.windowicons.setSizeIncrement(QSize(0, 0))
        self.windowicons.setStyleSheet(u"margin-top:10px")
        
        self.layout = QHBoxLayout(self.windowicons)
        self.layout.setSpacing(10)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.minimizewindow = QPushButton(self.windowicons)
        self.minimizewindow.setObjectName(u"minimizewindow")
        self.minimizewindow.setCursor(QCursor(Qt.PointingHandCursor))
        icon3 = QIcon()
        #icon3.addFile(u":/icons-white-small/assets/icons/small/icon_minimize.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon3.addPixmap(QPixmap(UIFunctions().set_svg_icon("icon_minimize.svg")))
        self.minimizewindow.setIcon(icon3)

        self.layout.addWidget(self.minimizewindow)

        self.maximisewindow = QPushButton(self.windowicons)
        self.maximisewindow.setObjectName(u"maximisewindow")
        self.maximisewindow.setCursor(QCursor(Qt.PointingHandCursor))
        icon4 = QIcon()
        #icon4.addFile(u":/icons-white-small/assets/icons/small/icon_maximize.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon4.addPixmap(QPixmap(UIFunctions().set_svg_icon("icon_maximize.svg")))
        self.maximisewindow.setIcon(icon4)

        self.layout.addWidget(self.maximisewindow)

        self.restorewindow = QPushButton(self.windowicons)
        self.restorewindow.setObjectName(u"restorewindow")
        self.restorewindow.setCursor(QCursor(Qt.PointingHandCursor))
        icon5 = QIcon()
        #icon5.addFile(u":/icons-white-small/assets/icons/small/icon_restore.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon5.addPixmap(QPixmap(UIFunctions().set_svg_icon("icon_restore.svg")))
        self.restorewindow.setIcon(icon5)

        self.layout.addWidget(self.restorewindow)

        self.closewindow = QPushButton(self.windowicons)
        self.closewindow.setObjectName(u"closewindow")
        self.closewindow.setCursor(QCursor(Qt.PointingHandCursor))
        icon6 = QIcon()
        #icon6.addFile(u":/icons-white-small/assets/icons/small/icon_close.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon6.addPixmap(QPixmap(UIFunctions().set_svg_icon("icon_close.svg")))
        self.closewindow.setIcon(icon6)
        self.closewindow.setStyleSheet(u"*{ margin-top: 10px; margin-right: 0px;}")
        self.closewindow.setStyleSheet(u"*:hover{ background: red; }")
        self.layout.addWidget(self.closewindow)

        self.restorewindow.hide()
        self.restorewindow.clicked.connect(self.maximisewindow.show)
        self.restorewindow.clicked.connect(self.restorewindow.hide)
        self.restorewindow.clicked.connect(self.window().showNormal)
        
        self.maximisewindow.clicked.connect(self.maximisewindow.hide)   
        self.maximisewindow.clicked.connect(self.restorewindow.show)
        self.maximisewindow.clicked.connect(self.window().showMaximized)
        
        self.minimizewindow.clicked.connect(self.window().showMinimized)
        self.closewindow.clicked.connect(self.window().close)
        
