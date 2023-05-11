from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line, Fbo, InstructionGroup
from kivy.core.image import Image
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivy.config import Config
import struct
import threading
import time


Window.size = (1280, 720)
#Window.fullscreen = True
#размер экрана моего телефона 2400x1080


brush_size = 5
color_red = 100
color_green = 100
color_blue = 100
alpha = 1
last_red = color_red
last_green = color_green
last_blue = color_blue
flag = True # пипетка вкл/выкл
krug_changes = False # смена пипеткой цвета
file_name = 'drawing'
settings_on = False

class drawer(Widget):
    undolist = []
    objects = []
    drawing = False


    def __init__(self):
        super(drawer, self).__init__()

    def on_touch_up(self, touch):
        self.drawing = False

    def on_touch_move(self, touch): # при движении пальца(мышки) по области рисования
        global color_green, color_red, color_blue, last_red, last_green, last_blue, flag, krug_changes
        try:
            if touch.x < Window.size[0] * 0.725:
                if flag:    # обычное рисование
                    '''self.canvas.add(Color(color_red / 255, color_green / 255, color_blue / 255, alpha))
                    self.line = Line(width=brush_size, close=False)
                    self.canvas.add(self.line)
                    self.line.points += (touch.x, touch.y)
                    self.line.points += (touch.x, touch.y - 1)'''
                    if self.drawing:
                        self.points.append(touch.pos)
                        self.obj.children[-1].points = self.points
                    else:
                        self.drawing = True
                        self.points = [touch.pos]
                        self.obj = InstructionGroup()
                        self.obj.add(Color(color_red / 255, color_green / 255, color_blue / 255, alpha))
                        self.obj.add(Line(width=brush_size))
                        self.objects.append(self.obj)
                        self.canvas.add(self.obj)

        except Exception as e:
            print(e)

    def on_touch_down(self, touch): # при касании пальца(мышки) области рисования
        global color_green, color_red, color_blue, last_red, last_green, last_blue, flag, alpha, krug_changes
        if touch.x < Window.size[0] * 0.725 and not flag:
            a = self.export_as_image()
            pixel = a.texture.get_region(touch.x, Window.height - touch.y, 1, 1)
            bp = pixel.pixels
            data = struct.unpack('4B', bp)
            print(data)
            color_red, last_red = round(data[0], 1), round(data[0], 1)
            color_green, last_green = round(data[1], 1), round(data[1], 1)
            color_blue, last_blue = round(data[2], 1), round(data[2], 1)
            print(color_red, color_green, color_blue)
            alpha = round(data[3] / 255, 1)

    def undo(self):
        try:
            item = self.objects.pop(-1)
            self.undolist.append(item)
            self.canvas.remove(item)
        except Exception as e:
            print(e)

    def redo(self):
        try:
            item = self.undolist.pop(-1)
            self.objects.append(item)
            self.canvas.add(item)
        except Exception as e:
            print(e)


class Krug(Widget):
    def __init__(self):
        super(Krug, self).__init__()
    def draw_krug(self,color_red, color_green, color_blue, alpha, brush_size):
        try:
            self.canvas.clear()
            self.canvas.add(Color(color_red / 255, color_green / 255, color_blue / 255, alpha))
            self.canvas.add(Ellipse(pos=(Window.size[0] * 0.885-brush_size,Window.size[1] * 0.45-brush_size),
                                   size=(brush_size*2,brush_size*2)))
            #self.canvas.add(Ellipse(pos_hint={'x': 2, 'y': 0.5}, size=(brush_size*2,brush_size*2)))
        except Exception as e:
            print(e)

