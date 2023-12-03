import csv
import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from CTkTable import *
from datetime import date
from tkinter import messagebox
from tkinter import ttk
from data_controller import data_controller

class main_window(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.controller = data_controller()
        self.controller.create_database()
        self.controller.create_tables()
        # self.controller.reset_attendance()
        
        # Color Theme 
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        #configure columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        #title and size of window
        self.title('RecogNice Dashboard')
        self.current_frame = "home"
        self.parent_frame = self.winfo_toplevel()

        #sidebar
        self.navbar = ctk.CTkFrame(master=self)
        self.navbar.grid_columnconfigure(0, weight=1)
        self.navbar.grid_columnconfigure(1, weight=1)
        self.navbar.grid_columnconfigure(2, weight=1)
        self.navbar.grid_rowconfigure(0, weight=1)
        font = ("Roboto",36)
        
        #Main Label
        self.main_label = ctk.CTkLabel(master=self.navbar, text="RecogNice Attendance Checker", font=font)
        self.main_label.grid(row=0, column=0, padx=20, pady=20, columnspan=3, sticky='ew')
        
        #buttons
        self.home_button = ctk.CTkButton(master=self.navbar, text="HOME", command=self.home)
        self.home_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.students_button = ctk.CTkButton(master=self.navbar, text="STUDENTS", command=self.students)
        self.students_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.reports_button = ctk.CTkButton(master=self.navbar, text="REPORTS", command=self.reports)
        self.reports_button.grid(row=1, column=2, padx=20, pady=10, sticky="ew")
        
        self.navbar.grid(row=1, column=0, sticky="nsew")
         
        #home
        self.home = home(master=self)
        self.home.grid(row=2, column=0, sticky="nsew")
        
    def home(self):
        if self.current_frame != "home":
            self.current_frame = "home"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["row"]) == 2:
                    frame.grid_forget()
                    self.home = home(master=self)
                    self.home.grid(row=2, column=0, sticky="nsew")
                    
            
    def students(self):
        if self.current_frame != "students":
            self.current_frame = "students"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["row"]) == 2:
                    frame.grid_forget()
                    self.students = students(master=self)
                    self.students.grid(row=2, column=0, sticky="nsew")
                    
        self.controller = data_controller()
        # self.controller.get_student_table_info(students=self.controller.get_students())
        
    def reports(self):
        if self.current_frame != "reports":
            self.current_frame = "reports"
            for frame in self.parent_frame.grid_slaves():
                if int(frame.grid_info()["row"]) == 2:
                    frame.grid_forget()
                    self.reports = reports(master=self)
                    self.reports.grid(row=2, column=0, sticky="nsew")
        
