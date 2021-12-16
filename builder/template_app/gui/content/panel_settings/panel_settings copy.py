from app.gui.functions.ui_functions import UIFunctions
from qt_core import *
class PanelSettings(QWidget):
	"""
	This "window" is a QWidget. If it has no parent, it
	will appear as a free-floating window as we want.
	"""
	def __init__(self):
		super().__init__()
#        self.resize(600, 300)
#        layout = QVBoxLayout()
#        self.label = QLabel("Another Window")
#        layout.addWidget(self.label)
#        self.setLayout(layout)
#        
#    
#    def Close(self):
#        self.close()
#
	#def setupUi(self, Form):
	#    if not Form.objectName():
	#        Form.setObjectName(u"Form")
		self.resize(688, 332)
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setObjectName(u"verticalLayout")
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.frame = QFrame(self)
		self.frame.setObjectName(u"frame")
		self.frame.setFrameShape(QFrame.StyledPanel)
		self.frame.setFrameShadow(QFrame.Raised)
		
		
		self.gridLayout = QGridLayout(self.frame)
		self.gridLayout.setObjectName(u"gridLayout")
		self.label = QLabel(self.frame)
		self.label.setObjectName(u"label")

		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

		self.lineEdit = QLineEdit(self.frame)
		self.lineEdit.setObjectName(u"lineEdit")

		self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

		self.label_2 = QLabel(self.frame)
		self.label_2.setObjectName(u"label_2")

		self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

		self.lineEdit_2 = QLineEdit(self.frame)
		self.lineEdit_2.setObjectName(u"lineEdit_2")

		self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

		self.label_3 = QLabel(self.frame)
		self.label_3.setObjectName(u"label_3")

		self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

		self.lineEdit_3 = QLineEdit(self.frame)
		self.lineEdit_3.setObjectName(u"lineEdit_3")

		self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

		self.label_5 = QLabel(self.frame)
		self.label_5.setObjectName(u"label_5")

		self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

		self.comboBox = QComboBox(self.frame)
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.addItem("")
		self.comboBox.setObjectName(u"comboBox")

		self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)

		self.label_4 = QLabel(self.frame)
		self.label_4.setObjectName(u"label_4")

		self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)

		self.spinBox = QSpinBox(self.frame)
		self.spinBox.setObjectName(u"spinBox")
		 
		self.gridLayout.addWidget(self.spinBox, 4, 1, 1, 1)

		self.buttonBox = QDialogButtonBox(self.frame)
		self.buttonBox.setObjectName(u"buttonBox")
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

		self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)


		self.verticalLayout.addWidget(self.frame)


		self.retranslateUi()

		QMetaObject.connectSlotsByName(self)

		effect = QGraphicsDropShadowEffect(self.frame, enabled=False, blurRadius=5)
		self.frame.setGraphicsEffect(effect)
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(15)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 150))
		# add the shadow object to the frame
		self.frame.raise_()
		self.frame.setGraphicsEffect(self.shadow)

		self.setGuiStyle("dark")
		#self.frame.setStyleSheet("background-color: #13161f; color: #fff;")
	# setupUi
	def setGuiStyle(self, theme):
		return
		template_stylesheet = ""
		with open(UIFunctions().resource_path(f'./app/gui/assets/style/dialog.qss')) as f:
				base_stylesheet = f.read()  
		if theme == "fusion":
			print("set theme", theme)
			self.frame.setStyleSheet(f"{base_stylesheet}")
		else:
			print("set theme", theme)
			with open(UIFunctions().resource_path(f'./app/gui/assets/style/colors.qss')) as f:
				template_stylesheet = f.read()
			with open(UIFunctions().resource_path(f'./app/gui/assets/themes/{theme}.json')) as f:
				theme_stylesheet = json.load(f)
				for key, value in theme_stylesheet.items():
					template_stylesheet = template_stylesheet.replace(key, value)
			#\n{template_stylesheet}
			self.frame.setStyleSheet(f"{base_stylesheet}")
	
	def retranslateUi(self):
		self.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
		self.label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
		self.label_2.setText(QCoreApplication.translate("Form", u"TextLabel", None))
		self.label_3.setText(QCoreApplication.translate("Form", u"TextLabel", None))
		self.label_5.setText(QCoreApplication.translate("Form", u"TextLabel", None))
		self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"Leftt To Rght", None))
		self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"Right To Left", None))
		self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"Up To Down", None))
		self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"Down to Up", None))

		self.label_4.setText(QCoreApplication.translate("Form", u"TextLabel", None))
	# retranslateUi
