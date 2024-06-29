import customtkinter as ctk
import tkinter.messagebox as tkmsgbox
import tkinter
import json
import os
import glob
import shutil
from datetime import date
from settings import *
from student_choose import *
# from student_choose import StudentsWindow
from process_all import process_all_files_user
from PIL import ImageTk
import win32print
from printer_manage import *
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from tktooltip import ToolTip
from CTkMenuBar import *
from courses_and_subjects import *


root = ctk.CTk() #set root window
ctk.set_appearance_mode("Light") #theme = light
# root.attributes("-alpha", 0.9) # transparency
root.minsize(570, 370) #set mninimum size of window
root.title("Line Printer Management System") # title of program
#logo icon
# root.wm_iconbitmap()
root.iconbitmap()
root.iconphoto(False, ImageTk.PhotoImage(file=("logo.ico")))
# functions

def open_settings():
    settings_window = SettingsWindow(root) #display settings window
    # settings_window.wm_attributes("-topmost", True) # always on top of all windows

#connect to server for z drive
def connect_server():
    try:
        os.system(f"net use Z: \\\\{ip_entry.get()}\data")
        print(f"net use Z: \\\\{ip_entry.get()}")
    except:
        tkmsgbox.showerror("Z error", "Z drive exists or can't be created")

# remover server , z drive
def disconnect_server():
    os.system("net use Z: /delete")

def ReCheck_printer():
    try:
        with open('settings.settings', 'r') as settings_file:
            settings_data = json.load(settings_file)
            printer_name.set(settings_data['printer'])
            printer_name_label.configure(text=f"{printer_name.get()}: ")

            if (printer_check(printer_name.get())):
                printer_on_off.configure(text="Online")
            else:
                printer_on_off.configure(text="Offline")
    except:
        pass

isStatusOpen = True
def display_status():
    global isStatusOpen
    if(isStatusOpen):
        isStatusOpen = False
        # status_frame.pack_forget()
        status_frame.grid_forget()
    else:
        isStatusOpen = True
        status_frame.grid(row = 0, column = 0)

isStatisticsOpen = True
def display_statistics():
    global isStatisticsOpen
    if(isStatisticsOpen):
        isStatisticsOpen = False
        statistics_frame.grid_forget()
    else:
        isStatisticsOpen = True
        statistics_frame.grid(row=0, column=2)

menubar = CTkMenuBar(master=root)
menubar.add_cascade("Printer ReCheck", command=ReCheck_printer)
menubar.add_cascade("Status", command=display_status)
menubar.add_cascade("Statistics", command=display_statistics)
menubar.add_cascade("Courses & Subjects", command=CoursesAndSubjects)
menubar.add_cascade("Settings", command=open_settings)
menubar.pack()

main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(expand=True, anchor=ctk.CENTER)

# central print and connection management frame
print_management = ctk.CTkFrame(main_frame, fg_color="transparent")
print_management.grid(row=0, column = 1)

printer_display_frame = ctk.CTkFrame(print_management, fg_color="transparent")
printer_display_frame.pack()
printer_name_label = ctk.CTkLabel(printer_display_frame, text="none")
printer_name_label.grid(row=0, column=0)
printer_on_off = ctk.CTkLabel(printer_display_frame, text="none")
printer_on_off.grid(row=0, column=1)

# top frame
top_frame = ctk.CTkFrame(print_management, fg_color="transparent") # color will transparent to merge with background
top_frame.pack(anchor=ctk.N, padx = 15, pady = 15, fill = ctk.X)

#settings button to open settings as inner seperate window
settings_btn = ctk.CTkButton(top_frame, text="⏣", font=('', 30), width = 30, command=open_settings)
settings_btn.pack(side = ctk.RIGHT)
# settings_btn.grid(row = 0, column = 2, padx=50, sticky=ctk.E)

# today's date
today = date.today().strftime("%d-%m-%Y") # formatting date
today_display = ctk.CTkLabel(top_frame, text = today)
today_display.pack(side = ctk.LEFT)
# today_display.grid(row = 0, column = 0,padx=50)

# all main inputs in central frame
central_frame = ctk.CTkFrame(print_management, fg_color="transparent") # central widget for every entries
central_frame.pack(padx=50, pady=50)

# ip
ip_label = ctk.CTkLabel(central_frame,text="IP: ") # declaring inside of central frame
ip_entry = ctk.CTkEntry(central_frame) # entry for ip address
ip_label.grid(row = 0, column = 0, pady = 5, padx = 10) #setting positions, margins
ip_entry.grid(row = 0, column = 1, pady = 5, padx = 10)

# user
# user_label = ctk.CTkLabel(central_frame,text="User: ")
# user_entry = ctk.CTkEntry(central_frame)
# user_label.grid(row = 1, column = 0, pady = 5, padx = 10)
# user_entry.grid(row = 1, column = 1, pady = 5, padx = 10)

