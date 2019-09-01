"""
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
"""

import os
import signal
from time import sleep
from tfs_connect import tfs
from credentials import handle_credentials
from operations import manageTasks
from operations import manageOperations
from watchdog import watchdog


def continue_program():
    """
    The function checks if the user wants to end the program
    :return: True/False
    """
    print()
    user_response = input("Enter any character and press enter to handle another PBI: ")
    return bool(user_response != "")


def get_operation(operations):
    """
    The function will get the required operation from the user.
    :return: A string representing the operation
    """

    retry = True
    # operations_list = operations.get_available_operations_ordered()
    # print("Available operations:")
    for operation in operations.get_operations_list_ordered():
        print(operation)

    print()
    while retry:
        selected_operation_ordinal_number = input("Please select the required operation:")
        selected_operation = \
            operations.get_operation_by_ordinal_number(selected_operation_ordinal_number)
        if selected_operation is None:
            print("Please try again...")
        else:
            return selected_operation


def print_welcome_message():
    """
    The function prints the welcome message
    :return: None
    """
    print()
    print("Hello! And welcome to the...")
    sleep(0.5)
    print()
    print(r" _____ ______  _____    ___          _                             _                ")
    print(r"|_   _||  ___|/  ___|  / _ \        | |                           | |               ")
    print(r"  | |  | |_   \ `--.  / /_\ \ _   _ | |_   ___   _ __ ___    __ _ | |_   ___   _ __ ")
    print(r"  | |  |  _|   `--. \ |  _  || | | || __| / _ \ | '_ ` _ \  / _` || __| / _ \ | '__|")
    print(r"  | |  | |    /\__/ / | | | || |_| || |_ | (_) || | | | | || (_| || |_ | (_) || |   ")
    print(r"  \_/  \_|    \____/  \_| |_/ \__,_| \__| \___/ |_| |_| |_| \__,_| \__| \___/ |_|   ")
    print(r"                                                                                    ")


def main():
    """
    The main program function
    """
    # Initialize variables
    retry = True
    user_credentials = ""
    tfs_instance = ""
    watch_dog = watchdog.Watchdog()
    watch_dog.start()

    print_welcome_message()

    while retry:
        sleep(1)
        print("What would you like to do?")
        print()

        if user_credentials == "":
            # Get credentials for the connection
            try:
                user_credentials = handle_credentials.get_credentials()
                watch_dog.refresh()
            except handle_credentials.CredentialsError:
                continue

        if tfs_instance == "":
            # Initialize a new TFS connection
            tfs_instance = tfs.TFSConnection(user_credentials['uri'],
                                             user_credentials['project'],
                                             user_credentials['userName'],
                                             user_credentials['password'])

        operations = manageOperations.Operations()
        selected_operation = get_operation(operations)
        watch_dog.refresh()
        if selected_operation.name == "RegularTasks" \
                or selected_operation.name == "CleanupTasks"\
                or selected_operation.name == "GoingLiveTasks"\
                or selected_operation.name == "E2ETasks"\
                or selected_operation.name == "ExploratoryTasks":
            manageTasks.add_tasks_to_pbi(tfs_instance, user_credentials,
                                         pbi_type=selected_operation.name)
        elif selected_operation.name == "CloneTasks":
            manageTasks.clone_pbi_tasks(tfs_instance)
        elif selected_operation.name == "CreateCleanup":
            manageTasks.copy_pbi_to_cleanup(tfs_instance, user_credentials)

        # check if need to continue
        if continue_program():
            print()
            continue
        else:
            retry = False
            watch_dog.refresh()
            continue
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    main()
