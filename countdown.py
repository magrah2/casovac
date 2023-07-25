from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FallOutTransition
import os
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import datetime
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader

from kivy.config import Config
Config.set('graphics', 'width', '2736')
Config.set('graphics', 'height', '1824')
Config.write()

from kivy.uix.floatlayout import FloatLayout
import sys
Window.fullscreen = True
Window.maximize()https://kivy.org/doc/stable/guide/environment.html

######
# How to use?
# ===========
#
# start script like: python timer.py 5m
# This will set the timer to 5minutes.
#
# Syntax: timer.py <minutes>m
######
#sound = SoundLoader.load("C:/Users/magvr/Documents/Scripts/VAH/Gong-sound.wav")

for arg in sys.argv:
    if arg.endswith("m"):
        sys.argv.remove(arg)  # remove this arg - so kivy will not get it
        countdown = int(arg.split("m")[0])
    else:
        countdown = 0


Builder.load_string("""
<MainLayout>:
    button: button
    Button:
        id: button
        on_press: root.toggle()
    AnchorLayout:
        Label:
            text: "%s:%s" % (root.minutes, root.seconds)
            font_size: root.width/3
""")



class MainLayout(Screen):
    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.start_time = datetime.datetime.now()
        self.total_elapsed_time = datetime.timedelta(0)
        Window.bind(on_key_down=self.on_keyboard_handler)
        self.button.background_color = (0,0,0,1)
        self.update()
        
    

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.datetime.now()
            Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        if self.running:
            self.running = False
            self.total_elapsed_time += datetime.datetime.now() - self.start_time
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        if self.running:
            elapsed_time = self.total_elapsed_time + (datetime.datetime.now() - self.start_time)
        else:
            elapsed_time = self.total_elapsed_time

        minutes, seconds = str(elapsed_time).split(":")[1:]
        self.minutes = minutes
        self.seconds = seconds[:2]
        
        #if int(self.minutes) == 0:
        #    if int(self.seconds.split(".")[0]) == 0:
        #        if int(self.seconds.split(".")[0]) < 2:
        #            self.seconds = "00"
        #            self.button.background_color = (1,0,0,1)
        #            self.stop()
#      if (int(self.minutes)%5) == 0:
 #           if float(seconds) < 0.1:
#                    sound.play()


    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def on_keyboard_handler(self, instance, keyboard, keycode, text, modifiers):
        #print(keycode)
        #print(countdown)
        if keycode == 40 or keycode == 88 or keycode == 44:  # 40 - Enter key pressed
            self.toggle()

#kv = Builder.load_file("layout.kv")



if __name__ == '__main__':

    class TimerApp(App):
        def build(self):
            return MainLayout()

    TimerApp().run()