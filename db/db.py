from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker()


def bind_engine(engine):
    Base.metadata.bind = engine
    Session.configure(bind=engine)
