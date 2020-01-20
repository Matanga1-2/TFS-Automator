import unittest
from credentials import handle_credentials


class TestCredentials(unittest.TestCase):
    def test_getting_the_credentials_from_file(self):
        """
        Tests the credentials are gotten from the file
        :return:
        """

        # setup

        # action
        credentials = handle_credentials.get_credentials_from_file()

        # assertion
        self.assertIsNotNone(credentials)


if __name__ == '__main__':
    unittest.main()
