"""
The module handles the user credentials managing
"""

from os import path
from os import remove
from os import environ
from os import mkdir


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

    desktop = path.join(path.join(environ['USERPROFILE']), 'Desktop')
    credentials_folder = desktop + "\\TFS"
    credentials_file = credentials_folder + "\\config.txt"

    if not path.isdir(credentials_folder):
        mkdir(credentials_folder)

    if path.exists(credentials_file):
        cred_file = open(credentials_file, "r")
        try:
            if cred_file.mode == 'r':
                credentials_input = cred_file.readlines()
                credentials['userName'] = credentials_input[0].rstrip()
                credentials['password'] = credentials_input[1].rstrip()
                credentials['uri'] = credentials_input[2].rstrip()
                credentials['project'] = credentials_input[3].rstrip()
                credentials['name'] = credentials_input[4].\
                    rstrip().replace(r'\\', r'\'').replace(r"'", "")
                cred_file.close()
            else:
                print("There was an error getting the credentials. Please try again")
                raise CredentialsError
        except IndexError:
            cred_file.close()
            remove(credentials_file)
            print("There was a problem reading your credentials. Please try again...")
            raise CredentialsError
    else:
        print("It looks like this is your first time...")
        credentials['userName'] = input("What is your TFS username? ")
        credentials['password'] = input("What is your TFS password? ")
        first_name = input("What is your first name? ")
        last_name = input("What is your last name? ")
        credentials['name'] = "{0} {1}<NET-BET\\{0}{2}>".format(first_name, last_name,
                                                                last_name[0])
        credentials['uri'] = "https://tfs2018.net-bet.net/tfs/DefaultCollection/"
        credentials['project'] = "theLotter"

        # Save credentials in config file
        cred_file = open(credentials_file, "w+")
        cred_file.write(credentials['userName'] + "\n")
        cred_file.write(credentials['password'] + "\n")
        cred_file.write(credentials['uri'] + "\n")
        cred_file.write(credentials['project'] + "\n")
        cred_file.write(credentials['name'] + "\n")
        cred_file.close()
    return credentials
