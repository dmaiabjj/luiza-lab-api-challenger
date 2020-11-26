from app import db


class BaseRepository:
    def __init__(self, clazz, session=db.session):
        if session:
            self.__session = session
        self.__clazz = clazz

    def add(self, entity):
        self.__session.add(entity)
        return entity

    def find_by_id(self, id):
        self.__session.query(self.__clazz).filter(self.__clazz.id == id).order_by(self.__clazz.id).first()

    def get_all(self):
        self.__session.query(self.__clazz).all()

    def get_all_by_paging(self, offset=None, limit=None):
        query = self.__session.query(self.__clazz).order_by(self.__clazz.id)
        query = query.offset(offset) if offset else query
        query = query.limit(limit) if limit else query
        return query.all()
