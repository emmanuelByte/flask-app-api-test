from flask_bcrypt import Bcrypt
from flask import current_app, g
from werkzeug.local import LocalProxy
from typing import Optional

from pymongo import MongoClient, WriteConcern
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        DB_URI = current_app.config["MONGODB_DATABASE_URI"]
        DB_NAME = current_app.config["MONGODB_DATABASE_NAME"]
        db = g._database = MongoClient(DB_URI)[DB_NAME]

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)
users: Collection = LocalProxy(lambda: db.users)
revoked_tokens: Collection = LocalProxy(lambda: db.revoked_tokens)

##########
#
# Helpers
#
#########


def as_oid(id) -> ObjectId:
    return (ObjectId(id) if type(id) != ObjectId else id)

##########
#
# User
#
#########


USER_PROJECTION = {
    '_id': 1,
    'first_name': 1,
    'last_name': 1,
    'email': 1,
    'password': 1,
    'email_verified': "$_email_verified",
}

def get_user(id: str = None, email: str = None) -> Optional[dict]:
    projection = USER_PROJECTION
    if id is not None and  not (ObjectId.is_valid(str(id))):
        return None

    result = None
    if id != None:
        result = users.find_one({'_id': as_oid(id)}, projection)
    elif email != None:
        email = email.lower().strip()
        result = users.find_one({'email': email}, projection)
    else:
        raise AssertionError('one of id and email must not be empty')

    return result


def get_users(page=1, limit=20, filters={}):
    query = {}
    page = page if page > 0 else 1
    if filters:
        if 'search' in filters:
            query.update({'$text': {'$search': filters.get("search")}})

    userss = list(users.find(query).skip((page - 1) * limit).limit(limit))
    total = users.count_documents(query) or 0
    return userss, total

def user_exists(id: str = None, email: str = None) -> bool:
    projection = {
        '_id': 1,
        'email': 1,
    }
    if id is not None and  not (ObjectId.is_valid(str(id))):
        return False

    result = None
    if id != None:
        result = users.find_one({'_id': as_oid(id)}, projection)
    elif email != None:
        email = email.lower().strip()
        result = users.find_one({'email': email}, projection)
    else:
        raise AssertionError('one of id and email must not be empty')

    return result != None

def create_user(user: dict) -> Optional[dict]:
    try:
        if '_id' in user:
            del user['_id']
        user['email'] = user['email'].lower().strip() if user['email'] else None
        result = users.with_options(
            write_concern=WriteConcern(w='majority')).insert_one(user)
        if result.acknowledged:
            return get_user(result.inserted_id)
        return {'error': 'There was an error creating the user.'}
    except DuplicateKeyError:
        return {'error': 'A user with the given email already exists.'}


def get_bcrypt():
    bcrypt = getattr(g, '_bcrypt', None)
    if bcrypt is None:
        bcrypt = g._bcrypt = current_app.config['BCRYPT']
    return bcrypt


crypt: Bcrypt = LocalProxy(get_bcrypt)


def update_user(id, update_obj: dict) -> Optional[dict]:
    assert isinstance(update_obj, dict)
    if not (ObjectId.is_valid(str(id))):
        return None
    users.update_one({'_id': as_oid(id)}, {'$set': update_obj})
    return get_user(id=id)

##########
#
# JWT
#
#########

def revoke_jwt(jti):
    revoked_tokens.insert_one({'jti': jti})


def is_token_revoked(jti) -> bool:
    return revoked_tokens.find_one({'jti': jti}) != None