class MyApp(App):
    #Window.clearcolor = (0.8, 0.8, 0.8)
    def build(self):
        global color_blue, color_green, color_red
        #создание виджетов
        self.global_space = FloatLayout()   # самый большой контейнер
        self.space = BoxLayout(orientation="horizontal")
        self.sheet = drawer()   # виджет рисования
        #self.scrolling = ScrollView(do_scroll_x=False, size_hint = (0.3,1))
        self.instruments = BoxLayout(orientation="vertical",
                                     size_hint=(0.3, 1),
                                     spacing=5)    # правая часть экрана
        self.top = BoxLayout(orientation="vertical")
        self.brushes = GridLayout(cols = 3, spacing=5)
        self.colors = BoxLayout(orientation="vertical")
        #self.RGB = ColorPicker()
        self.RGB = BoxLayout(orientation="vertical", spacing=0)


        self.pen = Button(text="" ,
                          background_normal='./images/Bpen.png',
                          background_down='./images/Bpen_down.png')
        self.pen.bind(on_press=self.color_pen)

        self.eraser = Button(text="" ,
                             background_normal='./images/Beraser.png',
                             background_down='./images/Beraser_down.png')
        self.eraser.bind(on_press=self.color_clean)

        self.pipette = Button(text='' ,
                              background_normal='./images/Bpipette.png',
                              background_down='./images/Bpipette_down.png')
        self.pipette.bind(on_press=self.hachy_color)

        self.undo_button = Button(text='',
                           background_normal='./images/undo.png',
                           background_down='./images/undo_down.png')
        self.undo_button.bind(on_press=self.start_undo)

        self.redo_button = Button(text='',
                           background_normal='./images/redo.png',
                           background_down='./images/redo_down.png')
        self.redo_button.bind(on_press=self.start_redo)

        self.gear_button = Button(text='',
                                  background_normal='./images/gear.png',
                                  background_down='./images/gear_down.png')
        self.gear_button.bind(on_press=self.start_settings)

        self.scale_box = BoxLayout(orientation="horizontal", size_hint = (1,0.5))
        self.scale = Slider(value=10, min=1, max=50, step=0.5)    #слайдер, меняющий размер кисти
        self.scale.bind(value = self.size_changes)
        self.scale_info = Label(text='SIZE ' + str(self.scale.value),
                                bold=True,
                                font_size='25sp',
                                size_hint=(0.5, 1))

        self.example_box = FloatLayout(size_hint=(1,0.3))
        self.example = Krug()
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)


        self.r_change = Slider(value=100, min=0, max=255, step=1, size_hint = (3,0.3))    # слайдеры, меняющие цвета
        self.r_change.bind(value=self.red)

        self.g_change = Slider(value=100, min=0, max=255, step=1, size_hint = (3,0.3))
        self.g_change.bind(value=self.green)

        self.b_change = Slider(value=100, min=0, max=255, step=1, size_hint = (3,0.3))
        self.b_change.bind(value=self.blue)

        self.a_change = Slider(value=1, min=0, max=1, step=0.01, size_hint = (3,0.3))
        self.a_change.bind(value=self.alpha)

        self.r_info = Label(text='R', color=(1, 0, 0, 1), font_size='30sp', bold=True)
        self.g_info = Label(text='G', color=(0, 1, 0, 1), font_size='30sp', bold=True)
        self.b_info = Label(text='B', color=(0, 0, 1, 1), font_size='30sp', bold=True)
        self.a_info = Label(text='A', color=(1, 1, 1, 1), font_size='30sp', bold=True)

        self.r_input = TextInput(text='100', background_normal='./images/buttonn.png',
                                 background_active='./images/buttonn.png',
                                 font_size='20sp')
        self.g_input = TextInput(text='100', background_normal='./images/buttonn.png',
                                 background_active='./images/buttonn.png',
                                 font_size='20sp')
        self.b_input = TextInput(text='100', background_normal='./images/buttonn.png',
                                 background_active='./images/buttonn.png',
                                 font_size='20sp')
        self.a_input = TextInput(text='1.0', background_normal='./images/buttonn.png',
                                 background_active='./images/buttonn.png',
                                 font_size='20sp')

        self.r = GridLayout(cols=3)
        self.g = GridLayout(cols=3)
        self.b = GridLayout(cols=3)
        self.a = GridLayout(cols=3)

        self.settings = BoxLayout(orientation="vertical",
                                  size_hint=(0.3, 0.3),
                                  pos_hint={'x':0.35 , 'y':0.34}
                                  )
        self.open = Button(text="OPEN", size_hint=(1, 1),
                           background_normal='./images/buttonn.png',
                           background_down='./images/buttonn_down.png')

        self.saving = GridLayout(cols=2, spacing=5, size_hint=(1, 0.9))  # блок про "сохранение и переименование"
        self.names = TextInput(text="file name",
                               background_normal='./images/buttonn.png',
                               background_active='./images/buttonn.png',
                               font_size='30sp',
                               # size_hint=(1, 1)
                               )
        self.names.bind(text=self.names_change)
        self.save = Button(text="SAVE",
                           font_size='20sp',
                           # size_hint=(1,1),
                           background_normal='./images/buttonn.png',
                           background_down='./images/buttonn_down.png')
        self.save.bind(on_press=self.save_img)


        #Добавление виджетов в контейнеры
        #self.top.add_widget(self.names)
        self.brushes.add_widget(self.pen)
        self.brushes.add_widget(self.eraser)
        self.brushes.add_widget(self.pipette)
        self.brushes.add_widget(self.undo_button)
        self.brushes.add_widget(self.redo_button)
        self.brushes.add_widget(self.gear_button)

        self.top.add_widget(self.brushes)
        self.space.add_widget(self.sheet)
        #self.scrolling.add_widget(self.instruments)
        #self.space.add_widget(self.scrolling)
        self.space.add_widget(self.instruments)
        self.instruments.add_widget(self.top)

        self.scale_box.add_widget(self.scale_info)
        self.scale_box.add_widget(self.scale)
        self.instruments.add_widget(self.scale_box)

        self.instruments.add_widget(self.example_box)
        self.example_box.add_widget(self.example)

        self.instruments.add_widget(self.colors)

        self.colors.add_widget(self.RGB)

        self.settings.add_widget(self.open)
        self.settings.add_widget(self.saving)
        self.saving.add_widget(self.names)
        self.saving.add_widget(self.save)

        self.r.add_widget(self.r_info)
        self.r.add_widget(self.r_input)
        self.r.add_widget(self.r_change)

        self.g.add_widget(self.g_info)
        self.g.add_widget(self.g_input)
        self.g.add_widget(self.g_change)

        self.b.add_widget(self.b_info)
        self.b.add_widget(self.b_input)
        self.b.add_widget(self.b_change)

        self.a.add_widget(self.a_info)
        self.a.add_widget(self.a_input)
        self.a.add_widget(self.a_change)

        self.RGB.add_widget(self.r)
        self.RGB.add_widget(self.g)
        self.RGB.add_widget(self.b)
        self.RGB.add_widget(self.a)

        self.global_space.add_widget(self.space)

        return self.global_space

    def size_changes(self, instanse, value):
        global brush_size
        try:
            brush_size = value
            self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)
            self.scale_info.text = 'SIZE ' + str(self.scale.value)
        except:
            pass

    def red(self, instanse, value):
        global color_red
        color_red = int(value)
        last_red = color_red
        self.r_input.text = str(color_red)
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def blue(self, instanse, value):
        global color_blue
        color_blue = int(value)
        last_blue = color_blue
        self.b_input.text = str(color_blue)
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def green(self, instanse, value):
        global color_green
        color_green = int(value)
        last_green = color_green
        self.g_input.text = str(color_green)
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def alpha(self, instanse, value):
        global alpha
        alpha = round(value,2)
        self.a_input.text = str(alpha)
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def save_img(self, instance):
        self.sheet.export_to_png(file_name + ".png")

    def color_clean(self, instanse):
        global color_red, color_green, color_blue, last_red, last_green, last_blue, flag
        flag = True # Отключение режима пипетки
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)
        self.pipette.background_normal = './images/Bpipette.png'
        if color_red != 0 and color_green != 0 and color_blue != 0:
            last_red = color_red
            last_green = color_green
            last_blue = color_blue
        color_red, color_green, color_blue = 0, 0, 0
        self.eraser.background_normal = './images/Beraser_active.png'
        self.pen.background_normal = './images/Bpen.png'

    def color_pen(self, instanse):
        global color_red, color_green, color_blue, last_red, last_green, last_blue, flag
        flag = True  # Отключение режима пипетки
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)
        self.pipette.background_normal = './images/Bpipette.png'
        color_red = last_red
        color_green = last_green
        color_blue = last_blue
        self.eraser.background_normal = './images/Beraser.png'
        self.pen.background_normal = './images/Bpen_active.png'

    def hachy_color(self, instanse):
        global flag
        if flag == True:
            flag = False
            self.pipette.background_normal = './images/Bpipette_active.png'
            self.eraser.background_normal = './images/Beraser.png'
            self.pen.background_normal = './images/Bpen.png'
        elif flag == False:
            flag = True
            self.pipette.background_normal = './images/Bpipette.png'
            self.pen.background_normal = './images/Bpen_active.png'
            self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def names_change(self, instanse, value):
        global file_name
        file_name = value

    def start_undo(self, instanse):
        self.sheet.undo()
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def start_redo(self, instanse):
        self.sheet.redo()
        self.example.draw_krug(color_red, color_green, color_blue, alpha, brush_size)

    def start_settings(self, instanse):
        global settings_on
        if not settings_on:
            self.global_space.add_widget(self.settings)
            self.gear_button.background_normal = './images/gear_down.png'
            settings_on = True
        else:
            self.global_space.remove_widget(self.settings)
            self.gear_button.background_normal = './images/gear.png'
            settings_on = False

if __name__ == "__main__":
    MyApp().run()