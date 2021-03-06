import json, sys, os
from builder.template_app.gui.functions.ui_functions import UIFunctions


# APP SETTINGS
# ///////////////////////////////////////////////////////////////
class Settings(object):
	def __init__(self, type=None):
		super(Settings, self).__init__()
		
		if type == "menu":
			self.json_file = f"builder/template_app/gui/settings/{type}_settings.json"
			self.settings_path = UIFunctions().resource_path(self.json_file)
		else:
			if getattr(sys, 'frozen', False):
				# we are running in a |PyInstaller| bundle
				base_path = sys._MEIPASS
				extDataDir = os.getcwd()
				print(base_path)
				print(extDataDir)
				self.json_file = f"settings/{type}_settings.json"
			else:
				# we are running in a normal Python environment
				base_path = os.getcwd()
				extDataDir = os.getcwd()
				self.json_file = f"builder/template_app/gui/settings/{type}_settings.json"
		
			self.settings_path = os.path.join(extDataDir, self.json_file)
		
		self.items = {}
		self.deserialize()
	
	def serialize(self):
		# WRITE JSON FILE
		with open(self.settings_path, "w", encoding='utf-8') as write:
			json.dump(self.items, write, indent=4)

	def deserialize(self):
		# READ JSON FILE
		with open(self.settings_path, "r", encoding='utf-8') as reader:
			settings = json.loads(reader.read())
			self.items = settings
	
