"""
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
"""

from TFSConnect import TFS
from credentials import handleCredentials
from operations import manageTasks


def end_program():
    user_response = input("Enter any character and press enter to handle another PBI: ")
    if user_response != "":
        return True
    else:
        return False


def get_operation():
    """
    The function will get the required operation from the user.
    :return: A string representing the operation
    """

    retry = True
    print("Available operations:")
    print("(1) Add regular tasks to a PBI")
    print("(2) Add cleanup tasks to a PBI")
    print("(3) Clone tasks between PBIs")


    while retry:
        operation = input("Please select the required operation:")
        if operation == "1":
            return "add_regular"
        elif operation == "2":
            return "add_cleanup"
        elif operation == "3":
            return "clone_tasks"
        else:
            print("Please try again...")


def main():
    """
    The main program function
    """
    # Initialize variables
    retry = True
    user_credentials = ""
    tfs_instance = ""

    while retry:

        print()
        print("Hello! Welcome the the TFS Assistant...")
        print()
        if user_credentials == "":
            # Get credentials for the connection
            try:
                user_credentials = handleCredentials.get_credentials()
            except handleCredentials.CredentialsError:
                continue

        if tfs_instance == "":
            # Initialize a new TFS connection
            tfs_instance = TFS.TFSConnection(user_credentials['uri'], user_credentials['project'],
                                             user_credentials['userName'], user_credentials['password'])

        operation = get_operation()
        if operation == "add_regular":
            manageTasks.add_regular_tasks_to_pbi(tfs_instance, user_credentials)
        elif operation == "add_cleanup":
            manageTasks.add_cleanup_tasks_to_pbi(tfs_instance, user_credentials)
        elif operation == "clone_tasks":
            manageTasks.clone_pbi_tasks(tfs_instance, user_credentials)

        # check if need to continue
        if end_program():
            continue
        else:
            retry = False
            continue
    exit()


if __name__ == "__main__":
    main()
