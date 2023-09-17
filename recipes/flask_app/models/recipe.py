
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Recipe:
    db = "recipes_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Recipes Models

    @classmethod
    def create_recipe(cls, data):
        # print (data['date_made']) used this to check date regex
        if not cls.validate_recipe(data): 
            return False
        data = data.copy()
        data['user_id'] = session['user_id']
        query = """
            INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s, %(user_id)s)
            ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # Read Recipes Models

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = """
            SELECT * FROM recipes
            JOIN users ON users.id = recipes.user_id
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for result in results:
            one_recipe = cls(result)
            one_recipe_creator_data = {
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }
            creator = user.User(one_recipe_creator_data)
            one_recipe.creator = creator
            all_recipes.append(one_recipe)
        return all_recipes
        
    @classmethod
    def get_recipe_with_user_by_id(cls, recipe_id):
        data = {
            'id' : recipe_id
        }
        query = """
            SELECT * FROM recipes
            JOIN users ON users.id = recipes.user_id
            WHERE recipes.id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0]
    
    @classmethod
    def get_user_id_of_recipe(cls, recipe_id):
        data = {
            'id' : recipe_id
        }
        query = """
            SELECT user_id
            FROM recipes
            WHERE id = %(id)s
            ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        user_id = result[0]['user_id']
        return user_id
    
    # Update Recipes Models

    @classmethod
    def update_recipe(cls, data):
        if session['user_id'] != cls.get_user_id_of_recipe(data['recipe_id']): return False# protects recipes from being updated by other users
        if not cls.validate_recipe(data): 
            return False
        data = {
            'id' : data['recipe_id'],
            'name' : data['name'],
            'description' : data['description'],
            'instructions' : data['instructions'],
            'under_30' : data['under_30'],
            'date_made' : data['date_made'],
        }
        query = """
            UPDATE recipes
            SET 
                name = %(name)s, 
                description = %(description)s,
                instructions = %(instructions)s,
                date_made = %(date_made)s,
                under_30 = %(under_30)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Recipes Models

    @classmethod
    def delete_recipe(cls, recipe_id):
        if session['user_id'] != cls.get_user_id_of_recipe(recipe_id): return False# protects recipes from being deleted by other users
        data = {
            'id' : recipe_id
        }
        query = """
            DELETE FROM recipes
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Validation
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 2:
            flash("Name must be at least 2 characters")
            is_valid = False
        if len(data['description']) < 4:
            flash("Description must be at least 4 characters")
            is_valid = False
        if len(data['instructions']) < 1:
            flash("You must include instructions")
            is_valid = False
        DATE_REGEX =re.compile(r'^\d{4}-\d{2}-\d{2}$') 
        if not DATE_REGEX.match(data['date_made']): 
            flash("Please provide the date made")
            is_valid = False
        if "under_30" not in data:
            flash("Please select if it is under 30 minutes")
            is_valid = False
        return is_valid