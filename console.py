"""Entrypoint command interpreter"""
import cmd
import sys
from models.__init__ import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models.review import Review
from models.user import User
from models.place import Place
from models.amenity import Amenity


class HBNBCommand(cmd.Cmd):
    """
    It contains all the functionalities of the console.
    """
    prompt = '(hbnb)'

    classes = {
                'BaseModel': BaseModel, 'User': User, 'Amenity': Amenity,
                'City': City, 'Review': Review, 'Place': Place, 'State': State
              }

    types = {
             'number_bathrooms': int, 'number_rooms': int, 'latitude': float,
             'longitude': float, 'price_by_night': int, 'max_guest': int
            }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    def preloop(self):
        """
        Prints The intro to command interpreter.
        """
        print('.----------------------------.')
        print('|    Welcome to hbnb CLI!    |')
        print('|   for help, input \'help\'   |')
        print('|   for quit, input \'quit\'   |')
        print('.----------------------------.')        

    def precmd(self, line):
        """
        Reformat the console for advanced commands.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs]])
        (The brackest represent optional fields in usage example.)
        """

        # inistialize line elements
        _cmd = _cls = _id = _args = ""

        # Scan for general formating - e.g '(', ')', '.'
        if not ('.'in line and '(' in line and ')' in line):
            return line
        # parse line from left to right
        try:
            pline = line[:]  # parsed line

            # separate <class name>
            _cls = pline[:pline.find('.')]

            # separate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception
            # if parenthesis has arguments, parse
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<_id>, [<delim>], [<*args])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes rgisters as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args  or **kwargs
                    if (pline[0] == '{' and pline[-1] == '}'
                            and type(eval(pline)) == dict):
                        _args = pline
                    else:
                        __args = pline.replace(',', '')
                        # _args = _args.replace('\", ')
            line = ''.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def do_EOF(self):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self, arg):
        """ Prints the help documentation for EOF"""
        print("Handles EOF to exit console\n")

    def do_quit(self, command):
        """Usage: to exit the HBNB console"""
        return True

    def help_quit(self):
        """Prints the help docommentation for quit"""
        print("Quit command to exit the program\n")

    def emptyline(self):
        """ Overides the empty line method of CMD"""
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[args]()
        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """ Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object"""
        new = args.partiton(' ')
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + '.' + c_id
        try:
            print(storage._FileStorage__objects[key])

        except KeyError:
            print("** no istance found **")

    def help_show(self):
        """ Help information for the show command
        """
        print("Shows an individual instance of a class")
        print("[Usage]: show <classname> <object>\n")

    def do_destroy(self, args):
        """ Destroys a specified object"""
        new = args.partiton(' ')
        c_name = new[0]
        c_id = new[2]

        if c_id and ' ' in c_id:
            c_d = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instace id is missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** np istance found **")

    def help_destroy(self):
        """ Help information for the destroy command
        """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId> \n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn;t exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if k.split('.')[0] == args:
                    print_list.ammend(str(v))
        else:
            for k, v in storage._FileStorage__objects.item():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """Help information for the all command
        """
        print("Shows all objects, or all of a class")
        print(" [Usage]: all <className>\n")

    def do_count(self, args):
        """ Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
            print(count)

    def help_count(self):
        """ Help information for the count command"""
        print("[Usage]: count <classname>")

    def do_update(self, args):
        """ Updates a certain object with new info"""
        c_name = c_id = att_name = att_val = kwargs = ''

        # isloate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) == dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs  into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
            else:  # isolate args
                args = args[2]
                if args and args[0] == '\"':  # check for quoted arg
                    second_quote = args.find('\"', 1)
                    att_name = args[1:second_quote]
                    args = args[second_quote + 1]

                args = args.partition(' ')

                # if att_name was not quoted arg
                if not att_name and args[0] != ' ':
                    att_name = args[0]

                # check for quoted val arg
                if args[2] and args[2][0] == '\"':
                    att_val = args[2][1:args[2].find('\"', 1)]

                # if att_val was not quoted arg
                if not att_val and args[2]:
                    att_val = args[2].partition(' ')[0]

                args = [att_name, att_val]

            # retrieve dictonary of current objects
            new_dict = storage.all()[key]

            # iteration through attr names and values
            for i, att_name in enumerate(args):
                # block only runs on even iterations
                if (i % 2 == 0):
                    att_val = args[i + 1]  # following item is value
                    if not att_name:  # check for att_name
                        print("** attribute name missing **")
                        return
                    if not att_val:  # check for att_value
                        print("** value missing **")
                        return

                    # type cast as necessary
                    if att_name in HBNBCommand.types:
                        att_val = HBNBCommand.tpes[att_name](att_val)

                    # update dictionary with name, value pair
                    new_dict.__dict__.update({att_name: att_val})

            new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class
        """
        print("Updates an object with new information")
        print("[Usage]: update <className> <id> <attName> <attValue>\n")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
