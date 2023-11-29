import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from CTkTable import *
from datetime import date
from tkinter import messagebox


class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Color Theme 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        #configure columns
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        #title and size of window
        self.title('RecogNice Dashboard')
        self.geometry('900x600')
        
        #sidebar
        self.sidebar = sidebar(master=self, fg_color="black")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        #home
        self.home = home(master=self)
        self.home.grid(row=0, column=1, sticky="nsew")
        
class sidebar(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.current_frame = "home"

        font = ("Roboto",20)
        user_image = ctk.CTkImage(dark_image= Image.open("student_images\errol liscano.jpg"), size=(100,100))
        
        self.user_image_label = ctk.CTkLabel(master=self, image=user_image, text="")
        self.user_image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        #Name Display
        self.user_name = ctk.CTkLabel(master=self, text="Errol Liscano", anchor='center', font=font)
        self.user_name.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        
        #buttons
        self.home_button = ctk.CTkButton(master=self, text="HOME", command=self.home)
        self.home_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.students_button = ctk.CTkButton(master=self, text="STUDENTS", command=self.students)
        self.students_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.reports_button = ctk.CTkButton(master=self, text="REPORTS", command=self.reports)
        self.reports_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
       
    def home(self):
        print("Logged In")
    
    def students(self):
        master = self.master
        old_frame = None
        if self.current_frame == "home":
            old_frame = home(master=master)
            for child in master.winfo_children():

                if isinstance(child, ctk.CTkFrame) and child == old_frame:
                    child.grid_forget()
                    child.grid(in_=master, row=0, column=1)
    
    def reports(self):
        print("Logged In")
        
class home(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        font = ("Roboto",36)
        
        #Main Label
        self.main_label = ctk.CTkLabel(master=self, text="RecogNice Attendance Checker", font=font)
        self.main_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        
        #Section Frame
        self.section_frame = ctk.CTkFrame(master=self)
        self.section_label = ctk.CTkLabel(master=self.section_frame, text="Sections", font=("Roboto", 24))
        self.section_label.grid(row=0, column=0, padx=20, pady=(20,5), sticky='w')

        today = date.today()
        date_today = today.strftime("%B %d, %Y")
        self.date_label = ctk.CTkLabel(master=self.section_frame, text="Date: " + date_today, font=("Roboto", 24))
        self.date_label.grid(row=0, column=1, padx=20, pady=(20,5), sticky='e')
        
        #Section Table
        self.section_table = CTkTable(master=self.section_frame, row=4, column=4, values=self.get_section_table_values())
        self.section_table.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky='ew')
        
        self.check_attendance_button = ctk.CTkButton(master=self, text="CHECK ATTENDANCE", command=self.check_attendance)
        self.check_attendance_button.grid(row=3, column=0, padx=20, pady=10, sticky='ew')
        
        self.section_frame.grid(row=1, column=0, padx=20, pady=20, sticky='ew')
        
    def check_attendance(self):
        confirm = messagebox.askyesno("Check Attendance?", "Do you wish to start checking?")
        if confirm:
            # for task_id in self.after_ids:
            #     self.after_cancel(task_id)
            # self.destroy()
            from face_window import face_panel
            next_window = face_panel()
            next_window.mainloop()
            in_main = False
        else:
            print("exit operation canceled")
        
        
    def get_section_table_values(self):
        value = [["Section","Students","Present","Absent"],
        ["BSCS-3A", 35, 35, 0],
        ["BSCS-3B", 30, 25, 5],
        ["BSCS-3C", 30, "Not Checked", "Not Checked"]]
            
        return value

class students(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        #Student Label
        self.student_label = ctk.CTkLabel(master=self, text = "Students", font= ("Roboto", 20))
        self.student_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        #section dropdown
        self.section_selection = ctk.CTkComboBox(master=self, values=["BSCS-3A", "BSCS-3B", "BSCS-3C"])
        self.section_selection.grid(row=0, column=1, padx=20, pady=20, sticky='ew')
        #Table
        self.student_table = CTkTable(master=self, row=5, column=4, values=self.get_student_table_values)
        self.student_table.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky='ew')

    def get_student_table_values(self):
        value = [["Student Number","Name", "Present","Absent"],
        [2021300193, "Errol Liscano", 15, 0],
        [2021300123, "Melvin Ramoran", 10, 5],
        [2021300321, "Nathaniel De Guzman", 15, 0],
        [2021306969, "Marc Dela Cruz", 0, 15]]
            
        return value
# class reports(ctk.CTkFrame):
#      def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

if __name__ == "__main__":
    main = main_window()
    main.mainloop()
            