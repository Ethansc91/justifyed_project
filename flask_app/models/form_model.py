from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Form:
    db = "justifyed_music_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.church_name = data['church_name']
        self.church_address = data['church_address']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_form(data):
        is_valid = True
        if len(data['name']) == 0 or len(data['email']) == 0 or len(data['church_name']) == 0 or len(data['church_address']) == 0 or len(data['description']) == 0:
            flash('All Fields Required' ,'form')
            is_valid = False
            return is_valid
        elif len(data['name']) < 2:
            flash('Name needs two characters at least' ,'form')
            is_valid = False
        elif len(data['email']) < 10 or not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email' ,'form')
            is_valid = False
        elif len(data['church_name']) < 3:
            flash('Church name needs 3 or more characters' ,'form')
            is_valid = False
        elif len(data['church_address']) < 5:
            flash('Invalid church address' ,'form')
            is_valid = False
        elif len(data['church_address']) < 8:
            flash('Description needs to be more than 5 cahracters' ,'form')
            is_valid = False
        return is_valid