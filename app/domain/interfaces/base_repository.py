from datetime import datetime

from sqlalchemy import and_

from app import db


class BaseRepository:
    def __init__(self, clazz, session=db.session):
        if session:
            self.__session = session
        self.__clazz = clazz

    def bind_filter(self, include_deleted, filter=None):
        if not include_deleted and filter is not None:
            filter = and_(filter, self.__clazz.deleted_date.is_(None))
        elif not include_deleted and filter is None:
            filter = self.__clazz.deleted_date.is_(None)

        return filter

    def add(self, entity):
        self.__session.add(entity)
        self.__session.commit()
        return entity

    def update_from_dict(self, entity, data):
        entity.update_from_dict(data)
        entity.updated_date = datetime.utcnow()
        entity.deleted_date = None
        self.__session.commit()
        return entity

    def update_from_model(self, entity, data):
        entity.update_from_model(data)
        entity.updated_date = datetime.utcnow()
        self.__session.commit()
        return entity

    def delete(self, entity):
        entity.deleted_date = datetime.utcnow()
        self.__session.commit()
        return entity

    def find_by_id(self, id, include_deleted=False):
        filter = self.bind_filter(filter=self.__clazz.id == id, include_deleted=include_deleted)
        return self.__clazz.query.filter(filter).one_or_none()

    def get_all(self, include_deleted=False):
        filter = self.bind_filter(include_deleted=include_deleted)
        return self.__clazz.query.filter(filter).all()

    def get_all_paginated(self, offset=None, limit=None, include_deleted=False):
        filter = self.bind_filter(include_deleted=include_deleted)
        query = self.__clazz.query.filter(filter).order_by(self.__clazz.id)
        query = query.offset(offset) if offset else query
        query = query.limit(limit) if limit else query
        return query.all()
