from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user, get_jwt_identity

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')
#
@user_views.route('/users/<id>/recipe_form', methods=['GET'])
@jwt_required()
def get_user_recipe_form(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    return render_template('recipe_form.html', user=current_user.id)
#get recipes created by the user

@user_views.route('/users/<id>/recipes', methods=['GET'])
@jwt_required()
def get_user_recipes(id):
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify(message="User not found"), 404

    # Convert id to an integer for comparison
    try:
        id = int(id)
        print(id)
    except ValueError:
        return jsonify(message="Invalid user ID"), 400

    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401

    recipes = get_all_recipes(current_user.id)
    print(current_user)
    return render_template('recipes.html', recipes=recipes, user=current_user.id)
#user created recipes

@user_views.route('/users/<id>/recipes', methods=['POST'])
@jwt_required()
def create_user_recipes(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Recipe {data['name']} created!")
    create_recipe(data['name'], data['description'], data['ingredients'])
    return redirect(url_for('user_views.get_user_recipes', id=current_user.id))
#delete user created recipes

@user_views.route('/users/<id>/recipes', methods=['DELETE'])
@jwt_required()
def delete_user_recipes(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Recipe {data['name']} deleted!")
    delete_recipe(data['id'])
    return redirect(url_for('user_views.get_user_recipes', id=current_user.id))
#update user created recipes
@user_views.route('/users/<id>/recipes', methods=['PUT'])
@jwt_required()
def update_user_recipes(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Recipe {data['name']} updated!")
    update_recipe(data['id'], data['name'], data['description'])
    return redirect(url_for('user_views.get_user_recipes', id=current_user.id))
#get a single recipe created by the user

@user_views.route('/users/<id>/recipes/<recipe_id>', methods=['GET'])
@jwt_required()
def get_user_recipe(id, recipe_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    recipe = get_recipe(recipe_id)
    if not recipe:
        return jsonify(message="Recipe not found"), 404
    return render_template('recipes.html', recipe=recipe, user=current_user)
#delete a single recipe created by the user

@user_views.route('/users/<id>/recipes/<recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_user_recipe(id, recipe_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    recipe = get_recipe(recipe_id)
    if not recipe:
        return jsonify(message="Recipe not found"), 404
    delete_recipe(recipe_id)
    flash(f"Recipe {recipe.name} deleted!")
    return redirect(url_for('user_views.get_user_recipes', id=current_user.id))
#view a user's pantry

@user_views.route('/users/<id>/pantry', methods=['GET'])
@jwt_required()
def get_user_pantry(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    pantry = get_all_ingredients(current_user.id)
    return render_template('pantry.html', pantry=pantry, user=current_user)
#user creates their pantry

@user_views.route('/users/<id>/pantry', methods=['POST'])
@jwt_required()
def create_user_pantry(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Ingredient {data['name']} created!")
    create_ingredient(data['name'], data['description'])
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
#user deletes their pantry

@user_views.route('/users/<id>/pantry', methods=['DELETE'])
@jwt_required()
def delete_user_pantry(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Ingredient {data['name']} deleted!")
    delete_ingredient(data['id'])
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
#user updates their pantry

@user_views.route('/users/<id>/pantry', methods=['PUT'])
@jwt_required()
def update_user_pantry(id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Ingredient {data['name']} updated!")
    update_ingredient(data['id'], data['name'], data['description'])
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
#user views a single ingredient in their pantry

@user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['GET'])
@jwt_required()
def get_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    ingredient = get_ingredient(ingredient_id)
    if not ingredient:
        return jsonify(message="Ingredient not found"), 404
    return render_template('pantry.html', ingredient=ingredient, user=current_user)
#user deletes a single ingredient in their pantry

@user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['DELETE'])
@jwt_required()
def delete_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    ingredient = get_ingredient(ingredient_id)
    if not ingredient:
        return jsonify(message="Ingredient not found"), 404
    delete_ingredient(ingredient_id)
    flash(f"Ingredient {ingredient.name} deleted!")
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
#user updates a single ingredient in their pantry

@user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['PUT'])
@jwt_required()
def update_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Ingredient {data['name']} updated!")
    update_ingredient(data['id'], data['name'], data['description'])
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))

""" @user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['GET'])
@jwt_required()
def get_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    ingredient = get_ingredient(ingredient_id)
    if not ingredient:
        return jsonify(message="Ingredient not found"), 404
    return render_template('pantry.html', ingredient=ingredient, user=current_user) """

""" @user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['DELETE'])
@jwt_required()
def delete_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    ingredient = get_ingredient(ingredient_id)
    if not ingredient:
        return jsonify(message="Ingredient not found"), 404
    delete_ingredient(ingredient_id)
    flash(f"Ingredient {ingredient.name} deleted!")
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
 """
""" @user_views.route('/users/<id>/pantry/<ingredient_id>', methods=['PUT'])
@jwt_required()
def update_user_ingredient(id, ingredient_id):
    current_user = jwt_current_user()
    if not current_user:
        return jsonify(message="User not found"), 404
    if current_user.id != id:
        return jsonify(message="Unauthorized"), 401
    data = request.form
    flash(f"Ingredient {data['name']} updated!")
    update_ingredient(data['id'], data['name'], data['description'])
    return redirect(url_for('user_views.get_user_pantry', id=current_user.id))
    ingredient = get_ingredient(ingredient_id)
    if not ingredient:
        return jsonify(message="Ingredient not found"), 404
    return render_template('pantry.html', ingredient=ingredient, user=current_user)
 """