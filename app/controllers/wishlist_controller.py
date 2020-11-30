from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.domain.product.product_service import ProductService
from app.domain.wishlist.wishlist import WishList
from app.domain.wishlist.wishlist_repository import WishListRepository
from app.domain.wishlist.wishlist_service import WishListService

wishlist_blueprint = Blueprint('wishlist', __name__, url_prefix='/api')
product_service = ProductService()
wishlist_service = WishListService(repository=WishListRepository())


@wishlist_blueprint.route('/wishlist/product/<product_id>', endpoint='add-wishlist', methods=['POST'])
@jwt_required
def add_wishlist(product_id):
    current_user = get_jwt_identity()
    customer_id = current_user['id']

    product = product_service.find_by_id(product_id)
    wishlist = wishlist_service.add(WishList(product_id=product['id'], customer_id=customer_id))

    return jsonify(wishlist)


@wishlist_blueprint.route('/wishlist/product/<product_id>', endpoint='delete-wishlist', methods=['DELETE'])
@jwt_required
def delete_wishlist(product_id):
    current_user = get_jwt_identity()
    customer_id = current_user['id']
    wishlist_service.delete(product_id=product_id, customer_id=customer_id)

    return {}, 200


@wishlist_blueprint.route('/wishlist/', endpoint='get-all-wishlist', methods=['GET'])
@wishlist_blueprint.route('/wishlist/<int:offset>/', endpoint='get-all-wishlist', methods=['GET'])
@wishlist_blueprint.route('/wishlist/<int:offset>/<int:limit>', endpoint='get-all-wishlist', methods=['GET'])
@jwt_required
def get_wishlist(offset=1, limit=10):
    current_user = get_jwt_identity()
    customer_id = current_user['id']
    users = wishlist_service.get_all_paginated(customer_id=customer_id, offset=offset, limit=limit)
    return jsonify(users)
