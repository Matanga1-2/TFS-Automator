from operations import getObjects
import requests.exceptions


def add_workitem(tfs_instance, item_fields, parent_item_id, workitem_type):
    """
    Function to add a TFS task linked as child to a given PBI
    :param tfs_instance: the TFS connection
    :param item_fields: dictionary with the task fields
    :param parent_item_id: the linked PBI ID
    :param workitem_type: the type of workitem to add
    :return: the new task ID
    """

    if parent_item_id is not None:
        relation_url = """https://tfs2018.net-bet.net/tfs/DefaultCollection/154f45b9-7e72-44b9-bd28-225c488dfde2/
            _apis/wit/workItems/"""
        relations = [{'rel': 'System.LinkTypes.Hierarchy-Reverse',  # parent
                      'url': relation_url + str(parent_item_id)
                      }
                     ]
        if workitem_type == "Task":
            new_workitem = tfs_instance.connection.create_workitem('Task', fields=item_fields, relations_raw=relations)
        elif workitem_type == "PBI":
            new_workitem = tfs_instance.connection.create_workitem('Product Backlog Item',
                                                                   fields=item_fields, relations_raw=relations)
    else:
        if workitem_type == "Task":
            new_workitem = tfs_instance.connection.create_workitem('Task', fields=item_fields)
        elif workitem_type == "PBI":
            new_workitem = tfs_instance.connection.create_workitem('Product Backlog Item', fields=item_fields)

    return new_workitem.id


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
            new_task = add_workitem(tfs_instance, target_task, target_pbi_data.id, workitem_type="Task")
            print("Task " + str(new_task) + " was copied to PBI " + str(target_pbi_data.id) + " successfully")
        except requests.exceptions.HTTPError as error:
            print("Oops.. there was an HTTP error: {0}".format(error))
            return


def copy_pbi_to_cleanup(tfs_instance, user_credentials):
    """
    Function to duplicate a PBI in the same feature if available
    :param tfs_instance: the TFS connection
    :param original_pbi_data: a TFS work item object of the PBI to copy
    :param target_feature_data: the target feature data (None if there is none)
    :return: the new PBI ID
    """

    # Get the original PBI ID
    print("Please enter the original PBI ID")
    pbi_id = getObjects.get_pbi_id()

    # Get PBI data
    try:
        original_pbi_data = tfs_instance.connection.get_workitem(pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Build the PBI fields
    original_pbi = original_pbi_data.fields

    try:
        feature_id = original_pbi_data.parent_id
    except:
        feature_id = None

    # Only if type is "Product Backglog Item"
    if original_pbi["System.WorkItemType"] == "Product Backlog Item":
        target_pbi = ({})
        try:
            target_pbi["System.Title"] = original_pbi["System.Title"] + " - Cleanup"
            if feature_id is not None:
                try:
                    feature_data = tfs_instance.connection.get_workitem(feature_id)
                    target_pbi["System.Title"] = feature_data["System.Title"] + ": Cleanup"
                except:
                    pass
            target_pbi["System.State"] = "Approved"
            target_pbi["Microsoft.VSTS.Common.BusinessValue"] = "3001"
            target_pbi["Microsoft.VSTS.Scheduling.Effort"] = "0"
            target_pbi["System.Description"] = "Cleanup PBI"
            target_pbi["NetBet.ProductPreparationState"] = "Not Started"
            target_pbi["NetBet.TechnicalPreparationState"] = "Not Started"
            fields_to_copy = ["NetBet.FinancialEntity2", "System.AreaId", "System.IterationId",
                              "NetBet.ProductPreparationAssignedTo", "NetBet.TechnicalPreparationAssignedTo"]
            for field in fields_to_copy:
                try:
                    target_pbi[field] = original_pbi[field]
                except:
                    pass
        except:
            print("There was an error.. please try again")
            return

        # Add the cleanup PBI
        try:
            new_pbi = add_workitem(tfs_instance, target_pbi, feature_id, workitem_type="PBI")
            print("PBI " + str(new_pbi) + " was created successfully")
            new_pbi_data = tfs_instance.connection.get_workitem(new_pbi)
        except requests.exceptions.HTTPError as error:
            print("Oops.. there was an HTTP error: {0}".format(error))
            return

        # Add the related relation
        try:
            relation_url = """https://tfs2018.net-bet.net/tfs/DefaultCollection/154f45b9-7e72-44b9-bd28-225c488dfde2/
                _apis/wit/workItems/"""
            relations = [{'rel': 'System.LinkTypes.Related',  # related
                          'url': relation_url + str(original_pbi_data.id)
                          }]
            new_pbi_data.add_relations_raw(relations)
        except:
            pass

        # Add cleanup tasks to the new PBI
        try:
            add_tasks_to_pbi(tfs_instance, user_credentials, tasks_type="CleanupTasks", pbi_id=new_pbi)
        except requests.exceptions.HTTPError as error:
            print("Oops.. there was an HTTP error: {0}".format(error))
            return
    else:
        print("ID doesn't match a PBI item")
        return


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
        new_task = add_workitem(tfs_instance, task, pbi_data.id, workitem_type="Task")  # Add a new task
    except requests.exceptions.HTTPError as error:
        print("Oops.. there was an HTTP error: {0}".format(error))
        return
    print("Task " + str(new_task) + " was added successfully")


def add_tasks_to_pbi(tfs_instance, user_credentials, pbi_id=None, tasks_type="regular"):
    """
    Add all of the required tasks to a PBI, based on a given type
    :param tfs_instance: the TFS connection
    :param user_credentials: the user credentials dictionary
    :param pbi_id: a given PBI to add the tasks to
    :param type: the type of tasks to add
    :return: nothing
    """

    if pbi_id is None:
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
    tasks = getObjects.get_tasks(user_credentials, type=tasks_type)

    # Add tasks
    for task in tasks:
        add_task_to_pbi(tfs_instance, task, pbi_data)


def clone_pbi_tasks(tfs_instance):
    """
    Copies a specific PBI tasks to another PBI
    :param tfs_instance: the TFS connection
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
