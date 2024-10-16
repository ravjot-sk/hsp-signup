import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os 
import json



class user_data:
    #important variables:
            #data_file: name of the file containing user details
            #old_data: data loaded from the file
    def __init__(self) -> None:
        self.data_file = "user_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.old_data= json.load(file)
        else:
            self.old_data = []
    
    def save_data(self,new_person):
        i=0
        for index,value in enumerate(self.old_data):
            if value['vorname']==new_person['vorname']:
                self.old_data[index] = new_person
                i=1
                break
        if i==0:
            self.old_data.append(new_person)
        with open(self.data_file, "w") as file:
            json.dump(self.old_data, file)

class gui_setup:
    def __init__(self,root,data) -> None:
        self.user_data_obj=data
        self.keys = ["vorname","name","strasse","ort","geburtsdatum","email","telefon","matnr","sex","iban"]
        self.form_display = {"vorname" : "First Name", "name": "Last Name", "strasse": "Street and Nr", "ort" : "PLZ and City", "geburtsdatum": "Birthday(dd.mm.yyyy)", "email": "Email", "telefon": "Telephone", "matnr": "Matrikel Nummer", "sex": "Sex(M/W/D/X)", "iban" : "IBAN"}
        root.title("User Input Form")

        frm = ttk.Frame(root, padding=10)
        frm.grid()

        ttk.Label(frm,text="Existing users: ").grid(column=0,row=0)
        self.display_var = tk.StringVar()
        self.user_list_box = ttk.Combobox(frm,textvariable=self.display_var)
        self.user_list_box.grid(column=1,row=0)
        self.user_list_box.state(["readonly"])
        self.existing_users_box()
        self.entries = {}
        #sex_var = tk.StringVar(value="Not Specified")  # Default value
        #frmm = ttk.Frame(frm,padding=3)
        #frmm.grid()
# Create radio buttons for sex selection
        #ttk.Radiobutton(frmm, text="Male", variable=sex_var, value="M").grid(row=0, column=0, sticky=tk.W)
        #ttk.Radiobutton(frmm, text="Female", variable=sex_var, value="W").grid(row=0,column=1,sticky=tk.W)
        #ttk.Radiobutton(frmm, text="Diverse", variable=sex_var, value="D").grid(row=0,column=2,sticky=tk.W)
        #ttk.Radiobutton(frmm, text="N/A", variable=sex_var, value="X").grid(row=0,column=3,sticky=tk.W)

        i=1
        for x in self.keys:
            ttk.Label(frm,text=self.form_display[x]).grid(column=0,row=i)
            self.entries[x] = ttk.Entry(frm,width=30)
            self.entries[x].grid(column=1,row=i)
            i=i+1
# Create a button to submit the input
        save_button = tk.Button(frm, text="Save Data", command=lambda: self.save_input(data))
        save_button.grid(column=1,row=i,pady=10)

#Entry fields for url and course number to register
        ttk.Label(frm,text="Enter course url: ").grid(column = 0,row = i+1)
        self.url = ttk.Entry(frm,width=30)
        self.url.grid(column = 1,row = i+1)

        ttk.Label(frm, text="Enter course number: ").grid(column=0,row=i+2)
        self.course_number = ttk.Entry(frm,width = 30)
        self.course_number.grid(column = 1,row = i+2)

#Submit button for starting the process. Will be binded to selenium process in main file
        self.submit_button = tk.Button(frm,text="Submit Form")
        self.submit_button.grid(column=1,row=i+3, pady=10) 
    
    #method to get user data from the entry fields
    def getData(self):
        person={}
        for x in self.keys:
            person[x] = self.entries[x].get()
        return person
    
    #method to load user names into dropdown box of existing users
    def existing_users_box(self):
        if self.user_data_obj.old_data:
            self.users = [person['vorname'] for person in self.user_data_obj.old_data]
            self.user_list_box['values']= self.users

        self.user_list_box.bind("<<ComboboxSelected>>", lambda event: self.autofill_data())

    #method to autofill existing user data into entry fields 
    def autofill_data(self):
        person = self.user_list_box.get()
        for x in self.user_data_obj.old_data:
            if x['vorname']==person:
                data = x
        for x in self.keys:
            self.entries[x].delete(0,'end')
            self.entries[x].insert(0,data[x])

    #method to save a new user's info into the saved file
    def save_input(self,data):
        new_person =self.getData()
        if all(new_person.values()):
            data.save_data(new_person)
            messagebox.showinfo("Saved", f"Your data has been saved!")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields")