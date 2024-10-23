import time
import datetime
import datagui_module as datagui
import browser_module as browser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datagui_module import tk
from datagui_module import ttk
#this function is called when the user clicks on submit button


def go_webpage():
    
    course_time = webstuff.openWebpage(gui.url.get(),gui.course_number.get()) #open url and click on the button for course number. if there is no button, it returns the text for the date and time
    if course_time:
        #print(f"{course_time.group(1)} {course_time.group(2)} {course_time.group(3)} {course_time.group(4)}")
        day = int(course_time.group(1))
        month= int(course_time.group(2))
        hour = int(course_time.group(3))
        minute = int(course_time.group(4))
        year = datetime.datetime.now().year
        registration = datetime.datetime(year,month,day,hour,minute)
        return registration
    webstuff.fillForm(gui.getData()) #fills in the form appearing on the new page
    webstuff.continueButton() #clicks on the continue button as soon as it is available
    webstuff.optionalEmail() #if email is asked again, fill it out
    #webstuff.finalButton() #FINAL BUTTON

def go_webpage_withflag():
    print("\nrunning without flag\n")
    webstuff.timeflag = False
    go_webpage()

def countdown_window(new_window,time_label,target_time):
    now = datetime.datetime.now()
    diff = target_time - now
    #print(f"\n{diff}\n")
    if diff.total_seconds() > 1:
     # Format the time difference
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Set the formatted remaining time to the StringVar
        time_label.config(text=f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}")
        new_window.after(1000,lambda: countdown_window(new_window,time_label,target_time))
    else:
        new_window.destroy()
    
def go_back(window,scheduler):
    window.destroy()
    scheduler.shutdown()
    root.deiconify()

def auxillary():
    root.withdraw()
    actual_time = go_webpage()
    if actual_time:
        target_time = actual_time - datetime.timedelta(seconds=30)
        #target_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
        #print(target_time)
        scheduler = BackgroundScheduler()
        scheduler.add_job(go_webpage_withflag,trigger=DateTrigger(run_date=target_time))
        scheduler.start()
        #print("\n Scheduled")
        new_window = tk.Toplevel(root)
        new_window.title("Countdown")
        frm2 = ttk.Frame(new_window,padding=10)
        frm2.grid()
        
        ttk.Label(frm2,text=f"Registration opens at{actual_time}. Program will start checking in").grid(row=0,column=0)
        time_label=ttk.Label(frm2,text="test")
        time_label.grid(row=1,column=0)
        quit_button = tk.Button(frm2,text="Quit", command=dismiss)
        quit_button.grid(row=2,column=1)
        cancel_button = tk.Button(frm2, text="Cancel", command = lambda: go_back(new_window,scheduler))
        cancel_button.grid(row =2, column=0)
        #print("new window created")
        countdown_window(new_window,time_label,target_time)
        #time.sleep(3)
        
        

def dismiss():
    root.destroy()
    webstuff.driver.close()


root = datagui.tk.Tk()

#Force tkinter window to be the topmost window and disable this 
root.attributes("-topmost", True)

root.bind("<FocusIn>",lambda e: root.attributes("-topmost",False))

#root.after(3000, lambda: root.attributes("-topmost", False))

gui = datagui.gui_setup(root) #sets up the gui for user data
webstuff = browser.webpage_handling() #sets up the browser

gui.submit_button.config(command = auxillary) #binds the submit button of gui to sending data to browser
root.protocol("WM_DELETE_WINDOW", dismiss) #calls function to close root and selenium

root.mainloop()
