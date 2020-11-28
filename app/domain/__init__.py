import enum
from datetime import datetime

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.inspection import inspect as sql_alchemy_inspect
from app import db

PRIMITIVE = (int, str, bool, float)


def is_primitive(thing):
    return isinstance(thing, PRIMITIVE)


class BaseModel(SerializerMixin):
    serialize_types = (
        (enum.Enum, lambda x: x.name),
    )

    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_date = db.Column(db.DateTime)

    def update_from_dict(self, source):
        for key, value in source.items():
            if hasattr(self, key) and is_primitive(value):
                setattr(self, key, value)

    def update_from_model(self, source):
        if not source:
            return None
        clazz = type(self)
        inspected_model = sql_alchemy_inspect(clazz)
        for attr, column in inspected_model.columns.items():
            if attr in source.__dict__:
                value = getattr(source, attr)
                setattr(self, attr, value)
