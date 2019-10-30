"""
The module implements the UI of the program
"""

import tkinter as tk
from functools import partial

# from operations import manageTasks
# import os
# import signal
# from time import sleep
# from tfs_connect import tfs
# from credentials import handle_credentials
# from operations import manageOperations
# from watchdog import watchdog


def button_click(event, action_type):
    if action_type == "RegularTasks" \
            or action_type == "CleanupTasks" \
            or action_type == "GoingLiveTasks" \
            or action_type == "E2ETasks" \
            or action_type == "ExploratoryTasks":
        print(action_type)
    elif action_type == "CloneTasks":
        print(action_type)
    elif action_type == "CreateCleanup":
        print(action_type)
    elif action_type == "RemovePBITasks":
        print(action_type)
    elif action_type == "RemoveTask":
        print(action_type)
    # if selected_operation.name == "RegularTasks" \
    #         or selected_operation.name == "CleanupTasks" \
    #         or selected_operation.name == "GoingLiveTasks" \
    #         or selected_operation.name == "E2ETasks" \
    #         or selected_operation.name == "ExploratoryTasks":
    #     manageTasks.add_tasks_to_pbi(tfs_instance, user_credentials,
    #                                  pbi_type=selected_operation.name)
    # elif selected_operation.name == "CloneTasks":
    #     manageTasks.clone_pbi_tasks(tfs_instance)
    # elif selected_operation.name == "CreateCleanup":
    #     manageTasks.copy_pbi_to_cleanup(tfs_instance, user_credentials)
    # elif selected_operation.name == "RemovePBITasks":
    #     manageTasks.remove_pbi_with_tasks(tfs_instance, user_credentials)
    # elif selected_operation.name == "RemoveTask":
    #     manageTasks.remove_task_from_pbi(tfs_instance, user_credentials)


# Create a new TK instance
win = tk.Tk()

# Window settings
win.title("TFS Automator")
win.minsize(850, 550)
win.resizable(False, False)

# Opening section
header = tk.Frame(win)
header.grid(sticky=tk.W)
title1_text = "Hello! And welcome to the..."
title1 = tk.Label(header, text=title1_text)
title1.grid(sticky=tk.W)

# Logo
logo_frame = tk.Frame(win)
logo_frame.grid()
logo = tk.Canvas(logo_frame, width=764, height=171)
logo.grid()
img = tk.PhotoImage(file="logo.gif")
logo.create_image(20, 20, image=img)

# Actions section
actions_dict = ({})
actions_dict["RegularTasks"] = {"name": "RegularTasks",
                                "description": "Add regular tasks"}
actions_dict["CleanupTasks"] = {"name": "CleanupTasks",
                                "description": "Add cleanup tasks"}
actions_dict["GoingLiveTasks"] = {"name": "GoingLiveTasks",
                                  "description": "Add going-live tasks"}
actions_dict["E2ETasks"] = {"name": "E2ETasks",
                            "description": "Add cleanup tasks"}
actions_dict["ExploratoryTasks"] = {"name": "ExploratoryTasks",
                                    "description": "Add exploratory tasks"}
actions_dict["CloneTasks"] = {"name": "CloneTasks",
                              "description": "Clonse tasks between PBIs"}
actions_dict["CreateCleanup"] = {"name": "CreateCleanup",
                                 "description": "Create cleanup PBI"}
actions_dict["RemovePBITasks"] = {"name": "RemovePBITasks",
                                  "description": "Remove PBI and tasks"}
actions_dict["RemoveTask"] = {"name": "RemoveTask",
                              "description": "Remove task"}

actions = tk.Frame(win)
actions.grid()

buttons_list = ([])
button_col = 0
button_row = 0

for action in actions_dict.values():
    buttons_list.append(
        tk.Button(actions, text=action["description"])
    )
    buttons_list[-1].grid(column=button_col, row=button_row)
    buttons_list[-1].bind('<Button-1>',
                          partial(button_click, action_type=action["name"]))
    button_col = (button_col + 1) % 2
    button_row = (button_row + 1) - button_col


# Start the GUI
win.mainloop()
