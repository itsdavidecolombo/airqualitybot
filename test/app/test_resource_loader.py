#################################################
#
# @Author: davidecolombo
# @Date: lun, 18-10-2021, 19:29
# @Description: a script for testing the resource_loader.py module
#
#################################################

import unittest
from airquality.app.resource_loader import ResourceLoader
from airquality.app.session import Session


class TestResourceLoader(unittest.TestCase):


    def setUp(self) -> None:
        self.path = "properties/resources.json"
        self.session = Session(settings = {})
        self.loader = ResourceLoader(
                path = self.path,
                session = self.session
        )

    def test_new_resource_loader(self):
        """Test create resource loader"""

        self.assertIsNotNone(self.loader)
        self.assertIsInstance(self.loader, ResourceLoader)

    def test_load_resources(self):
        """Test loading the resource file locally."""

        response = self.loader.load_resources()
        self.assertTrue(response)

    def test_system_exit_load_resources(self):
        """Test SystemExit when try to load more than once the resources."""
        self.loader.load_resources()
        with self.assertRaises(SystemExit):
            self.loader.load_resources()

    def test_file_not_found(self):
        """Test FileNotFoundError when file does not exist."""

        path = "properties/bad_file.json"
        loader = ResourceLoader(path, session = self.session)
        with self.assertRaises(SystemExit):
            loader.load_resources()

    def test_parse_resources(self):
        """Test parse resources correct behaviour."""
        response = self.loader.load_resources()
        self.assertTrue(response)
        response = self.loader.parse_resources()
        self.assertTrue(response)

    def test_system_exit_parse_resources(self):
        """
        Test SystemExit when user attemp to parse resources more than once.
        """
        self.loader.load_resources()
        self.loader.parse_resources()
        with self.assertRaises(SystemExit):
            self.loader.parse_resources()

    def test_system_exit_when_raw_content_is_empty(self):
        """
        Test SystemExit when try to parse resources but raw content is empty.
        """
        with self.assertRaises(SystemExit):
            self.loader.parse_resources()

    def test_system_exit_while_parsing_resources(self):
        """Test SystemExit when parsing unsupported file extension.

        ParserFactory raises a TypeError that ResourceLoader catches and
        so SystemExit is raised.

        ATTENTION: THIS TEST WILL FAIL IF THE FILE
        'properties/text.txt' DOES NOT EXIST
        """

        path = "properties/test.txt"
        loader = ResourceLoader(path = path, session = self.session)
        try:
            response = loader.load_resources()
            self.assertTrue(response)
            with self.assertRaises(SystemExit):
                loader.parse_resources()
        except SystemExit:
            print("YOU MUST CREATE 'test.txt' file in 'properties' directory.")
            self.assertTrue(False)

    def test_empty_resources_database_connection(self):
        """Test SystemExit if try to get database connection without having
        parsed the resources."""

        with self.assertRaises(SystemExit):
            self.loader.database_connection("correct_username")

    def test_system_exit_database_connection(self):
        """Test SystemExit when try to open more than once connection to
        the database."""

        self.loader.load_resources()
        self.loader.parse_resources()
        self.loader.database_connection("bot_mobile_user")
        with self.assertRaises(SystemExit):
            self.loader.database_connection("bot_mobile_user")


if __name__ == '__main__':
    unittest.main()