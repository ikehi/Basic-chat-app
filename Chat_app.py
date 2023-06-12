import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime

kivy.require("2.0.0")

# Kivy Builder strings
kv_string = """
<LoginScreen>:
    BoxLayout:
        orientation: "vertical"

        Label:
            text: "Enter your name:"

        TextInput:
            id: input_text
            multiline: False

        Button:
            text: "Login"
            on_release: root.login(input_text.text)
"""

kv_string += """
<UserSelectionScreen>:
    BoxLayout:
        orientation: "vertical"

        Label:
            text: "Select a user to message:"

        Button:
            text: "User 1"
            size_hint_y: None
            height: 50
            on_release: root.select_user(self.text)

        Button:
            text: "User 2"
            size_hint_y: None
            height: 50
            on_release: root.select_user(self.text)

        Button:
            text: "User 3"
            size_hint_y: None
            height: 50
            on_release: root.select_user(self.text)
"""

kv_string += """
<ChatScreen>:
    BoxLayout:
        orientation: "vertical"

        ScrollView:
            BoxLayout:
                id: message_layout
                orientation: "vertical"
                size_hint_y: None
                spacing: 10
                padding: (10, 10)

        TextInput:
            id: input_text
            size_hint_y: None
            height: 50
            multiline: False
            on_text_validate: root.send_message()

        Button:
            text: "Send"
            size_hint_y: None
            height: 50
            on_release: root.send_message()

        BoxLayout:
            size_hint_y: None
            height: 50
            padding: (10, 10)

            Button:
                text: "Back"
                on_release: root.go_to_user_selection()
"""


# Declare screens

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def login(self, username):
        app = App.get_running_app()
        app.username = username
        app.screen_manager.current = 'user_selection'


class UserSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(UserSelectionScreen, self).__init__(**kwargs)

    def select_user(self, selected_user):
        app = App.get_running_app()
        app.selected_user = selected_user
        app.screen_manager.current = 'chat'
        app.screen_manager.get_screen('chat').selected_user = selected_user



from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

from datetime import datetime

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)

        self.messages = {}
        self.selected_user = ''

        layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView()
        layout.add_widget(self.scroll_view)

        self.message_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=(10, 10))
        self.scroll_view.add_widget(self.message_box)

        self.message_layouts = {}
        self.create_message_layout(self.selected_user)  # Create the initial message layout

        self.input_text = TextInput(size_hint_y=None, height=50, multiline=False, on_text_validate=self.send_message)
        layout.add_widget(self.input_text)

        send_button = Button(text='Send', size_hint_y=None, height=50)
        send_button.bind(on_release=self.send_message)
        layout.add_widget(send_button)

        nav_layout = BoxLayout(size_hint_y=None, height=50, padding=(10, 10))
        back_button = Button(text='Back')
        back_button.bind(on_release=self.go_to_user_selection)
        nav_layout.add_widget(back_button)
        layout.add_widget(nav_layout)

        self.add_widget(layout)

        self.send_initial_message(f"Hi {App.get_running_app().username}!")

    def create_message_layout(self, user):
        message_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=(10, 10))
        self.message_layouts[user] = message_layout

    def send_initial_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        label = Label(text=formatted_message, size_hint_y=None, height=30, markup=True, halign='left')

        if self.selected_user.lower() in self.message_layouts:
            self.message_layouts[self.selected_user].add_widget(label)
            self.message_box.add_widget(self.message_layouts[self.selected_user])
            self.scroll_view.scroll_to(label)

    def send_message(self, _=None):
        message = self.input_text.text.strip()
        if message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            label = Label(text=formatted_message, size_hint_y=None, height=30, markup=True, halign='left')

            # Check if the message is from the selected user
            if self.selected_user.lower() in self.message_layouts:
                self.message_layouts[self.selected_user].add_widget(label)
                self.scroll_view.scroll_to(label)
            else:
                # Create a new message layout for the user and add the label
                self.create_message_layout(self.selected_user)
                self.message_layouts[self.selected_user].add_widget(label)
                self.message_box.add_widget(self.message_layouts[self.selected_user])
                self.scroll_view.scroll_to(label)

            # Add the message to the user's message dictionary
            if self.selected_user not in self.messages:
                self.messages[self.selected_user] = []
            self.messages[self.selected_user].append(formatted_message)

            self.input_text.text = ''

    def go_to_user_selection(self, _=None):
        self.input_text.text = ''
        self.manager.current = 'user_selection'





class ChatApp(App):
    username = ''

    def build(self):
        self.screen_manager = ScreenManager()

        Builder.load_string(kv_string)

        login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(login_screen)

        user_selection_screen = UserSelectionScreen(name='user_selection')
        self.screen_manager.add_widget(user_selection_screen)

        chat_screen = ChatScreen(name='chat')
        self.screen_manager.add_widget(chat_screen)

        return self.screen_manager

    def on_stop(self):
        # Clean up resources or perform any necessary actions when the app is closed
        pass


if __name__ == '__main__':
    ChatApp().run()
