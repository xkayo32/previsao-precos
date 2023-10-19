import nicegui
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.stocks import StocksPage
from decouple import config


@nicegui.ui.page('/login', title='Login')
def login_page():
    LoginPage(nicegui).body()


@nicegui.ui.page('/register', title='Register')
def register_page():
    RegisterPage(nicegui).body()


@nicegui.ui.page('/stocks', title='Stocks')
def stocks_page():
    StocksPage(nicegui).body()


@nicegui.ui.page('/')
def home_page():
    nicegui.ui.link('Login', '/login')
    nicegui.ui.link('Register', '/register')
    nicegui.ui.link('Stocks', '/stocks')


nicegui.ui.run(storage_secret='teste')
