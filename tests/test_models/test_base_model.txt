#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os
import pycodestyle
import inspect
from unittest.mock import patch
from time import sleep
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from os import getenv
import pycodestyle

storage_t = getenv("HBNB_TYPE_STORAGE")
class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity


class test_Amenity_BaseModel(unittest.TestCase):
    """Testing user class"""
    def test_instances(self):
        with patch('models.amenity'):
            instance = Amenity()
            self.assertEqual(type(instance), Amenity)
            instance.name = "Barbie"
            expectec_attrs_types = {
                    "id": str,
                    "created_at": datetime,
                    "updated_at": datetime,
                    "name": str,
                    }
            inst_dict = instance.to_dict()
            expected_dict_attrs = [
                    "id",
                    "created_at",
                    "updated_at",
                    "name",
                    "__class__"
                    ]
            self.assertCountEqual(inst_dict.keys(), expected_dict_attrs)
            self.assertEqual(inst_dict['name'], 'Barbie')
            self.assertEqual(inst_dict['__class__'], 'Amenity')


    def test_user_id_and_createat(self):
        """testing id for every user"""
        user_1 = Amenity()
        sleep(2)
        user_2 = Amenity()
        sleep(2)
        user_3 = Amenity()
        sleep(2)
        list_users = [user_1, user_2, user_3]
        for instance in list_users:
            user_id = instance.id
            with self.subTest(user_id=user_id):
                self.assertIs(type(user_id), str)
        self.assertNotEqual(user_1.id, user_2.id)
        self.assertNotEqual(user_1.id, user_3.id)
        self.assertNotEqual(user_2.id, user_3.id)
        self.assertTrue(user_1.created_at <= user_2.created_at)
        self.assertTrue(user_2.created_at <= user_3.created_at)
        self.assertNotEqual(user_1.created_at, user_2.created_at)
        self.assertNotEqual(user_1.created_at, user_3.created_at)
        self.assertNotEqual(user_3.created_at, user_2.created_at)

    def test_str_method(self):
        """
        Testin str magic method
        """
        inst = Amenity()
        str_output = "[Amenity] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(str_output, str(inst))

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Testing save method and if it update"""
        instance5 = Amenity()
        created_at = instance5.created_at
        sleep(2)
        updated_at = instance5.updated_at
        instance5.save()
        new_created_at = instance5.created_at
        sleep(2)
        new_updated_at = instance5.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))

    def test_name_attr(self):
        """Test that Amenity has attribute name, and it's as an empty string"""
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, "name"))

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        am = Amenity()
        print(am.__dict__)
        new_d = am.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in am.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        am = Amenity()
        new_d = am.to_dict()
        self.assertEqual(new_d["__class__"], "Amenity")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], am.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], am.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        amenity = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amenity.__dict__)
        self.assertEqual(string, str(amenity))
if __name__ == "__main__":
    unittest.main()
