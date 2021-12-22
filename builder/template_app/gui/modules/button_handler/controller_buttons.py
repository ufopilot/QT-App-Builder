from builder.template_app.gui.functions.settings import Settings
from builder.template_app.gui.functions.ui_functions import UIFunctions
from qt_core import *
import webbrowser

class SetControllerButtons(QWidget):
	_panels_closed = []
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		#self.setupUi(self)
		self.ui = parent
		settings = Settings('ui')
		self.settings = settings.items
		theme_settings = Settings('theme')
		self.theme_settings = theme_settings.items
		
		self.footer_icon_color = self.theme_settings['theme']['footerbar']['icons']
		self.dividers_icon_color = self.theme_settings['theme']['dividers']['icons']
		for divider in (self.ui.headerPanel1, self.ui.headerPanel2, self.ui.headerPanel3, self.ui.headerPanel4, self.ui.headerPanel5):
			name = divider.objectName()
			panel = name.lower().replace("header", "")
			divider.setText(self.settings[panel]['title'])
			if not self.settings[panel]['divider']:
				print("hide", panel)
				divider.parent().hide()
		#for x in range(1,6):
		#	panel = str(f"panel{x}")
		#	print(panel)
		#	self.ui.headerPanel1.setText(self.settings[panel]['title'])
		#self.ui.headerPanel2.setText(self.settings['panel2']['title'])
		#self.ui.headerPanel3.setText(self.settings['panel3']['title'])
		#self.ui.headerPanel4.setText(self.settings['panel4']['title'])
		#self.ui.headerPanel5.setText(self.settings['panel5']['title'])


		self.ui.menuTitle.setText(self.settings['panel1']['title'])
		self.ui.settingsTitle.setText(self.settings['panel2']['title'])
		
	def handle_ui_btns(self):
		self.ui.closeOtherPanels.clicked.connect(self.close_all_panels)
		self.ui.closeOtherPanels.setToolTip("Close all other Panels")
		self.ui.buttonGroup = QButtonGroup(self)
		for button in self.ui.findChildren(QAbstractButton):
			#self.ui.buttonGroup.addButton(button)
			button.setCursor(QCursor(Qt.PointingHandCursor))
			#if isinstance(button, QPushButton):
			#	button.setFlat(True)
			
			if button.objectName().startswith("togglePanel"):
				button.clicked.connect(self.toggle_panel)
				button.setToolTip("Toggle Panel")
			if button.objectName().startswith("panelSettings"):
				button.setToolTip("Settings")
				button.clicked.connect(self.panel_settings)
			if button.objectName() == "goToGitHub":
				icon = qta.icon("fa.github", color=self.dividers_icon_color)
				button.setIcon(icon)
				button.clicked.connect(self.openGithub)
				button.setToolTip('Open Project in GitHub')
		
		
		
		icon = qta.icon("fa.chevron-left", color=self.dividers_icon_color)
		self.ui.togglePanel1.setIcon(icon)
		self.ui.togglePanel1.setIcon(icon)
		icon = qta.icon("fa.chevron-right", color=self.dividers_icon_color)
		self.ui.togglePanel4.setIcon(icon)
		icon = qta.icon("fa.chevron-down", color=self.dividers_icon_color)
		self.ui.togglePanel5.setIcon(icon)
		icon = qta.icon("mdi.crop-free", color=self.dividers_icon_color)
		self.ui.closeOtherPanels.setIcon(icon)
		
	def openGithub(self):
		webbrowser.open("https://github.com/ufopilot/PyQT-DemoAPP/")

	def panel_settings(self):
		button = self.sender()
		panel_name = button.objectName().lower().replace('settings', '')
		#self.dialog = PanelSettings()
		#self.dialog.setWindowFlag(Qt.FramelessWindowHint)
		#self.dialog.show()

	def disableToggleButtons(self):
		togglebuttons = (self.ui.closeOtherPanels, self.ui.togglePanel1, self.ui.togglePanel2, self.ui.togglePanel4, self.ui.togglePanel5)
		for i, button in enumerate(togglebuttons):
			button.setEnabled(False)
	
	def EnableToggleButtons(self):
		togglebuttons = (self.ui.closeOtherPanels, self.ui.togglePanel1, self.ui.togglePanel2, self.ui.togglePanel4, self.ui.togglePanel5)
		for i, button in enumerate(togglebuttons):
			button.setEnabled(True)
	
	def close_all_panels(self):
		togglebuttons = (self.ui.togglePanel1, self.ui.togglePanel2, self.ui.togglePanel4, self.ui.togglePanel5)
		for i, button in enumerate(togglebuttons):
			panel_name = button.objectName().replace('toggle', '').lower()
			if panel_name not in self._panels_closed:
				self.toggle_panel(button, 0)	
				#QTimer.singleShot(self.settings['time_animation'], lambda: self.toggle_panel(button))
		
	def toggle_all(self):
		self.ui.buttonGroup = QButtonGroup(self)
		for button in self.ui.findChildren(QAbstractButton):
			if button.objectName().startswith("togglePanel"):
				panel_name = button.objectName().replace("toggle", "").lower()
				if not self.settings[panel_name]['show_onstart']:
					self.toggle_panel(button, 0)
	
	def toggle_panel(self, button=False, timeAnimation=-1):
		if not button:
			button = self.sender()
		if not button.isEnabled():
			return
		panel = button.parent().parent().parent()
		panel_name = button.objectName().replace('toggle', '').lower()
		panel_index = panel_name.replace("panel", '')
		enable = self.settings[panel_name]['toggle']
		if enable:
			width = panel.width()
			height = panel.height()
			maximum = self.settings[panel_name]['maximum']
			minimum = self.settings[panel_name]['minimum']
			if timeAnimation == -1:
				timeAnimation = self.settings['time_animation']
			
			
			# ANIMATION
			direction = self.settings[panel_name]['direction']
			if direction == "rtl":
				icon_svg_close = "fa.chevron-left"
				icon_svg_expand = "fa.chevron-right"
				size_option = "minimumWidth"
				startValue = width

			if direction == "ltr":
				icon_svg_close = "fa.chevron-right"
				icon_svg_expand = "fa.chevron-left"
				size_option = "minimumWidth"
				startValue = width

			if direction == "btt":
				icon_svg_close = "fa.chevron-down"
				icon_svg_expand = "fa.chevron-up"
				size_option = "minimumHeight"
				startValue = height

			if direction == "ttb": 
				icon_svg_close = "fa.chevron-down"
				icon_svg_expand = "fa.chevron-up"
				size_option = "minimumHeight"
				startValue = height
			

			panel_title = panel.findChild(QLabel, f"headerPanel{panel_index}")
			
			if startValue == minimum:
				self._panels_closed.remove(panel_name)
				endValue = maximum
				panel_title_style = ""
				#panel_title.setStyleSheet("")
				#icon.addPixmap(QPixmap(UIFunctions().set_svg_icon(icon_svg_close, self.theme_settings['colors']['content_icon_color'])))
				icon = qta.icon(icon_svg_close, color=self.dividers_icon_color)
			
			else:
				self._panels_closed.append(panel_name)
				endValue = minimum
				panel_title_style = "color: #333"	
				#panel_title.setStyleSheet("color: #333")
				#icon.addPixmap(QPixmap(UIFunctions().set_svg_icon(icon_svg_expand, self.theme_settings['colors']['content_icon_color'])))
				icon = qta.icon(icon_svg_expand, color=self.dividers_icon_color)
			button.setIcon(icon)
			
			self.animation = QPropertyAnimation(panel, bytes(size_option, encoding='utf-8'))
			self.animation.setDuration(timeAnimation)
			self.animation.setStartValue(startValue)
			self.animation.setEndValue(endValue)
			self.animation.setEasingCurve(QEasingCurve.InOutQuart)
			self.animation.start()
			QTimer.singleShot(timeAnimation, lambda: panel_title.setStyleSheet(panel_title_style))
	