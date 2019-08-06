"""
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
"""

from TFSConnect import TFS
from credentials import handleCredentials
from operations import manageTasks
from operations import manageOperations


def end_program():
    user_response = input("Enter any character and press enter to handle another PBI: ")
    if user_response != "":
        return True
    else:
        return False


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

    while retry:
        selected_operation_ordinal_number = input("Please select the required operation:")
        selected_operation = operations.get_operation_by_ordinal_number(selected_operation_ordinal_number)
        if selected_operation is None:
            print("Please try again...")
        else:
            return selected_operation


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

        operations = manageOperations.Operations()
        selected_operation = get_operation(operations)
        if selected_operation.name == "RegularTasks" \
                or selected_operation.name == "CleanupTasks"\
                or selected_operation.name == "GoingLiveTasks":
            manageTasks.add_tasks_to_pbi(tfs_instance, user_credentials, type=selected_operation.name)
        elif selected_operation.name == "CloneTasks":
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
