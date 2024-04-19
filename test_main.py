import sys
import unittest
import argparse
import xml.etree.ElementTree as ET

from unittest.mock import patch
from io import StringIO
from main import filter_persons, print_person

class TestFilterPerson(unittest.TestCase):
    def setUp(self):
        try:
            tree = ET.parse('example.xml')
            self.root = tree.getroot()
        except FileNotFoundError:
            sys.stderr.write("XML file not found. Please ensure the XML file exists.\n")
        except ET.ParseError:
            sys.stderr.write("XML file has a bad format. Please check the XML file.\n")
    
    def test_filter_by_rank(self):
        argsManager = argparse.Namespace(rank="Manager", gender=None, age_range=None, salary_range=None)
        argsDeveloper = argparse.Namespace(rank="Developer", gender=None, age_range=None, salary_range=None)

        # mocking console output 
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            filter_persons(self.root, argsManager)
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Wojciech\nSurname:  Kantor\nAge:  44\nGender:  Male\nRank:  Manager\nSalary:  44000\n\n",
                mocked_output.getvalue()
                )
            
            filter_persons(self.root, argsDeveloper)
            self.assertIn(
                "Name:  Jane\nSurname:  Smith\nAge:  25\nGender:  Female\nRank:  Developer\nSalary:  60000\n\n",
                mocked_output.getvalue()
                )

    def test_filter_by_gender(self):
        argsMale = argparse.Namespace(rank=None, gender="Male", age_range=None, salary_range=None)
        argsFemale = argparse.Namespace(rank=None, gender="Female", age_range=None, salary_range=None)

        with patch('sys.stdout', new=StringIO()) as mocked_output:

            filter_persons(self.root, argsMale)
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Wojciech\nSurname:  Kantor\nAge:  44\nGender:  Male\nRank:  Manager\nSalary:  44000\n\n",
                mocked_output.getvalue()
                )
            
            filter_persons(self.root, argsFemale)
            self.assertIn(
                "Name:  Jane\nSurname:  Smith\nAge:  25\nGender:  Female\nRank:  Developer\nSalary:  60000\n\n",
                mocked_output.getvalue()
                )

    def test_filter_by_age_range(self):
        argsLowerAge = argparse.Namespace(rank=None, gender=None, age_range=[20, 30], salary_range=None)
        argsHigherAge = argparse.Namespace(rank=None, gender=None, age_range=[30, 50], salary_range=None)

        with patch('sys.stdout', new=StringIO()) as mocked_output:

            filter_persons(self.root, argsLowerAge)
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Jane\nSurname:  Smith\nAge:  25\nGender:  Female\nRank:  Developer\nSalary:  60000\n\n",
                mocked_output.getvalue()
                )

            filter_persons(self.root, argsHigherAge)
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Jane\nSurname:  Smith\nAge:  25\nGender:  Female\nRank:  Developer\nSalary:  60000\n\nName:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Wojciech\nSurname:  Kantor\nAge:  44\nGender:  Male\nRank:  Manager\nSalary:  44000\n\n",
                mocked_output.getvalue()
                )
            
    def test_filter_by_salary_range(self):
        argsSalaryRange = argparse.Namespace(rank=None, gender=None, age_range=None, salary_range=[40000.0, 50000.0])
        argsToLowSalaryRange = argparse.Namespace(rank=None, gender=None, age_range=None, salary_range=[10000.0, 30000.0])

        with patch('sys.stdout', new=StringIO()) as mocked_output:

            filter_persons(self.root, argsSalaryRange)
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\nName:  Wojciech\nSurname:  Kantor\nAge:  44\nGender:  Male\nRank:  Manager\nSalary:  44000\n\n",
                mocked_output.getvalue()
                )

            filter_persons(self.root, argsToLowSalaryRange)
            self.assertIn(
                "",
                mocked_output.getvalue()
                )

    def test_print_person(self):
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            print_person(self.root[0])
            self.assertIn(
                "Name:  John\nSurname:  Doe\nAge:  30\nGender:  Male\nRank:  Manager\nSalary:  50000\n\n",
                mocked_output.getvalue()
                )

if __name__ == '__main__':
    unittest.main()
