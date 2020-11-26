from app import db


# Define the Product data domain
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    brand = db.Column(db.String(256))
    image = db.Column(db.Text)
    price = db.Column(db.Float)
    review_score = db.Column(db.Float)
