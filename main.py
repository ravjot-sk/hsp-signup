import datagui_module as datagui
import browser_module as browser

#this function is called when the user clicks on submit button
def go_webpage():
    webstuff.openWebpage(gui.url.get(),gui.course_number.get()) #open url and click on the button for course number
    webstuff.fillForm(gui.getData()) #fills in the form appearing on the new page
    webstuff.continueButton() #clicks on the continue button as soon as it is available

root = datagui.tk.Tk()

#Force tkinter window to be the topmost window and disable this 
root.attributes("-topmost", True)

root.bind("<FocusIn>",lambda e: root.attributes("-topmost",False))

#root.after(3000, lambda: root.attributes("-topmost", False))

users = datagui.user_data() #handles the user data stored in file
gui = datagui.gui_setup(root,users) #sets up the gui for user data
webstuff = browser.webpage_handling() #sets up the browser

gui.submit_button.config(command = go_webpage) #binds the submit button of gui to sending data to browser
root.mainloop()
