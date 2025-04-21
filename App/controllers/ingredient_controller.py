from App.models import Ingredient
from App.database import db

def create_ingredient(name, description):
    new_ingredient = Ingredient(name=name, description=description, quantity=quantity, expiry_date=expiry_date)
    if not new_ingredient:
        return None
    # Check if the ingredient already exists
    existing_ingredient = Ingredient.query.filter_by(name=name).first()
    if existing_ingredient:
        return None  # Ingredient already exists
    # Add the new ingredient to the session and commit
    new_ingredient = Ingredient(name=name, description=description)
    if not new_ingredient:
        return None
    # Check if the ingredient already exists
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient_by_name(name):
    return Ingredient.query.filter_by(name=name).first()

def get_ingredient(id):
    return Ingredient.query.get(id)

def get_all_ingredients(id):
    Ingredient.query.filter_by(owner_id=user_id).all()

def get_all_ingredients_json():
    ingredients = Ingredient.query.all()
    if not ingredients:
        return []
    ingredients = [ingredient.get_json() for ingredient in ingredients]
    return ingredients

def update_ingredient(id, name, description):
    ingredient = get_ingredient(id)
    if ingredient:
        ingredient.name = name
        ingredient.description = description
        db.session.add(ingredient)
        return db.session.commit()
    return None

def delete_ingredient(id):
    ingredient = get_ingredient(id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return True
    return False