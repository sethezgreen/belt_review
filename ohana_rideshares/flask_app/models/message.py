
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
        self.user_id = data['user_id']
        self.creator = None 
        self.ride = None
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Messages Models

    @classmethod
    def create_message(cls, data):
        if not cls.validate_message(data): return False
        data = data.copy()
        data['user_id'] = session['user_id']
        query = """
            INSERT INTO messages (content, ride_id, user_id)
            VALUES (%(content)s, %(ride_id)s, %(user_id)s)
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
            JOIN users
            ON users.id = messages.user_id
            JOIN rides
            ON rides.id = messages.ride_id
            WHERE ride_id = %(id)s
            ORDER BY messages.created_at
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        all_messages = []
        for result in results:
            one_message = cls(result)
            one_message.creator = user.User({
                'id' : result['users.id'],
                'first_name' : result['first_name'],
                'last_name' : result['last_name'],
                'email' : result['email'],
                'password' : result ['password'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            })
            one_message.ride = ride.Ride({
                'id' : result['rides.id'],
                'destination' : result['destination'],
                'pick_up_location' : result['pick_up_location'],
                'date' : result['date'],
                'details' : result['details'],
                'created_at' : result['rides.created_at'],
                'updated_at' : result['rides.updated_at'],
                'rider_id' : result['rider_id'],
                'driver_id' : result['driver_id']
            })
            
            all_messages.append(one_message)
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