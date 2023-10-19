import sqlite3
from cryptography.fernet import Fernet
from decouple import config
from collections import namedtuple


class DataBase:

    def __init__(self) -> None:
        self.conn = sqlite3.connect('database/data.db')
        self.cursor = self.conn.cursor()
        self.__key = config('SECRET_KEY')

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symbol TEXT NOT NULL UNIQUE
        );
        """)

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS stocks_favorite (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER NOT NULL,
                                stock_id INTEGER NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (id),
                                FOREIGN KEY (stock_id) REFERENCES stocks (id)
                            );
                            """)

    def password_encrypt(self, password):
        self.__key = self.__key.encode()
        fernet = Fernet(self.__key)
        password = password.encode()
        return fernet.encrypt(password).decode()

    def password_decrypt(self, password):
        self.__key = self.__key.encode()
        fernet = Fernet(self.__key)
        return fernet.decrypt(password).decode()

    def insert(self, name: str, email: str, password: str):
        try:
            self.cursor.execute(
                f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{self.password_encrypt(password)}')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def select(self, email, password):
        user = self.cursor.execute(
            f"SELECT * FROM users WHERE email = '{email}'").fetchone()
        if not user is None:
            if self.password_decrypt(user[3]) == password:
                return user
        return None

    def insert_stock(self, name: str, symbol: str):
        try:
            self.cursor.execute(
                f"INSERT INTO stocks (name, symbol) VALUES ('{name}', '{symbol}')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def list_stock(self):
        stocks = self.cursor.execute("SELECT * FROM stocks").fetchall()
        return {stocks[2]: stocks[1] for stocks in stocks}


if __name__ == '__main__':
    db = DataBase()
    db.create_table()
