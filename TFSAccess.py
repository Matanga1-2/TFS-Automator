"""
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
"""

from TFSConnect import TFS
import requests.exceptions
from os import path
from os import remove


def end_program():
    input("Press any key to continue...")


def get_credentials():
    """
    The function checks if credentials exists in the config file.
    If not, it asks for the user to input his credentials.
    :return: A 'credentials' dictionary
    """

    # Check the connection credentials, if they do not exist get and save them
    credentials = {}
    if path.isfile('./config.txt'):
        f = open("config.txt", "r")
        try:
            if f.mode == 'r':
                credentials_input = f.readlines()
                credentials['userName'] = credentials_input[0].rstrip()
                credentials['password'] = credentials_input[1].rstrip()
                credentials['uri'] = credentials_input[2].rstrip()
                credentials['project'] = credentials_input[3].rstrip()
                credentials['name'] = credentials_input[4].rstrip().replace(r'\\',r'\'').replace(r"'","")
                f.close()
            else:
                print("There was an error getting the credentials. Please try again")
                end_program()
        except IndexError:
            f.close()
            remove("config.txt")
            print("There was a problem reading your credentials. Please try again...")
            end_program()
    else:
        print("It looks like this is your first time...")
        credentials['userName'] = input("What is your TFS username? ")
        credentials['password'] = input("What is your TFS password: ")
        first_name = input("What is your first name? ")
        last_name = input("What is your last name? ")
        credentials['name'] = first_name + " " + last_name + "<NET-BET\\" + first_name + last_name[0] + ">"
        credentials['uri'] = "https://tfs2018.net-bet.net/tfs/DefaultCollection/"
        credentials['project'] = "theLotter"

        # Save credentials in config file
        f = open("config.txt", "w+")
        f.write(credentials['userName'] + "\n")
        f.write(credentials['password'] + "\n")
        f.write(credentials['uri'] + "\n")
        f.write(credentials['project'] + "\n")
        f.write(credentials['name'] + "\n")
    return credentials


def get_pbi_id():
    """
    The function gets a PBI number from the user.
    :return: An integer representing the PBI ID
    """

    while True:
        try:
            pbi_id = int(input("Enter PBI ID:"))
        except:
            print("Invalid ID. Try again")
        else:
            return pbi_id


def get_tasks(credentials):
    """
    Function to get the tasks we want to add to the PBI
    :param credentials: a TFS credentials object
    :return: a list of dictionaries with the tasks fields
    """
    tasks = list([])
    # HLD
    tasks.append({
         'System.Title': 'High Level Design',               # Title
         'Microsoft.VSTS.Common.BacklogPriority': '10',     # Backlog Priority
         'Microsoft.VSTS.Common.Activity': 'Development',   # Activity
         'Microsoft.VSTS.Scheduling.RemainingWork': '0',    # Remaining Work
        })
    # Release plan
    tasks.append({
         'System.Title': 'Release Plan',                    # Title
         'Microsoft.VSTS.Common.BacklogPriority': '150',    # Backlog Priority
         'Microsoft.VSTS.Common.Activity': 'Development',   # Activity
         'Microsoft.VSTS.Scheduling.RemainingWork': '0.5',  # Remaining Work
         'System.Description': "1) What needs to be released? including work order</br></br>2) Dependencies (other " +
                               "PBIs, other teams)</br></br>3) PM Work (demo, content, security…)</br></br>4)" +
                               "Release to all environments</br>* QA2 (full QA)</br>* Staging2</br>* Production " +
                               "(feature sanity if possible)</br>* PerfCD</br>* ProdLikeCD"
        })
    # Write tests
    tasks.append({
        'System.Title': 'Write Tests',                      # Title
        'Microsoft.VSTS.Common.BacklogPriority': '160',     # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',    # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',      # Remaining Work
    })
    # Run Tests
    tasks.append({
        'System.Title': 'Run Tests',                        # Title
        'Microsoft.VSTS.Common.BacklogPriority': '180',     # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',    # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',      # Remaining Work
    })
    # Review tests
    tasks.append({
        'System.Title': 'Review Tests',                    # Title
        'Microsoft.VSTS.Common.BacklogPriority': '170',     # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Requirements',    # Activity
        'System.AssignedTo': credentials['name'],      # Remaining Work
    })
    return tasks


def add_task(TFS_INSTANCE ,task_fields, pbi_id):
    """
    Function to add a TFS task linked as child to a given PBI
    :param TFS_INSTANCE: the TFS connection
    :param task_fields: dictionary with the task fields
    :param pbi_id: the linked PBI ID
    :return: the new task ID
    """
    relation_url = 'https://tfs2018.net-bet.net/tfs/DefaultCollection/154f45b9-7e72-44b9-bd28-225c488dfde2/_apis/wit/workItems/'
    relations = [{'rel': 'System.LinkTypes.Hierarchy-Reverse',  # parent
                  'url': relation_url + str(pbi_id)
                  }
                 ]

    task = TFS_INSTANCE.connection.create_workitem('Task', fields=task_fields, relations_raw=relations)
    return task.id


def main():
    """
    The main program function
    """

    # Get credentials for the connection
    credentials = get_credentials()

    # Initialize a new TFS connection
    TFS_INSTANCE = TFS.TFSConnection(credentials['uri'], credentials['project'],
                                     credentials['userName'], credentials['password'])

    # Ask for PBI Get the PBI information
    pbi_id = get_pbi_id()

    # Get the PBI data
    while True:
        try:
            pbi_data = TFS_INSTANCE.connection.get_workitem(pbi_id)
        except requests.exceptions.HTTPError as error:
            print('An HTTP error: {0}'.format(error))
            end_program()
        else:
            break

    # Get tasks to add
    tasks = get_tasks(credentials)

    # Add tasks
    for task in tasks:
        task['System.AreaId'] = pbi_data['System.AreaId']            # Area Path
        task['System.IterationId'] = pbi_data['System.IterationId']  # Iteration Path
        try:
            new_task = add_task(TFS_INSTANCE, task, pbi_id)              # Add a new task
        except requests.exceptions.HTTPError as error:
            print("Oops.. there was an HTTP error: {0}".format(error))
            end_program()
        print("Task " + str(new_task) + " was added successfully")
    end_program()


if __name__ == "__main__":
    main()
