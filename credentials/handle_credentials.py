"""
The module handles the user credentials managing
"""

from os import path
from os import remove
from os import environ
from os import mkdir
import getpass

CREDENTIALS_PATH = {'desktop': path.join(path.join(environ['USERPROFILE']), 'Desktop')}
CREDENTIALS_PATH['folder'] = CREDENTIALS_PATH['desktop'] + "\\TFS"
CREDENTIALS_PATH['file'] = CREDENTIALS_PATH['folder'] + "\\config.txt"


class CredentialsError(Exception):
    """
    An error indicating there was a problem with the user credentials
    """


def get_credentials():
    """
    The function checks if credentials exists in the config file.
    If not, it asks for the user to input his credentials.
    :return: A 'credentials' dictionary
    """

    # Check the connection credentials, if they do not exist get and save them
    credentials = {}

    if not path.isdir(CREDENTIALS_PATH['folder']):
        mkdir(CREDENTIALS_PATH['folder'])

    if path.exists(CREDENTIALS_PATH['file']):
        with open(CREDENTIALS_PATH['file'], "r") as file:
            try:
                credentials_input = file.readlines()
                credentials['userName'] = credentials_input[0].rstrip()
                credentials['password'] = credentials_input[1].rstrip()
                credentials['uri'] = credentials_input[2].rstrip()
                credentials['project'] = credentials_input[3].rstrip()
                credentials['name'] = credentials_input[4].\
                    rstrip().replace(r'\\', r'\'').replace(r"'", "")
            except IndexError:
                remove(CREDENTIALS_PATH['file'])
                print("There was a problem reading your credentials. Please try again...")
                raise CredentialsError
    else:
        print("It looks like this is your first time...")
        credentials = add_new_credentials()
    return credentials


def add_new_credentials():
    """
    The function prompts the user to enter new credentials.
    Once finished, it returns the new credentials.
    :return: credentials dictionary
    """
    credentials = {}

    # Get new credentials
    credentials['userName'] = input("What is your TFS username (email)? ")
    credentials['password'] = getpass.getpass(prompt="What is your TFS password? ")
    first_name = input("What is your first name? ")
    last_name = input("What is your last name? ")
    credentials['name'] = "{0} {1}<NET-BET\\{0}{2}>".format(first_name, last_name, last_name[0])
    credentials['uri'] = "https://tfs2018.net-bet.net/tfs/DefaultCollection/"
    credentials['project'] = "theLotter"

    # Save credentials in config file
    if not path.isdir(CREDENTIALS_PATH['folder']):
        mkdir(CREDENTIALS_PATH['folder'])
    with open(CREDENTIALS_PATH['file'], "w+") as file:
        file.write(credentials['userName'] + "\n")
        file.write(credentials['password'] + "\n")
        file.write(credentials['uri'] + "\n")
        file.write(credentials['project'] + "\n")
        file.write(credentials['name'] + "\n")
    return credentials
