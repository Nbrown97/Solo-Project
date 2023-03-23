from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


db = 'project'
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data ['email']
        self.password = data['password']
        self.date_due = data['date_due']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","registration")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!","registration")
        if len(user['first_name']) < 2:
            flash("First name must have at least 2 characters!","registration")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must have at least 2 characters!","registration")
            is_valid = False
        if len(user['password']) < 10:
            flash("Your password must have at least 10 charatcers!","registration")
            is_valid = False
        if user['date_due'] == "":
            flash('Please enter date','registration')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(db).query_db(query,data)
        if len(results) <1:
            return False
        return cls(results[0])
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, date_due) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(date_due)s);"
        return connectToMySQL(db).query_db(query,data)
    