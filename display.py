from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'exit_on_escape', 1)

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import *



class Main(Widget):
    
    def __init__(self, **kwargs):
        super(Main,self).__init__(**kwargs)

        self.max_width =Window.width
        self.max_height =Window.height
        if (self.max_width > self.max_height):
            self.image_size = self.max_height
            self.margin = (self.max_width-self.image_size)/2
        else:
            self.image_size = self.max_width
            self.margin = (self.max_height-self.image_size)/2

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.showImage('./session-1/1/original.bmp')

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print keycode[1]
        self.showBlank()
        
            
    def showImage(self, src):
        self.canvas.clear()
        with self.canvas:
            Rectangle(source=src,pos=(self.margin,0), size=(self.image_size,self.image_size))

    def showBlank(self):
        self.canvas.clear()




            
class Display(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    
    Display().run()
