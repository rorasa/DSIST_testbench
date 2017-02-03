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
        self.showSplash()

    def initialise(self):
        self.autorun = False
        self.current_pair = 0
        self.title = "TITLE HERE"
        self.version_no = "0.1alpha"
        self.session_folder = "./session-1"
        self.session_name = "session-1"
        self.view_duration = 7
        self.break_duration = 3
        self.vote_duration = 10
        self.datetime = time.strftime("%d/%m/%y %H:%M:%S")
        self.session_filename = self.session_name+"-"+time.strftime("%y-%m-%d-%M-%H")+".txt"

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (keycode[1]=="d"):
            self.showDemo(-1)
            return
        
        if (self.autorun):
            print "[CONTROL] Autorun is OFF"
            self.autorun = False
        else:
            print "[CONTROL] Autorun is ON"
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
        
    def showSplash(self):
        self.consoleSplash()
        
        self.canvas.clear()
        self.drawText(self.title,self.image_size/15,50,2*self.max_height/3,1,1,1,1)
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

    def consoleSplash(self):
        print "===================================="
        print "    DSIST Evaluation Test Bench     "
        print "                                    "
        print " Version: "+self.version_no
        print " Copyright 2017 Wattanit Hotrakool  "
        print "                                    "
        print " This software is released under    "
        print " GNU General Public License v3.0    "
        print "===================================="
        print "Command key:"
        print " ESC : quit "
        print "  d  : show demo "
        print "  s  : setting (unavailable)"
        print "  r  : restart (unavailable)"
        print " Any other key : forward"
        print "===================================="
        print " Session name: "+self.session_name
        print " Date/time   : "+self.datetime
        print " Session sequence will be saved at "+ self.session_folder+"/"+self.session_filename

    def showDemo(self,dt):
        if (dt < 0):
            self.demo_step = 0

        print self.demo_step
        if (self.demo_step==9):
            self.showSplash()
            return
            
        self.canvas.clear()
        self.drawText("Guideline for evaluation", self.image_size/20,50,self.max_height*9/10,1,1,1,1)
        if (self.demo_step==0):
            self.demo_step = self.demo_step+1
            self.drawText("Please rate the quality of image B relative to image A.", self.image_size/20,70,self.max_height*8/10,1,1,1,1)
            self.drawText("81-100: difference is imperceptible", self.image_size/20,70,self.max_height*7/10,1,1,1,1)
            self.drawText("61-80: difference is perceptible but not annoying", self.image_size/20,70,self.max_height*6/10,1,1,1,1)
            self.drawText("41-60: slightly annoying", self.image_size/20,70,self.max_height*5/10,1,1,1,1)
            self.drawText("21-40: annoying", self.image_size/20,70,self.max_height*4/10,1,1,1,1)
            self.drawText("1-20 : very annoying", self.image_size/20,70,self.max_height*3/10,1,1,1,1)
            event = Clock.schedule_once(self.showDemo,10)
        elif (self.demo_step==1):
            self.canvas.add(Rectangle(source="./demo/demo1.bmp", pos=(self.margin,0), size=(self.image_size*9/10,self.image_size*9/10)))
            self.drawText("A", self.image_size/20, 50, self.max_height*7/10,0.8,0.8,0.8,1)
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.view_duration)            
        elif (self.demo_step==2):
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.break_duration)            
        elif (self.demo_step==3):
            self.canvas.add(Rectangle(source="./demo/demo2.bmp", pos=(self.margin,0), size=(self.image_size*9/10,self.image_size*9/10)))
            self.drawText("B", self.image_size/20, 50, self.max_height*7/10,0.8,0.8,0.8,1)
            self.demo_step = self.demo_step+1 
            event = Clock.schedule_once(self.showDemo,self.view_duration)           
        elif (self.demo_step==4):
            self.drawText("Vote: 0 - 20", self.image_size/20, self.max_width/3, self.max_height/2,1,1,1,1)
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.vote_duration)            
        elif (self.demo_step==5):
            self.canvas.add(Rectangle(source="./demo/demo1.bmp", pos=(self.margin,0), size=(self.image_size*9/10,self.image_size*9/10)))
            self.drawText("A", self.image_size/20, 50, self.max_height*7/10,0.8,0.8,0.8,1)
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.view_duration)            
        elif (self.demo_step==6):
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.break_duration)            
        elif (self.demo_step==7):
            self.canvas.add(Rectangle(source="./demo/demo3.bmp", pos=(self.margin,0), size=(self.image_size*9/10,self.image_size*9/10)))
            self.drawText("B", self.image_size/20, 50, self.max_height*7/10,0.8,0.8,0.8,1)
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.view_duration)            
        elif (self.demo_step==8):
            self.drawText("Vote: 61 - 80", self.image_size/20, self.max_width/3, self.max_height/2,1,1,1,1)
            self.demo_step = self.demo_step+1
            event = Clock.schedule_once(self.showDemo,self.vote_duration)
               

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
#                random.shuffle(l)  # random pair order between original and impaired
                self.experiment_sequence.append(l)

        random.shuffle(self.experiment_sequence)

    def mainLoopForward(self):
        self.current_pair = self.current_pair+1
        if (len(self.experiment_sequence) < 1):
            self.autorun = False
            print "[DISPLAY] End of Session"
            self.showEnd()
            return
        if (self.current_pair==1):
            record_file = open(self.session_folder+"/"+self.session_filename,"w")
            record_file.write("DSIST Experiment sequence\n")
            record_file.write("Title: "+self.title+"\n")
            record_file.write("Session name: "+self.session_name+"\n")
            record_file.write("Date/time: "+self.datetime+"\n")
            record_file.write("---------------------------------------------\n")
        else:
            record_file = open(self.session_folder+"/"+self.session_filename,"a")
            
        pair = self.experiment_sequence.pop()
        self.mediaA = pair[0]
        self.mediaB = pair[1]
        self.next_media = "A"

        record_file.write(str(self.current_pair)+" "+self.mediaA+" "+self.mediaB+"\n")
        record_file.close()
        
        event_1 = Clock.schedule_once(self.mainLoopDisplay,0) # A
        event_2 = Clock.schedule_once(self.mainLoopDisplay,self.view_duration) # Blank
        event_3 = Clock.schedule_once(self.mainLoopDisplay,self.view_duration+self.break_duration) # B
