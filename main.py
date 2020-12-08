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

    chunk_list = []
    chunk_view_index = 0

    thread_state = True


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

        self.thread_state = True
        self.chunk_list = []
        self.root.ids.textbox.text = ''

        tol_list = []

        if self.e24_choose:
            tol_list.append('E24')
        if self.e96_choose:
            tol_list.append('E96')
        if self.e192_choose:
            tol_list.append('E192')

        self.t = Thread(target = serial_combine, args = (float(self.value), float(self.tolerance[:-1]), 0, int(self.count), tol_list, self.chunk_list, self.thread_state))
        self.t.daemon = True
        if not self.t.is_alive():
            self.t.start()

        def render_first_chunk(*args):
           if self.chunk_list:
            self.root.ids.textbox.text = self.chunk_list[0]

        Clock.schedule_once(render_first_chunk, 0.25)


    def clear(self):
        if self.t.is_alive():
            self.thread_state = False

        self.chunk_list = []
        self.root.ids.textbox.text = ''





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

    def view_prev_chunk(self):
        if self.chunk_view_index > 0:
            self.chunk_view_index -= 1
            self.root.ids.textbox.text = self.chunk_list[self.chunk_view_index]

    def view_next_chunk(self):
        if self.chunk_view_index < (len(self.chunk_list) - 1):
            self.chunk_view_index += 1
            self.root.ids.textbox.text = self.chunk_list[self.chunk_view_index]




app = App()

if __name__ == "__main__":
    app.run()
