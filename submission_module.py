#links the browser module and datagui_module to submit user data

import datetime
import datagui_module as datagui
import browser_module as browser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

continue_flag=False
final_button_flag = False


""" class countdownWindow:
    def __init__(self,registration_time):
        self.window = tk.Toplevel(root)
        self.target_time = registration_time - datetime.timedelta(seconds=30)
        self.window.title("Countdown")
        frm2 = ttk.Frame(self.window,padding=10)
        frm2.grid()
        
        ttk.Label(frm2,text=f"Registration opens at{registration_time}. Program will start checking in").grid(row=0,column=0)
        self.time_label=ttk.Label(frm2,text="")
        self.time_label.grid(row=1,column=0)
        self.quit_button = tk.Button(frm2,text="Quit")
        self.quit_button.grid(row=2,column=1)
        self.cancel_button = tk.Button(frm2, text="Cancel")
        self.cancel_button.grid(row =2, column=0)

    
    def countdown_window(self):
        now = datetime.datetime.now()
        diff = self.target_time - now
        if diff.total_seconds() > 1:
            days = diff.days
            hours, remainder = divmod(diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.window.after(1000,lambda: self.countdown_window())
        else:
            self.window.destroy()
 """

class submissionHandling:
    def __init__(self,root):
        self.gui = datagui.guiSetup(root) #sets up the gui for user data
        self.root= root
        self.gui.submit_button.config(command = self.auxillary) #binds the submit button of gui to sending data to browser
        self.webstuff = browser.webpageHandling()
        self.root.protocol("WM_DELETE_WINDOW", self.dismiss) #calls function to close root and selenium

    def dismiss(self):
        self.root.destroy()
        self.webstuff.driver.close()

    def auxillary(self):
        self.root.withdraw()
        registration_time = self.go_webpage()
        if registration_time:
            target_time = registration_time - datetime.timedelta(seconds=30)
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.go_webpage_withflag,trigger=DateTrigger(run_date=target_time))
            scheduler.start()

            countdown = datagui.countdownWindow(self.root,registration_time)
            countdown.quit_button.config(command=self.dismiss)
            countdown.cancel_button.config(command = lambda: self.go_back(countdown.window,scheduler))
            countdown.countdown_window()

    def go_webpage(self):
        course_time = self.webstuff.open_webpage(self.gui.url.get(),self.gui.course_number.get())
        if course_time:
            day, month, hour, minute = map(int, course_time.groups())
            year = datetime.datetime.now().year
            registration = datetime.datetime(year,month,day,hour,minute)
            return registration
        
        self.webstuff.fill_form(self.gui.get_data())
        if self.gui.user2_flag.get():
            self.webstuff.fill_form_user2(self.gui.get_data_user2())
        
        if continue_flag:    
            self.webstuff.continue_button() #clicks on the continue button as soon as it is available
            self.webstuff.optional_email() #if email is asked again, fill it out
            if final_button_flag:
                self.webstuff.final_button() #FINAL BUTTON

    def go_webpage_withflag(self):
        self.webstuff.timeflag = False
        self.go_webpage()
    
    def go_back(self,window,scheduler):
        window.destroy()
        scheduler.shutdown()
        self.root.deiconify()
