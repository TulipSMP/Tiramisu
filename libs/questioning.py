from logging42 import logger
import yaml
import itertools
import sys
from libs.database import Database

class Questioning:
    def __init__(self, quiz_type, guild, user):
        self.type = quiz_type
        self.guild = guild
        self.id = user.id
        self.user = user

        with open('config/questions.yml', 'r') as ymlfile:
            self.questions = yml.load(ymlfile, Loader=yaml.FullLoader)
        with open('config/config.yml', 'r') as ymlfile:
            self.cfg = yml.load(ymlfile, Loader=yaml.FullLoader)
        
        self.db = Database(self.guild, reason=f'Questions Module')
    
    def make(self, quiz, channel):
        """ Create a quiz, stored in a database """
        self.db.cursor.execute(f'INSERT INTO "{self.questions["database"]["name"]}_{self.guild.id}" ( id,  modules) VALUES ("quiz:{quiz}", "presets:mod_application")')
