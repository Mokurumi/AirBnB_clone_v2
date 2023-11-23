#!/usr/bin/python3
"""Test for the console"""
import unittest
from unittest.mock import patch
from io import StringIO
import os
from os import getenv
import pep8
import json
import console
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """Test case for the console"""

    @classmethod
    def setUpClass(cls):
        """Set up for the test"""
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Tear down after the test"""
        del cls.console

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_console(self):
        """Check Pep8 for console.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["console.py"])
        self.assertEqual(result.total_errors, 0, 'Fix Pep8 issues')

    def test_docstrings_in_console(self):
        """Check docstrings"""
        self.assertIsNotNone(console.__doc__)
        methods = [
            HBNBCommand.emptyline, HBNBCommand.do_quit, HBNBCommand.do_EOF,
            HBNBCommand.do_create, HBNBCommand.do_show, HBNBCommand.do_destroy,
            HBNBCommand.do_all, HBNBCommand.do_update, HBNBCommand.count,
            HBNBCommand.strip_clean, HBNBCommand.default
        ]
        for method in methods:
            self.assertIsNotNone(method.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """Test quit command input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test create command input"""
        test_cases = [
            {"input": "create", "output": "** class name missing **\n"},
            {"input": "create asdfsfsd", "output": "** class doesn't exist **\n"},
            {"input": "create User", "output": "[[User]"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_show(self):
        """Test show command input"""
        test_cases = [
            {"input": "show", "output": "** class name missing **\n"},
            {"input": "show asdfsdrfs", "output": "** class doesn't exist **\n"},
            {"input": "show BaseModel", "output": "** instance id missing **\n"},
            {"input": "show BaseModel abcd-123", "output": "** no instance found **\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_destroy(self):
        """Test destroy command input"""
        test_cases = [
            {"input": "destroy", "output": "** class name missing **\n"},
            {"input": "destroy Galaxy", "output": "** class doesn't exist **\n"},
            {"input": "destroy User", "output": "** instance id missing **\n"},
            {"input": "destroy BaseModel 12345", "output": "** no instance found **\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_all(self):
        """Test all command input"""
        test_cases = [
            {"input": "all asdfsdfsd", "output": "** class doesn't exist **\n"},
            {"input": "all State", "output": "[]\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_update(self):
        """Test update command input"""
        test_cases = [
            {"input": "update", "output": "** class name missing **\n"},
            {"input": "update sldkfjsl", "output": "** class doesn't exist **\n"},
            {"input": "update User", "output": "** instance id missing **\n"},
            {"input": "update User 12345", "output": "** no instance found **\n"},
            {"input": "update User abcd-123", "output": "** attribute name missing **\n"},
            {"input": "update User abcd-123 Name", "output": "** value missing **\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_z_all(self):
        """Test alternate all command input"""
        test_cases = [
            {"input": "asdfsdfsd.all()", "output": "** class doesn't exist **\n"},
            {"input": "State.all()", "output": "[]\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_z_count(self):
        """Test count command input"""
        test_cases = [
            {"input": "asdfsdfsd.count()", "output": "** class doesn't exist **\n"},
            {"input": "State.count()", "output": "0\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_z_show(self):
        """Test alternate show command input"""
        test_cases = [
            {"input": "safdsa.show()", "output": "** class doesn't exist **\n"},
            {"input": "BaseModel.show(abcd-123)", "output": "** no instance found **\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    def test_destroy_alternate(self):
        """Test alternate destroy command input"""
        test_cases = [
            {"input": "Galaxy.destroy()", "output": "** class doesn't exist **\n"},
            {"input": "User.destroy(12345)", "output": "** no instance found **\n"},
        ]

        for case in test_cases:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(case["input"])
                self.assertEqual(case["output"], f.getvalue()[:len(case["output"])])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Not using db")
    def test_update_db(self):
        """Test alternate update command input DB"""
        return True


if __name__ == "__main__":
    unittest.main()
