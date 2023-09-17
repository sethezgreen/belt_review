from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Recipes Controller

@app.route('/recipes/create', methods=["GET", "POST"])
def create_recipe():
    if "user_id" not in session: return redirect('/')
    if request.method == "GET":
        return render_template("new_recipe.html")
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/recipes')
    return redirect('/recipes/create')

# Read Recipes Controller

@app.route('/recipes')
def dashboard():
    if 'user_id' not in session: return redirect('/')
    all_recipes = recipe.Recipe.get_all_recipes_with_creator()
    return render_template('dashboard.html', all_recipes = all_recipes)

@app.route('/recipes/<int:recipe_id>')
def read_one_recipe(recipe_id):
    if "user_id" not in session: return redirect('/')
    one_recipe = recipe.Recipe.get_recipe_with_user_by_id(recipe_id)
    return render_template('read_one_recipe.html', recipe = one_recipe)


# Update Recipes Controller

@app.route('/recipes/edit/<int:recipe_id>')
def render_update_recipe(recipe_id):
    if "user_id" not in session: return redirect('/')
    one_recipe = recipe.Recipe.get_recipe_with_user_by_id(recipe_id)
    return render_template('update_recipe.html', recipe = one_recipe)

@app.route('/recipes/update', methods=["POST"])
def update_recipe():
    if "user_id" not in session: return redirect('/')
    if recipe.Recipe.update_recipe(request.form):
        return redirect('/recipes')
    return redirect(f'/recipes/edit/{request.form["recipe_id"]}')

# Delete Recipes Controller

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if "user_id" not in session: return redirect('/')
    recipe.Recipe.delete_recipe(recipe_id)
    return redirect('/recipes')

# Test
# @app.route('/test')
# def test():
#     return recipe.Recipe.get_recipe_with_user_by_id(1)


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