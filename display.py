from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')
Config.set('kivy', 'exit_on_escape', 1)

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import *

from os import listdir
from os.path import isfile, join, isdir
import random
import time

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

        self.initialise()

        self.generateExperimentSequence(self.session_folder)
        self.showSplash(self.title)

    def initialise(self):
        self.autorun = False
        self.current_pair = 0
        self.title = "TITLE HERE"
        self.session_folder = "./session-1"
        self.session_name = "session 1"
        self.datetime = time.strftime("%d/%m/%y %H:%M:%S")

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (self.autorun):
            self.autorun = False
        else:
            self.autorun = True
            self.mainLoopForward()
                    
    def showImage(self, src):
        self.canvas.clear()
        self.drawText(str(self.current_pair)+self.next_media,self.image_size/15,30,self.max_height*9/10,0.7,0.7,0.7,1)
        with self.canvas:
            Rectangle(source=src,pos=(self.margin,0), size=(self.image_size,self.image_size))

    def showBlank(self):
        self.canvas.clear()

    def showVote(self):
        self.canvas.clear()
        self.drawText("Please VOTE",self.image_size/10,self.max_width/3,self.max_height/2,1,1,1,1)
        self.drawText("No: "+str(self.current_pair), self.image_size/15,self.max_width/3, self.max_height/3,1,1,1,1)

        if (not self.autorun):
            self.drawText("Autorun is off. Press any key to continue..", self.image_size/25,40,40,0.5,0.5,0.5,1)
        
    def showSplash(self,title):
        self.canvas.clear()
        self.drawText(title,self.image_size/15,50,2*self.max_height/3,1,1,1,1)
        self.drawText("Double Stimulus Impairment Scale Test (DSIST)", self.image_size/20,50,self.max_height/2,0.8,0.8,0.8,1)
        self.drawText("DSIST Evaluation Test Bench. Copyright 2017 Wattanit Hotrakool. (Licensed under GNU GPL 3)", self.image_size/40,50,50,0.6,0.3,0.3,1)
        self.drawText(self.datetime, 30, self.max_width-300, self.max_height-70,0.5,0.5,0.5,1)
        
    def showEnd(self):
        self.canvas.clear()
        self.drawText("The End", self.image_size/10, self.max_width/3, self.max_height/2,1,1,1,1)
        self.drawText("Thank you for your cooperation", self.image_size/20, self.max_width/3, self.max_height/3,0.6,0.3,0.3,1)

    def drawText(self,text,size,x,y,r,g,b,a):
        label = Label(text=text, font_size=size, color=(r,g,b,a))
        label.refresh()
        texture = label.texture
        texture_size = list(texture.size)
        with self.canvas:
            Rectangle(texture=texture, pos=(x,y), size=texture_size)
        

    def generateExperimentSequence(self, PATH):
        self.experiment_sequence = []

        samples_sets = [f for f in listdir(PATH) if isdir(join(PATH,f))]

        for samples_set in samples_sets:
            set_files = [f for f in listdir(PATH+"/"+samples_set) if f.endswith(".bmp")]
    
            if "original.bmp" in set_files:
                set_files.remove("original.bmp")
            else:
                print "Warning: no original file. Skipping this set"
                continue

            for item in set_files:
                l = [PATH+"/"+samples_set+"/original.bmp", PATH+"/"+samples_set+"/"+item]
                random.shuffle(l)
                self.experiment_sequence.append(l)

        random.shuffle(self.experiment_sequence)

    def mainLoopForward(self):
        self.current_pair = self.current_pair+1
        if (len(self.experiment_sequence) < 1):
            self.autorun = False
            self.showEnd()
            return
        pair = self.experiment_sequence.pop()
        self.mediaA = pair[0]
        self.mediaB = pair[1]
        self.next_media = "A"
        event_1 = Clock.schedule_once(self.mainLoopDelay,0) # A
        event_2 = Clock.schedule_once(self.mainLoopDelay,5) # Blank
        event_3 = Clock.schedule_once(self.mainLoopDelay,8) # B
        event_4 = Clock.schedule_once(self.mainLoopDelay,13)# Blank
        event_5 = Clock.schedule_once(self.mainLoopDelay,16)# A
        event_6 = Clock.schedule_once(self.mainLoopDelay,21)# Blank
        event_7 = Clock.schedule_once(self.mainLoopDelay,24)# B
        event_8 = Clock.schedule_once(self.mainLoopBreak,29)# End pair
                
    def mainLoopDelay(self,dt):
        if (self.next_media == "A"):
            self.showImage(self.mediaA)
            self.next_media = "AtoB"
        elif (self.next_media == "B"):
            self.showImage(self.mediaB)
            self.next_media = "BtoA"
        else:
            self.showBlank()
            if (self.next_media=="AtoB"):
                self.next_media = "B"
            else:
                self.next_media = "A"

    def mainLoopBreak(self,dt):
        self.showVote()
        print "Please vote now"
        if (self.autorun):
            event = Clock.schedule_once(self.mainLoopRestart,10)

    def mainLoopRestart(self,dt):
        self.mainLoopForward()
                
            
class Display(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    
    Display().run()
