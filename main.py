from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock

from threading import  Thread
import queue

from combinator import serial_combine

with open("param.kv", encoding='utf8') as f:
    param = Builder.load_string(f.read())

caption_height = dp(20)
apple_green_color = (.55, .71, 0, 1)
x11_gray_color = (.75, .75, .75, 1)
medium_orchid_color = (.73, .33, .83, 1)




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

    x2_choose = True
    x3_choose = False

    output_list = []

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


        qe = queue.Queue()
        t = Thread(target = serial_combine, args = (100, 5, 0, 2, tol_list, qe))
        t.daemon = True
        t.start()

        def render_callback(*args):
            self.output_list.append(qe.get())

        event = Clock.schedule_interval(render_callback, 1 / 100.)






    def change_count(self, value, widget):
        self.count = str(value)
        if widget.name == 'x2_button' and self.x3_choose:
            self.x2_choose = True
            self.x3_choose = False
            widget.md_bg_color = medium_orchid_color
            self.root.ids.x3_button.md_bg_color = x11_gray_color

        if widget.name == 'x3_button' and self.x2_choose:
            self.x3_choose = True
            self.x2_choose = False
            widget.md_bg_color = medium_orchid_color
            self.root.ids.x2_button.md_bg_color = x11_gray_color

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
