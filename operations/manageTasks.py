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


def copy_task(tfs_instance, original_task_data, target_pbi_data):
    """
    Function to copy a TFS task from one PBI to another PBI as a child
    :param tfs_instance: the TFS connection
    :param original_task_data: a TFS work item object of the task to copy
    :param target_pbi_data: the target PBI data
    :return: the new task ID
    """

    # Build the task fields
    original_task = original_task_data.fields

    # Only if type is "Task"
    if original_task["System.WorkItemType"] == "Task":
        target_task = ({})
        try:
            target_task["System.State"] = "To Do"
            target_task["System.AreaId"] = target_pbi_data['System.AreaId']
            target_task["System.IterationId"] = target_pbi_data["System.IterationId"]
            target_task["System.Title"] = original_task["System.Title"]
            target_task["Microsoft.VSTS.Common.BacklogPriority"] = original_task["Microsoft.VSTS.Common.BacklogPriority"]
            target_task["Microsoft.VSTS.Common.Activity"] = original_task["Microsoft.VSTS.Common.Activity"]
            target_task["System.Description"] = original_task["System.Description"]
        except:
            pass

        # Add a new task to the target PBI with the source task fields
        try:
            new_task = add_task(tfs_instance, target_task, target_pbi_data.id)
        except requests.exceptions.HTTPError as error:
            print("Oops.. there was an HTTP error: {0}".format(error))
            return

        print("Task " + str(new_task) + " was copied to PBI " + str(target_pbi_data.id) + " successfully")


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


def add_tasks_to_pbi(tfs_instance, user_credentials, type="regular"):
    """
    Add all of the required tasks to a PBI, based on a given type
    :param tfs_instance: the TFS connection
    :param user_credentials: the user credentials dictionary
    :param type: the type of tasks to add
    :return: nothing
    """
    # Ask for PBI ID
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
    tasks = getObjects.get_tasks(user_credentials, type=type)

    # Add tasks
    for task in tasks:
        add_task_to_pbi(tfs_instance, task, pbi_data)


def clone_pbi_tasks(tfs_instance, user_credentials):
    """
    Copies a specific PBI tasks to another PBI
    :param tfs_instance: the TFS connection
    :param user_credentials: the user credentials dictionary
    :return: nothing
    """

    # Ask for the first PBI ID
    print("You need to specify the source PBI ID")
    source_pbi_id = getObjects.get_pbi_id()

    # Get the first PBI data
    try:
        source_pbi_data = tfs_instance.connection.get_workitem(source_pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Ask for the second PBI ID
    print("You need to specify the target PBI ID")
    target_pbi_id = getObjects.get_pbi_id()

    # Get the second PBI data
    try:
        target_pbi_data = tfs_instance.connection.get_workitem(target_pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Copy tasks
    for task_id in source_pbi_data.child_ids:
        task = tfs_instance.connection.get_workitem(task_id)
        copy_task(tfs_instance, task, target_pbi_data)