# course
# courses = ["select course","mcs1", "mcs2", "mcs3", "mca"]
courses = []
# sub
subjects = {
    # "select course": ["select a course"],
    # "mcs1": ["fop", ""],
    # "mcs2": ["ap", "dbms"],
    # "mcs3": ["oocp", "dbms2"],
    # "mca": ["s1", "s2"]
}

def load_data_from_json(file_path):
            global courses, subjects
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    # print("----data------")
                    # print(data)
                    if 'courses' in data and 'subjects' in data:
                        courses = data['courses']
                        subjects = data['subjects']
                    else:
                        # print("Invalid JSON file format: Missing 'courses' or 'subjects' key.")
                        tkmsgbox.showerror("File: courses.subjects","Invalid JSON file format: Missing 'courses' or 'subjects' key.")
            except FileNotFoundError:
                # print("File not found:", file_path)
                tkmsgbox.showerror("File not found:","File not found: "+ file_path)
            except json.JSONDecodeError:
                # print("Invalid JSON file format.")
                tkmsgbox.showerror("JSON format","Invalid JSON file format.")
            except Exception as e:
                # print("Error loading data from JSON file:", str(e))
                tkmsgbox.showerror("Error loading data from JSON file:", str(e))

load_data_from_json('courses.subjects')

def main_dropdown_selected(event):
    selected = course_entry.get()
    sub_entry.configure(values = subjects[selected])
    # tkmsgbox.showinfo("hi", selected)

    # selected_main_option = course_entry.get()
    # if selected_main_option in subjects:
    #     subjects['values'] = subjects[selected_main_option]
    #     # subjects.current(0)

course_label = ctk.CTkLabel(central_frame, text="Course: ")
course_entry = ctk.CTkComboBox(central_frame, values=courses, command=main_dropdown_selected)
course_label.grid(row = 1, column = 0, pady = 5, padx = 10)
course_entry.grid(row = 1, column = 1, pady = 5, padx = 10)


sub_label = ctk.CTkLabel(central_frame, text="Subject: ")
sub_label.grid(row = 2, column = 0, pady = 5, padx = 10)

sub_entry = ctk.CTkComboBox(central_frame, values=[""])
sub_entry.grid(row = 2, column = 1, pady = 5, padx = 10)

# buttons
btn_frame = ctk.CTkFrame(print_management, fg_color="transparent")
btn_frame.pack(anchor=ctk.SE, padx = (200, 15), pady = 15)

connect_btn = ctk.CTkButton(btn_frame, text="Connect", command=connect_server, width=90)
connect_btn.grid(row=0, column=3, padx = 15, pady = 15)

disconnect_btn = ctk.CTkButton(btn_frame, text="Disconnect", command=disconnect_server, width=110)
disconnect_btn.grid(row=0, column=4, padx = 15, pady = 15)

#printers
# printer_frame = ctk.CTkFrame(print_management, fg_color="transparent")
# printer_frame.pack(anchor=ctk.SW, padx = 15, pady = 15)

# printer_btn = ctk.CTkButton(btn_frame, text="Printers", width=80)
# printer_btn.grid(row=0, column=1, padx = 15, pady = 15)

# printer_btn = ctk.CTkButton(btn_frame, text="Status", width=80)
# printer_btn.grid(row=0, column=2, padx = 15, pady = 15)

global data_path

def student_selection():
    # print(sub_entry.get(), course_entry.get())
    StudentsWindow(sub_entry.get(), course_entry.get(), data_path)

print_btn = ctk.CTkButton(btn_frame, text="Print", width=80, command=student_selection)
print_btn.grid(row=0, column=5, padx = 15, pady = 15)

printer_name = tkinter.StringVar(value=None)

# -----------------------------------------------

# status frame for pending and completed
status_frame = ctk.CTkFrame(main_frame)
status_frame.grid(row = 0, column = 0)

# pending in status
pending_frame = ctk.CTkFrame(status_frame)
pending_frame.grid(row=0, column=0)
pending_title_label = ctk.CTkLabel(pending_frame, text="Pending Jobs: ")
pending_title_label.pack()

pending_list_frame = ctk.CTkScrollableFrame(pending_frame)
pending_list_frame.pack()


#completed in status
completed_frame = ctk.CTkFrame(status_frame)
completed_frame.grid(row=1, column=0)
completed_title_label = ctk.CTkLabel(completed_frame, text="Completed Jobs: ")
completed_title_label.pack()


completed_list_frame = ctk.CTkScrollableFrame(completed_frame)
completed_list_frame.pack()

# ------------------------------------
statistics_frame = ctk.CTkFrame(main_frame)
statistics_frame.grid(row=0, column=2)
log_title = ctk.CTkLabel(statistics_frame, text="Searches:")
log_title.pack()
log_frame = ctk.CTkScrollableFrame(statistics_frame)
log_frame.pack()

