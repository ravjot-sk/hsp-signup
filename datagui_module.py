import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data_module import user_data

class gui_setup:
    def __init__(self,root) -> None:
        self.data = user_data()
        self.keys = ["vorname","name","strasse","ort","geburtsdatum","email","telefon","matnr","sex","iban"]
        self.form_display = {
            "vorname" : "First Name", 
            "name": "Last Name", 
            "strasse": "Street and Nr", 
            "ort" : "PLZ and City", 
            "geburtsdatum": "Birthday(dd.mm.yyyy)", 
            "email": "Email", 
            "telefon": "Telephone", 
            "matnr": "Matrikel Nummer", 
            "iban" : "IBAN"
            }
        
        self.row_counter=0
        self.user1_frame = ttk.Frame(root, padding=10)
        self.user1_gui()
        self.user1_frame.grid()

# Create a button to submit the input
        frm_saveButton = ttk.Frame(self.user1_frame,padding=3)
        frm_saveButton.grid(column=0,row=self.row_counter,columnspan=4)
        self.row_counter += 1
        save_button = tk.Button(frm_saveButton, text="Save Data", command=lambda: self.save_input())
        save_button.grid()

#Entry fields for url and course number to register
        ttk.Label(self.user1_frame,text="Enter course url: ").grid(column = 0,row = self.row_counter, columnspan=2)
        self.url = ttk.Entry(self.user1_frame,width=30)
        self.url.grid(column = 2,row = self.row_counter)
        self.row_counter += 1

        ttk.Label(self.user1_frame, text="Enter course number: ").grid(column=0,row=self.row_counter, columnspan=2)
        self.course_number = ttk.Entry(self.user1_frame,width = 30)
        self.course_number.grid(column = 2,row = self.row_counter)
        self.row_counter += 1

        self.dance_course(root)
        self.dance_var = tk.IntVar()
        self.danceButton = ttk.Checkbutton(self.user1_frame,text="Two person course: ",variable=self.dance_var, command=self.lets_dance)
        self.danceButton.grid(column=0,row=self.row_counter,columnspan=2)
        self.row_counter += 1

#Submit button for starting the process. Will be binded to selenium process in main file
        self.frm_submitButton = ttk.Frame(root,padding=10)
        self.frm_submitButton.grid(column=0,row = 1,columnspan=4)
        self.submit_button = tk.Button(self.frm_submitButton,text="Submit Form")
        self.submit_button.grid() 
    
    def user1_gui(self):
        ttk.Label(self.user1_frame,text="Enter User Data").grid(column=0,row=self.row_counter,columnspan=3)
        self.row_counter += 1
        ttk.Label(self.user1_frame,text="Existing users: ").grid(column=0,row=self.row_counter, columnspan=2)
        self.display_var = tk.StringVar()
        self.user_list_box = ttk.Combobox(self.user1_frame,textvariable=self.display_var)
        self.user_list_box.grid(column=2,row=self.row_counter)
        self.row_counter += 1
        self.user_list_box.state(["readonly"])
        self.existing_users_box()
        self.entries = {}
        self.sex_var = tk.StringVar(value="X")  # Default value
# Create radio buttons for sex selection
        frm_radioButtons=ttk.Frame(self.user1_frame,padding=3)
        frm_radioButtons.grid(column=0,row=self.row_counter,columnspan=4)
        self.row_counter += 1
        ttk.Radiobutton(frm_radioButtons, text="Male", variable=self.sex_var, value="M").grid(row=0, column=0,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="Female", variable=self.sex_var, value="W").grid(row=0,column=1,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="Diverse", variable=self.sex_var, value="D").grid(row=0,column=2,padx=3)
        ttk.Radiobutton(frm_radioButtons, text="N/A", variable=self.sex_var, value="X").grid(row=0,column=3,padx=3)

        for key,val in self.form_display.items():
            ttk.Label(self.user1_frame,text=val).grid(column=0,row=self.row_counter)
            self.entries[key] = ttk.Entry(self.user1_frame,width=30)
            self.entries[key].grid(column=1,row=self.row_counter,columnspan=3)
            self.row_counter += 1


    #method to get user data from the entry fields
    def getData(self):
        person={}
        for x in self.form_display:
            person[x] = self.entries[x].get()
        person['sex']=self.sex_var.get()
        return person
    
    def getData_user2(self):
        person={}
        for x in self.form_display_2:
            person[x] = self.entries_2[x].get()
        person['sex_2'] = self.sex_var_2.get()
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
                break
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

    def dance_course(self,root):
        self.user2_frame = ttk.Frame(root,padding=10)
        self.keys_2 = [
            key + "_2" 
            for key in self.keys 
            if key != "iban"
        ]
        self.form_display_2 = {
            key+"_2" : value 
            for key,value in self.form_display.items()
            if key!="iban"
            }
        local_row_counter =0

        ttk.Label(self.user2_frame,text="Enter User2 Data").grid(column=0,row=local_row_counter,columnspan=3)
        local_row_counter += 1

        ttk.Label(self.user2_frame,text="Existing users: ").grid(column=0,row=local_row_counter, columnspan=2)
        self.display_var_2 = tk.StringVar()
        self.user_list_box_2 = ttk.Combobox(self.user2_frame,textvariable=self.display_var_2)
        self.user_list_box_2.grid(column=2,row=local_row_counter)
        local_row_counter +=1
        self.user_list_box_2.state(["readonly"])
        
        if self.users:
            self.user_list_box_2['values'] = self.users

        self.user_list_box_2.bind("<<ComboboxSelected>>",lambda event: self.autofill_data_2())

        self.entries_2 = {}
        self.sex_var_2 = tk.StringVar(value="X")  # Default value
# Create radio buttons for sex selection
        frm2_radioButtons=ttk.Frame(self.user2_frame,padding=3)
        frm2_radioButtons.grid(column=0,row=local_row_counter,columnspan=4)
        local_row_counter += 1
        ttk.Radiobutton(frm2_radioButtons, text="Male", variable=self.sex_var_2, value="M").grid(row=0, column=0,padx=3)
        ttk.Radiobutton(frm2_radioButtons, text="Female", variable=self.sex_var_2, value="W").grid(row=0,column=1,padx=3)
        ttk.Radiobutton(frm2_radioButtons, text="Diverse", variable=self.sex_var_2, value="D").grid(row=0,column=2,padx=3)
        ttk.Radiobutton(frm2_radioButtons, text="N/A", variable=self.sex_var_2, value="X").grid(row=0,column=3,padx=3)

        for key,val in self.form_display_2.items():
            ttk.Label(self.user2_frame,text=val).grid(column=0,row=local_row_counter)
            self.entries_2[key] = ttk.Entry(self.user2_frame,width=30)
            self.entries_2[key].grid(column=1,row=local_row_counter,columnspan=3)
            local_row_counter += 1

    def autofill_data_2(self):
        person = self.user_list_box_2.get()
        for x in self.data.existing_data:
            if x['vorname']==person:
                person_data = x
                break
        person_data = {
            key + "_2" :value 
            for key,value in person_data.items()
            }
        for key in self.form_display_2:
            self.entries_2[key].delete(0,'end')
            self.entries_2[key].insert(0,person_data[key])
        self.sex_var_2.set(person_data['sex_2'])

    def lets_dance(self):
        if self.dance_var.get():
            self.user2_frame.grid(column=0,row=1)
            self.frm_submitButton.grid(column=0,row=2,columnspan=4)
        else:
            self.user2_frame.grid_forget()
            self.frm_submitButton.grid(column=0,row=1,columnspan=4)