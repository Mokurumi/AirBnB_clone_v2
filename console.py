#!/usr/bin/python3
"""This is the console for AirBnB"""
import cmd
import re
from models import storage
from shlex import split


class HBNBCommand(cmd.Cmd):
    """This class is the entry point of the command interpreter."""

    prompt = "(hbnb) "
    all_classes = {"BaseModel", "User", "State", "City",
                   "Amenity", "Place", "Review"}

    def emptyline(self):
        """Ignores empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Quit command to exit the program at the end of the file."""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel and saves it."""
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line)
            obj = eval("{}()".format(my_list[0]))
            for pair in my_list[1:]:
                pair = pair.split('=', 1)
                if len(pair) == 1 or "" in pair:
                    continue
                match = re.search('^"(.*)"$', pair[1])
                cast = str
                if match:
                    value = match.group(1).replace('_', ' ')
                    value = re.sub(r'(?<!\\)"', r'\\"', value)
                else:
                    value = pair[1]
                    cast = float if "." in value else int
                try:
                    value = cast(value)
                except ValueError:
                    pass
                setattr(obj, pair[0], value)
            obj.save()
            print("{}".format(obj.id))
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance."""
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line)
            if my_list[0] not in self.all_classes or len(my_list) < 2:
                raise NameError()
            objects = storage.all()
            key = "{}.{}".format(my_list[0], my_list[1])
            print(objects[key]) if key in objects else print("** no instance found **")
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id."""
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line)
            if my_list[0] not in self.all_classes or len(my_list) < 2:
                raise NameError()
            objects = storage.all()
            key = "{}.{}".format(my_list[0], my_list[1])
            storage.delete(objects[key]) if key in objects else print("** no instance found **")
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")

    def do_all(self, line):
        """Prints all string representation of all instances."""
        objects = storage.all()
        my_list = [objects[key] for key in objects] if not line else [objects[key] for key in objects if key.split('.')[0] == line.split(" ")[0]]
        print(my_list)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute."""
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line)
            if my_list[0] not in self.all_classes or len(my_list) < 4:
                raise NameError()
            objects = storage.all()
            key = "{}.{}".format(my_list[0], my_list[1])
            v = objects[key]
            v.__dict__[my_list[2]] = eval(my_list[3]) if len(my_list) > 3 else my_list[3]
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
        """Count the number of instances of a class."""
        counter = 0
        try:
            my_list = split(line)
            if my_list[0] not in self.all_classes:
                raise NameError()
            objects = storage.all()
            counter = sum(1 for key in objects if key.split('.')[0] == my_list[0])
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """Strips the argument and returns a string of command."""
        new_list = [args[0]]
        try:
            my_dict = eval(args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.extend(((new_str.split(", "))[0]).strip('"'), my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """Retrieve all instances of a class and retrieve the number of instances."""
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = "{} {}".format(args[0], args[1])
                    for k, v in args[2].items():
                        self.do_update(f'{key} "{k}" "{v}"')
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
