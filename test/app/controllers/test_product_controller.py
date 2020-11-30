import responses
from werkzeug.security import generate_password_hash

from app import Customer
from app.domain.user.user import User, UserRole, RoleCategory
from test import build_header, DATE_FORMAT
from test.conftest import set_up


@responses.activate
def test_get_product_by_id(client, db):
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

    response = client.get(f'/api/product/{product_id}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == product['id']
    assert response.json['title'] == product['title']
    assert response.json['brand'] == product['brand']
    assert response.json['image'] == product['image']
    assert response.json['price'] == product['price']
    assert response.json['reviewScore'] == product['reviewScore']


@responses.activate
def test_get_products(client, db):
    set_up(db)
    products = {
        "meta": {
            "page_number": 1,
            "page_size": 100
        },
        "products": [
            {
                "price": 1699,
                "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
                "brand": "bébé confort",
                "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
                "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown",
                "reviewScore": 3.4
            },
            {
                "price": 1149,
                "image": "http://challenge-api.luizalabs.com/images/958ec015-cfcf-258d-c6df-1721de0ab6ea.jpg",
                "brand": "bébé confort",
                "id": "958ec015-cfcf-258d-c6df-1721de0ab6ea",
                "title": "Moisés Dorel Windoo 1529",
                "reviewScore": 4.352941
            }]}
    responses.add(responses.GET, f'http://challenge-api.luizalabs.com/api/product/?page=1',
                  json=products, status=200)

    page = 1
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

    response = client.get(f'/api/product/{page}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert len(response.json['products']) == 2
    assert response.json['meta']['page_number'] == products['meta']['page_number']
    assert response.json['meta']['page_size'] == products['meta']['page_size']

    for index, product in enumerate(response.json['products'], start=0):
        product_api = products['products'][index]
        assert product['id'] == product_api['id']
        assert product['title'] == product_api['title']
        assert product['brand'] == product_api['brand']
        assert product['image'] == product_api['image']
        assert product['price'] == product_api['price']
        assert product['reviewScore'] == product['reviewScore']
