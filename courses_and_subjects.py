import customtkinter as ctk
import tkinter.messagebox as tkmsgbox
import json


class CoursesAndSubjects(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Courses and Subjects")
        self.minsize(400, 200)
        center_frame = ctk.CTkFrame(self)
        center_frame.pack(padx=50, pady=50)

        self.courses = []
        # courses = ["select course","mcs1", "mcs2", "mcs3", "mca"]
        # # sub
        self.subjects = {
            # "select course": ["select a course"],
            # "mcs1": ["fop", ""],
            # "mcs2": ["ap", "dbms"],
            # "mcs3": ["oocp", "dbms2"],
            # "mca": ["s1", "s2"]
        }
        
        def add_course(course_name, subjects):
            if course_name not in subjects:
                subjects[course_name] = []
                self.courses.append(course_name)
                # print(self.courses)
                tkmsgbox.showinfo("Add Course",f" {self.courses} Added")
            else:
                tkmsgbox.showinfo("Add Course", "Course already exist")
                # print("Course already exists!")

        def del_course(course_name, subjects):
            if course_name in subjects:
                del subjects[course_name]
                self.courses.remove(course_name)
                # print(self.courses)
                tkmsgbox.showinfo("Delete Course", f"{course_name} deleted")
            else:
                tkmsgbox.showinfo("Delete Course", "Course not fouond")
                # print("Course not found!")
            update()

        def add_sub(course_name, subject_name, subjects):
            if course_name in subjects:
                if subject_name != "" and subject_name not in subjects[course_name]:
                    subjects[course_name].append(subject_name)
                    tkmsgbox.showinfo("Add Subject", f"Subject '{subject_name}' added to '{course_name}'")
                    update()
                elif subject_name == "":
                    tkmsgbox.showinfo("Add Subject", "Subject name cannot be empty!")
                else:
                    tkmsgbox.showinfo("Add Subject", f"Subject '{subject_name}' already exists in the course '{course_name}'")
            else:
                tkmsgbox.showinfo("Add Subject", "Course not found")
            update()

        # Function to delete a subject from a course
        def del_sub(course_name, subject_name, subjects):
            if course_name in subjects:
                if subject_name in subjects[course_name]:
                    subjects[course_name].remove(subject_name)
                    tkmsgbox.showinfo("Delete Subject", f"{subject_name} deleted from {course_name}")
                else:
                    tkmsgbox.showinfo("Delete Subject", "Subject not found in the course!")
                    # print("Subject not found in the course!")
            else:
                tkmsgbox.showinfo("Delete Subject", "Course not found!")
                # print("Course not found!")
            update()

        # Function to save data to a JSON file
        def save_data_to_json(data, file_path):
            data = {
                "courses": self.courses,
                "subjects": self.subjects
            }
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            # print("Data saved to", file_path)
            tkmsgbox.showinfo("Data saved to", file_path)

            # Function to add a new course
        def add_course_func():
            in_course = ctk.CTkInputDialog(text="Enter Course:", title="Test")
            # selected_course = course_entry.get()
            selected_course = in_course.get_input()
            add_course(selected_course, self.subjects)
            update()

        # Function to delete a course
        def del_course_func():
            selected_course = course_entry.get()
            del_course(selected_course, self.subjects)
            update()

        # Function to add a subject to a course
        def add_subject_func():
            in_sub = ctk.CTkInputDialog(text="Entere Subject", title="Subject")
            selected_course = course_entry.get()
            # selected_subject = sub_entry.get()
            selected_subject = in_sub.get_input()
            add_sub(selected_course, selected_subject, self.subjects)
            update()

        # Function to delete a subject from a course
        def del_subject_func():
            selected_course = course_entry.get()
            selected_subject = sub_entry.get()
            del_sub(selected_course, selected_subject, self.subjects)
            print(self.subjects)
            update()

        # Function to save data to a JSON file
        def save_data():
            save_data_to_json(self.subjects, "courses.subjects")

        def update():
            course_entry = ctk.CTkComboBox(center_frame, values=self.courses, command=main_dropdown_selected)
            course_entry.grid(row = 1, column = 1, pady = 5, padx = 10)
            
            sub_entry = ctk.CTkComboBox(center_frame, values=[""])
            sub_entry.grid(row = 2, column = 1, pady = 5, padx = 10)
            print(self.courses, self.subjects)
            # main_dropdown_selected()
        
        def main_dropdown_selected(event):
            selected = course_entry.get()
            if selected in self.subjects:
                sub_entry.configure(values=self.subjects[selected])
            else:
                sub_entry.configure(values=[""])

        def load_data_from_json(file_path):
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    print("----data------")
                    print(data)
                    if 'courses' in data and 'subjects' in data:
                        self.courses = data['courses']
                        self.subjects = data['subjects']
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
            update()

        load_data_from_json("courses.subjects")
        update()

        # print(self.courses)
        # print(self.subjects)

        course_label = ctk.CTkLabel(center_frame, text="Course: ")
        # course_entry = ctk.CTkComboBox(center_frame, values=self.courses, command=main_dropdown_selected)
        course_entry = ctk.CTkComboBox(center_frame, values=self.courses, command=main_dropdown_selected)
        course_label.grid(row = 1, column = 0, pady = 5, padx = 10)
        course_entry.grid(row = 1, column = 1, pady = 5, padx = 10)

        add_course_btn = ctk.CTkButton(center_frame, text="+", width=30, height=30, font=('', 20), command=add_course_func)
        add_course_btn.grid(row = 1, column = 2, padx=3)
        del_course_btn = ctk.CTkButton(center_frame, text="-", width=30, height=30, font=('', 20), command=del_course_func)
        del_course_btn.grid(row = 1, column = 3, padx=3)

        
        sub_label = ctk.CTkLabel(center_frame, text="Subject: ")
        sub_label.grid(row = 2, column = 0, pady = 5, padx = 10)
        sub_entry = ctk.CTkComboBox(center_frame, values=[], state='readonly')
        # sub_entry = ctk.CTkComboBox(center_frame, values=[""])
        sub_entry.grid(row = 2, column = 1, pady = 5, padx = 10)

        add_subject_btn = ctk.CTkButton(center_frame, text="+", width=30, height=30, font=('', 20), command=add_subject_func)
        add_subject_btn.grid(row = 2, column = 2, padx=3)
        del_subject_btn = ctk.CTkButton(center_frame, text="-", width=30, height=30, font=('', 20), command=del_subject_func)
        del_subject_btn.grid(row = 2, column = 3, padx=3)

        
        #save 
        save_btn = ctk.CTkButton(center_frame, text="Save", command=save_data)
        save_btn.grid(row=3, column=1, padx = 10, pady = 10)

        

        
# test
# root = ctk.CTk()

# app = CoursesAndSubjects(root)

# root.mainloop()
