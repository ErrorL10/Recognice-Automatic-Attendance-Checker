import os
import shutil
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from data_controller import data_controller

class add_student(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title('Add Student')
        self.geometry('275x500')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.controller = data_controller()
        
        self.form_frame = ctk.CTkScrollableFrame(master=self)
        self.form_frame.grid(row=0, column=0, sticky='nesw')
        
        for i in range(22):
            self.form_frame.grid_columnconfigure(i, minsize=250)
            self.form_frame.grid_rowconfigure(i, weight=1)
        
        #add student
        self.add_student_label = ctk.CTkLabel(master=self.form_frame, text="Add new Student", font=("Roboto", 24))
        self.add_student_label.grid(row=0,column=0,padx=20,pady=20, sticky='ew')
        
        #first name
        self.student_number_label = ctk.CTkLabel(master=self.form_frame, text="Enter Student Number", font=("Roboto", 18))
        self.student_number_label.grid(row=1,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.student_number_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Student Number", font=("Roboto", 18))
        self.student_number_entry.grid(row=2,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #first name
        self.first_name_label = ctk.CTkLabel(master=self.form_frame, text="First Name", font=("Roboto", 18))
        self.first_name_label.grid(row=3,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.first_name_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter First Name", font=("Roboto", 18))
        self.first_name_entry.grid(row=4,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #last name
        self.last_name_label = ctk.CTkLabel(master=self.form_frame, text="Last Name", font=("Roboto", 18))
        self.last_name_label.grid(row=5,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.last_name_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Last Name", font=("Roboto", 18))
        self.last_name_entry.grid(row=6,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #middle initial
        self.middle_initial_label = ctk.CTkLabel(master=self.form_frame, text="Middle Initial", font=("Roboto", 18))
        self.middle_initial_label.grid(row=7,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.middle_initial_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Middle Initial", font=("Roboto", 18))
        self.middle_initial_entry.grid(row=8,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #section
        self.section_label = ctk.CTkLabel(master=self.form_frame, text="Section", font=("Roboto", 18))
        self.section_label.grid(row=9,column=0,padx=20,pady=(20, 5), sticky='w')
        
        values=[section[1] for section in self.controller.get_sections()]
        self.section_select = ctk.CTkComboBox(master=self.form_frame, values=values)
        self.section_select.grid(row=10,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #birthday
        self.birthday_label = ctk.CTkLabel(master=self.form_frame, text="Birthday", font=("Roboto", 18))
        self.birthday_label.grid(row=11,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.birthday_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Birthday", font=("Roboto", 18))
        self.birthday_entry.grid(row=12,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #age
        self.age_label_label = ctk.CTkLabel(master=self.form_frame, text="Age", font=("Roboto", 18))
        self.age_label_label.grid(row=13,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.age_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Age", font=("Roboto", 18))
        self.age_entry.grid(row=14,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #gender
        self.gender_label = ctk.CTkLabel(master=self.form_frame, text="Gender", font=("Roboto", 18))
        self.gender_label.grid(row=15,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.gender_select = ctk.CTkComboBox(master=self.form_frame, state='readonly', values=['Male', 'Female'])
        self.gender_select.grid(row=16,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #contact no
        self.contact_no_label = ctk.CTkLabel(master=self.form_frame, text="Contact No.", font=("Roboto", 18))
        self.contact_no_label.grid(row=17,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.contact_no_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Contact No.", font=("Roboto", 18))
        self.contact_no_entry.grid(row=18,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #student email
        self.student_email_label = ctk.CTkLabel(master=self.form_frame, text="Student Email", font=("Roboto", 18))
        self.student_email_label.grid(row=19,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.student_email_entry = ctk.CTkEntry(master=self.form_frame, placeholder_text="Enter Student Email", font=("Roboto", 18))
        self.student_email_entry.grid(row=20,column=0,padx=20,pady=(5, 20), sticky='ew')
        
        #add picture
        self.add_picture_label = ctk.CTkLabel(master=self.form_frame, text="Add Picture", font=("Roboto", 18))
        self.add_picture_label.grid(row=21,column=0,padx=20,pady=(20, 5), sticky='w')
        
        self.add_picture_button = ctk.CTkButton(master=self.form_frame, text="Add Picture", command=self.add_picture)
        self.add_picture_button.grid(row=22,column=0,padx=20,pady=20, sticky='ew')
        
        self.confirm_button = ctk.CTkButton(master=self.form_frame, text="CONFIRM", command=self.confirm)
        self.confirm_button.grid(row=23,column=0,padx=20,pady=(30, 5), sticky='ew')
        
        self.cancel_button = ctk.CTkButton(master=self.form_frame, text="CANCEL", command=self.cancel)
        self.cancel_button.grid(row=24,column=0,padx=20,pady=(5, 20), sticky='ew')
    
    def confirm(self):
        selected_section = self.section_select.get()
        confirm = messagebox.askyesno("Confirm?", "Add Student?")
        fullname = self.first_name_entry.get() + " " + self.middle_initial_entry.get() + " " + self.last_name_entry.get()
        
        source_folder = 'student_images/temp'
        target_folder = f'student_images/{selected_section}'

        jpg_count = len([filename for filename in os.listdir(source_folder)])
        print(jpg_count)
        if jpg_count == 5:
            section = ''
            if confirm:
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                for i, filename in enumerate(os.listdir(source_folder), start=1):
                    print("start")
                    if filename.endswith('.jpg'):
                        new_filename = '{}{}.jpg'.format(fullname, i)
                        os.rename(os.path.join(source_folder, filename), os.path.join(source_folder, new_filename))
                        shutil.copy(os.path.join(source_folder, new_filename), os.path.join(target_folder, new_filename))
                        os.remove(os.path.join(source_folder, new_filename))
                        print("success")
                    
                if self.controller.find_section(selected_section):
                    print(self.controller.find_section(selected_section))
                    section = self.controller.get_section_id(selected_section)
                else:
                    self.controller.add_section(selected_section)
                    section = self.controller.get_section_id(selected_section)
                    
                values = [self.student_number_entry.get(), self.first_name_entry.get(), self.last_name_entry.get(), 
                        self.middle_initial_entry.get(), section, self.birthday_entry.get(), 
                        self.age_entry.get(),self.gender_select.get(), self.contact_no_entry.get(), 
                        self.student_email_entry.get()]
                
                self.controller.add_student(values=values)
                self.destroy()
        else:
            messagebox.showinfo("Not Enough Pictures", "Not Enough Pictures taken, please take more")
    
    def cancel(self):
        confirm = messagebox.askyesno("Cancel?", "Do you cancel adding a student?")
        if confirm:
            self.destroy()
    
    def add_picture(self):
        from camera_window import camera_window
        camera = camera_window()
        camera.mainloop()
        