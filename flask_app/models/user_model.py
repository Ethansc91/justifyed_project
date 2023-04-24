from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class User:
    db = 'justifyed_music_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = []


    @classmethod
    def save_user_db(cls, data):
        query = """INSERT INTO users(first_name,last_name,email,password)
        VALUES(%(fname)s,%(lname)s,%(email)s,%(password)s)"""
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users 
        WHERE email = %(email)s"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_user(cls, data):
        query = """UPDATE users 
        SET first_name=%(fname)s, last_name=%(lname)s, email=%(email)s, description=%(description)s
        WHERE users.id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_users_description(cls, data):
        query = """UPDATE users
        SET description=%(description)s
        WHERE users.id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def registration_validation(data):
        is_valid = True
        if len(data['fname']) == 0 or len(data['lname']) == 0 or len(data['email']) == 0 or len(data['password']) == 0:
            flash('All Fields Required' ,'registration')
            is_valid = False
            return is_valid
        elif len(data['fname']) < 2:
            flash('Name needs two characters at least' ,'registration')
            is_valid = False
        elif len(data['lname']) < 2:
            flash('Name needs two characters at least' ,'registration')
            is_valid = False
        elif len(data['email']) < 2 or not EMAIL_REGEX.match(data['email']) or User.get_user_by_email({'email': data['email']}) != False:
            flash('Invalid Email' ,'registration')
            is_valid = False
        elif not PASSWORD_REGEX.match(data['password']):
            flash('Password needs at least 1 Capital, lower case letter, at least 1 number and 1 special character-!@#$%^&*()-', 'registration')
            is_valid = False
        elif data['password'] != data['cpassword']:
            flash('Passwords need to match' ,'registration')
            is_valid = False
        return is_valid
    


    @staticmethod
    def login_validation(data):
        is_valid = True
        if len(data['email']) == 0 or len(data['password']) == 0:
            flash('Invalid Email/Password', 'login')
            is_valid = False
            return is_valid
        return is_valid