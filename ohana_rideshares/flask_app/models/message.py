
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import ride, user

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Message:
    db = "ohana_rideshares_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ride_id = data['ride_id']
        self.rider_id = data['rider_id']
        self.driver_id = data['driver_id']
        self.creator = None # should this also go in sql?
        # could have creator_id and check that against the rider_id and driver_id to know who the other user is
        self.rider = None
        self.driver = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Messages Models

    @classmethod
    def create_message(cls, data):
        if not cls.validate_message(data): return False
        query = """
            INSERT INTO messages (content, ride_id, rider_id, driver_id)
            VALUES (%(content)s, %(ride_id)s, %(rider_id)s, %(driver_id)s)
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Read Messages Models

    @classmethod
    def read_messages(cls, ride_id):
        data = {'id' : ride_id}
        query = """
            SELECT *
            FROM messages
            WHERE ride_id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        all_messages = []
        # for result in results:
        #     one_message = cls(result)
        #     one_message.
        return all_messages
    
    # Update Messages Models



    # Delete Messages Models



    # Validation
    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data['content']) < 1:
            flash("Message cannot be blank")
            is_valid = False
        return is_valid