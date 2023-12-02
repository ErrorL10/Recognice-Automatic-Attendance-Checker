import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from CTkTable import *
from datetime import date
from tkinter import messagebox
from tkinter import ttk
from data_controller import data_controller

class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.controller = data_controller()
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
        
        self.current_frame = "home"
        self.parent_frame = self.winfo_toplevel()
        
        #sidebar
        self.sidebar = ctk.CTkFrame(master=self)
        font = ("Roboto",20)
        user_image = ctk.CTkImage(dark_image= Image.open("student_images\BAGS.jpg"), size=(100,100))
        
        self.user_image_label = ctk.CTkLabel(master=self.sidebar, image=user_image, text="")
        self.user_image_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        #Name Display
        self.user_name = ctk.CTkLabel(master=self.sidebar, text="Errol Liscano", anchor='center', font=font)
        self.user_name.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")
        
        #buttons
        self.home_button = ctk.CTkButton(master=self.sidebar, text="HOME", command=self.home)
        self.home_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.students_button = ctk.CTkButton(master=self.sidebar, text="STUDENTS", command=self.students)
        self.students_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.reports_button = ctk.CTkButton(master=self.sidebar, text="REPORTS", command=self.reports)
        self.reports_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        #home
        self.home = home(master=self)
        self.home.grid(row=0, column=1, sticky="nsew")
        
    def home(self):
        if self.current_frame != "home":
            self.current_frame = "home"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["column"]) == 1:
                    frame.grid_forget()
                    self.home = home(master=self)
                    self.home.grid(row=0, column=1, sticky="nsew")
                    
        self.controller.create_database()
        self.controller.create_tables()
                    
            
    
    def students(self):
        if self.current_frame != "students":
            self.current_frame = "students"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["column"]) == 1:
                    frame.grid_forget()
                    self.students = students(master=self)
                    self.students.grid(row=0, column=1, sticky="nsew")
                    
        from data_controller import data_controller
        controller = data_controller()
        controller.get_student_table_info(students=controller.get_students())
        
    def reports(self):
        if self.current_frame != "reports":
            self.current_frame = "reports"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["column"]) == 1:
                    frame.grid_forget()
                    self.reports = reports(master=self)
                    self.reports.grid(row=0, column=1, sticky="nsew")
        
class home(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = data_controller()
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

            from face_window import face_panel
            next_window = face_panel()
            next_window.mainloop()
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
        columns = ["student_number", "name", "present", "absent"]
        self.students_table = ttk.Treeview(self, columns=columns)

        self.students_table.heading("#0", text="#")
        self.students_table.heading("student_number", text="Student Number")
        self.students_table.heading("name", text="Name")
        self.students_table.heading("present", text="Presences")
        self.students_table.heading("absent", text="Absences")

            
        self.students_table.column("#0", width=50)
        self.students_table.column("present", width=100)  
        self.students_table.column("absent", width=100)  
        
        controller = data_controller()
        students_list = controller.get_student_table_info(students=controller.get_students())
        
        counter = 1
        for student in students_list:
            self.students_table.insert("", tk.END,text=counter, values=student)
            counter+=1

        self.students_table.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky='nsew')

class reports(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.student_label = ctk.CTkLabel(master=self, text = "Reports", font= ("Roboto", 20))
        self.student_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        # controller = data_controller()
        # controller.insert_attendance()

if __name__ == "__main__":
    main = main_window()
    main.mainloop()
            