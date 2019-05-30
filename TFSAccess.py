from TFSConnect import TFS

# https://devopshq.github.io/tfs/examples.html

# Initialize the connection parameters
URI = ""
PROJECT = ""
USER_NAME = ""
PASSWORD = ""

# Initialize a new TFS connection
TFS_INSTANCE = TFS.TFSConnection(URI, PROJECT, USER_NAME, PASSWORD)

# Test connection
# WorkItem = TFS_INSTANCE.connection.get_workitem(21573)
# print(WorkItem.field_names)

# query = """SELECT
#     [System.Id],
#     [System.WorkItemType],
#     [System.Title],
#     [System.ChangedDate]
# FROM workitems
# WHERE
#     [System.WorkItemType] = 'Bug'
# AND [System.WorkItemid] = '23234'
# ORDER BY [System.ChangedDate]"""
#
# wiql = TFS_INSTANCE.connection.run_wiql(query, params={'$top': 10, 'timePrecision': True, 'api-version': '1.0'})

# query = TFS_INSTANCE.connection.run_query('4fb0a26f-154c-41b9-beca-73abec43b3db')
# result = query.result
# print(query.columns)
# print(query.column_names)
# formatted_workitems_id = [workitem['ID'] for workitem in query.workitems]
# print(formatted_workitems_id)