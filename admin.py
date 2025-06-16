from dotenv import load_dotenv
import os
from flask_login import UserMixin

load_dotenv()

class user(UserMixin):

    def __init__(self):
        self.username = os.getenv('ADMIN_USERNAME')
        self.password = os.getenv('ADMIN_PASSWORD')

    def check_username(self, username):
        if username == self.username:
            return True
        else:
            return False

    def check_password(self, password): # TODO: add hashing
        if password == self.username:
            return True
        else:
            return False
    
    def get_id(self):
        return 0