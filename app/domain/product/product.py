from app import db
from app._domain.base_model import BaseModel


# Define the Product data _domain
class Product(BaseModel):
    __tablename__ = 'products'
    title = db.Column(db.String(256))
    brand = db.Column(db.String(256))
    image = db.Column(db.Text)
    price = db.Column(db.Float)
    review_score = db.Column(db.Float)
