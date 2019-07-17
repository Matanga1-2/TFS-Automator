'''
The program handles managing work items in TFS.
It uses Dohq package(https://devopshq.github.io/tfs/examples.html)
'''

from TFSConnect import TFS
from os import path
import sys


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
            sys.exit()
    else:
        f = open("config.txt", "w+")
        print("It looks like this is your first time...")
        credentials['userName'] = input("What is your TFS username? ")
        credentials['password'] = input("What is your TFS password? ")
        first_name = input("What is your first name? ")
        last_name = input("What is your last name? ")
        credentials['name'] = first_name + " " + last_name + r"<NET-BET\\" + first_name + last_name[0] + ">"
        credentials['uri'] = "https://tfs2018.net-bet.net/tfs/DefaultCollection/"
        credentials['project'] = "theLotter"

        # Save credentials in config file
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
            PBIId = int(input("Enter PBI ID:"))
        except:
            print("Invalid ID. Try again")
        else:
            return PBIId


def get_tasks(credentials):
    tasks = []
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
    relation_url = 'https://tfs2018.net-bet.net/tfs/DefaultCollection/154f45b9-7e72-44b9-bd28-225c488dfde2/_apis/wit/workItems/'
    relations = [{'rel': 'System.LinkTypes.Hierarchy-Reverse',  # parent
                  'url': relation_url + str(pbi_id)
                  }
                 ]

    task = TFS_INSTANCE.connection.create_workitem('Task', fields=task_fields, relations_raw=relations)
    print("Task " + task.id + " Added successfully")


def end_program():
    input("Press any key to continue...")


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
        task['System.AreaId'] = pbi_data['System.AreaId']           # Area Path
        task['System.IterationId'] = pbi_data['System.IterationId']  # Iteration Path
        try:
            add_task(TFS_INSTANCE, task, pbi_id)
        except requests.exceptions.HTTPERror as error:
            print('An HTTP error: {0}'.format(error))
            end_program()


if __name__== "__main__":
    main()
