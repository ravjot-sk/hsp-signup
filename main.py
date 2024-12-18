import datagui_module as datagui
import submission_module as submitter
#this function is called when the user clicks on submit button


#Setting continue flag to true clicks on the continue button after filling user data
submitter.continue_flag = True

#Setting final flag to true clicks on the cost based final booking button
submitter.final_button_flag= False

root = datagui.tk.Tk()
root.title("User Input Form")

#Force tkinter window to be the topmost window and disable this 
root.attributes("-topmost", True)
root.bind("<FocusIn>",lambda e: root.attributes("-topmost",False))


submit = submitter.submissionHandling(root)

root.mainloop()
