from os import getenv as env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():
    engine = create_engine(get_connection_string())
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


def get_connection_string():
    driver = "postgresql+psycopg2"
    return f'{driver}://{env("POSTGRES_USER")}:{env("POSTGRES_PASSWORD")}@{env("POSTGRES_SERVICE_PORT_5432_TCP_ADDR")}:{env("POSTGRES_SERVICE_PORT_5432_TCP_PORT")}/{env("POSTGRES_DB")}'  # noqa: E501


def get_db():
    try:
        db = create_session()
        yield db
    finally:
        if db:
            db.close()
