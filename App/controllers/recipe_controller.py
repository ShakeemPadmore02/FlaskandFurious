from App.models import Recipe
from App.database import db

def create_recipe(name, description, ingredients):
    new_recipe = Recipe(name=name, description=description)
    if not new_recipe:
        return None
    # Check if the recipe already exists
    existing_recipe = Recipe.query.filter_by(name=name).first()
    if existing_recipe:
        return None  # Recipe already exists
    # Add the new recipe to the session and commit
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe

def get_recipe_by_name(name):
    return Recipe.query.filter_by(name=name).first()

def get_recipe(id):
    return Recipe.query.get(id)

def get_all_recipes(user_id):
    recipes = Recipe.query.filter_by(owner_id=user_id).all()
    if not recipes:
        return []
    recipes = [recipe.get_json() for recipe in recipes]
    return recipes

def get_all_recipes_json():
    recipes = Recipe.query.all()
    if not recipes:
        return []
    recipes = [recipe.get_json() for recipe in recipes]
    return recipes

def update_recipe(id, name, description):
    recipe = get_recipe(id)
    if recipe:
        recipe.name = name
        recipe.description = description
        db.session.add(recipe)
        return db.session.commit()
    return None

def delete_recipe(id):
    recipe = get_recipe(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return True
    return False

def get_recipes_by_ingredient(ingredient_name):
    recipes = Recipe.query.filter(Recipe.ingredients.any(name=ingredient_name)).all()
    if not recipes:
        return []
    recipes = [recipe.get_json() for recipe in recipes]
    return recipes

def get_recipes_by_user(user_id):
    recipes = Recipe.query.filter_by(owner_id=user_id).all()
    if not recipes:
        return []
    recipes = [recipe.get_json() for recipe in recipes]
    return recipes

