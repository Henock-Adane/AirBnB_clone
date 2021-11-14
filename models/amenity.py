#!/usr/bin/python3
""" Amenity module for Airbnb clone project"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent an amenity.
    Attributes:
        name (str): The name of the amenity.
    """
    name = ""
