# App/models/recipe.py
from . import db

recipe_ingredients = db.Table(
    "recipe_ingredients",
    db.Column("recipe_id",      db.Integer, db.ForeignKey("recipes.id")),
    db.Column("ingredient_id",  db.Integer, db.ForeignKey("ingredients.id")),
)

class Recipe(db.Model):
    __tablename__ = "recipes"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(120), nullable=False)
    directions  = db.Column(db.Text,        nullable=False)
    owner_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner       = db.relationship("User", back_populates="recipes")
    ingredients = db.relationship("Ingredient",
                                  secondary=recipe_ingredients,
                                  backref="recipes")

    def missing_items(self):
        """Return ingredient names that are not in owner’s current pantry."""
        pantry_names = {ing.name.lower() for ing in self.owner.ingredients}
        return [ing.name for ing in self.ingredients
                if ing.name.lower() not in pantry_names]