import customtkinter as ctk
import tkinter.messagebox as tkmsgbox
import tkinter
import json
import os
import glob
import shutil
from datetime import date
from settings import SettingsWindow
from student_choose import StudentsWindow
from process_all import process_all_files_user
from PIL import ImageTk
# from printers import *

root = ctk.CTk() #set root window
ctk.set_appearance_mode("Light") #theme = light
# root.attributes("-alpha", 0.9) # transparency
root.minsize(650, 370) #set mninimum size of window
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
        os.system("net use Z: \\\\" + ip_entry.get())
    except:
        tkmsgbox.showerror("Z error", "Z drive exists or can't be created")

# remover server , z drive
def disconnect_server():
    os.system("net use Z: /delete")

printer_display_frame = ctk.CTkFrame(root, fg_color="transparent")
printer_display_frame.pack()
printer_name_label = ctk.CTkLabel(printer_display_frame, text="none")
printer_name_label.grid(row=0, column=0)
printer_on_off = ctk.CTkLabel(printer_display_frame, text="offline")
printer_on_off.grid(row=0, column=1)

# top frame
top_frame = ctk.CTkFrame(root, fg_color="transparent") # color will transparent to merge with background
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
central_frame = ctk.CTkFrame(root, fg_color="transparent") # central widget for every entries
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
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(anchor=ctk.SE, padx = 15, pady = 15)

connect_btn = ctk.CTkButton(btn_frame, text="Connect", command=connect_server, width=90)
connect_btn.grid(row=0, column=3, padx = 15, pady = 15)

disconnect_btn = ctk.CTkButton(btn_frame, text="Disconnect", command=disconnect_server, width=110)
disconnect_btn.grid(row=0, column=4, padx = 15, pady = 15)

#printers
# printer_frame = ctk.CTkFrame(root, fg_color="transparent")
# printer_frame.pack(anchor=ctk.SW, padx = 15, pady = 15)

printer_btn = ctk.CTkButton(btn_frame, text="Printers", width=80)
printer_btn.grid(row=0, column=1, padx = 15, pady = 15)

printer_btn = ctk.CTkButton(btn_frame, text="Status", width=80)
printer_btn.grid(row=0, column=2, padx = 15, pady = 15)

global data_path

def student_selection():
    # print(sub_entry.get(), course_entry.get())
    StudentsWindow(sub_entry.get(), course_entry.get(), data_path)

print_btn = ctk.CTkButton(btn_frame, text="Print", width=80, command=student_selection)
print_btn.grid(row=0, column=5, padx = 15, pady = 15)

printer_name = tkinter.StringVar(value=None)

def printer_status():
    pending_frame = ctk.CTkFrame(root)
    pending_frame.pack()

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
        # print(printer_name.get())

        # print(data_path, kermit_path)

except:
    # print("doesn't exist")
    pass

root.mainloop() # run window
