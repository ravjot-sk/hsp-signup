import datagui_module as datagui
import browser_module as browser

def go_webpage():
    webstuff.openWebpage(gui.url.get(),gui.course_number.get())
    webstuff.fillForm(gui.getData())

root = datagui.tk.Tk()
users = datagui.user_data()
gui = datagui.gui_setup(root,users)
webstuff = browser.webpage_handling()

gui.submit_button.config(command = go_webpage)
root.mainloop()
