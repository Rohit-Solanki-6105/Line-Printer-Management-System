import customtkinter as ctk
import tkinter.messagebox as tkmsgbox
import json
from courses_and_subjects import CoursesAndSubjects
# from printers import get_all_printers
import tkinter
import win32print

def get_all_printers():
    printers_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
    printers = [printer_info[2] for printer_info in printers_info]
    return printers

def destroy_all_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Settings")

        self.minsize(600, 410)
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
                'kermit_path': kermit_path_entry.get(),
                'printer': self.printer_entry.get()
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

        self.printer_var = tkinter.StringVar(value=None)

        # def printer_window():
        self.printer_window = None
        def show_printer_display():
            self.printer_window = ctk.CTkToplevel(master=None)
            self.printer_window.title("Select Printer")
            self.printer_var = tkinter.StringVar(value=None)
            def display_printers():
                all_printers = get_all_printers()
                if all_printers:
                    destroy_all_widgets(self.scroll_frame)
                    # printer_list.delete(1.0, tk.END)  # Clear previous content
                    for printer in all_printers:
                        # printer_list = ctk.CTkLabel(self.scroll_frame, text=printer)
                        printer_list = ctk.CTkRadioButton(self.scroll_frame, text=printer, variable=self.printer_var, value=printer)
                        printer_list.pack()
                        # printer_list.insert(tk.END, printer + '\n')
                else:
                    destroy_all_widgets(self.scroll_frame)
                    # printer_list.delete(1.0, tk.END)  # Clear previous content
                    # printer_list.insert(tk.END, "No printers found.")
                    printer = ctk.CTkLabel(self.scroll_frame, text="No printers found")
                    printer.pack()

            self.refresh_btn = ctk.CTkButton(self.printer_window, text="↻", command=display_printers)
            self.refresh_btn.pack(padx=10, pady=10)

            self.scroll_frame = ctk.CTkScrollableFrame(self.printer_window, width=300)
            self.scroll_frame.pack(padx=10, pady=10)

            def test():
                print(self.printer_var.get())

            def return_printer():
                self.printer_entry.delete(0, ctk.END)
                self.printer_entry.insert(0, self.printer_var.get())
                # return self.printer_var.get()
                self.printer_window.destroy()

            self.show_btn = ctk.CTkButton(self.printer_window, text="ok", command=return_printer)
            self.show_btn.pack(padx=10, pady=10)

            display_printers()

        printer_label = ctk.CTkLabel(central_frame, text="Printer: ")
        self.printer_entry = ctk.CTkEntry(central_frame, width=entry_width)
        printer_selector = ctk.CTkButton(central_frame,text="🖶", font=('', 25), width=25, command=show_printer_display)
        printer_selector.grid(row=4, column=2, padx=10, pady = 5)
        printer_label.grid(row=4, column=0, padx = 10, pady = 5)
        self.printer_entry.grid(row=4, column=1, padx = 10, pady = 5)


        #courses and subjects
        course_sub_btn = ctk.CTkButton(central_frame, text="Courses and Subjects", command=CoursesAndSubjects)
        course_sub_btn.grid(row=5, column = 1, padx = 10, pady = 10)

        #save 
        save_btn = ctk.CTkButton(central_frame, text="Save", command=save_settings)
        save_btn.grid(row=6, column=1, padx = 10, pady = 10)

        # Load existing settings if available
        try:
            with open('settings.settings', 'r') as settings_file:
                settings_data = json.load(settings_file)
                # print(settings_data)
                default_ip_entry.insert(0, settings_data['default_ip'])
                default_data_folder_entry.insert(0, settings_data['default_data_folder'])
                backup_folder_entry.insert(0, settings_data['backup_folder'])
                kermit_path_entry.insert(0, settings_data['kermit_path'])
                self.printer_entry.insert(0, settings_data['printer'])

        except:
            # print("doesn't exist")
            pass
