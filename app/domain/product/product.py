from app import db
from app.domain import BaseModel


# Define the Product Domain
class Product(db.Model, BaseModel):
    __tablename__ = 'products'
    title = db.Column(db.String(256), nullable=False)
    brand = db.Column(db.String(256), nullable=False)
    image = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    review_score = db.Column(db.Float, nullable=True)
