import customtkinter as ctk
import tkinter.messagebox as tkmsgbox
import json
from courses_and_subjects import CoursesAndSubjects

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Settings")

        self.minsize(300, 200)
        entry_width = 260 # setting entry width for every entrybox
        
        # functions

        # def open_courses_subjects():
        #     CoursesAndSubjects_window = CoursesAndSubjects(self)

        def save_settings():
        # Save configuration to config file
            settings_data = {
                'default_ip': default_ip_entry.get(),
                'default_data_folder': default_data_folder_entry.get(),
                'backup_folder': backup_folder_entry.get(),
                'kermit_path': kermit_path_entry.get() 
            }
            # print(settings_data)
            with open('settings.settings', 'w') as settings_file:
                json.dump(settings_data, settings_file)
                tkmsgbox.showinfo("save", "Settings saved")

        def path_finder(entry):
            folder_path = ctk.filedialog.askdirectory()
            if folder_path:
                entry.delete(0, ctk.END)  # Clear the entry
                entry.insert(0, folder_path)
            else:
                tkmsgbox.showwarning("Folder", "Please select a folder path")
        
        #main labels and entries
        central_frame = ctk.CTkFrame(self) # central frame to taplevel / self
        central_frame.pack(padx = 50, pady = 50)

        #setting default ip
        default_ip_label = ctk.CTkLabel(central_frame, text="Default IP:")
        default_ip_entry = ctk.CTkEntry(central_frame)
        default_ip_label.grid(row = 0, column = 0, padx = 10, pady = 5)
        default_ip_entry.grid(row = 0, column = 1, padx = 10, pady = 5)

        #setting default data folder
        def data_select():
            path_finder(default_data_folder_entry)

        default_data_folder_label = ctk.CTkLabel(central_frame, text="Default Data Folder:")
        default_data_folder_entry = ctk.CTkEntry(central_frame, width=entry_width)
        default_data_folder_selector = ctk.CTkButton(central_frame,text="📂", font=('', 25), width=25, command=data_select)
        default_data_folder_selector.grid(row=1, column=2, padx=10, pady = 5)
        default_data_folder_label.grid(row = 1, column = 0, padx = 10, pady = 5)
        default_data_folder_entry.grid(row = 1, column = 1, padx = 10, pady = 5)

        #setting back folder
        def backup_select():
            path_finder(backup_folder_entry)

        backup_folder_label = ctk.CTkLabel(central_frame, text="BackUp Folder: ")
        backup_folder_entry = ctk.CTkEntry(central_frame, width=entry_width)
        backup_folder_selector = ctk.CTkButton(central_frame,text="📂", font=('', 25), width=25, command=backup_select)
        backup_folder_selector.grid(row=2, column=2, padx=10, pady = 5)
        backup_folder_label.grid(row=2, column=0, padx = 10, pady = 5)
        backup_folder_entry.grid(row=2, column=1, padx = 10, pady = 5)

        # setting kermit path
        def kermit_select():
            path_finder(kermit_path_entry)

        kermit_path_label = ctk.CTkLabel(central_frame, text="Kermit Path: ")
        kermit_path_entry = ctk.CTkEntry(central_frame, width=entry_width)
        kermit_path_selector = ctk.CTkButton(central_frame,text="📂", font=('', 25), width=25, command=kermit_select)
        kermit_path_selector.grid(row=3, column=2, padx=10, pady = 5)
        kermit_path_label.grid(row=3, column=0, padx = 10, pady = 5)
        kermit_path_entry.grid(row=3, column=1, padx = 10, pady = 5)

        #courses and subjects
        course_sub_btn = ctk.CTkButton(central_frame, text="Courses and Subjects", command=CoursesAndSubjects)
        course_sub_btn.grid(row=4, column = 1, padx = 10, pady = 10)

        #save 
        save_btn = ctk.CTkButton(central_frame, text="Save", command=save_settings)
        save_btn.grid(row=5, column=1, padx = 10, pady = 10)

        # Load existing settings if available
        try:
            with open('settings.settings', 'r') as settings_file:
                settings_data = json.load(settings_file)
                # print(settings_data)
                default_ip_entry.insert(0, settings_data['default_ip'])
                default_data_folder_entry.insert(0, settings_data['default_data_folder'])
                backup_folder_entry.insert(0, settings_data['backup_folder'])
                kermit_path_entry.insert(0, settings_data['kermit_path'])

        except:
            # print("doesn't exist")
            pass
