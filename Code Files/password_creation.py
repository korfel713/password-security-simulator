import random
import string

#class that holds functions for password creation/generation
class PasswordCreation:
    def __init__(self, DB):
        self.DB = DB

   #User Created password function
    def user_create(self, password):
        if not password:
            return "Error: No password entered."
        if any(c.isspace() for c in password):
            return "Error: Password cannot contain spaces."

        # Store with temp values
        res = self.DB.input_pass(
            text=password,
            ifgen=0,
            time=0,
            qual=0,
            score=0
        )

        return res

    #generate password for user
    def generate(self, length=12):
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))

        res = self.DB.input_pass(
            text=password,
            ifgen=1,
            time=0,
            qual=0,
            score=0
        )

        return res