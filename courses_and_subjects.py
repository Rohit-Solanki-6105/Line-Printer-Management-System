import customtkinter as ctk
import tkinter.messagebox as tkmsgbox

class CoursesAndSubjects(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Courses and Subjects")
        self.minsize(400, 200)
        center_frame = ctk.CTkFrame(self)
        center_frame.pack(padx=50, pady=50)

        # course
        courses = ["select course","mcs1", "mcs2", "mcs3", "mca"]

        def main_dropdown_selected(event):
            selected = course_entry.get()
            sub_entry = ctk.CTkComboBox(center_frame, values=subjects[selected])
            sub_entry.grid(row = 2, column = 1, pady = 5, padx = 10)
            # tkmsgbox.showinfo("hi", selected)

            # selected_main_option = course_entry.get()
            # if selected_main_option in subjects:
            #     subjects['values'] = subjects[selected_main_option]
            #     # subjects.current(0)

        course_label = ctk.CTkLabel(center_frame, text="Course: ")
        course_entry = ctk.CTkComboBox(center_frame, values=courses, command=main_dropdown_selected)
        course_label.grid(row = 1, column = 0, pady = 5, padx = 10)
        course_entry.grid(row = 1, column = 1, pady = 5, padx = 10)

        add_course_btn = ctk.CTkButton(center_frame, text="+", width=30, height=30, font=('', 20))
        add_course_btn.grid(row = 1, column = 2, padx=3)
        del_course_btn = ctk.CTkButton(center_frame, text="-", width=30, height=30, font=('', 20))
        del_course_btn.grid(row = 1, column = 3, padx=3)

        # # sub
        subjects = {
            "select course": ["select a course"],
            "mcs1": ["fop", ""],
            "mcs2": ["ap", "dbms"],
            "mcs3": ["oocp", "dbms2"],
            "mca": ["s1", "s2"]
        }
        sub_label = ctk.CTkLabel(center_frame, text="Subject: ")
        sub_label.grid(row = 2, column = 0, pady = 5, padx = 10)

        add_subject_btn = ctk.CTkButton(center_frame, text="+", width=30, height=30, font=('', 20))
        add_subject_btn.grid(row = 2, column = 2, padx=3)
        del_subject_btn = ctk.CTkButton(center_frame, text="-", width=30, height=30, font=('', 20))
        del_subject_btn.grid(row = 2, column = 3, padx=3)

        
        #save 
        save_btn = ctk.CTkButton(center_frame, text="Save")
        save_btn.grid(row=3, column=1, padx = 10, pady = 10)

# test
root = ctk.CTk()

app = CoursesAndSubjects(root)

root.mainloop()
