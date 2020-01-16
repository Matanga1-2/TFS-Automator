"""
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
"""

import os
import signal
from time import sleep
from tfs_connect import tfs
from credentials import handle_credentials
from operations import manage_tasks
from operations import manage_operations
from watchdog import watchdog


def continue_program():
    """
    The function checks if the user wants to end the program
    :return: True/False
    """
    print("Choose another operation or exit the program")
    return True


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


def activate_operation(selected_operation, tfs_instance, user_credentials):
    """
    The function activated an operation based on "selected operation"
    :param selected_operation: an object of operation
    :param tfs_instance: the tfs instance
    :param user_credentials: the credentials
    :return:
    """
    if selected_operation.name == "RegularTasks" \
            or selected_operation.name == "CleanupTasks" \
            or selected_operation.name == "GoingLiveTasks" \
            or selected_operation.name == "E2ETasks" \
            or selected_operation.name == "ExploratoryTasks":
        manage_tasks.add_tasks_to_pbi(tfs_instance, user_credentials,
                                      pbi_type=selected_operation.name)
    elif selected_operation.name == "CloneTasks":
        manage_tasks.clone_pbi_tasks(tfs_instance)
    elif selected_operation.name == "CreateCleanupFromPBI" \
            or selected_operation.name == "CreateCleanupFromFeature":
        manage_tasks.copy_pbi_to_cleanup(tfs_instance, user_credentials,
                                         title_type=selected_operation.name)
    elif selected_operation.name == "RemovePBITasks":
        manage_tasks.remove_pbi_with_tasks(tfs_instance, user_credentials)
    elif selected_operation.name == "RemoveTask":
        manage_tasks.remove_task_from_pbi(tfs_instance, user_credentials)
    elif selected_operation.name == "UpdateCredentials":
        handle_credentials.add_new_credentials()
    elif selected_operation.name == "EndProgram":
        os.kill(os.getpid(), signal.SIGTERM)


def main():
    """
    The main program function
    """
    # Initialize variables
    retry = True
    user_credentials = ""
    operations = ""
    watch_dog = watchdog.Watchdog()
    watch_dog.start()

    print_welcome_message()

    while retry:
        sleep(1)
        print("What would you like to do?")
        print()

        # Get credentials for the connection
        try:
            user_credentials = handle_credentials.get_credentials()
            watch_dog.refresh()
        except handle_credentials.CredentialsError:
            continue

        # Get available operations
        if operations == "":
            operations = manage_operations.Operations()

        # Select the require operation
        selected_operation_id = get_operation(operations)
        watch_dog.refresh()

        with tfs.TFSConnection(user_credentials) as con:
            activate_operation(selected_operation_id, con, user_credentials)

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
