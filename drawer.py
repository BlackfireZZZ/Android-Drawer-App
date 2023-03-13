from kivy.app import App
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line, Fbo
from kivy.core.image import Image
from kivy.uix.slider import Slider
import struct
Window.size = (1280, 840)
#размер экрана моего телефона 2400x1080

Flag = True
brush_size = 5
color_red = 1
color_green = 0
color_blue = 0
last_red = color_red
last_green = color_green
last_blue = color_blue
flag = True

class drawer(Widget):
    def __init__(self):
        super(drawer, self).__init__()
    def on_touch_down(self, touch):
        global color_green, color_red, color_blue,last_red,last_green,last_blue,flag
        try:
            if touch.x < Window.size[0] * 0.725:
                if flag == True:
                    self.canvas.add(Color(color_red, color_green, color_blue, 1))
                    self.line = Line(width=brush_size, close=False)
                    self.canvas.add(self.line)
                    self.line.points += (touch.x, touch.y)
                    self.line.points += (touch.x, touch.y -1 )
                elif flag == False:
                    a = self.export_as_image()
                    pixel = a.texture.get_region(touch.x,Window.height-touch.y, 1, 1)
                    bp = pixel.pixels
                    data = struct.unpack('4B', bp)
                    color_red, last_red = round(data[0]/255,1),round(data[0]/255,1)
                    color_green,last_green = round(data[1]/255,1),round(data[1]/255,1)
                    color_blue, last_blue = round(data[2]/255, 1), round(data[2]/255, 1)
                    Krug.example.draw_krug(self, color_red, color_green, color_blue, brush_size)
        except Exception as e:
            print(e)
    def on_touch_move(self, touch):
        try:
            if flag == True:
                if touch.x < Window.size[0] * 0.725:
                    self.line.points += (touch.x, touch.y)
        except:
            pass
    def saver(self, filename):
        pass

class Krug(drawer):
    def __init__(self):
        super(Krug, self).__init__()
        self.draw_krug(color_red, color_green, color_blue, brush_size)
    def draw_krug(self,color_red, color_green, color_blue, brush_size):
        try:
            self.canvas.clear()
            self.canvas.add(Color(color_red, color_green, color_blue, 1))
            self.canvas.add(Ellipse(pos=(Window.size[0] * 0.885-brush_size,Window.size[1] * 0.54-brush_size),size=(brush_size*2,brush_size*2)))
        except:
            pass

class MyApp(App):
    def build(self):
        global color_blue, color_green, color_red
        self.space = BoxLayout(orientation="horizontal")
        self.sheet = drawer()
        self.instruments = BoxLayout(orientation="vertical", size_hint = (0.3,1), spacing=5)
        self.top = BoxLayout(orientation="vertical")
        self.brushes = GridLayout(cols = 3, spacing=5)
        self.colors = BoxLayout(orientation="vertical")
        self.RGB = BoxLayout(orientation="horizontal", spacing=10)
        self.open = Button(text="OPEN", size_hint = (1,0.6), background_normal='./images/buttonn.png',background_down='./images/buttonn_down.png')
        self.save = Button(text="SAVE", size_hint=(1,0.6), background_normal='./images/buttonn.png',background_down='./images/buttonn_down.png')
        self.save.bind(on_press=self.save_img)
        self.pen = Button(text="" , background_normal='./images/Bpen.png', background_down='./images/Bpen_down.png')
        self.pen.bind(on_press=self.color_pen)
        self.eraser = Button(text="" , background_normal='./images/Beraser.png', background_down='./images/Beraser_down.png')
        self.eraser.bind(on_press=self.color_clean)
        self.pipette = Button(text='' , background_normal='./images/Bpipette.png',background_down='./images/Bpipette_down.png')
        self.pipette.bind(on_press=self.hachy_color)
        self.names = TextInput(text = "NAME")
        self.scale = Slider(value=10, min=1, max=50, step=1, size_hint = (1,0.5))
        self.scale.bind(value = self.size_changes)
        self.example = Krug()
        self.r = Button(text=str(color_red), background_normal='./images/buttonn.png',background_down='./images/buttonn_down.png')
        self.r.bind(on_press=self.red)
        self.g = Button(text=str(color_green), background_normal='./images/buttonn.png',background_down='./images/buttonn_down.png')
        self.g.bind(on_press=self.green)
        self.b = Button(text=str(color_blue), background_normal='./images/buttonn.png',background_down='./images/buttonn_down.png')
        self.b.bind(on_press=self.blue)


        self.top.add_widget(self.names)
        self.brushes.add_widget(self.pen)
        self.brushes.add_widget(self.eraser)
        self.brushes.add_widget(self.pipette)
        self.top.add_widget(self.brushes)
        self.space.add_widget(self.sheet)
        self.space.add_widget(self.instruments)
        self.instruments.add_widget(self.top)
        self.instruments.add_widget(self.scale)
        self.instruments.add_widget(self.colors)
        self.colors.add_widget(self.example)
        self.colors.add_widget(self.RGB)
        self.instruments.add_widget(self.open)
        self.instruments.add_widget(self.save)

        self.RGB.add_widget(self.r)
        self.RGB.add_widget(self.g)
        self.RGB.add_widget(self.b)
        return self.space

    def size_changes(self, instanse, value):
        global brush_size
        try:
            brush_size = value
            self.example.draw_krug(color_red, color_green, color_blue, brush_size)
        except:
            pass
    def red(self,instanse):
        global color_green, color_red, color_blue, flag
        flag = True
        if color_red < 1:
            color_red += 0.1
            last_red = color_red
        else:
            color_red = 0
            last_red = color_red
        self.r.text = str(round(color_red,1))
        self.example.draw_krug(color_red, color_green, color_blue, brush_size)
    def green(self,instanse):
        global color_green, color_red, color_blue, flag
        flag = True
        if color_green < 1:
            color_green += 0.1
            last_green = color_green
        else:
            color_green = 0
            last_green = color_green
        self.g.text = str(round(color_green,1))
        self.example.draw_krug(color_red, color_green, color_blue, brush_size)
    def blue(self,instanse):
        global color_green, color_red, color_blue, flag
        flag = True
        if color_blue < 1:
            color_blue += 0.1
            last_blue = color_blue
        else:
            color_blue = 0
            last_blue = color_blue
        self.b.text = str(round(color_blue,1))
        self.example.draw_krug(color_red, color_green, color_blue, brush_size)

    def save_img(self, instance):
        self.sheet.export_to_png('image.png')
    def color_clean(self, instanse):
        global color_red, color_green, color_blue, last_red, last_green, last_blue, flag
        flag = True
        if color_red != 0 and color_green != 0 and color_blue != 0:
            last_red = color_red
            last_green = color_green
            last_blue = color_blue
        color_red, color_green, color_blue = 0,0,0
    def color_pen(self, instanse):
        global color_red, color_green, color_blue, last_red, last_green, last_blue, flag
        flag = True
        color_red = last_red
        color_green = last_green
        color_blue = last_blue
    def hachy_color(self,instanse):
        global flag
        if flag == True:
            flag = False
            self.pipette.background_normal = './images/Bpipette_active.png'
        elif flag == False:
            flag = True
            self.pipette.background_normal = './images/Bpipette.png'


if __name__ == "__main__":
    MyApp().run()