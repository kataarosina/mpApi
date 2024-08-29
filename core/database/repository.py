from sqlalchemy import select, update
from sqlalchemy.orm.exc import NoResultFound

from core.database.session import DBSession


# TODO do it better.
class SQLAlchemyModelRepository:

    model_class = None

    @classmethod
    def get(cls, db_session: DBSession, pk: int):
        obj = db_session.get(cls.model_class, pk)
        if obj is None:
            raise NoResultFound(f'Record with id={pk} of class {cls.model_class.__name__} was not found.')
        return obj

    @classmethod
    def get_all(cls, db_session: DBSession):
        stmt = select(cls.model_class)
        objs = db_session.scalars(stmt).all()
        return objs

    @classmethod
    def create(cls, db_session: DBSession, data: dict):
        try:
            new_obj = cls.model_class(**data)
            db_session.add(new_obj)
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            db_session.commit()
            return new_obj

    @classmethod
    def update(cls, db_session: DBSession, pk: int, data: dict):
        stmt = update(cls.model_class).where(cls.model_class.id == pk).values(**data)
        db_session.execute(stmt)
        return None

    @classmethod
    def delete(cls, db_session: DBSession, pk: int):  # TODO, can i get pk or obj instead only pk?
        obj = cls.get(db_session, pk)
        db_session.delete(obj)
        db_session.commit()
