#!/usr/bin/python3
"""
This is a Model class that will be the base for all the
classes to be created in the airbnb module. This class
will define all the basic things (attributes and functions)
that will be used through out the project by other class
as well
"""

from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """A base for all the classes in the AirBnb console project
    Public instance Atrributes:
        @id: string - assigned with an uuid when an instance is created
        @created_at: datetime - assign with the current datetime when
                     an instance is created
        @updated_at: datetime - assign with the current datetime when
                     an instance is created and it will be updated every
                     time you change your object
    Public instance Methods:
        @__str__: should print: [<class name>] (<self.id>) <self.__dict__>
        @save(self): updates the public instance attribute updated_at with
                     the current datetime
        @to_dict(self): returns a dictionary containing all keys/values of
                        __dict__ of the instance:
            - by using self.__dict__, only instance attributes set will be
              returned
            - a key __class__ must be added to this dictionary with the class
              name of the object
            - created_at and updated_at must be converted to string object in
              ISO format:
                - format: %Y-%m-%dT%H:%M:%S.%f (ex: 2017-06-14T22:31:03.285259)
    """
    def __init__(self, *args, **kwargs):
        """
        Initlizes the public attributes of the instance after creation
        """

        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = self.created_at

    def __str__(self):
        """
        Returns the string representation of this class
        """

        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """
        updates the updated_at public instance variable
        """

        self.updated_at = datetime.today()

    def to_dict(self):
        """
            return the dictionary representation of the object
        """

        obj_dict = {}
        obj_dict["__class__"] = self.__class__.__name__
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                obj_dict[key] = value.isoformat()
            else:
                obj_dict[key] = value

        return obj_dict
