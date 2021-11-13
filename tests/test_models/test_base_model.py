#!/usr/bin/python3
"""
Tests attributs and methods in the base_model module
"""
from models.base_model import BaseModel
import unittest
from datetime import datetime

class TestBaseInitiation(unittest.TestCase):
    """
    Tests the initiation of the BaseModel class
    """
    def test_initiation(self):
        """Tests initiation"""

        cls = BaseModel()
        self.assertIsInstance(cls, BaseModel)


class TestBaseNoKwargs(unittest.TestCase):
    """
    Tests the public attributes of the BaseModel class.
    Requirment:
        Public instance attributes:
            id: string - assign with an uuid when an instance
                is created:
            created_at: datetime - assign with the current
                        datetime when an instance is created
            updated_at: datetime - assign with the current datetime
                        when an instance is created and it will be updated
                        every time you change your objet
        __str__: should print: [<class name>] (<self.id>) <self.__dict__>
        Public instance methods:
            save(self): updates the public instance attribute updated_at with
                        the current datetime
            to_dict(self): returns a dictionary containing all keys/values of
                            __dict__ of the instance:
                - by using self.__dict__, only instance attributes set will be
                    returned
                - a key __class__ must be added to this dictionary with the
                    class name of the object
                - created_at and updated_at must be converted to string
                    object in ISO format:
                    format: %Y-%m-%dT%H:%M:%S.%f
    """
    def assertDateTimeAlmostEqual(self, t1, t2):
        """
            checks the two datetime objects
            by comparing their year, month, date, hour, and minute but
            not sec and millissecond
        """
        self.assertEqual(t1.year, t2.year)
        self.assertEqual(t1.month, t2.month)
        self.assertEqual(t1.day, t2.day)
        self.assertEqual(t1.hour, t2.hour)
        self.assertEqual(t1.minute, t2.minute)

    def setUp(self):
        """
        Creates objects needed for testing
        """

        self.obj1_creation = datetime.today()
        self.obj1 = BaseModel()

        self.obj2 = BaseModel()

        self.obj3 = BaseModel()
        # Include extra variables to make sure they are handeld
        # by the to_dict function
        self.obj3.name = "string three"
        self.obj3.number = 1216
        self.obj3_obj = self.obj3.to_dict()


    def test_id_exists(self):
        """
        test if the id attribute exists
        """
        # Test if id attribute exists
        self.assertIn("id", self.obj1.__dict__.keys())
        self.assertIn("id", self.obj2.__dict__.keys())
        self.assertIn("id", self.obj3.__dict__.keys())

    def test_id_type(self):
        """
        Tests the type for the id attribute
        """

        # Test if it is a string
        self.assertIsInstance(self.obj1.id, str)
        self.assertIsInstance(self.obj2.id, str)

    def test_id_uniquness(self):
        """
        Tests the uniquness of each id attribute
        """

        TESTS = 100
        obj_id = [BaseModel().id for i in range(TESTS)]
        # Test that ids from different objects
        for i in range(TESTS):
            for j in range(i + 1, TESTS):
                self.assertNotEqual(obj_id[i], obj_id[j])

    def test_time_exists(self):
        """
        Tests the created_at and updated_at
        public attributes
        """

        # Test if created_at and updated_at attribute exists
        self.assertIn("created_at", self.obj1.__dict__.keys())
        self.assertIn("created_at", self.obj2.__dict__.keys())
        self.assertIn("created_at", self.obj3.__dict__.keys())

        self.assertIn("updated_at", self.obj1.__dict__.keys())
        self.assertIn("updated_at", self.obj2.__dict__.keys())
        self.assertIn("updated_at", self.obj3.__dict__.keys())

    def test_time_type(self):
        """
            Test if the created_at and updated_at attrubutes have the
            corrcet datatype
        """

        # Tests if they are instances of datetime
        self.assertIsInstance(self.obj1.created_at, datetime)
        self.assertIsInstance(self.obj2.created_at, datetime)
        self.assertIsInstance(self.obj3.created_at, datetime)

        self.assertIsInstance(self.obj1.updated_at, datetime)
        self.assertIsInstance(self.obj2.updated_at, datetime)
        self.assertIsInstance(self.obj3.updated_at, datetime)

    def test_time(self):
        """
        Tests the value of created_at and updated_at
        public attributes
        """

        # Test if the created_at attribute is around the correct time
        self.assertDateTimeAlmostEqual(self.obj1_creation,
                                       self.obj1.created_at)

        # Tests if updated_at is coorrectly set
        self.assertDateTimeAlmostEqual(self.obj1.created_at,
                                       self.obj1.updated_at)

        self.obj1_update = datetime.today()
        # Test the change of updtaed time with the change of attribute
        self.obj1.id = "Random string has been set to be the id"

        # Test if the class updated_at variable is updated corrctly
        # with class updates
        self.assertDateTimeAlmostEqual(self.obj1_update, self.obj1.updated_at)

    def test_str(self):
        """
        Check if the string represtnation of the object is correctly formated
        """

        returned = self.obj1.__str__()
        expected = "[{}] ({}) {}".format(self.obj1.__class__.__name__,
                                         self.obj1.id, self.obj1.__dict__)

        # Test if the string represntation follows the format
        self.assertEqual(returned, expected)

    def test_save_exist(self):
        """
            Tests the existance of the save function
        """

        self.assertIn("save", self.obj2.__dir__())

    def test_save(self):
        """
            Test if the save function updates the time
        """

        self.obj2_update = datetime.today()
        self.obj2.save()

        # Test if the class updated_at variable is updated corrctly
        # with object updates
        self.assertDateTimeAlmostEqual(self.obj2_update, self.obj2.updated_at)

    def test_to_dict_exists(self):
        """
            check if the to_dict function exists
        """

        self.assertIn("to_dict", self.obj3.__dir__())

    def test_to_dict_keys(self):
        """
            Test if the basic attributes exist in the the reuturned object from
            to_dict function
        """

        self.assertIn("updated_at", self.obj3_obj.keys())
        self.assertIn("created_at", self.obj3_obj.keys())

    def test_to_dict(self):
        """
            Test if the to_dict function
            operates as it is intended
        """

        # Test if dict["updated_at"] & dict["created_at"] use the
        # isotime format
        self.assertEqual(self.obj3_obj["updated_at"],
                         self.obj3.updated_at.isoformat())
        self.assertEqual(self.obj3_obj["created_at"],
                         self.obj3.created_at.isoformat())

        self.obj3_dic = {
            "name": "string three",
            "number": 1216,
            "id": self.obj3.id,
            "updated_at": str(self.obj3.updated_at.isoformat()),
            "created_at": str(self.obj3.created_at.isoformat()),
            "__class__": self.obj3.__class__.__name__,
        }

        # Test if returned dictionary from to_dict  and the
        # excpected one are equal
        self.assertDictEqual(self.obj3_dic, self.obj3_obj)

