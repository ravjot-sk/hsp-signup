#data entry and retrieval from user_data.json file
import os 
import json

class user_data:
    #important variables:
            #data_file: name of the file containing user details
            #existing_data: data loaded from the file
    def __init__(self) -> None:
        self.data_file = "user_data.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                self.existing_data= json.load(file)
        else:
            self.existing_data = []
    
    def save_data(self,new_person):
        i=0
        for index,value in enumerate(self.existing_data):
            if value['vorname']==new_person['vorname']:
                self.existing_data[index] = new_person
                i=1
                break
        if i==0:
            self.existing_data.append(new_person)
        with open(self.data_file, "w") as file:
            json.dump(self.existing_data, file)