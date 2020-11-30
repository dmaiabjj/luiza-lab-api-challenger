import responses
from werkzeug.security import generate_password_hash

from app import Customer
from app.domain.user.user import User, UserRole, RoleCategory
from app.domain.wishlist.wishlist import WishList
from test import build_header, DATE_FORMAT
from test.conftest import set_up


@responses.activate
def test_add_product_into_wishlist(client, db):
    set_up(db)
    product_id = "e9a72482-7e95-44ff-ea5a-75147aef2184"
    product = {
        "price": 7999.9,
        "image": "http://challenge-api.luizalabs.com/images/e9a72482-7e95-44ff-ea5a-75147aef2184.jpg",
        "brand": "fender",
        "id": "e9a72482-7e95-44ff-ea5a-75147aef2184",
        "title": "Guitarra Telecaster Fender Standard",
        "reviewScore": 4.352941
    }
    responses.add(responses.GET, f'http://challenge-api.luizalabs.com/api/product/{product_id}/',
                  json=product, status=200)

    product_id = "e9a72482-7e95-44ff-ea5a-75147aef2184"
    password = "iAmDarthVader"
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(password))

    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/customer/token', json=dict(
        email=customer.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.post(f'/api/wishlist/product/{product_id}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['product_id'] == product_id

    wishlist_db = db.session.query(WishList).filter_by(id=response.json['id']).one_or_none()

    assert wishlist_db
    assert wishlist_db.product_id == product_id


@responses.activate
def test_delete_product_from_wishlist(client, db):
    set_up(db)
    product_id = "e9a72482-7e95-44ff-ea5a-75147aef2184"
    product = {
        "price": 7999.9,
        "image": "http://challenge-api.luizalabs.com/images/e9a72482-7e95-44ff-ea5a-75147aef2184.jpg",
        "brand": "fender",
        "id": "e9a72482-7e95-44ff-ea5a-75147aef2184",
        "title": "Guitarra Telecaster Fender Standard",
        "reviewScore": 4.352941
    }
    responses.add(responses.GET, f'http://challenge-api.luizalabs.com/api/product/{product_id}/',
                  json=product, status=200)

    product_id = "e9a72482-7e95-44ff-ea5a-75147aef2184"
    password = "iAmDarthVader"
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(password))

    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/customer/token', json=dict(
        email=customer.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.post(f'/api/wishlist/product/{product_id}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['product_id'] == product_id

    wishlist_db = db.session.query(WishList).filter_by(id=response.json['id']).one_or_none()

    assert wishlist_db
    assert wishlist_db.product_id == product_id

    response = client.delete(f'/api/wishlist/product/{product_id}', headers=headers, follow_redirects=True)
    assert response.status_code == 200

    wishlist_db = db.session.query(WishList).filter_by(id=wishlist_db.id).one_or_none()

    assert wishlist_db
    assert wishlist_db.deleted_date


def test_get_wishlist(client, db):
    set_up(db)
    password = "iAmDarthVader"
    customer = Customer(id=2, name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(password))

    db.session.add(customer)

    product_1 = WishList(customer_id=customer.id, product_id="1")
    product_2 = WishList(customer_id=customer.id, product_id="2")
    product_3 = WishList(customer_id=customer.id, product_id="3")

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)

    db.session.commit()

    response = client.post('/api/auth/customer/token', json=dict(
        email=customer.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/wishlist/', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 3

    products = db.session.query(WishList).filter_by(customer_id=customer.id).all()

    for index, product in enumerate(response.json, start=0):
        product_db = products[index]
        assert product_db.product_id == product['product_id']

    response = client.get(f'/api/wishlist/1/1', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 1

    products = db.session.query(WishList).filter_by(customer_id=customer.id).all()
    product_db = products[0]
    product = response.json[0]

    assert product_db.product_id == product['product_id']
