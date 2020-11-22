from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

with open("param.kv", encoding='utf8') as f:
    param = Builder.load_string(f.read())

caption_height = dp(20)


class ScreenManagement(ScreenManager):
    pass


class ToleranceDropDown(DropDown):
    pass


class DimensionDropDown(DropDown):
    pass


class App(MDApp):
    title = 'ResistorCombinator'
    tolerance = StringProperty('5%')
    dimension = StringProperty('kOm')
    count = StringProperty('2')
    value = StringProperty('1')
    value_max = StringProperty('1.050 kOm')
    value_min = StringProperty('0.950 kOm')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tolerance_menu = ToleranceDropDown()
        self.dimension_menu = DimensionDropDown()

    def build(self):
        return ScreenManagement()

    def resistor_change(self, tolerance, dimension):
        if tolerance:
            self.tolerance = str(tolerance) + '%'

        if dimension:
            self.dimension = dimension

        self.value_max = str(round(float(self.value) * (1 + ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)), 3)) + ' ' + self.dimension
        self.value_min = str(round(float(self.value) * (1 - ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)), 3)) + ' ' + self.dimension

    def calc_combination(self):
        if self.root.ids.chk_serial.active:
            output_string = ""
            for num in range(int(self.count)):
                output_string += str(num + 1) + "-vvv-: "

            self.root.ids.box.add_widget(MDLabel(text=output_string, height = caption_height))

    def change_count(self, value):
        if (int(self.count) >= 2 and value > 0) or (int(self.count) > 2 and value < 0):
            self.count = str(int(self.count) + value)


if __name__ == "__main__":
    App().run()
