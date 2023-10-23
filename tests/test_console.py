#!/usr/bin/python3
"""Unittest module for the console"""

from console import HBNBCommand
import unittest
from io import StringIO
import MySQLdb
import io
import os
import json
from models.engine.file_storage import FileStorage
from unittest.mock import patch
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from tests import clear_stream
import sqlalchemy
from models import storage



class TestCommand(unittest.TestCase):
    """Class that tests the console"""
    
    def setUp(self):
        """set up function by emptying file.json"""
        FileStorage._FileStorage__objects = {}
        FileStorage().save()
    
    def test_console_docstring(self):
        """checking docstrings for functions"""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
    
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_create_filestorage(self):
        """Tests the create cmd with the file storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            consule = HBNBCommand()
            consule.onecmd('create City name="Cairo"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            consule.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Cairo'", cout.getvalue().strip())
            clear_stream(cout)
            consule.onecmd('create User name="Salma" age=30 height=160')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            consule.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'Salma'", cout.getvalue().strip())
            self.assertIn("'age': 30", cout.getvalue().strip())
            self.assertIn("'height': 160", cout.getvalue().strip())
    
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create cmd with the database storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            consule = HBNBCommand()
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                consule.onecmd('create User')
            clear_stream(cout)
            consule.onecmd('create User email="salma@email.com" password="0000"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('salma@email.com', result)
            self.assertIn('0000', result)
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Cairo"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cursor.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show cmd with the database storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            consule = HBNBCommand()
            new_obj = User(email="salma@email.com", password="0000")
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
            res = cursor.fetchone()
            self.assertTrue(res is None)
            consule.onecmd('show User {}'.format(new_obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            new_obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = dbc.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new_obj.id))
            clear_stream(cout)
            consule.onecmd('show User {}'.format(new_obj.id))
            res = cursor.fetchone()
            self.assertTrue(res is not None)
            self.assertIn('salma@email.com', res)
            self.assertIn('0000', res)
            self.assertIn('salma@email.com', cout.getvalue())
            self.assertIn('0000', cout.getvalue())
            cursor.close()
            dbc.close()
        

if __name__ == '__main__':
    unittest.main()

