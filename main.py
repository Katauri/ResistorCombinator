from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class ScreenManagement(ScreenManager):
	pass

with open("app.kv", encoding='utf8') as f:
    app = Builder.load_string(f.read())

class App(MDApp):
	title = 'ResistorCombinator'

	def build(self):
		return ScreenManagement()
		
	
if __name__ == "__main__":				
	App().run()