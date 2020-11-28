from app import db
from app.domain import BaseModel


# Define the WishList Domain
class WishList(db.Model, BaseModel):
    __tablename__ = 'wish_list'
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='_customer_id_product_id'),)
    serialize_rules = ('-customer_id', '-deleted_date', '-updated_date', '-created_date',)

    product_id = db.Column(db.String(512), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
