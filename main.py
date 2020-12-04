from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from threading import  Thread
from combinator import serial_combine

with open("param.kv", encoding='utf8') as f:
    param = Builder.load_string(f.read())

caption_height = dp(20)
apple_green_color = (.55, .71, 0, 1)
x11_gray_color = (.75, .75, .75, 1)
max_resistor_count = 4



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

    e24_choose = True
    e96_choose = True
    e192_choose = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tolerance_menu = ToleranceDropDown()
        self.dimension_menu = DimensionDropDown()


    def build(self):
        sm = ScreenManagement()
        return sm

    def resistor_change(self, tolerance, dimension):
        if tolerance:
            self.tolerance = str(tolerance) + '%'

        if dimension:
            self.dimension = dimension

        self.value_max = str(round(float(self.value) * (1 + ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)), 3)) + ' ' + self.dimension
        self.value_min = str(round(float(self.value) * (1 - ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)), 3)) + ' ' + self.dimension

    def calc_combination(self):


        tol_list = []
        if self.e24_choose:
            tol_list.append('E24')
        if self.e96_choose:
            tol_list.append('E96')
        if self.e192_choose:
            tol_list.append('E192')

        gen = serial_combine(value=float(self.value), power=0,
                                     tolerance = float(self.tolerance[:-1]), count = int(self.count),
                                     tol_list = tol_list, widget = self.root.ids.box)

        t = Thread(target = serial_combine, args = (100, 5, 0, 3, tol_list, self.root.ids.box))
        t.daemon = True
        t.start()

        for i in gen:
            self.root.ids.box.add_widget((MDLabel(text=str(i), height=caption_height)))
            print(i)

        # if self.root.ids.chk_serial.active:
        #     gen = serial_combine(value = float(self.value), power = 0,
        #                                              tolerance = float(self.tolerance[:-1]), count = int(self.count),
        #                                              tol_list = tol_list, widget = self.root.ids.box)
        #     for i in gen:
        #
        #         self.root.ids.box.add_widget((MDLabel(text=str(i), height=caption_height)))
        #         print(i)


    def change_count(self, value):
        if (int(self.count) >= 2 and value > 0 and (int(self.count) < max_resistor_count)) or (int(self.count) > 2 and value < 0):
            self.count = str(int(self.count) + value)

    def tolerance_button_click(self, widget):
        if widget.name == 'e24_button' and (self.e96_choose or self.e192_choose):
            self.e24_choose = not self.e24_choose
            if self.e24_choose:
                widget.md_bg_color = apple_green_color
            else:
                widget.md_bg_color = x11_gray_color

        if widget.name == 'e96_button' and (self.e192_choose or self.e24_choose):
            self.e96_choose = not self.e96_choose
            if self.e96_choose:
                widget.md_bg_color = apple_green_color
            else:
                widget.md_bg_color = x11_gray_color

        if widget.name == 'e192_button' and (self.e96_choose or self.e24_choose):
            self.e192_choose = not self.e192_choose
            if self.e192_choose:
                widget.md_bg_color = apple_green_color
            else:
                widget.md_bg_color = x11_gray_color



app = App()

if __name__ == "__main__":
    app.run()
