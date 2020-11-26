from app import db
from app.domain import BaseModel


# Define the WishList Domain
class WishList(db.Model, BaseModel):
    __tablename__ = 'wish_list'
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='_customer_id_product_id'), )

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
