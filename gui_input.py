import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os 
import json

data_file = "user_data.json"

keys = ["vorname","name","strasse","ort","geburtsdatum","email","telefon","matnr","sex","iban"]

form_display = {"vorname" : "First Name", "name": "Last Name", "strasse": "Street and Nr", "ort" : "PLZ and City", "geburtsdatum": "Birthday(dd.mm.yyyy)", "email": "Email", "telefon": "Telephone", "matnr": "Matrikel Nummer", "sex": "Sex(M/W/D/X)", "iban" : "IBAN"}


# Function to get the input and display it
def get_input():
    user_data ={}
    for x in keys:
        user_data[x]=entries[x].get()

    if all(user_data.values()):
        old_data.append(user_data)
        save_data(old_data)
        messagebox.showinfo("Saved", f"Your data has been saved!")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields")

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return []

def autofill_data(person):
    for users in old_data:
        if users['vorname']==person:
            data = users
    for x in keys:
        entries[x].delete(0,'end')
        entries[x].insert(0,data[x])

# Create the main window
root = tk.Tk()
root.title("User Input Form")

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm,text="Existing users: ").grid(column=0,row=0)
user_data_var = tk.StringVar()
user_data_combo = ttk.Combobox(frm,textvariable=user_data_var)
user_data_combo.grid(column=1,row=0)
user_data_combo.state(["readonly"])
old_data = load_data()

if old_data:
    users = [person['vorname'] for person in old_data]
    user_data_combo['values']= users

user_data_combo.bind("<<ComboboxSelected>>", lambda event: autofill_data(user_data_combo.get()))

entries = {}
i=1
for x in keys:
    ttk.Label(frm,text=form_display[x]).grid(column=0,row=i)
    entries[x] = ttk.Entry(frm,width=30)
    entries[x].grid(column=1,row=i)
    i=i+1



# Create a button to submit the input
save_button = tk.Button(frm, text="Save Data", command=get_input)
save_button.grid(column=0,row=i,pady=10)

submit_button = tk.Button(frm,text="Submit Form")
submit_button.grid(column=1,row=i, pady=10) 
# Run the Tkinter event loop
root.mainloop()


    #test to see all data are taken
"""if user_data["vorname"]:
        lines=[]
        for x in keys:
            lines.append(user_data[x])
        #lines = [firstName, lastName, streetNum, pinOrt,bday,email,telephone]
        #messagebox.showinfo("Input", f"Hello, {firstName}!")
        messagebox.showinfo('Text', '\n'.join(lines))
    else:
        messagebox.showwarning("Input", "Please enter your first name")"""
#form_data = {"vorname" : None, "name": None, "strasse": None, "ort" : None, "geburtsdatum": None, "email": None, "telefon": None, "matnr": None, "sex": None, "iban" : None}

"""firstName = entry_firstName.get()  # Get the value from the entry widget
    lastName = entry_lastName.get()
    streetNum = entry_streetNum.get()
    pinOrt = entry_pinOrt.get()
    bday = entry_bday.get()
    email = entry_email.get()
    telephone = entry_telephone.get()"""

""" ttk.Label(frm, text="Vorname:").grid(column=0, row=0)
entry_firstName = ttk.Entry(frm, width=30)  # Create the Entry widget
entry_firstName.grid(column=1, row=0)  # Place the Entry widget in the grid

ttk.Label(frm, text="Familienname:").grid(column=0, row=1)
entry_lastName = ttk.Entry(frm,width=30)
entry_lastName.grid(column=1,row=1)

ttk.Label(frm, text="Strasse  Nr:").grid(column=0, row=2)
entry_streetNum = ttk.Entry(frm,width=30)
entry_streetNum.grid(column=1,row=2)

ttk.Label(frm, text="PLZ Ort:").grid(column=0, row=3)
entry_pinOrt = ttk.Entry(frm,width=30)
entry_pinOrt.grid(column=1,row=3)

ttk.Label(frm, text="Geburtsdatum(tt.mm.yyyy):").grid(column=0, row=4)
entry_bday = ttk.Entry(frm,width=30)
entry_bday.grid(column=1,row=4)

ttk.Label(frm, text="Email:").grid(column=0, row=5)
entry_email = ttk.Entry(frm,width=30)
entry_email.grid(column=1,row=5)

ttk.Label(frm, text="Telefon:").grid(column=0, row=6)
entry_telephone = ttk.Entry(frm,width=30)
entry_telephone.grid(column=1,row=6) """


