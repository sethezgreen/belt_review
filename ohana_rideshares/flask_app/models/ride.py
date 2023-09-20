
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, message
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.

class Ride:
    db = "ohana_rideshares_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.pick_up_location = data['pick_up_location']
        self.date = data['date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rider_id = data['rider_id']
        self.driver_id = data['driver_id']
        self.rider = None
        self.driver = None
        self.messages = []
        # What changes need to be made above for this project?
        #What needs to be added here for class association?



    # Create Rides Models

    @classmethod
    def create_ride(cls, data):
        if not cls.validate_ride(data): return False
        data = {
            'destination' : data['destination'],
            'pick_up_location' : data['pick_up_location'],
            'date' : data['date'],
            'details' : data['details'],
            'rider_id' : session['user_id']
        }
        query = """
            INSERT INTO rides (destination, pick_up_location, date, details, rider_id)
            VALUES (%(destination)s, %(pick_up_location)s, %(date)s, %(details)s, %(rider_id)s)
            ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # Read Rides Models

    @classmethod
    def get_ride_by_id(cls, ride_id):
        data = {
            'id' : ride_id
        }
        query = """
            SELECT * 
            FROM rides
            JOIN users AS riders 
            ON riders.id = rides.rider_id
            LEFT JOIN users 
            AS drivers 
            ON drivers.id = rides.driver_id
            WHERE rides.id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        result = results[0]
        one_ride = cls(result)
        one_ride.rider = user.User({
                    'id' : result['riders.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'password' : result['password'],
                    'created_at' : result['riders.created_at'],
                    'updated_at' : result['riders.updated_at']
        })
        one_ride.driver = user.User({
                    'id' : result['drivers.id'],
                    'first_name' : result['drivers.first_name'],
                    'last_name' : result['drivers.last_name'],
                    'email' : result['drivers.email'],
                    'password' : result['drivers.password'],
                    'created_at' : result['drivers.created_at'],
                    'updated_at' : result['drivers.updated_at']
        })
        one_ride.messages = message.Message.read_messages(ride_id)
        return one_ride

    @classmethod
    def get_user_id_of_ride(cls, ride_id):
        data = {
            'id' : ride_id
        }
        query = """
            SELECT user_id
            FROM rides
            WHERE id = %(id)s
            ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        user_id = result[0]['user_id']
        return user_id

    @classmethod
    def get_all_ride_requests_with_rider(cls):
        query = """
            SELECT * 
            FROM rides
            JOIN users AS riders 
            ON riders.id = rides.rider_id
            LEFT JOIN users 
            AS drivers 
            ON drivers.id = rides.driver_id
            ORDER BY date
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_rides = {}
        ride_requests = []
        booked_rides = []
        for result in results:
            # look up as for sql --> need to use as for the id's so there is riders.id and drivers.id
            if result['driver_id'] == None:
                ride_request = cls(result)
                ride_request.rider = user.User({
                    'id' : result['riders.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'password' : result['password'],
                    'created_at' : result['riders.created_at'],
                    'updated_at' : result['riders.updated_at']
                })
                ride_requests.append(ride_request)
            else:
                booked_ride = cls(result)
                booked_ride.rider = user.User({
                    'id' : result['riders.id'],
                    'first_name' : result['first_name'],
                    'last_name' : result['last_name'],
                    'email' : result['email'],
                    'password' : result['password'],
                    'created_at' : result['riders.created_at'],
                    'updated_at' : result['riders.updated_at']
                })
                booked_ride.driver = user.User({
                    'id' : result['drivers.id'],
                    'first_name' : result['drivers.first_name'],
                    'last_name' : result['drivers.last_name'],
                    'email' : result['drivers.email'],
                    'password' : result['drivers.password'],
                    'created_at' : result['drivers.created_at'],
                    'updated_at' : result['drivers.updated_at']
                })
                booked_rides.append(booked_ride)
        all_rides['ride_requests'] = ride_requests
        all_rides['booked_rides'] = booked_rides
        return all_rides

    # Update Rides Models

    @classmethod
    def update_ride(cls, data):
        # if session['user_id'] != cls.get_user_id_of_ride(data['ride_id']): return False
        if not cls.validate_ride(data): return False
        data = {
            'id' : data['ride_id'],
            'pick_up_location' : data['pick_up_location'],
            'details' : data['details']
        }
        query = """
            UPDATE rides
            SET 
                pick_up_location = %(pick_up_location)s,
                details = %(details)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def add_driver_by_ride_id(cls, ride_id):
        # update ride to add driver foreign key using session
        data = {
            'id' : ride_id,
            'driver_id': session['user_id']
            }
        query = """
            UPDATE rides
            SET
                driver_id = %(driver_id)s
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True
    
    @classmethod
    def remove_driver_by_ride_id(cls, ride_id):
        data = {'id' : ride_id}
        query = """
            UPDATE rides
            SET
                driver_id = null
            WHERE id = %(id)s
            ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

    # Delete Rides Models

    @classmethod
    def delete_ride_by_id(cls, ride_id):
        data = {'id' : ride_id}
        query = """
            DELETE FROM rides
            WHERE id = %(id)s
            ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # Validation
    @staticmethod
    def validate_ride(data):
        is_valid = True
        if len(data['destination']) < 3:
            flash("Destination must be at least 3 characters")
            is_valid = False
        if len(data['pick_up_location']) < 3:
            flash("Pick-up location must be at least 3 characters")
            is_valid = False
        if len(data['details']) < 10:
            flash("Details must be at least 10 characters")
            is_valid = False
        DATE_REGEX =re.compile(r'^\d{4}-\d{2}-\d{2}$') 
        if not DATE_REGEX.match(data['date']): 
            flash("Please provide the date")
            is_valid = False
        return is_valid