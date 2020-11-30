from werkzeug.security import generate_password_hash

from app import Customer
from app.domain.user.user import User, UserRole, RoleCategory
from test import build_header, DATE_FORMAT
from test.conftest import set_up


def test_add_customer(client, db):
    set_up(db)

    name = "Anakin Skywalker"
    email = "anakin@starwars.com"
    password = "iAmDarthVader"

    response = client.post('/api/customer', json=dict(
        name=name,
        email=email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['name'] == name
    assert response.json['email'] == email
    assert response.json['created_date']

    customer = db.session.query(Customer).filter_by(id=response.json['id']).one_or_none()

    assert customer
    assert customer.id == response.json['id']
    assert customer.name == response.json['name']
    assert customer.email == response.json['email']
    assert customer.created_date.strftime(DATE_FORMAT) == response.json['created_date']
    assert customer.verify_password(password)


def test_update_customer(client, db):
    set_up(db)
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

    name = "Darth Vader"
    email = "darthvader@starwars.com"
    headers = build_header(access_token)

    response = client.put('/api/customer', json=dict(
        name=name,
        email=email
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['name'] == name
    assert response.json['email'] == email
    assert response.json['created_date']
    assert response.json['updated_date']

    customer_db = db.session.query(Customer).filter_by(id=response.json['id']).one_or_none()

    assert customer_db
    assert customer_db.id == response.json['id']
    assert customer_db.name == response.json['name']
    assert customer_db.email == response.json['email']
    assert customer_db.created_date.strftime(DATE_FORMAT) == response.json['created_date']
    assert customer_db.updated_date.strftime(DATE_FORMAT) == response.json['updated_date']
    assert customer_db.verify_password(password)


def test_update_customer_by_id(client, db):
    set_up(db)
    user_password = "youAreMyOnlyHope"
    customer_password = "iAmDarthVader"
    user = User(name='Leia Organa', email='leia@luizalabs.com.br',
                password=generate_password_hash(user_password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(customer_password))
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=user_password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']

    name = "Darth Vader"
    email = "darthvader@starwars.com"
    headers = build_header(access_token)

    response = client.put(f'/api/customer/{customer.id}', json=dict(
        name=name,
        email=email
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['name'] == name
    assert response.json['email'] == email
    assert response.json['created_date']
    assert response.json['updated_date']

    customer_db = db.session.query(Customer).filter_by(id=response.json['id']).one_or_none()

    assert customer_db
    assert customer_db.id == response.json['id']
    assert customer_db.name == response.json['name']
    assert customer_db.email == response.json['email']
    assert customer_db.created_date.strftime(DATE_FORMAT) == response.json['created_date']
    assert customer_db.updated_date.strftime(DATE_FORMAT) == response.json['updated_date']
    assert customer_db.verify_password(customer_password)


def test_delete_customer(client, db):
    set_up(db)
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

    response = client.delete('/api/customer', headers=headers, follow_redirects=True)

    assert response.status_code == 200

    customer_db = db.session.query(Customer).filter_by(id=customer.id).one_or_none()

    assert customer_db
    assert customer_db.id == customer.id
    assert customer_db.name == customer.name
    assert customer_db.email == customer.email
    assert customer_db.verify_password(password)
    assert customer_db.created_date.strftime(DATE_FORMAT) == customer.created_date.strftime(DATE_FORMAT)
    assert customer_db.updated_date.strftime(DATE_FORMAT) == customer.updated_date.strftime(DATE_FORMAT)
    assert customer_db.deleted_date


def test_delete_customer_by_id(client, db):
    set_up(db)
    user_password = "youAreMyOnlyHope"
    customer_password = "iAmDarthVader"
    user = User(name='Leia Organa', email='leia@luizalabs.com.br',
                password=generate_password_hash(user_password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(customer_password))
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=user_password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']

    name = "Darth Vader"
    email = "darthvader@starwars.com"
    headers = build_header(access_token)

    response = client.delete(f'/api/customer/{customer.id}', json=dict(
        name=name,
        email=email
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200

    customer_db = db.session.query(Customer).filter_by(id=customer.id).one_or_none()

    assert customer_db
    assert customer_db.id == customer.id
    assert customer_db.name == customer.name
    assert customer_db.email == customer.email
    assert customer_db.created_date.strftime(DATE_FORMAT) == customer.created_date.strftime(DATE_FORMAT)
    assert customer_db.updated_date.strftime(DATE_FORMAT) == customer.updated_date.strftime(DATE_FORMAT)
    assert customer_db.deleted_date


def test_change_customer_password(client, db):
    set_up(db)
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

    new_password = "iAmVader"

    headers = build_header(access_token)

    response = client.put('/api/customer/password', json=dict(
        password=password,
        new_password=new_password
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200

    customer_db = db.session.query(Customer).filter_by(id=customer.id).one_or_none()

    assert customer_db.verify_password(new_password)


def test_get_customer(client, db):
    set_up(db)
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

    response = client.get('/api/customer', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == customer.id
    assert response.json['name'] == customer.name
    assert response.json['email'] == customer.email
    assert customer.verify_password(password)


def test_get_customer_by_id(client, db):
    set_up(db)
    user_password = "youAreMyOnlyHope"
    customer_password = "iAmDarthVader"
    user = User(name='Leia Organa', email='leia@luizalabs.com.br',
                password=generate_password_hash(user_password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(customer_password))
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=user_password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/customer/{customer.id}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == customer.id
    assert response.json['name'] == customer.name
    assert response.json['email'] == customer.email
    assert customer.verify_password(customer_password)


def test_get_customer_by_email(client, db):
    set_up(db)
    user_password = "youAreMyOnlyHope"
    customer_password = "iAmDarthVader"
    user = User(name='Leia Organa', email='leia@luizalabs.com.br',
                password=generate_password_hash(user_password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    customer = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                        password=generate_password_hash(customer_password))
    db.session.add(user)
    db.session.add(customer)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=user_password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/customer/email/{customer.email}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == customer.id
    assert response.json['name'] == customer.name
    assert response.json['email'] == customer.email
    assert customer.verify_password(customer_password)


def test_get_all_customers(client, db):
    set_up(db)
    user_password = "youAreMyOnlyHope"
    customer_1_password = "iAmDarthVader"
    customer_2_password = "iKnow"
    user = User(name='Leia Organa', email='leia@luizalabs.com.br',
                password=generate_password_hash(user_password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    customer_1 = Customer(name="Anakin Skywalker", email="anakin@starwars.com",
                          password=generate_password_hash(customer_1_password))
    customer_2 = Customer(name="Han Solo", email="han@starwars.com",
                          password=generate_password_hash(customer_2_password))

    db.session.add(user)
    db.session.add(customer_1)
    db.session.add(customer_2)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=user_password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/customer/', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 3

    customers = db.session.query(Customer).all()

    for index, customer in enumerate(response.json, start=0):
        customer_db = customers[index]
        assert customer_db.id == customer['id']
        assert customer_db.name == customer['name']
        assert customer_db.email == customer['email']

    response = client.get(f'/api/customer/1/1', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 1

    customers = db.session.query(Customer).all()
    customer_db = customers[0]
    customer = response.json[0]

    assert customer_db.id == customer['id']
    assert customer_db.name == customer['name']
    assert customer_db.email == customer['email']
