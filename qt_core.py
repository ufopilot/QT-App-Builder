import platform
import json
import os
import sys
from functools import partial

#from PySide2.QtCore import *
#from PySide2.QtGui import *
#from PySide2.QtWidgets import * 
#from PySide2.QtUiTools import loadUiType
#from PySide2.QtSvg import QSvgWidget

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, pyqtSlot as Slot, QRectF, QPointF, QTimer, QRegExp, QIODevice, QByteArray, QDataStream,
	QMetaObject, QObject, QPoint, QRect, QEvent, pyqtSignal as Signal, pyqtProperty as Property, QSequentialAnimationGroup, QRunnable, QThreadPool,
	QSize, QTime, QUrl, Qt, QPropertyAnimation, QEasingCurve, QAbstractAnimation, QParallelAnimationGroup, QPropertyAnimation, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QScreen,
	QFont, QFontDatabase, QGradient, QIcon, QFontMetrics, QMovie, QDrag,
	QImage, QKeySequence, QLinearGradient, QPainter, QPen, QPaintEvent,
	QPalette, QPixmap, QRadialGradient, QTransform, QStandardItem)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenuBar, QSizePolicy, QGridLayout, QLineEdit, QComboBox, QSpinBox, QDialogButtonBox, QMessageBox,QFormLayout, QMenu,
	QStatusBar, QWidget, QLabel, QButtonGroup, QAbstractButton, QPushButton, QGraphicsDropShadowEffect, QSizeGrip, QGroupBox, QSplashScreen, QTabWidget, QScrollArea, QTreeWidgetItemIterator,
	QVBoxLayout, QFrame, QHBoxLayout, QCheckBox, QTreeWidgetItem, QHeaderView, QAbstractItemView, QTreeWidget, QFileSystemModel, QTreeView, QDialog, QColorDialog, QFileDialog)
from PyQt5.uic import loadUiType

import qtawesome as qta