#        event_4 = Clock.schedule_once(self.mainLoopDisplay,2*self.view_duration+self.break_duration)# Blank
#        event_5 = Clock.schedule_once(self.mainLoopDisplay,2*self.view_duration+2*self.break_duration)# A
#        event_6 = Clock.schedule_once(self.mainLoopDisplay,3*self.view_duration+2*self.break_duration)# Blank
#        event_7 = Clock.schedule_once(self.mainLoopDisplay,3*self.view_duration+3*self.break_duration)# B
        event_8 = Clock.schedule_once(self.mainLoopBreak,2*self.view_duration+self.break_duration)# End pair
                
    def mainLoopDisplay(self,dt):
        if (self.next_media == "A"):
            print "[DISPLAY] No: "+str(self.current_pair)+self.next_media+" | "+self.mediaA
            self.showImage(self.mediaA)
            self.next_media = "AtoB"
        elif (self.next_media == "B"):
            print "[DISPLAY] No: "+str(self.current_pair)+self.next_media+" | "+self.mediaB
            self.showImage(self.mediaB)
            self.next_media = "BtoA"
        else:
            print "[DISPLAY] No: "+str(self.current_pair)+self.next_media+" | Blank ..."
            self.showBlank()
            if (self.next_media=="AtoB"):
                self.next_media = "B"
            else:
                self.next_media = "A"

    def mainLoopBreak(self,dt):
        self.showVote()
        print "[DISPLAY] No: "+str(self.current_pair)+" | VOTING SCREEN"
        if (self.autorun):
            event = Clock.schedule_once(self.mainLoopRestart,self.vote_duration)

    def mainLoopRestart(self,dt):
        self.mainLoopForward()
                
            
class Display(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    
    Display().run()
