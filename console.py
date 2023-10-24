#!/usr/bin/python3
"""Defines the HBNB console needed for airbnb."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNB COMMAND """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel", "User", "State", "City", "Amenity","Place","Review"
    }

    def emptyline(self):
        """Ignore empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """
        updated create function
        """
        try:
            if not line:
                raise SyntaxError()
            mylist = line.split(" ")

            kwargs = {}
            for i in range(1, len(mylist)):
                key, value = tuple(mylist[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value
            if kwargs == {}:
                obj = eval(mylist[0])()
            else:
                obj = eval(mylist[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        shows the string representation of an instance
        """
        try:
            if not line:
                raise SyntaxError()
            mylist = line.split(" ")
            if mylist[0] not in self.__classes:
                raise NameError()
            if len(mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = mylist[0] + '.' + mylist[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """
        Destroy instances
        """
        try:
            if not line:
                raise SyntaxError()
            mylist = line.split(" ")
            if mylist[0] not in self.__classes:
                raise NameError()
            if len(mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = mylist[0] + '.' + mylist[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """
        do all
        """
        if not line:
            my_all = storage.all()
            print([my_all[key].__str__() for key in my_all])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            my_all = storage.all(eval(args[0]))
            print([my_all[key].__str__() for key in my_all])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
        Updates an instanceby adding or updating attribute
        """
        try:
            if not line:
                raise SyntaxError()
            mylist = split(line, " ")
            if mylist[0] not in self.__classes:
                raise NameError()
            if len(mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = mylist[0] + '.' + mylist[1]
            if key not in objects:
                raise KeyError()
            if len(mylist) < 3:
                raise AttributeError()
            if len(mylist) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[mylist[2]] = eval(mylist[3])
            except Exception:
                v.__dict__[mylist[2]] = mylist[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """
        count method
        """
        i = 0
        try:
            mylist = split(line, " ")
            if mylist[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == mylist[0]:
                    i += 1
            print(i)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """
        cleans up
        """
        newlist = []
        newlist.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            newlist.append(((new_str.split(", "))[0]).strip('"'))
            newlist.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        newlist.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in newlist)

    def default(self, line):
        """
        default function
        """
        mylist = line.split('.')
        if len(mylist) >= 2:
            if mylist[1] == "all()":
                self.do_all(mylist[0])
            elif mylist[1] == "count()":
                self.count(mylist[0])
            elif mylist[1][:4] == "show":
                self.do_show(self.strip_clean(mylist))
            elif mylist[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(mylist))
            elif mylist[1][:6] == "update":
                args = self.strip_clean(mylist)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
