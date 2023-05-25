#setting the maxfps to 120fps / 最大fpsを120fpsに設定
from kivy.config import Config
Config.set('graphics', 'maxfps', '120')


from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.button import MDIconButton
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.modalview import ModalView
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
from plyer import filechooser


import os
#adding Japanese Filename support via Official Google Fonts / 公式グーグルフォントで日本語ファイルネームのサポート追加
# Link/リンク (https://fonts.google.com/noto/specimen/Noto+Sans+JP)
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
fontfolder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "font")
resource_add_path(fontfolder)
LabelBase.register(DEFAULT_FONT, 'NotoSansJP-Black.otf')

import shutil

class mainApp(MDApp):
    def build(self):
        self.title="Gallery Vault"
        self.icon="images/vault.png"

        Window.maximize()
        Window.bind(on_resize=self.windowresize)

        self.screen = Screen()
        self.selectedimages = []
        self.imagepaths = []
        self.checkboxlist = []

        mainfold = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mainfolder")

        for filename in os.listdir(mainfold):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
                self.imagepaths.append(os.path.join(mainfold, filename))
            elif filename.endswith('.mp4') or filename.endswith('.avi') or filename.endswith('.mov'):
                self.imagepaths.append(os.path.join(mainfold, filename))

        self.currentimage = 0  
        box = MDBoxLayout(orientation="vertical", size_hint_y=None, padding=50, spacing=30)
        scrollview = ScrollView()
        box.bind(minimum_height=box.setter('height')) 

        for filename in os.listdir(mainfold):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif') or filename.endswith(".mp4") or filename.endswith('.avi') or filename.endswith('.mov'):
                layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=50,width=50)
                extension = os.path.splitext(filename)[1]
                modifiedfilename = f"{filename[:10]}..{extension}" if len(filename) > 10 else filename
                
                label = MDLabel(text=modifiedfilename, size_hint_x=0.7,halign="left")
                layout.add_widget(label)
                
                checkbox = MDCheckbox(size_hint_x=None, width=50, opacity=0)
                checkbox.bind(active=self.checkboxactive)
                layout.add_widget(checkbox)
                self.checkboxlist.append(checkbox)
                
                box.add_widget(layout)
                
                if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
                    image = AsyncImage(source=os.path.join("mainfolder", filename), allow_stretch=True, keep_ratio=False, size_hint_x=None, width=50, height=50, pos_hint={ "right": 0 })
                    layout.add_widget(image)
                    image.bind(on_touch_down=self.imagepressed)
                if filename.endswith('.mp4') or filename.endswith('.avi') or filename.endswith('.mov'):
                    video=MDIconButton(icon="video",  icon_size="25sp")
                    layout.add_widget(video)
                    video.bind(on_release=lambda instance, video_path=os.path.join("mainfolder", filename): self.showvideo(video_path))
        
        scrollview.add_widget(box)
        
        self.screen.add_widget(scrollview)
        
        toolbar = MDBoxLayout(size_hint_y=None, height=50, padding=0, spacing=50, md_bg_color=[0.3, 0.2, 0.1, 1.0])
        
        buttonc=Button(text="RESET",size_hint_y=1,size_hint_x=0.4,background_color="limegreen",on_release=self.res)
        buttona = Button(text="+",size_hint_y=1, size_hint_x=0.3, background_color="limegreen")
        buttona.bind(on_release=self.openfilechooser)
        buttonb = Button(halign="left",text="x", size_hint_x=0.3,size_hint_y=1, background_color="limegreen", on_release=self.showcheckbox)
        
        toolbar.add_widget(buttonc)
        toolbar.add_widget(buttonb)
        toolbar.add_widget(buttona)

        self.screen.add_widget(toolbar)

        return self.screen
    
    def res(self, *args):
        currentdir = os.path.abspath(os.path.dirname(__file__))
        os.remove(os.path.join(currentdir, "password/pass.txt"))
        MDApp.get_running_app().stop()

    def showvideo(self, video_path):
        videoplayer = VideoPlayer(source=video_path, state='pause', options={'allow_stretch': True, 'eos': 'loop'}, allow_fullscreen=False)
        view = ModalView(size_hint=(1, 1))
        layout = FloatLayout(size=(1, 1))
        view.add_widget(layout)
        layout.add_widget(videoplayer)

        def toggleexit(*args):
            if exitbutton.opacity == 1:
                exitbutton.opacity = 0
            else:
                exitbutton.opacity = 1
        
        exitbutton = MDFlatButton(text="Exit", size_hint=(None, None), height=0.5, padding=0.5, pos_hint={'x': 0.01, 'y': 0.925}, md_bg_color="skyblue")        
        exitbutton.bind(on_press=view.dismiss)

        layout.add_widget(exitbutton)
        videoplayer.bind(on_touch_down=toggleexit)

        view.on_dismiss = lambda: self.viddismiss(videoplayer, view)
        view.open()

    def viddismiss(self,videoplayer,view):
       videoplayer.state="stop"
       view.content=None
       view=None

    def imagepressed(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.imagefullscreen(instance.source)

    def imagefullscreen(self, image_path):
        fullscreen = AsyncImage(source=image_path, size_hint=(None, None), size=(Window.width, Window.height))
        view = ModalView(size_hint=(1, 1))
        layout = FloatLayout(size=(1, 1))
        view.add_widget(layout)
        layout.add_widget(fullscreen)

        def toggleexit(*args):
            if buttonback.opacity == 1:
                buttonback.opacity = 0
            else:
                buttonback.opacity = 1

        buttonback = MDFlatButton(text="Exit", size_hint=(None, None), height=0.5, padding=0.5, pos_hint={'x': 0.01, 'y': 0.925}, md_bg_color="skyblue")        
        buttonback.bind(on_press=view.dismiss)
        
        view.bind(on_touch_down=toggleexit)
        layout.add_widget(buttonback)
        view.on_dismiss = lambda: self.virismiss(view)
        view.open()

    def virismiss(self,view):
       view.content=None
       view=None

    def windowresize(self, Window, width, height):
        if width > height:
            self.screen.orientation = 'landscape'
        else:
            self.screen.orientation = 'portrait'

    def checkboxactive(self, checkbox, value):
     if value:
        index = self.checkboxlist.index(checkbox)
        if self.checkboxlist[index].opacity != 0: 
            os.remove(self.imagepaths[index])
            del self.imagepaths[index]
            self.checkboxlist.remove(checkbox)
            checkbox.parent.parent.remove_widget(checkbox.parent)

    def showcheckbox(self, instance):
        for checkbox in self.checkboxlist:
            checkbox.visible = False
            if checkbox.opacity == 0:
                checkbox.opacity = 1
            else:
                checkbox.opacity = 0

    def openfilechooser(self, instance):
        filechoose = filechooser.open_file(title="Select", multiple=True)
        mfolder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mainfolder")

        for file in filechoose:
            try:
                shutil.copy(file, os.path.join(mfolder, os.path.basename(file)))
            except shutil.SameFileError:
                pass

        self.screen.clear_widgets()
        self.stop()
        mainApp().run()

mainApp().run()
