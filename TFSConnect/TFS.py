from tfs import TFSAPI
from requests_ntlm import HttpNtlmAuth


class TFSConnection (TFSAPI):
    """
    this class represents a TFS connection.
    Once initialized and connected properly, it can be used to retrieve/update data from TFS
    """
    def __init__(self, tfs_uri, tfs_project, tfs_username, tfs_password):
        self.uri = tfs_uri
        self.username = tfs_username
        self.password = tfs_password
        self.project = tfs_project
        self.connection = None
        self.connection = TFSAPI(
            self.uri, project=self.project,
            user=self.username, password=self.password, auth_type=HttpNtlmAuth
        )


