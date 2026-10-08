class User:
    def __init__(self, username, password, name, age):
        self.username = username
        self.password = password
        self.name = name
        self.age = age

    def check_password(self, password_guess):
        return self.password == password_guess

