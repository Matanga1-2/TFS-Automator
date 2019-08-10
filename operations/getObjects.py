"""
The module is responsible for giving PBI and tasks information
"""
import requests

class WorkitemDoesntMatchIDError:
    pass


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


def __get_available_tasks(user_credentials):
    """
    The function is responsible of creating the template for each type of task
    :param user_credentials: The user credentials object
    :return: a dictionary of all tasks
    """
    tasks_dict = ({})

    # Write tests
    tasks_dict["WriteTests"] = {
        'System.Title': 'Write Tests',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '160',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }
    # Run Tests
    tasks_dict["RunTests"] = {
        'System.Title': 'Run Tests',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '180',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }
    # Review tests
    tasks_dict["ReviewTests"] = {
        'System.Title': 'Review Tests',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '170',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Requirements',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '0.5',  # Remaining Work
        'System.AssignedTo': user_credentials['name'],  # Assigned to the System Analyst
    }
    # HLD
    tasks_dict["HighLevelDesign"] = {
        'System.Title': 'High Level Design',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '10',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '0',  # Remaining Work
    }
    # Release plan
    tasks_dict["ReleasePlan"] = {
        'System.Title': 'Release Plan',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '150',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '0.5',  # Remaining Work
        'System.Description': "1) What needs to be released? including work order</br></br>2) Dependencies (other " +
                              "PBIs, other teams)</br></br>3) PM Work (demo, content, security…)</br></br>4)" +
                              "Release to all environments</br>* QA2 (full QA)</br>* Staging2</br>* Production " +
                              "(feature sanity if possible)</br>* PerfCD</br>* ProdLikeCD"
    }
    # Remove toggle from code
    tasks_dict["RemoveToggleCode"] = {
        'System.Title': 'Remove toggle from code',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '50',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }
    # Remove toggle from consul
    tasks_dict["RemoveToggleConsul"] = {
        'System.Title': 'Remove toggle from consul',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '60',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }
    # Activate toggle
    tasks_dict["ActivateToggle"] = {
        'System.Title': 'Activate feature toggle',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '50',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }
    # Rollback plan
    tasks_dict["Rollback"] = {
        'System.Title': 'Rollback Plan',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '20',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '0',  # Remaining Work
    }
    # Notify
    tasks_dict["Notify"] = {
        'System.Title': 'Notify ...',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '50',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Requirements',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '0',  # Remaining Work
    }
    # Exploratory Tests
    tasks_dict["ExploratoryTests"] = {
        'System.Title': 'Exploratory Tests',  # Title
        'Microsoft.VSTS.Common.BacklogPriority': '180',  # Backlog Priority
        'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
        'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
    }

    return tasks_dict


def get_tasks(user_credentials, type):
    """
    Function to get the tasks we want to add to the PBI
    :param user_credentials: a TFS credentials object
    :param type: a string representing the type of tasks required, default is "regular"
    :return: a list of dictionaries with the tasks fields
    """

    available_tasks = __get_available_tasks(user_credentials)
    tasks = list([])

    if type == "RegularTasks":
        tasks.append(available_tasks["WriteTests"])
        tasks.append(available_tasks["RunTests"])
        tasks.append(available_tasks["ReviewTests"])
        tasks.append(available_tasks["HighLevelDesign"])
        tasks.append(available_tasks["ReleasePlan"])

    if type == "CleanupTasks":
        tasks.append(available_tasks["RemoveToggleCode"])
        tasks.append(available_tasks["RemoveToggleConsul"])
        tasks.append(available_tasks["HighLevelDesign"])
        tasks.append(available_tasks["ReleasePlan"])

    if type == "GoingLiveTasks":
        tasks.append(available_tasks["ActivateToggle"])
        tasks.append(available_tasks["Rollback"])
        tasks.append(available_tasks["Notify"])
        tasks.append(available_tasks["ExploratoryTests"])

    if type == "E2ETasks":
        tasks.append(available_tasks["WriteTests"])
        tasks.append(available_tasks["RunTests"])
        tasks.append(available_tasks["ReviewTests"])

    return tasks


def get_cleanup_pbi(tfs_instance, original_pbi_id):
    """
    The function returns
    :param tfs_instance:
    :param original_pbi_id:
    :return: A dictionary with the cleanup fields ("data") and its parent_id ("parent_id") if exists
    """

    cleanup_pbi = ({})
    cleanup_pbi["data"] = ({})
    cleanup_pbi["parent_id"] = None

    # Get PBI data
    try:
        original_pbi_data = tfs_instance.connection.get_workitem(original_pbi_id)
    except requests.exceptions.HTTPError as error:
        print('An HTTP error: {0}'.format(error))
        return
    except:
        return

    # Build the PBI fields
    original_pbi_fields = original_pbi_data.fields

    # Check if the PBI has a feature
    try:
        feature_id = original_pbi_data.parent_id
    except:
        feature_id = None
    finally:
        cleanup_pbi["parent_id"] = feature_id

    # Only if type is "Product Backglog Item"
    if original_pbi_fields["System.WorkItemType"] == "Product Backlog Item":

        # Determine the cleanup item title
        # has feature: {Feature name} + ': Cleanup'
        # No feature: {PBI name} + ' - Cleanup'
        if cleanup_pbi["parent_id"] is not None:
            try:
                feature_data = tfs_instance.connection.get_workitem(cleanup_pbi["parent_id"])
                cleanup_pbi_title = feature_data["System.Title"] + ": Cleanup"
            except:
                cleanup_pbi_title = original_pbi_fields["System.Title"] + " - Cleanup"
                pass
        else:
            cleanup_pbi_title = original_pbi_fields["System.Title"] + " - Cleanup"
        cleanup_pbi["data"]["System.Title"] = cleanup_pbi_title

        # Static fields
        cleanup_pbi["data"]["System.State"] = "Approved"
        cleanup_pbi["data"]["Microsoft.VSTS.Common.BusinessValue"] = "3001"
        cleanup_pbi["data"]["Microsoft.VSTS.Scheduling.Effort"] = "0"
        cleanup_pbi["data"]["System.Description"] = "Cleanup PBI"
        cleanup_pbi["data"]["NetBet.ProductPreparationState"] = "Not Started"
        cleanup_pbi["data"]["NetBet.TechnicalPreparationState"] = "Not Started"

        # Fields that should be as the original PBI (if they have any value)
        fields_to_copy = ["NetBet.FinancialEntity2", "System.AreaId", "System.IterationId",
                          "NetBet.ProductPreparationAssignedTo", "NetBet.TechnicalPreparationAssignedTo"]
        for field in fields_to_copy:
            try:
                cleanup_pbi["data"][field] = original_pbi_fields[field]
            except:
                pass
    else:
        raise WorkitemDoesntMatchIDError

    return cleanup_pbi
