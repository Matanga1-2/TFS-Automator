"""
The module manages the connection to the TFS server
"""

from requests_ntlm import HttpNtlmAuth
from tfs import TFSAPI


class TFSConnection:
    """
    this class represents a TFS connection.
    Once initialized and connected properly, it can be used to retrieve/update data from TFS
    """
    def __init__(self, credentials):
        self.uri = credentials['uri']
        self.username = credentials['userName']
        self.password = credentials['password']
        self.project = credentials['project']
        self.connection = None

    def __enter__(self):
        self.connection = self.connect_to_tfs()
        return self.connection

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection = None

    def add_workitem(self, item_fields, parent_item_id=None, workitem_type="Task"):
        """
        The function adds a work item in the given TFS connection
        :param item_fields: the item fields, a dictionary
        :param parent_item_id: indicates if the item should be the child of a parent item
        :param workitem_type: Task or PBI
        :return:
        """

        if workitem_type == "PBI":
            workitem_type = "Product Backlog Item"

        if parent_item_id is not None:
            relation_url = """https://tfs2018.net-bet.net/tfs/DefaultCollection/
                154f45b9-7e72-44b9-bd28-225c488dfde2/_apis/wit/workItems/"""
            relations = [{'rel': 'System.LinkTypes.Hierarchy-Reverse',  # parent
                          'url': relation_url + str(parent_item_id)
                          }
                         ]
            new_workitem = self.connection.create_workitem(workitem_type,
                                                           fields=item_fields,
                                                           relations_raw=relations)
        else:
            new_workitem = self.connection.create_workitem(workitem_type, fields=item_fields)

        return new_workitem.id

    def connect_to_tfs(self):
        """
        Creates a TFS server connection and assign it to the object
        :return: None
        """
        return TFSAPI(
            self.uri, project=self.project,
            user=self.username, password=self.password, auth_type=HttpNtlmAuth, connect_timeout=10
        )
