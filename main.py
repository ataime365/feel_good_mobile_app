# The Kivy App
from kivy.app import App #import class from kivy.app python file
from kivy.lang import Builder #This is what we would use to link the python backend logic to the front end gui
from kivy.uix.screenmanager import ScreenManager, Screen #importing classes
# from kivy.uix.gridlayout import GridLayout #If we were to use python alone to build, instead of python and kivy 
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen): #Screen is the base class here, LoginScreen is the sub class
    def sign_up(self):
        self.manager.current = "sign_up_screen" #screen_name #To navigate to another screen
    def login_success(self, uname, pword):
        with open('users.json') as f: #default is read mode
            users = json.load(f) #This becomes the dictionary
        all_users = [(v.get('username'), v.get('password')) for k,v in users.items()]
        if (uname, pword) in all_users:
            self.manager.current = "login_screen_success" #to Transition
        else:
            self.ids.login_wrong.text = "Wrong Username or Password!!"
            # print('Username or Password is Invalid')

class RootWidget(ScreenManager): #ScreenManager is the base class here
    pass

class SignUpScreen(Screen):
    
    def add_user(self, uname, pword):
        #if there was already an existing database
        with open('users.json') as f:
            users = json.load(f) #This becomes the dictionary
        today = datetime.now()
        users[uname] = {'username': uname, 'password':pword,
            'created': today.strftime("%Y-%m-%d %H:%M:%S")}
        print(users)
        with open('users.json', 'w') as f: #The write 'w' method creates a new file, but still retains previous data, because we loaded the data earlier
            f.write(json.dumps(users))
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def login_page(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen" #To navigate

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    #Limit the use of for loops inside functions, because functions already acts like a for loop
    def get_quotes_function(self, original_text): #Enlighten me button
        available_files_name_list = [Path(file).stem for file in glob.glob("Files/*.txt")]#glob is used to get relative file paths
        
        if original_text.lower() in available_files_name_list:
            with open('Files/'+original_text.lower()+'.txt', 'r', encoding='utf-8') as f:
                quotes_list = f.readlines() #readlines produces a list

            self.ids.original_text_label_id.text = random.choice(quotes_list) #random.choice takes a list #so it will choose one from the list
        else:
            self.ids.original_text_label_id.text = 'Try another feeling'


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App): #The subclass 'MainApp' has all attributes of the base class 'App'
    def build(self): #build is a method from App, check documentation using python shell
        return RootWidget() #returning the root widget class
     
     
if __name__ == "__main__":
    MainApp().run() #run is an attribute of App