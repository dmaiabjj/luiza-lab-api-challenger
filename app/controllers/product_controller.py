from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.domain.product.product_service import ProductService

product_blueprint = Blueprint('product', __name__, url_prefix='/api')
product_service = ProductService()


@product_blueprint.route('/product/<id>', endpoint='get-product-by-id', methods=['GET'])
@jwt_required
def get_product_by_id(id):
    product = product_service.find_by_id(id=id)
    return jsonify(product)


@product_blueprint.route('/product/', endpoint='get-all-products', methods=['GET'])
@product_blueprint.route('/product/<int:offset>/', endpoint='get-all-products', methods=['GET'])
@jwt_required
def get_all_products(offset=1):
    products = product_service.get_all_paginated(offset=offset)
    return jsonify(products)
