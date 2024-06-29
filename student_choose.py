import tkinter.messagebox as tkmsgbox
import shutil
import tkinter as tk
import customtkinter as ctk
import os
import glob
import json
from process_all import *
from PIL import ImageTk
from printer_manage import *

selected_students = []

class StudentsWindow(ctk.CTkToplevel):
    def __init__(self, subject, course, data_path, master=None):
        super().__init__(master)
        self.title("Select Students")
        
        self.iconbitmap()
        self.iconphoto(False, ImageTk.PhotoImage(file=("logo.ico")))
        self.minsize(400, 300)
        self.subject = subject
        self.course = course
        self.data_path = data_path
        # self.printer_status = False

        with open('settings.settings', 'r') as settings_file:
            settings_data = json.load(settings_file)
            # self.printer_status = is_printer_online(settings_data['printer'])

        students = glob.glob(os.path.join(data_path, f"{self.course}*", "print", self.subject))
        usernames = []
        students_paths = []
        for student_path in students:
            username = student_path.lstrip(f"{data_path}\\")
            username = username.rstrip(f"\print\{self.subject}")
            students_paths.append(student_path)
            usernames.append(username)

        self.selected_users = []  # List to store selected users with their paths
        self.checkbox_vars = []  # List to store IntVar objects for checkboxes

        # Set the maximum width for the frame
        max_width = 200  # Adjust this value according to your needs

        top_frame = ctk.CTkFrame(self,fg_color="transparent")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create a checkbox to select/deselect all users
        select_all_var = ctk.IntVar()
        select_all_checkbox = ctk.CTkCheckBox(top_frame, text="Select All", variable=select_all_var)
        select_all_checkbox.pack(side=tk.LEFT, padx=5)
        select_all_checkbox.bind("<Button-1>", lambda event: on_select_all_click(select_all_var))
        
        def print_selected():
            if(printer_check()):
                get_selected_users()
                with open('settings.settings', 'r') as settings_file:
                    settings_data = json.load(settings_file)
                    process_all_files_user(settings_data['kermit_path'])
            else:
                tkmsgbox.showinfo("Error","Printer not found! Please check your printer connection.")
            self.quit()
        # Add a button to get selected users when clicked
        print_selected_button = ctk.CTkButton(top_frame, text="Print Selected", command=print_selected)
        print_selected_button.pack(side=tk.RIGHT, padx=5)

        # Create a frame to hold the checkboxes with a maximum width
        frame = ctk.CTkScrollableFrame(self)
        # frame = ctk.CTkFrame(self)
        frame.pack(fill=ctk.BOTH, padx=10, pady=10)

        # l1 = ctk.CTkLabel(frame, text="under test")
        # l1.grid(row=0, column=0)
        # l2 = ctk.CTkLabel(frame, text="under test")
        # l2.grid(row=1, column=1)
        def show_users():
            current_width = 0
            row_count = 0
            column_count = 0
            for i, user in enumerate(usernames):
                var = ctk.IntVar()
                self.checkbox_vars.append(var)
                checkbox = ctk.CTkCheckBox(frame, text=user, variable=var)
                # checkbox.pack(side=tk.LEFT)
                checkbox.grid(row=row_count, column = column_count, padx=3, pady = 3)
                column_count = column_count+1
                checkbox.bind("<Button-1>", lambda event, index=i: on_checkbox_click(index))  # Bind checkbox click event
                if column_count > 2:
                    column_count = 0
                    row_count = row_count+1
                # Update current width based on the width of the checkbox
                # current_width += checkbox.winfo_reqwidth() + 5  # 5 pixels padding
                # If the current width exceeds the maximum width, start a new line
                # if current_width > max_width:
                #     current_width = 0
                #     checkbox.pack(side=tk.TOP, padx=5)  # Start a new line

        def on_checkbox_click(index):
            if self.checkbox_vars[index].get() == 1:
                self.selected_users.append([usernames[index], students_paths[index]])
            elif [usernames[index], students_paths[index]] in self.selected_users:
                self.selected_users.remove([usernames[index], students_paths[index]])

        def on_select_all_click(select_all_var):
            # Update the selected_users list based on the state of the "Select All" checkbox
            self.selected_users = []
            if select_all_var.get() == 1:
                self.selected_users = [[username, path] for username, path in zip(usernames, students_paths)]

            # Update individual checkboxes based on the state of the "Select All" checkbox
            for var in self.checkbox_vars:
                var.set(select_all_var.get())

        show_users()

        def get_selected_users():
            global selected_students
            # Function to retrieve selected users with their paths
            for user_data in self.selected_users:
                username, student_path = user_data
                # selected_students.append(user_data)
                print(f"Copying files for user: {username}: {student_path}")
                copy_to(username, student_path)
            print("All selected users processed.")
            selected_students = self.selected_users

        # copy specific files from user print folder
        def copy_specific_files(source_folder, destination_folder, extensions, username):
            # Ensure the source folder exists
            if not os.path.exists(source_folder):
                print(f"Source folder '{source_folder}' does not exist.")
                return

            # Create the destination folder if it doesn't exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Loop through all files in the source folder
            for filename in os.listdir(source_folder):
                source_path = os.path.join(source_folder, filename)

                # Check if it's a file (not a subfolder) and copy it if its extension is in the list of extensions
                if os.path.isfile(source_path):
                    file_extension = os.path.splitext(filename)[1].lower()
                    if file_extension in extensions:
                        # Rename the file with user_filename.extension format
                        new_filename = f"{username}_{filename}"
                        destination_path = os.path.join(destination_folder, new_filename)
                        shutil.copy2(source_path, destination_path)
                        # print(f"Copied '{source_path}' to '{destination_path}'")

        def copy_to(user, student_path):
            try:
                with open('settings.settings', 'r') as settings_file:
                    settings_data = json.load(settings_file)
                    # print(settings_data)
                    data_path = settings_data['default_data_folder']
                    kermit_path = settings_data['kermit_path']
                    source_directory = student_path
                    destination_directory = kermit_path

                    if not os.path.exists(source_directory):
                        tkmsgbox.showwarning("Source Directory Error", f"Source directory '{source_directory}' does not exist.")
                        return

                    if not os.path.exists(destination_directory):
                        tkmsgbox.showwarning("Destination Directory Error", f"Destination directory '{destination_directory}' does not exist.")
                        return
                    
                    # source_folder = "C:/Users/Rohit/Desktop/test_Print/data/mcs2106/print/dbms"
                    # destination_folder = "C:/Users/Rohit/Desktop/test_Print/kermit"
                    source_folder = source_directory
                    destination_folder = destination_directory
                    allowed_extensions = {'.txt', '.c', '.cpp'}
                    # print(source_folder, destination_folder, allowed_extensions)
                    
                    copy_specific_files(source_folder, destination_folder, allowed_extensions, user)
                    # tkmsgbox.showinfo("Copied", "Copied to kermit and print started")

            except Exception as e:
                tkmsgbox.showerror("Error", f"An error occurred while copying files: {str(e)}")

def return_selected_students():
    return selected_students
