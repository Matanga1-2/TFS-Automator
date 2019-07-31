"""
The module is responsible for giving PBI and tasks information
"""


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


def get_tasks(user_credentials, type="regular"):
    """
    Function to get the tasks we want to add to the PBI
    :param user_credentials: a TFS credentials object
    :param type: a string representing the type of tasks required, default is "regular"
    :return: a list of dictionaries with the tasks fields
    """
    tasks = list([])

    if type == "regular":
        # Write tests
        tasks.append({
            'System.Title': 'Write Tests',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '160',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
        })
        # Run Tests
        tasks.append({
            'System.Title': 'Run Tests',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '180',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
        })
        # Review tests
        tasks.append({
            'System.Title': 'Review Tests',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '170',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Requirements',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '0.5',  # Remaining Work
            'System.AssignedTo': user_credentials['name'],  # Assigned to the System Analyst
        })

    if type == "cleanup":
        # Remove toggle from code
        tasks.append({
            'System.Title': 'Remove toggle from code',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '50',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
        })
        # Remove toggle from consul
        tasks.append({
            'System.Title': 'Remove toggle from consul',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '60',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
        })

    if type == "regular" or type == "cleanup":
        # HLD
        tasks.append({
            'System.Title': 'High Level Design',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '10',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '0',  # Remaining Work
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
        # Exploratory Tests
        tasks.append({
            'System.Title': 'Exploratory Tests',  # Title
            'Microsoft.VSTS.Common.BacklogPriority': '180',  # Backlog Priority
            'Microsoft.VSTS.Common.Activity': 'Development',  # Activity
            'Microsoft.VSTS.Scheduling.RemainingWork': '',  # Remaining Work
        })
    return tasks
