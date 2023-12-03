from datetime import date
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from data_controller import data_controller

class view_student(ctk.CTkToplevel):
    def __init__(self, master, student_info, **kwargs):
        super().__init__(master, **kwargs)       
        
        self.controller = data_controller()
        self.student_info = student_info
                
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title('Add Student')
        self.geometry('600x400')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.student_number_label = ctk.CTkLabel(master=self, text=f"Student Number: {student_info[0]}", font=("Roboto", 18))
        self.student_number_label.grid(row=0,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.form_frame = ctk.CTkScrollableFrame(master=self)
        self.form_frame.grid(row=1, column=0, sticky='nesw')
        
        self.form_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.form_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        #first name
        self.first_name_label = ctk.CTkLabel(master=self.form_frame, text="First Name", font=("Roboto", 18))
        self.first_name_label.grid(row=0,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.first_name_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter First Name", font=("Roboto", 18))
        self.first_name_entry.grid(row=1,column=0,padx=20,pady=(5, 20), sticky='ew')
        self.first_name_entry.insert(0, student_info[1])
        
        #middle initial
        self.middle_initial_label = ctk.CTkLabel(master=self.form_frame, text="Middle Initial", font=("Roboto", 18))
        self.middle_initial_label.grid(row=0,column=1,padx=20,pady=(20, 5), sticky='w')
        
        self.middle_initial_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Middle Initial", font=("Roboto", 18))
        self.middle_initial_entry.grid(row=1,column=1,padx=20,pady=(5, 20), sticky='ew')
        self.middle_initial_entry.insert(0, student_info[3])
        
        #last name
        self.last_name_label = ctk.CTkLabel(master=self.form_frame, text="Last Name", font=("Roboto", 18))
        self.last_name_label.grid(row=0,column=2,padx=20,pady=(20, 5), sticky='w')
        
        self.last_name_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Last Name", font=("Roboto", 18))
        self.last_name_entry.grid(row=1,column=2,padx=20,pady=(5, 20), sticky='ew')
        self.last_name_entry.insert(0, student_info[2])
        
        #section
        self.section_label = ctk.CTkLabel(master=self.form_frame, text="Section", font=("Roboto", 18))
        self.section_label.grid(row=2,column=0,padx=20,pady=(20, 5), sticky='w')
        
        section_select_values = [section[1] for section in self.controller.get_sections()]
        self.section_select = ctk.CTkComboBox(master=self.form_frame, values=section_select_values)
        self.section_select.grid(row=3,column=0,padx=20,pady=(5, 20), sticky='ew')
        self.section_select.set(section_select_values[student_info[4] - 1])
        
        #birthday
        self.birthday_label = ctk.CTkLabel(master=self.form_frame, text="Birthday", font=("Roboto", 18))
        self.birthday_label.grid(row=2,column=1,padx=20,pady=(20, 5), sticky='w')
        
        
        self.birthday_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Birthday", font=("Roboto", 18))
        self.birthday_entry.grid(row=3,column=1,padx=20,pady=(5, 20), sticky='ew')
        self.birthday_entry.insert(0, date.strftime(student_info[5], "%Y/%m/%d"))
        
        #age
        self.age_label_label = ctk.CTkLabel(master=self.form_frame, text="Age", font=("Roboto", 18))
        self.age_label_label.grid(row=2,column=2,padx=20,pady=(20, 5), sticky='w')
        
        self.age_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Age", font=("Roboto", 18))
        self.age_entry.grid(row=3,column=2,padx=20,pady=(5, 20), sticky='ew')
        self.age_entry.insert(0, student_info[6])
        
        #gender
        self.gender_label = ctk.CTkLabel(master=self.form_frame, text="Gender", font=("Roboto", 18))
        self.gender_label.grid(row=4,column=0,padx=20,pady=(20, 5), sticky='w')
        
        gender_values=['Male', 'Female']
        self.gender_select = ctk.CTkComboBox(master=self.form_frame, state='readonly', values=gender_values)
        self.gender_select.grid(row=5,column=0,padx=20,pady=(5, 20), sticky='ew')
        self.gender_select.set(student_info[7])
        
        #contact no
        self.contact_no_label = ctk.CTkLabel(master=self.form_frame, text="Contact No.", font=("Roboto", 18))
        self.contact_no_label.grid(row=4,column=1,padx=20,pady=(20, 5), sticky='w')
        
        self.contact_no_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Contact No.", font=("Roboto", 18))
        self.contact_no_entry.grid(row=5,column=1,padx=20,pady=(5, 20), sticky='ew')
        self.contact_no_entry.insert(0, student_info[8])
        
        #student email
        self.student_email_label = ctk.CTkLabel(master=self.form_frame, text="Student Email", font=("Roboto", 18))
        self.student_email_label.grid(row=4,column=2,padx=20,pady=(20, 5), sticky='w')
        
        self.student_email_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Student Email", font=("Roboto", 18))
        self.student_email_entry.grid(row=5,column=2,padx=20,pady=(5, 20), sticky='ew')
        self.student_email_entry.insert(0, student_info[9])
        
        self.button_panel = ctk.CTkFrame(master=self)
        self.button_panel.grid(row=2, column=0, sticky='nsew')
        self.button_panel.grid_columnconfigure((0, 1), weight=1)
        
        self.edit_student_button = ctk.CTkButton(master=self.button_panel, text="Edit Student", command=self.edit_student)
        self.edit_student_button.grid(row=0,column=0,padx=20,pady=20, columnspan=2, sticky='ew')
        
        self.confirm_button = ctk.CTkButton(master=self.button_panel, text="CONFIRM", command=self.confirm)
        
        self.cancel_button = ctk.CTkButton(master=self.button_panel, text="CANCEL", command=self.cancel)
    
    def edit_student(self):
        self.edit_student_button.grid_forget()
        self.confirm_button.grid(row=0,column=1,padx=20,pady=20, sticky='ew')
        self.cancel_button.grid(row=0,column=0,padx=20,pady=20, sticky='ew')
    
    def confirm(self):
        confirm = messagebox.askyesno("Update Student", "Are you sure you want to update the student info?")
        
        if confirm:
            self.edit_student_button.grid(row=0,column=0,padx=20,pady=20, columnspan=2, sticky='ew')
            self.confirm_button.grid_forget()
            self.cancel_button.grid_forget()
            
            values = [self.first_name_entry.get(), self.last_name_entry.get(), self.middle_initial_entry.get(),
                    self.controller.get_section_id(self.section_select.get()), self.birthday_entry.get(), 
                    self.age_entry.get(),self.gender_select.get(), self.contact_no_entry.get(), 
                    self.student_email_entry.get(), self.student_info[0]]
            self.controller.update_student(values)
        else:
            print("cancel")
    
    def cancel(self):
        self.edit_student_button.grid(row=0,column=0,padx=20,pady=20, columnspan=2, sticky='ew')
        self.confirm_button.grid_forget()
        self.cancel_button.grid_forget()
        