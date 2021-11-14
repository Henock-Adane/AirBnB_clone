#!/usr/bin/python3
""" 
This module defines a class to manage file storage 
for the Airbnnb clone project
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """ This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """initialising"""
        pass

    def all(self):
        """ Returns a dictionary of models currently in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """ Adds new object to storage dictionary"""
        FileStorage.__objects["{}.{}".format(obj.__class__.__name__,
                                             obj.id)] = obj

    def save(self):
        """ Saves storage dictionary to a file"""
        obj_dict = {
            key: value.to_dict()
            for key, value in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as json_file:
            json.dump(obj_dict, json_file)

    def reload(self):
        """ Loads storage dictionary from file"""
        try:
            with open(FileStorage.__file_path, "r") as json_file:
                obj_dict = json.load(json_file)
                for obj_str in obj_dict.values():
                    cls = eval(obj_str["__class__"])
                    new_obj = cls(**obj_str)
                    self.new(new_obj)

        except FileNotFoundError:
            pass
