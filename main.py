import sqlite3
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
from kivy.properties import StringProperty
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDRoundFlatButton
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import sqlite3 as sql

kivy.config.Config.set('graphics', 'resizable', True)
Window.size = (360, 640)  # (720, 1280)


class LoginScreen(Screen):

    email = ObjectProperty
    passw = ObjectProperty
    avatar = ObjectProperty

    def hide(self):
        if self.passw.password == True:
            self.passw.password =False

        elif self.passw.password == False:
            self.passw.password = True


    def sign_in(self):

        try:
            con = sqlite3.connect('devis.db')
            cur = con.cursor()
            m = cur.execute("""
            SELECT * FROM id WHERE emailreg LIKE "{}" AND passwreg LIKE "{}";""".format(self.ids.email.text, self.ids.passw.text))
            for x in m:
                username = x[1]
                firstname = x[2]
                surname = x[3]
                city = x[4]
                email = x[5]
                avatar = x[9]

            print(username)
            print(firstname)
            print(surname)
            print(city)
            print(email)

            # with open('Avatar.png', 'wb') as f:
            #     f.write(avatar)
            self.parent.current = 'profile'
            self.parent.transition.direction = 'left'

        except:
            layout = BoxLayout(orientation='vertical')
            labelError = Label(text='Email is not registered!')
            layout.add_widget(labelError)
            self.pop = Popup(title='Error!', background_color='navy',
                             content=layout,
                             size_hint=(None, None), size=(650, 250),
                             on_touch_down=Popup.dismiss)
            self.pop.open()


class RegistrationScreen(Screen):
    email = ObjectProperty
    passwreg = ObjectProperty
    username = ObjectProperty
    firstname = ObjectProperty
    surname = ObjectProperty
    country = ObjectProperty
    emailreg = ObjectProperty
    male = ObjectProperty
    female = ObjectProperty
    photo = ObjectProperty

    def add_to_database(self):
        with open('Avatar.png', 'rb') as f:
            self.avatar = f.read()

        con = sql.connect('devis.db')
        cur = con.cursor()
        cur.execute(""" INSERT INTO id (username,firstname,surname,country,emailreg,passwreg,male,female,avatar) VALUES (?,?,?,?,?,?,?,?,?)""",
                    (self.username.text, self.firstname.text, self.surname.text, self.country.text, self.emailreg.text, self.passwreg.text,
                     self.male.state, self.female.state, self.avatar))
        con.commit()
        con.close()


    def hide(self):
        if self.passwreg.password == True:
            self.passwreg.password = False

        elif self.passwreg.password == False:
            self.passwreg.password = True

    def take_photo(self):
        layout = BoxLayout(orientation='vertical')
        layout1 = BoxLayout(orientation='horizontal', spacing=100)
        self.image = Image()
        layout.add_widget(self.image)
        self.close_window = MDRoundFlatButton(text='X',
                                              pos_hint={'center_x': .5, 'center_y': .5},
                                              size_hint=(None, None))

        self.close_window.bind(on_press=self.closeWindow)
        layout1.add_widget(self.close_window)

        self.save_img = MDRoundFlatButton(text='Take Photo',
                                         pos_hint={'center_x': .5, 'center_y': .5},
                                         size_hint=(None, None))

        self.save_img.bind(on_press=self.take_picture)
        layout1.add_widget(self.save_img)

        layout.add_widget(layout1)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.load_video, 1.0/30.0)
        self.pop = Popup(title='Smile!', background_color='white',
                         content=layout,
                         size_hint=(None, None), size=(600, 800))
                         #on_touch_down=Popup.dismiss)
        self.pop.open()
        return layout

    def load_video(self, *args):
        ret, frame = self.capture.read()
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture


    def take_picture(self, *args):
        image_name = 'Avatar.png'
        cv2.imwrite(image_name, self.image_frame)

    def closeWindow(self, obj):
        self.pop.dismiss()
        #self.capture.release()
        #cv2.destroyAllWindows()

    def registration_complete(self):
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Welcome, '+self.username.text+'!', font_size='18dp', halign="center")
        layout.add_widget(label)
        self.pop = Popup(title='Registration Successful!', title_align="center", background_color='navy',
                         content=layout,
                         size_hint=(None, None), size=(450, 200),
                         on_touch_down=Popup.dismiss)
        self.pop.open()



class ProfileScreen(Screen):
    email = ObjectProperty
    passw = ObjectProperty

    # def log_out(self):
    #     self.email.text = ""
    #     self.passw.text = ""


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

    con = sql.connect('devis.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE  IF NOT EXISTS  id(
        UserID integer PRIMARY KEY,
        username text,
        firstname text,
        surname text,
        country text,
        emailreg text,
        passwreg text,
        male state,
        female state,
        avatar BLOB)
        """)
    con.commit()
    con.close()


if __name__ == "__main__":
    LoginRegForm().run()
