from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.core.window import Window
from kivy.app import App

import os 
import subprocess

class SetupPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.maximize()
        Window.bind(on_resize=self.windowresize)
        self.cols = 3
        self.password = ""
        self.passwordinput = TextInput(multiline=True,readonly=True,width=55,font_size=25,background_color="black",foreground_color="white")
        self.add_widget(self.passwordinput)
        self.add_widget(Label(text=''))
        self.add_widget(Label(text='Set Code'))
        self.deletebutton = Button(text="Clear",background_color="limegreen",background_normal="")
        self.deletebutton.bind(on_press=self.deletebuttons)
        self.add_widget(self.deletebutton)
        self.enterbutton = Button(text="Enter",background_color="limegreen",background_normal="")
        self.enterbutton.bind(on_press=self.enterpassword)
        self.add_widget(self.enterbutton)
        for i in range(10):
            btn = Button(background_color="dimgrey",background_normal="",text=str(i))
            btn.bind(on_press=self.numberpress)
            self.add_widget(btn)
    def deletebuttons(self, instance):
        self.passwordinput.text = ''
        self.password = ''
    def numberpress(self, instance):
        self.password += instance.text
        self.passwordinput.text = self.password
    def enterpassword(self, _):
        password = str(self.password).encode()
        currentdir = os.path.abspath(os.path.dirname(__file__))
        if not os.path.exists(os.path.join(currentdir, "password")):
            os.mkdir(os.path.join(currentdir, "password"))
        if password:
            with open(os.path.join(currentdir,"password/pass.txt"), "wb") as f:
                f.write(password)
        else:
            ()
        App.get_running_app().stop()
    def windowresize(self, window, width, height):
        if width > height:
            self.screen.orientation = 'landscape'
        else:
            self.screen.orientation = 'portrait'

class Calc(App):
    def build(self):
        Window.maximize()
        Window.bind(on_resize=self.windowresize)
        currentd = os.path.abspath(os.path.dirname(__file__))
        if os.path.exists(os.path.join(currentd, "password/pass.txt")):
            self.title="K3Tree"
            self.icon="images/k3t.png"
            self.endb = None
            self.enda=None
            self.pass2 = ""
            self.calcs = ["+","-","*","/"]
            self.solution=TextInput(foreground_color="white",background_color="black",halign="right",font_size=60,height=55,readonly=True,multiline=True)
            self.mainpage=BoxLayout(orientation="vertical")
            self.mainpage.add_widget(self.solution)

            chars=[["/",".","0","C"],
                   ["*","7","8","9"],
                   ["-","4","5","6"],
                   ["+","1","2","3"],]
            
            for row in chars:
                spage=BoxLayout()
                for label in row:
                    if label in self.calcs:
                        click=Button(text=label,pos_hint={"center_x":0.5,"center_y":0.5},background_color="limegreen",background_normal="",font_size=30,) 
                    else:
                     click=Button(text=label,pos_hint={"center_x":0.5,"center_y":0.5},background_color="black",background_normal="",font_size=30)
                    click.bind(on_press=self.pressing)
                    spage.add_widget(click)
                self.mainpage.add_widget(spage)

            equals=Button(
                text="=",font_size=30,background_color="limegreen",background_normal="",
                pos_hint={"center_x":0.5,"center_y":0},
                size_hint=(1, 0.8)
            )
            equals.bind(on_press=self.results)
            self.mainpage.add_widget(equals)

            return self.mainpage 
        else:
            return SetupPage()

    def results(self, instance):   
        try:
            chars = self.solution.text
            if chars:
                over = str(eval(self.solution.text))
                self.solution.text = over
                if self.pass2 == self.getpassword():
                    currentd = os.path.abspath(os.path.dirname(__file__))
                    filename = "sub.py"
                    paths = os.path.join(currentd, filename)
                    subprocess.Popen(["python", paths])
        except (SyntaxError, ZeroDivisionError, NameError):
            self.solution.text = "Error"

    def windowresize(self, window, width, height):
        if width > height:
            self.screen.orientation = 'landscape'
        else:
            self.screen.orientation = 'portrait'

    def pressing(self,instance):
        r = self.solution.text
        charb = instance.text
        if charb=="C":
            self.solution.text=""
            self.pass2 = ""
        else:
            if r and (self.endb and charb in self.calcs):
                return
            elif r=="" and charb in self.calcs:
                return
            else:
                solid=r+charb
                self.solution.text=solid
                self.pass2 += charb
        self.enda=charb
        self.endb=self.enda in self.calcs
    def getpassword(self):
        currentd = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(currentd,"password/pass.txt"), "rb") as f:
            return f.read().decode()
        
            
class MyApp(App):
    def build(self):
        currentdirect = os.path.abspath(os.path.dirname(__file__))
        if os.path.exists(os.path.join(currentdirect, "password/pass.txt")):
            return Calc()
        else:
            return SetupPage()
if __name__ == "__main__":
    Calc().run()  
