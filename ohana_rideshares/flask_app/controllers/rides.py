from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, ride, message # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Rides Controller

@app.route('/rides/new', methods=["POST", "GET"])
def new_ride():
    if "user_id" not in session: return redirect ('/')
    if request.method == "GET":
        return render_template('new_ride.html')
    if ride.Ride.create_ride(request.form):
        return redirect('/rides/dashboard')
    return redirect('/rides/new')

# Read Rides Controller

@app.route('/rides/dashboard')
def users_main():
    if 'user_id' not in session: return redirect('/')
    all_rides = ride.Ride.get_all_ride_requests_with_rider()
    return render_template('home.html', all_rides = all_rides)

@app.route('/rides/<int:ride_id>')
def read_one_ride(ride_id):
    one_ride = ride.Ride.get_ride_by_id(ride_id)
    # this_ride_with_messages = message.Message.read_messages(ride_id)
    return render_template('one_ride.html', ride = one_ride)

# Update Rides Controller

@app.route('/rides/edit/<int:ride_id>', methods=["POST", "GET"])
def update_ride(ride_id):
    if request.method == "GET":
        one_ride = ride.Ride.get_ride_by_id(ride_id)
        return render_template('edit_ride.html', ride = one_ride)
    if ride.Ride.update_ride(request.form):
        return redirect(f'/rides/{ride_id}')
    return redirect(f'/rides/edit/{ride_id}')

@app.route('/rides/accept/<int:ride_id>')
def accept_ride(ride_id):
    ride.Ride.add_driver_by_ride_id(ride_id)
    return redirect('/rides/dashboard')

@app.route('/rides/cancel/<int:ride_id>')
def cancel_ride(ride_id):
    ride.Ride.remove_driver_by_ride_id(ride_id)
    return redirect('/rides/dashboard')

# Delete Rides Controller

@app.route('/rides/delete/<int:ride_id>')
def delete_ride(ride_id):
    ride.Ride.delete_ride_by_id(ride_id)
    return redirect('/rides/dashboard')



# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.