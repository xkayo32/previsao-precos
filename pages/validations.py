class Validate:

    def check_values(self, email: str, password: str):
        if self.__validate_email(email) and self.__validate_password(password):
            return True
        return False

    @staticmethod
    def __validate_password(password):
        if len(password) >= 8:
            return True
        return False

    @staticmethod
    def __validate_email(email):
        if len(email) >= 3 and email.find('@') != -1 and email.find('.') != -1:
            return True
        return False

    @staticmethod
    def validate_stocks(name: str, symbol: str):
        if len(name) >= 3 and len(symbol) >= 3:
            return True
        return False
