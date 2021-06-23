import kivy
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDRoundFlatButton
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture


kivy.config.Config.set('graphics', 'resizable', True)
Window.size = (360, 640)  # (720, 1280)


class LoginScreen(Screen):
    email = ObjectProperty
    passw = ObjectProperty

    def hide(self):
        if self.passw.password == True:
            self.passw.password =False

        elif self.passw.password == False:
            self.passw.password = True

    def login(self):
        layout = BoxLayout(orientation='vertical')
        image = Image(source='images/6.png')
        labelEmail = Label(text='Email: '+self.email.text)
        labelPass = Label(text='Password: ' + self.passw.text)

        layout.add_widget(image)
        layout.add_widget(labelEmail)
        layout.add_widget(labelPass)
        self.pop = Popup(title='Done!', background_color='navy',
                         content=layout,
                         size_hint=(None, None), size=(650, 1200),
                         on_touch_down=Popup.dismiss)
        self.pop.open()

    # def closePopUp(self, obj):
    #     self.pop.dismiss()


class RegistrationScreen(Screen):
    email = ObjectProperty
    passwreg = ObjectProperty

    def hide(self):
        if self.passwreg.password == True:
            self.passwreg.password = False

        elif self.passwreg.password == False:
            self.passwreg.password = True

    def take_photo(self):
        layout = BoxLayout(orientation='vertical')
        self.image = Image()
        layout.add_widget(self.image)
        self.save_img = MDRoundFlatButton(text='Take Photo',
                                         pos_hint={'center_x': .5, 'center_y': .5},
                                         size_hint=(None, None))

        self.save_img.bind(on_press=self.take_picture)
        layout.add_widget(self.save_img)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        self.pop = Popup(title='Smile!', background_color='white',
                         content=layout,
                         size_hint=(None, None), size=(650, 600),
                         on_touch_down=Popup.dismiss)
        self.pop.open()
        #self.capture.release()
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


    def take_picture(self, *args):
        image_name = 'picture.png'
        cv2.imwrite(image_name, self.image_frame)
        # self.capture.release()


class ProfileScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(RegistrationScreen(name='registration'))
sm.add_widget(ProfileScreen(name='profile'))

class MyToggleButton(MDFillRoundFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_down = self.theme_cls.primary_light

class LoginRegForm(MDApp):

    def build(self):

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'DeepPurple'
        screen = Builder.load_file('my.kv')
        return screen



if __name__ == "__main__":
    LoginRegForm().run()
