from nicegui import events
import nicegui
from database.data import DataBase


class LoginPage(DataBase):

    def __init__(self, nicegui: nicegui) -> None:
        super().__init__()
        self.ui = nicegui.ui

    def body(self):
        with self.ui.card().style('width: 30%; margin: 0 auto; margin-top: 10%;'):
            self.ui.label('Login').style(
                'font-size: 20px; align-self: center;')
            self.username = self.ui.input(
                label='Email', placeholder='Email', on_change=self.__enable_login).style('margin-top: 10px; width: 100%;')
            self.password = self.ui.input(label='Password', placeholder='Password',
                                          password=True, password_toggle_button=True, on_change=self.__enable_login).style('margin-top: 10px; width: 100%;')
            with self.ui.row().style('margin-top: 25px; align-items: center; justify-content: space-between; width: 100%;'):
                self.button_register = self.ui.button(
                    'Register', on_click=lambda: self.ui.open('/register'), icon='add_circle')
                self.button_login = self.ui.button(
                    'Login', on_click=self.check_login, icon='login')
                self.button_login.enabled = False

    def __enable_login(self, event: events):
        if self.username.value != '' and self.password.value != '' and len(self.password.value) >= 8 and len(self.username.value) >= 3:
            self.button_login.enabled = True
        else:
            self.button_login.enabled = False

    def check_login(self, event: events.SceneClickEventArguments):
        if not self.select(self.username.value, self.password.value) is None:
            nicegui.app.storage.user.update(
                {'username': self.username.value, 'authenticated': True})
            self.ui.notify(message='Login successful',
                           type='positive', position='top-right')
            self.ui.open('/')
        else:
            self.ui.notify(message='Invalid username or password',
                           type='negative', position='top-right')
