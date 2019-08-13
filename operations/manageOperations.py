"""
Define the available operation types
"""


class OperationType:
    """
       this class represents an operation type.
    """

    def __init__(self, ordinal_number, name, description):
        self.ordinal_number = ordinal_number
        self.name = name
        self.description = description

    def __str__(self):
        return "(" + str(self.ordinal_number) + ")  --  " + str(self.description)


class Operations:
    """
        This class represents all of the available operations
    """
    def __init__(self):
        self.operations_list = initiate_operations()

    def get_operations_list_ordered(self):
        return sorted(self.operations_list, key=lambda operation: operation.ordinal_number)

    def get_operation_by_ordinal_number(self, ordinal_number):
        try:
            operation_number = int(ordinal_number)
        except ValueError:
            return None
        except:
            return None

        for operation in self.operations_list:
            if operation.ordinal_number == operation_number:
                return operation
        return None


def initiate_operations():
    operations_list = ([])
    operations_list.append(OperationType(1, "RegularTasks", "Add regular tasks to a PBI"))
    operations_list.append(OperationType(2, "CleanupTasks", "Add cleanup tasks to a PBI"))
    operations_list.append(OperationType(3, "GoingLiveTasks", "Add going live tasks to a PBI"))
    operations_list.append(OperationType(6, "CloneTasks", "Clone tasks between PBIs"))
    operations_list.append(OperationType(5, "E2ETasks", "Add E2E tasks to a PBI"))
    operations_list.append(OperationType(7, "CreateCleanup", "Create a cleanup PBI from an existing PBI"))
    operations_list.append(OperationType(4, "ExploratoryTasks", "Add exploratory tasks PBI"))

    return operations_list
