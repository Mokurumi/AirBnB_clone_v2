#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        # Use f-strings for better readability
        self.__engine = create_engine(f"mysql+mysqldb://{getenv(
            'HBNB_MYSQL_USER')}:{getenv('HBNB_MYSQL_PWD')}@{getenv(
                'HBNB_MYSQL_HOST')}/{getenv('HBNB_MYSQL_DB')}",
                pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            # Use declarative_base instead of Base.metadata.drop_all
            # for better code organization
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects of the given class.

        If cls is None, queries all types of objects.

        Returns:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        # Simplify the code using a dictionary comprehension
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
            objs = [obj for cls in classes
                    for obj in self.__session.query(cls).all()]
        else:
            # Use isinstance for checking the type
            objs = self.__session.query(cls) if isinstance(
                cls, type) else self.__session.query(eval(cls))
        return {f"{type(o).__name__}.{o.id}": o for o in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        # Use declarative_base instead of Base.metadata.drop_all
        # for better code organization
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        call remove() method on the private session attribute (self.__session)
        or close() on the class Session
        """
        self.__session.remove()