class home(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = data_controller()
        self.section = ""
        
        self.today = date.today()
        
        #Section Frame
        self.section_frame = ctk.CTkFrame(master=self)
        self.section_label = ctk.CTkLabel(master=self.section_frame, text="Sections", font=("Roboto", 24))
        self.section_label.grid(row=0, column=0, padx=30, pady=(20,5), sticky='w')

        self.section_frame.grid_columnconfigure(0, weight=1)
        self.section_frame.grid_rowconfigure(1, weight=1)
        
        date_today = self.today.strftime("%B %d, %Y")
        self.date_label = ctk.CTkLabel(master=self.section_frame, text="Date: " + date_today, font=("Roboto", 24))
        self.date_label.grid(row=0, column=1, padx=(20,30), pady=(20,5), sticky='e')
        
        #Section Table
        columns = ["section", "students", "present", "absent"]
        self.section_table = ttk.Treeview(self.section_frame, columns=columns)

        self.section_table.heading("#0", text="#")
        self.section_table.heading("section", text="Section")
        self.section_table.heading("students", text="Students")
        self.section_table.heading("present", text="Present")
        self.section_table.heading("absent", text="Absent")

            
        self.section_table.column("#0", width=50)
        self.section_table.column("students", width=100)  
        self.section_table.column("present", width=100)  
        self.section_table.column("absent", width=100)  
        
        controller = data_controller()
        section_list = controller.get_section_table_info()
        
        counter = 1
        for section in section_list:
            self.section_table.insert("", tk.END,text=counter, values=section)
            counter+=1
        
        self.section_table.grid(row=2, column=0, padx=30, pady=20, columnspan=2, sticky='ew')
        self.section_table.bind("<<TreeviewSelect>>", self.on_select)
        
        self.check_attendance_button = ctk.CTkButton(master=self, text="CHECK ATTENDANCE", command=self.check_attendance)
        self.check_attendance_button.grid(row=3, column=0, padx=30, pady=20, sticky='ew')
        self.check_attendance_button.configure(state=tk.DISABLED)
        
        self.section_frame.grid(row=0, column=0, padx=30, pady=30, sticky='ew')
    
    def on_select(self, event):
        self.check_attendance_button.configure(state=tk.NORMAL)
        item = event.widget.focus()
        values = event.widget.item(item, "values")
        self.section = values
        self.section_id =  event.widget.item(item, "text")
        
        
    def check_attendance(self):
        date_today = self.today.strftime("%Y/%m/%d")
        if self.section[2] == "Not Checked" and self.section[3] == "Not Checked":
            
            if self.controller.attendance_is_empty():
                confirm = messagebox.askyesno("Check Attendance?", f"Do you wish to start checking the Attendance for {self.section[0]}?")
                if confirm:

                    from face_window import face_panel
                    next_window = face_panel(self.section)
                    next_window.mainloop()
                else:
                    print("exit operation canceled")
            else:
                with open('attendance.csv', "r") as file:
                    reader = csv.reader(file)
                    old_data = list(reader)
                if int(old_data[0][2]) == self.section_id and old_data[0][3] == date_today:
                    confirm = messagebox.askyesno("Check Attendance?", f"It seems there is a previous session for {self.section[0]}, do you want to continue the session?")
                    
                    if not confirm:
                        self.controller.reset_attendance()
                    
                    from face_window import face_panel
                    next_window = face_panel(self.section)
                    next_window.mainloop()
                else:
                    self.controller.reset_attendance()
                    
                    from face_window import face_panel
                    next_window = face_panel(self.section)
                    next_window.mainloop()
                    
        else: 
            messagebox.showinfo("Finished Attendance", f"Attendance Already Checked for {self.section[0]}")
         
class students(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = data_controller()
        
        self.selected_student = 0
        #Student Label
        self.student_label = ctk.CTkLabel(master=self, text = "Students", font= ("Roboto", 20))
        self.student_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        #section dropdown
        values=[section[1] for section in self.controller.get_sections()]
        combobox_var = ctk.StringVar(value=values[0])
        self.section_selection = ctk.CTkComboBox(master=self, state='readonly', values=values, command=self.section_on_select, variable=combobox_var)
        self.section_selection.grid(row=0, column=1, padx=20, pady=20, sticky='ew')
        # self.section_selection.bind("<<ComboboxSelected>>", self.section_on_select)

        
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
        
        students_list = controller.get_student_table_info(students=controller.get_students(self.section_selection.get()))
        
        counter = 1
        for student in students_list:
            self.students_table.insert("", tk.END,text=counter, values=student)
            counter+=1

        self.students_table.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky='nsew')
        self.students_table.bind("<<TreeviewSelect>>", self.on_select)
        
        self.view_student_info = ctk.CTkButton(master=self, text="VIEW STUDENT", command=self.view_student)
        self.view_student_info.grid(row=2, column=0, padx=30, pady=20, sticky='ew')
        self.view_student_info.configure(state=tk.DISABLED)

        self.add_student_button = ctk.CTkButton(master=self, text="ADD STUDENT", command=self.add_student)
        self.add_student_button.grid(row=2, column=1, padx=30, pady=20, sticky='ew')
        
    def view_student(self):
        from view_student import view_student
        student_info = view_student(master=self, student_info=self.controller.get_student_info(int(self.selected_student)))
        student_info.mainloop()
    
    def add_student(self):
        from add_student import add_student
        new_student = add_student()
        new_student.mainloop()
    
    def section_on_select(self, event):
        selected_value = self.section_selection.get()
        self.controller.get_student_table_info(selected_value)
            
    def on_select(self, event):
        self.view_student_info.configure(state=tk.NORMAL)
        item = event.widget.focus()
        values = event.widget.item(item, "values")
        self.selected_student = values[0]
       
class reports(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = data_controller()
        
        self.student_label = ctk.CTkLabel(master=self, text = "Reports", font= ("Roboto", 24))
        self.student_label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        
        #section dropdown
        values=[section[1] for section in self.controller.get_sections()]
        combobox_var = ctk.StringVar(value=values[0])
        self.section_selection = ctk.CTkComboBox(master=self, state='readonly', values=values, command=self.on_select, variable=combobox_var)
        self.section_selection.grid(row=0, column=1, padx=20, pady=20, sticky='ew')
        
        #date selection
        values=self.controller.get_dates(self.section_selection.get())
        combobox_var = ctk.StringVar(value=values[0])
        self.date_selection = ctk.CTkComboBox(master=self, state='readonly', values=values, command=self.on_select, variable=combobox_var)
        self.date_selection.grid(row=0, column=0, padx=20, pady=20, sticky='ew')
        
        #Table
        columns = ["student_number", "name", "today"]
        self.students_table = ttk.Treeview(self, columns=columns)

        self.students_table.heading("#0", text="#")
        self.students_table.heading("student_number", text="Student Number")
        self.students_table.heading("name", text="Name")
        self.students_table.heading("today", text="Status")

            
        self.students_table.column("#0", width=50)
        self.students_table.column("today", width=100)   
        
        students_list = self.controller.get_report_table_info(students=self.controller.get_students(self.section_selection.get()), date=self.date_selection.get())
        
        counter = 1
        for student in students_list:
            self.students_table.insert("", tk.END,text=counter, values=student)
            counter+=1

        self.students_table.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky='nsew')
        self.students_table.bind("<<TreeviewSelect>>", self.on_select)
        
        self.download_report_button = ctk.CTkButton(master=self, text="DOWNLOAD REPORT", command=self.download_report)
        self.download_report_button.grid(row=2, column=0, columnspan=2, padx=30, pady=20, sticky='ew')
        
        
    def download_report(self):
        date_path = self.date_selection.get().replace('/', '')
        filename = self.section_selection.get() + date_path  + 'Attendance.csv'
        downloads_folder = os.path.expanduser("~") + "/Downloads"
        file_path = os.path.join(downloads_folder, filename)
        
        data = self.controller.get_report_table_info(students=self.controller.get_students(self.section_selection.get()), date=self.date_selection.get())
        data.insert(0, ['Student Number', 'Full Name', 'Attendance Status'])
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
        messagebox.showinfo("Download Successful", f"File: {filename} has been successfully downloaded. Check your Downloads Folder")
        file.close()
    
    def on_select(self, event):
        self.students_table.delete(*self.students_table.get_children())
        selected_value = self.section_selection.get()
        selected_date = self.date_selection.get()
        
        students_list = self.controller.get_report_table_info(students=self.controller.get_students(selected_value), date=selected_date)
        
        counter = 1
        for student in students_list:
            self.students_table.insert("", tk.END,text=counter, values=student)
            counter+=1
            
        
class view_student(ctk.CTkFrame):
     def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

if __name__ == "__main__":
    main = main_window()
    main.mainloop()
            