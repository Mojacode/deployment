from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.tree import Tree
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.trees = []

    @staticmethod
    def validate_register(user):
        # connect to db to check for existing user
        query = "SELECT * FROM trees.users WHERE email = %(email)s;"
        results = connectToMySQL("trees").query_db(query,user)
        # Validation
        is_valid = True # we assume this is true
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters.")
            is_valid = False
        if len(user['password']) < 3:
            flash("Password must be at least 3 characters.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password does not match")
            is_valid = False
        return is_valid

    @classmethod
    def validate_email(cls,data):
        query = "SELECT * FROM trees.users WHERE email = %(email)s;"
        results = connectToMySQL("trees").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    
    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM trees.users WHERE id = %(users_id)s;"
        results = connectToMySQL("trees").query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO trees.users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s, NOW(),NOW());"
        return connectToMySQL("trees").query_db(query, data)

