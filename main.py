from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown

class ScreenManagement(ScreenManager):
	pass

class CustomDropDown(DropDown):
    pass

with open("app.kv", encoding='utf8') as f:
    app = Builder.load_string(f.read())



class App(MDApp):
	title = 'ResistorCombinator'

	def build(self):
		self.drop_menu = CustomDropDown()
		return ScreenManagement()
		
	
if __name__ == "__main__":				
	App().run()