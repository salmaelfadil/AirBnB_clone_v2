#!/usr/bin/python3
""" new class for sqlAlchemy """
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """
    New engine DBStorage
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        public instances methods
        """
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        all method which returns a dictionary of instance
        """
        dictionary = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for i in query:
                key = "{}.{}".format(type(i).__name__, i.id)
                dic[key] = i
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for i in query:
                    key = "{}.{}".format(type(i).__name__, i.id)
                    dictionary[key] = i
        return (dictionary)

    def new(self, obj):
        """
        add new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """
        save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete element in table
        """
        if obj:
            self.session.delete(obj)

    def reload(self):
        """
        reload object
        """
        Base.metadata.create_all(self.__engine)
        sect = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sect)
        self.__session = Session()

    def close(self):
        """
        close session
        """
        self.__session.close()
