from functools import wraps

from core.database.session import DBSession


def with_db_session(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        db_session = DBSession()
        result = method(db_session, *args, **kwargs)
        db_session.close()
        return result
    return wrapper
