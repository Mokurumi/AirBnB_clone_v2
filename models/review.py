#!/usr/bin/python3
"""This is the review class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Review class for storing review information.

    Attributes:
        text (str): Review description.
        place_id (str): Place ID.
        user_id (str): User ID.
    """
    __tablename__ = "reviews"

    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
