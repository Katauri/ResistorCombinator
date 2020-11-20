from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown

with open("app.kv", encoding='utf8') as f:
    app = Builder.load_string(f.read())


class ScreenManagement(ScreenManager):
    pass


class PercentDropDown(DropDown):
    pass


class ValueDropDown(DropDown):
    pass


class App(MDApp):
    title = 'ResistorCombinator'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.percent_menu = PercentDropDown()
        self.value_menu = ValueDropDown()

    def build(self):
        return ScreenManagement()


if __name__ == "__main__":
    App().run()
