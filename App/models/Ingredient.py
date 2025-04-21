from . import db

class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(80), nullable=False, unique=True)
    quantity    = db.Column(db.String(40))
    expiry_date = db.Column(db.Date)
    owner_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="ingredients")

    def __init__(self, name, quantity=None, expiry_date=None):
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

        

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
        }