from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen


class App(MDApp):
	def build(self):
		kv = Builder.load_file("app.kv")
		return kv
		
	
if __name__ == "__main__":				
	App().run()