from app import db


# Define the WishList data domain
class WishList(db.Model):
    __tablename__ = 'wish_list'
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='_customer_id_product_id'))

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
