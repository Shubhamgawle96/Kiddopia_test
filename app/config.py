import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB_URI = os.environ.get('SECRET_KEY') or 'https://kiddopia-73f9e-default-rtdb.firebaseio.com/'