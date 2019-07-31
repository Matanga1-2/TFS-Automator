from operations import getObjects
import requests.exceptions


def add_task(tfs_instance, task_fields, pbi_id):
    """
    Function to add a TFS task linked as child to a given PBI
    :param tfs_instance: the TFS connection
    :param task_fields: dictionary with the task fields
    :param pbi_id: the linked PBI ID
    :return: the new task ID
    """
    relation_url = """https://tfs2018.net-bet.net/tfs/DefaultCollection/154f45b9-7e72-44b9-bd28-225c488dfde2/
        _apis/wit/workItems/"""
    relations = [{'rel': 'System.LinkTypes.Hierarchy-Reverse',  # parent
                  'url': relation_url + str(pbi_id)
                  }
                 ]

    task = tfs_instance.connection.create_workitem('Task', fields=task_fields, relations_raw=relations)
    return task.id


def add_task_to_pbi(tfs_instance, task, pbi_data):
    """
    Add a new task to a specific PBI (with correct area and iteration)
    :param tfs_instance: the TFS connection
    :param task: a task fields dictionary
    :param pbi_data: a PBI object
    :return: nothing
    """
    task['System.AreaId'] = pbi_data['System.AreaId']  # Area Path
    task['System.IterationId'] = pbi_data['System.IterationId']  # Iteration Path
    try:
        new_task = add_task(tfs_instance, task, pbi_data.id)  # Add a new task
    except requests.exceptions.HTTPError as error:
        print("Oops.. there was an HTTP error: {0}".format(error))
        return
    print("Task " + str(new_task) + " was added successfully")


def add_regular_tasks_to_pbi(tfs_instance, user_credentials):
    """
    Add all of the required regular tasks to a PBI
    :param tfs_instance: the TFS connection
    :param user_credentials: the user credentials dictionary
    :return: nothing
    """
    # Ask for PBI Get the PBI information
    pbi_id = getObjects.get_pbi_id()

    # Get the PBI data
    try:
        pbi_data = tfs_instance.connection.get_workitem(pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Get tasks to add
    tasks = getObjects.get_tasks(user_credentials, type="Regular")

    # Add tasks
    for task in tasks:
        add_task_to_pbi(tfs_instance, task, pbi_data)


def add_cleanup_tasks_to_pbi(tfs_instance, user_credentials):
    """
    Add all of the required cleanup tasks to a PBI
    :param tfs_instance: the TFS connection
    :param user_credentials: the user credentials dictionary
    :return: nothing
    """
    # Ask for PBI Get the PBI information
    pbi_id = getObjects.get_pbi_id()

    # Get the PBI data
    try:
        pbi_data = tfs_instance.connection.get_workitem(pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Get tasks to add
    tasks = getObjects.get_tasks(user_credentials, type="cleanup")

    # Add tasks
    for task in tasks:
        add_task_to_pbi(tfs_instance, task, pbi_data)
