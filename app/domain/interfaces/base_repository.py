from app import db


class BaseRepository:
    def __init__(self, clazz, session=db.session):
        if session:
            self.__session = session
        self.__clazz = clazz

    def add(self, entity):
        self.__session.add(entity)
        self.__session.commit()
        return entity

    def update(self, entity):
        self.__session.add(entity)
        self.__session.commit()
        return entity

    def find_by_id(self, id):
        return self.__clazz.query.filter(self.__clazz.id == id).one_or_none()

    def get_all(self):
        return self.__clazz.query.all()

    def get_all_by_paging(self, offset=None, limit=None):
        query = self.__clazz.query.order_by(self.__clazz.id)
        query = query.offset(offset - 1) if offset else query
        query = query.limit(limit) if limit else query
        return query.all()
