from werkzeug.security import generate_password_hash
from app.domain.user.user import User, UserRole, RoleCategory
from test import build_header, DATE_FORMAT
from test.conftest import set_up


def test_add_user(client, db):
    set_up(db)

    response = client.post('/api/auth/user/token', json=dict(
        email="luke@luizalabs.com.br",
        password="darthVaderIsMyFather"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    name = "Anakin Skywalker"
    email = "anakin@luizalabs.com.br"
    password = "iAmDarthVader"

    response = client.post('/api/user', json=dict(
        name=name,
        email=email,
        password=password
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['name'] == name
    assert response.json['email'] == email
    assert response.json['created_date']

    user = db.session.query(User).filter_by(id=response.json['id']).one_or_none()

    assert user
    assert user.id == response.json['id']
    assert user.name == response.json['name']
    assert user.email == response.json['email']
    assert user.created_date.strftime(DATE_FORMAT) == response.json['created_date']
    assert user.verify_password(password)


def test_update_user(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    name = "Darth Vader"
    email = "darthvader@starwars.com"
    headers = build_header(access_token)

    response = client.put('/api/user', json=dict(
        name=name,
        email=email
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id']
    assert response.json['name'] == name
    assert response.json['email'] == email
    assert response.json['created_date']
    assert response.json['updated_date']

    user_db = db.session.query(User).filter_by(id=response.json['id']).one_or_none()

    assert user_db
    assert user_db.id == response.json['id']
    assert user_db.name == response.json['name']
    assert user_db.email == response.json['email']
    assert user_db.created_date.strftime(DATE_FORMAT) == response.json['created_date']
    assert user_db.updated_date.strftime(DATE_FORMAT) == response.json['updated_date']
    assert user_db.verify_password(password)


def test_delete_user(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.delete('/api/user', headers=headers, follow_redirects=True)

    assert response.status_code == 200

    user_db = db.session.query(User).filter_by(id=user.id).one_or_none()

    assert user_db
    assert user_db.id == user.id
    assert user_db.name == user.name
    assert user_db.email == user.email
    assert user_db.verify_password(password)
    assert user_db.created_date.strftime(DATE_FORMAT) == user.created_date.strftime(DATE_FORMAT)
    assert user_db.updated_date.strftime(DATE_FORMAT) == user.updated_date.strftime(DATE_FORMAT)
    assert user_db.deleted_date


def test_change_customer_password(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])

    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    new_password = "iAmVader"
    headers = build_header(access_token)

    response = client.put('/api/user/password', json=dict(
        password=password,
        new_password=new_password
    ), headers=headers, follow_redirects=True)

    assert response.status_code == 200

    user_db = db.session.query(User).filter_by(id=user.id).one_or_none()

    assert user_db.verify_password(new_password)


def test_get_user(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])

    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email=user.email,
        password=password
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']

    headers = build_header(access_token)

    response = client.get('/api/user', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == user.id
    assert response.json['name'] == user.name
    assert response.json['email'] == user.email
    assert user.verify_password(password)


def test_get_user_by_id(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])

    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email="luke@luizalabs.com.br",
        password="darthVaderIsMyFather"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/user/{user.id}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == user.id
    assert response.json['name'] == user.name
    assert response.json['email'] == user.email
    assert user.verify_password(password)


def test_get_user_by_email(client, db):
    set_up(db)
    password = "iAmDarthVader"
    user = User(name="Anakin Skywalker", email="anakin@luizalabs.com.br",
                password=generate_password_hash(password),
                roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])

    db.session.add(user)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email="luke@luizalabs.com.br",
        password="darthVaderIsMyFather"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/user/email/{user.email}', headers=headers, follow_redirects=True)

    assert response.status_code == 200
    assert response.json['id'] == user.id
    assert response.json['name'] == user.name
    assert response.json['email'] == user.email
    assert user.verify_password(password)


def test_get_all_user(client, db):
    set_up(db)
    user_1_password = "youAreMyOnlyHope"
    user_2_password = "iKnow"
    user_1 = User(name='Leia Organa', email='leia@luizalabs.com.br',
                  password=generate_password_hash(user_1_password),
                  roles=[UserRole(category=RoleCategory.SUPER_USER), UserRole(category=RoleCategory.ADMIN)])
    user_2 = User(name="Han Solo", email="han@starwars.com",
                  password=generate_password_hash(user_2_password))

    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    response = client.post('/api/auth/user/token', json=dict(
        email="luke@luizalabs.com.br",
        password="darthVaderIsMyFather"
    ), follow_redirects=True)

    assert response.status_code == 200
    assert response.json['access_token'] is not None

    access_token = response.json['access_token']
    headers = build_header(access_token)

    response = client.get(f'/api/user/', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 3

    users = db.session.query(User).all()

    for index, customer in enumerate(response.json, start=0):
        user_db = users[index]
        assert user_db.id == customer['id']
        assert user_db.name == customer['name']
        assert user_db.email == customer['email']

    response = client.get(f'/api/user/1/1', headers=headers, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 1

    users = db.session.query(User).all()
    user_db = users[0]
    user = response.json[0]

    assert user_db.id == user['id']
    assert user_db.name == user['name']
    assert user_db.email == user['email']