# def trial():
    # print(return_selected_students())
# log_btn = ctk.CTkButton(log_frame, text="t", command=trial)
# log_btn.pack()


# ----- logs of students --------
# New data to be appended
# new_data = {
#     "default_data_folder": "C:/new/folder",
#     "backup_folder": "C:/new/backup",
#     "kermit_path": "C:/new/kermit",
#     "printer": "New Printer"
# }

# json_file_path = 'students.logs'

# try:
#     # Open the file in append mode
#     with open(json_file_path, 'a') as log_file:
#         # Move to the next line if the file is not empty
#         if log_file.tell() > 0:
#             log_file.write('\n')

#         # Dump the new data to the file
#         json.dump(new_data, log_file)
# except Exception as e:
#     print(f"An error occurred: {e}")


json_file_path = 'students.logs'

# # Initialize an empty list to store the parsed JSON objects
data_list = []

# try:
#     with open(json_file_path, 'r') as log_file:
#         # Iterate over each line in the file
#         for line in log_file:
#             try:
#                 # Load the JSON data from the current line
#                 data = json.loads(line)
                
#                 # Append the data to the list
#                 data_list.append(data)
#             except json.JSONDecodeError as e:
#                 print(f"Error decoding JSON: {e}")
#         for data in data_list:
#             print(data)
# except FileNotFoundError:
#     print(f"File not found: {json_file_path}")
# except Exception as e:
#     print(f"An error occurred: {e}")



# Now, 'data_list' contains a list of dictionaries, each representing a JSON object from the file
# print(data_list)
# ------ stats of all courses -----------------
stats_frame = ctk.CTkFrame(statistics_frame)
stats_frame.pack()
graph_frame = ctk.CTkFrame(stats_frame)
graph_frame.grid(row=1, column=1)
table_frame = ctk.CTkScrollableFrame(stats_frame)
table_frame.grid(row=1, column=0)

# -- graph visible or not
# isGraphVisible = True
# def display_graph():
#     global isGraphVisible
#     if(isGraphVisible):
#         isGraphVisible = False
#         graph_frame.grid_forget()
#     else:
#         isGraphVisible = True
#         graph_frame.grid(row=1, column=1)

# display_graph()

# graph_button = ctk.CTkButton(stats_frame, text="Graph", command=display_graph)
# graph_button.grid(row=0, column=0, padx=5, pady=5)

# # stats_frame.destroy()

# def create_histogram(courses_data):
#     # Check if there is any data to plot
#     if not courses_data:
#         print("No data to plot.")
#         return

#     # Extract course names and heights from the provided dictionary
#     courses = list(courses_data.keys())
#     heights = list(courses_data.values())

#      # Set the figure size to make the graph smaller
#     fig, ax = plt.subplots(figsize=(4, 4))  # Adjust the width and height as needed

#     # Plot the histogram
#     ax.bar(courses, heights, color='#3b8ed0')
#     ax.set_xlabel('Courses')
#     ax.set_ylabel('Submitted %')
#     ax.tick_params(axis='x', rotation=45, labelright=True)  # Rotate x-axis labels for better visibility
#     ax.set_ylim(0, 100)
#     plt.tight_layout()

#     canvas = FigureCanvasTkAgg(fig, master=graph_frame)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
    
#     # Add a toolbar (optional)
#     # toolbar = NavigationToolbar2Tk(canvas, statistics_frame)
#     # toolbar.update()
#     canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#     # plt.show()

#     for course, percentage in courses_data.items():
#         per_label = ctk.CTkLabel(table_frame, text=f"{course}: {percentage}")
#         per_label.pack(padx=5, pady=5)


# # Example usage:
# course_heights = {
#     'MCA1': 70,
#     'MCS1': 84,
#     'MCS3': 67,
#     'MTech': 100,
# }
#  # Create a canvas to embed the Matplotlib figure
# create_histogram(course_heights)


# inserting ip
try:
    with open('settings.settings', 'r') as settings_file:
        settings_data = json.load(settings_file)
        # print(settings_data)
        ip_entry.insert(0, settings_data['default_ip'])
        data_path = settings_data['default_data_folder']
        kermit_path = settings_data['kermit_path']
        printer_name.set(settings_data['printer'])
        printer_name_label.configure(text=f"{printer_name.get()}: ")

        if (printer_check()):
            printer_on_off.configure(text="Online")
        else:
            printer_on_off.configure(text="Offline")

        # print(printer_name.get())

        # print(data_path, kermit_path)

except:
    # print("doesn't exist")
    pass

#-----------tool tips -------------------
# ToolTip(settings_btn, msg="Settings")

root.mainloop() # run window
