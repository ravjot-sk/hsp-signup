import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data_module import user_data

class gui_setup:
    def __init__(self,root) -> None:
        self.data = user_data()
        self.keys = ["vorname","name","strasse","ort","geburtsdatum","email","telefon","matnr","sex","iban"]
        self.form_display = {"vorname" : "First Name", "name": "Last Name", "strasse": "Street and Nr", "ort" : "PLZ and City", "geburtsdatum": "Birthday(dd.mm.yyyy)", "email": "Email", "telefon": "Telephone", "matnr": "Matrikel Nummer", "iban" : "IBAN"}
        root.title("User Input Form")

        frm = ttk.Frame(root, padding=10)
        frm.grid()

        ttk.Label(frm,text="Existing users: ").grid(column=0,row=0, columnspan=2)
        self.display_var = tk.StringVar()
        self.user_list_box = ttk.Combobox(frm,textvariable=self.display_var)
        self.user_list_box.grid(column=2,row=0)
        self.user_list_box.state(["readonly"])
        self.existing_users_box()
        self.entries = {}
        self.sex_var = tk.StringVar(value="X")  # Default value
# Create radio buttons for sex selection
        frm_radioButtons=ttk.Frame(frm,padding=3)
        frm_radioButtons.grid(column=0,row=1,columnspan=4)
        ttk.Radiobutton(frm_radioButtons, text="Male", variable=self.sex_var, value="M").grid(row=0, column=0,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="Female", variable=self.sex_var, value="W").grid(row=0,column=1,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="Diverse", variable=self.sex_var, value="D").grid(row=0,column=2,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="N/A", variable=self.sex_var, value="X").grid(row=0,column=3,padx=3)

        i=2
        for key,val in self.form_display.items():
            ttk.Label(frm,text=val).grid(column=0,row=i)
            self.entries[key] = ttk.Entry(frm,width=30)
            self.entries[key].grid(column=1,row=i,columnspan=3)
            i=i+1
# Create a button to submit the input
        frm_saveButton = ttk.Frame(frm,padding=3)
        frm_saveButton.grid(column=0,row=i,columnspan=4)
        save_button = tk.Button(frm_saveButton, text="Save Data", command=lambda: self.save_input())
        save_button.grid()

#Entry fields for url and course number to register
        ttk.Label(frm,text="Enter course url: ").grid(column = 0,row = i+1, columnspan=2)
        self.url = ttk.Entry(frm,width=30)
        self.url.grid(column = 2,row = i+1)

        ttk.Label(frm, text="Enter course number: ").grid(column=0,row=i+2, columnspan=2)
        self.course_number = ttk.Entry(frm,width = 30)
        self.course_number.grid(column = 2,row = i+2)

#Submit button for starting the process. Will be binded to selenium process in main file
        frm_submitButton = ttk.Frame(frm,padding=3)
        frm_submitButton.grid(column=0,row = i+3,columnspan=4)
        self.submit_button = tk.Button(frm_submitButton,text="Submit Form")
        self.submit_button.grid() 
    
    #method to get user data from the entry fields
    def getData(self):
        person={}
        for x in self.form_display:
            person[x] = self.entries[x].get()
        person['sex']=self.sex_var.get()
        return person
    
    #method to load user names into dropdown box of existing users
    def existing_users_box(self):
        if self.data.existing_data:
            self.users = [person['vorname'] for person in self.data.existing_data]
            self.user_list_box['values']= self.users

        self.user_list_box.bind("<<ComboboxSelected>>", lambda event: self.autofill_data())

    #method to autofill existing user data into entry fields 
    def autofill_data(self):
        person = self.user_list_box.get()
        for x in self.data.existing_data:
            if x['vorname']==person:
                person_data = x
        for key in self.form_display:
            self.entries[key].delete(0,'end')
            self.entries[key].insert(0,person_data[key])
        self.sex_var.set(person_data['sex'])

    #method to save a new user's info into the saved file
    def save_input(self):
        new_person =self.getData()
        if all(new_person.values()):
            self.data.save_data(new_person)
            messagebox.showinfo("Saved", f"Your data has been saved!")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")