#!/usr/bin/python3
"""User class for storing user information."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class User(BaseModel, Base):
    """User class for storing user information.

    Attributes:
        email (str): Email address.
        password (str): Password for login.
        first_name (str): First name.
        last_name (str): Last name.
    """
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    places = relationship(
        "Place",
        cascade="all,delete",
        backref=backref("user", cascade="all,delete"),
        passive_deletes=True,
        single_parent=True)

    reviews = relationship(
        "Review",
        cascade="all,delete",
        backref=backref("user", cascade="all,delete"),
        passive_deletes=True,
        single_parent=True)
