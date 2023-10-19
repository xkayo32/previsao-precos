from nicegui import events
from database.data import DataBase
import nicegui
from pages.validations import Validate


class RegisterPage(DataBase):

    def __init__(self, ui: nicegui.ui) -> None:
        super().__init__()
        self.ui = ui

    def body(self):
        with self.ui.card().style('width: 30%; margin: 0 auto; margin-top: 10%;'):
            self.ui.label('Register').style(
                'font-size: 20px; align-self: center;')
            self.name = self.ui.input(
                label='Name', placeholder='Name', on_change=self.__enable_register).style('margin-top: 10px; width: 100%;')
            self.username = self.ui.input(
                label='Email', placeholder='Email', on_change=self.__enable_register).style('margin-top: 10px; width: 100%;')
            self.password = self.ui.input(label='Password', placeholder='Password',
                                          password=True, password_toggle_button=True, on_change=self.__enable_register).style('margin-top: 10px; width: 100%;')
            with self.ui.row().style('margin-top: 25px; align-items: center; justify-content: space-between; width: 100%;'):
                self.button_login = self.ui.button(
                    'Login', on_click=lambda: self.ui.open('/login'), icon='login')
                self.button_register = self.ui.button(
                    'Save', on_click=self.register, icon='add_circle')
                self.button_register.enabled = False

    def __enable_register(self, event: events):
        validate = Validate()
        if validate.check_values(self.username.value, self.password.value) is True:
            self.button_register.enabled = True
        else:
            self.button_register.enabled = False

    def register(self, event: events.SceneClickEventArguments):
        if self.insert(self.name.value, self.username.value, self.password.value) is True:
            self.ui.notify(message='Register successful',
                           type='positive', position='top-right')
            self.ui.open('/login')
        else:
            self.ui.notify(message='Email already registered',
                           type='negative', position='top-right')
