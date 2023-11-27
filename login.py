import tkinter as tk
import customtkinter as ctk


class login(tk.Tk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title('RecogNice')
        self.geometry('300x400')
        
        self.main_frame = frame(master=self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        

class frame(ctk.CTkFrame):
  
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        font = ("Roboto",20)
          
        self.login_label = ctk.CTkLabel(master=self, text="RecogNice Login", anchor='center', font=font)
        self.login_label.grid(row=0, column=0, padx=20, pady=20)
        
        self.email_label = ctk.CTkLabel(master=self, text='Email')
        self.email_label.grid(row=1, column=0, padx=20)
        
        self.email_textbox = ctk.CTkTextbox(master=self, width=250, height=20, corner_radius=0.5, activate_scrollbars=False)
        self.email_textbox.grid(row=2, column=0, padx=20)
        
        self.password_label = ctk.CTkLabel(master=self, text='Password')
        self.password_label.grid(row=3, column=0, padx=20)
        
        self.password_textbox = ctk.CTkTextbox(master=self, width=250, height=20, corner_radius=0.5, activate_scrollbars=False)
        self.password_textbox.grid(row=4, column=0, padx=20)
        
        self.login_button = ctk.CTkButton(self, text="LOGIN", command=self.login)
        self.login_button.grid(row=5, column=0, padx=20, pady=20)
     
    def login(self):
        print("Logged In")
        
if __name__ == "__main__":
    login = login()
    login.mainloop()
    