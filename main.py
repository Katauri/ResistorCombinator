from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.dropdown import DropDown
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from kivmob import KivMob, TestIds

from kivy.clock import Clock

from threading import Thread

from combinator import serial_combine, parallel_combine

apple_green_color = (.55, .71, 0, 1)
x11_gray_color = (.75, .75, .75, 1)
medium_orchid_color = (.73, .33, .83, 1)


class ScreenManagement(ScreenManager):
    pass

class ThreadState:
    def __init__(self, stop):
        self.stop = stop

class ChunkView:
    def __init__(self, index):
        self.index = index


def exception_cather(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            return False

    return wrapper


Builder.load_file('app_layout.kv')


class App(MDApp):
    title = 'ResistorCombinator'
    tolerance = StringProperty('5%')
    dimension = StringProperty('kOm')
    count = StringProperty('2')
    value = StringProperty('1')
    value_max = StringProperty('1.050 kOm')
    value_min = StringProperty('0.950 kOm')
    power = StringProperty('0')

    dimension_menu = ObjectProperty()

    e24_choose = True
    e96_choose = True
    e192_choose = False

    x2_choose = True
    x3_choose = False

    chunk_list = []

    thread_state = ThreadState(stop=False)
    chunk_view = ChunkView(index=0)

    t = Thread()

    def on_start(self):
        dimension_menu_items = [{"text": "mOm"}, {"text": "Om"}, {"text": "kOm"}, {"text": "MOm"}]
        tolerance_menu_items = [{"text": "10%"}, {"text": "5%"}, {"text": "1%"}, {"text": "0.5%"}]

        self.dimension_menu = MDDropdownMenu(
            caller = self.root.ids.dimension_button,
            items = dimension_menu_items,
            width_mult = 2,
            background_color = [0.32,.67,.95, 1]
        )

        self.tolerance_menu = MDDropdownMenu(
            caller = self.root.ids.tolerance_button,
            items = tolerance_menu_items,
            width_mult = 2,
            background_color=[0.32, .67, .95, 1]
        )

        self.dimension_menu.bind(on_release=self.dimension_menu_callback)
        self.tolerance_menu.bind(on_release=self.tolerance_menu_callback)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def dimension_menu_callback(self, instance_menu, instance_menu_item):
        self.resistor_change(dimension = instance_menu_item.text, tolerance = None)
        instance_menu.dismiss()


    def tolerance_menu_callback(self, instance_menu, instance_menu_item):
        self.resistor_change(dimension=None, tolerance=instance_menu_item.text)
        self.resistor_change()
        instance_menu.dismiss()








    def build(self):
        self.ads = KivMob(TestIds.APP)
        self.ads.new_banner(TestIds.BANNER, top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()

        sm = ScreenManagement()
        return sm

    @exception_cather
    def resistor_change(self, tolerance, dimension):
        if tolerance:
            self.tolerance = tolerance

        if dimension:
            self.dimension = dimension

        self.value_max = str(
            round(float(self.value) * (1 + ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)),
                  3)) + ' ' + self.dimension
        self.value_min = str(
            round(float(self.value) * (1 - ((float(str(self.tolerance)[:len(str(self.tolerance)) - 1])) / 100)),
                  3)) + ' ' + self.dimension

    @exception_cather
    def calc_combination(self):

        self.thread_state.stop = True

        self.chunk_list = []
        self.chunk_view.index = 0
        self.root.ids.textbox.text = ''
        self.root.ids.caption_pagination.text = '%d/%d' % (1, 1)

        tol_list = []

        if self.e24_choose:
            tol_list.append('E24')
        if self.e96_choose:
            tol_list.append('E96')
        if self.e192_choose:
            tol_list.append('E192')

        multiplier = 1

        if self.dimension == 'Om':
            multiplier = 1
        elif self.dimension == 'kOm':
            multiplier = 10 ** 3
        elif self.dimension == 'MOm':
            multiplier = 10 ** 6
        elif self.dimension == 'mOm':
            multiplier = 10 ** (-3)

        value = float(self.value) * multiplier


        if self.power == '':
            self.power = '0'

        if float(self.power) <= 90:
            power = float(self.power)
        else:
            self.power = '0'
            power = 0

        def render_first_chunk(*args):
            if self.chunk_list:
                self.root.ids.textbox.text = self.chunk_list[0]

        def render_chunk(*args):
            if self.chunk_list:
                self.root.ids.textbox.text = self.chunk_list[self.chunk_view.index]

        def start_thread(*args):
            if self.root.ids.chk_serial.active:
                if not self.t.is_alive():
                    self.t = Thread(target=serial_combine, args=(
                        value, float(self.tolerance[:-1]), power, int(self.count), tol_list, self.chunk_list,
                        self.thread_state, self.root.ids.caption_pagination, self.chunk_view))
                    self.t.daemon = True
                    self.thread_state.stop = False
                    self.t.start()

            elif self.root.ids.chk_parallel.active:
                if not self.t.is_alive():
                    self.t = Thread(target=parallel_combine, args=(
                        value, float(self.tolerance[:-1]), power, int(self.count), tol_list, self.chunk_list,
                        self.thread_state, self.root.ids.caption_pagination, self.chunk_view))
                    self.t.daemon = True
                    self.thread_state.stop = False
                    self.t.start()

        Clock.schedule_once(start_thread, 0.25)
        Clock.schedule_once(render_first_chunk, 0.5)
        Clock.schedule_once(render_first_chunk, 2)
        Clock.schedule_once(render_chunk, 5)
        Clock.schedule_once(render_chunk, 10)

    @exception_cather
    def clear(self):
        if self.t.is_alive():
            self.thread_state.stop = True


        self.chunk_view.index = 0
        self.chunk_list = []
        self.root.ids.textbox.text = ''
        self.root.ids.caption_pagination.text = '%d/%d' % (1, 1)

    @exception_cather
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

    @exception_cather
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

    @exception_cather
    def view_prev_chunk(self):
        if self.chunk_view.index > 0:
            self.chunk_view.index -= 1
            current_chunk = self.chunk_list[self.chunk_view.index]
            self.root.ids.textbox.text = current_chunk
            self.root.ids.caption_pagination.text = '%d/%d' % (self.chunk_view.index + 1, len(self.chunk_list))

    @exception_cather
    def view_next_chunk(self):
        if self.chunk_view.index < (len(self.chunk_list) - 1):
            self.chunk_view.index += 1
            current_chunk = self.chunk_list[self.chunk_view.index]
            self.root.ids.textbox.text = current_chunk
            self.root.ids.caption_pagination.text = '%d/%d' % (self.chunk_view.index + 1, len(self.chunk_list))


app = App()

if __name__ == "__main__":
    app.run()
