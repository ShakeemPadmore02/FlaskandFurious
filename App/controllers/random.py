from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Ingredient  # Import your models
from datetime import datetime

# Create a blueprint for the ingredient routes
ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
@login_required
def get_ingredients():
    """
    Get all ingredients owned by the current user.
    """
    ingredients = Ingredient.query.filter_by(owner_id