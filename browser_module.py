#webpage handling using selenium for  form submission

import time
import re
from selenium import webdriver #importing webdriver
from selenium.webdriver.common.by import By #to locate elements
from selenium.webdriver.support.ui import Select, WebDriverWait #to get select objects
from selenium.webdriver.support import expected_conditions as EC #for condition fulfillment
from selenium.common.exceptions import NoSuchElementException, TimeoutException #exception handling
from selenium_stealth import stealth


class webpageHandling:
    #initialise selenium to use Chrome
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)

        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        #flag set to true if we want to check for registration time and wait. set to false if we want to keep refreshing until the button appears
        self.timeflag = True


    #method returns registration time in case timeflag=true and book button not present. else it returns none once the book button is clicked

    def open_webpage(self,url,course_number):
        self.driver.get(url)
        wait = WebDriverWait(self.driver,10)
        our_row = f"//tr[td[@class='bs_sknr' and text()='{course_number}']]" #html element of our required row
        
        while True:
            try:
                target_row=wait.until(EC.visibility_of_element_located((By.XPATH,our_row)))
                booking_button = target_row.find_element(By.CSS_SELECTOR, "input.bs_btn_buchen")
                break
            except NoSuchElementException:
                #if time flag is set true, then check for the registration time and return that
                if self.timeflag:
                    start_time_data = target_row.find_element(By.CSS_SELECTOR,"span.bs_btn_autostart").text
                    match = re.search(r"(\d{2})\.(\d{2})\.,\s(\d{2}):(\d{2})", start_time_data)
                    return match
                
                #if time flag is false, keep refreshing every 5 seconds until the button appears
                else:
                    print("Button not found, refreshing...")
                    self.driver.refresh()
                    time.sleep(5) 

        booking_button.click()
        #need to switch to newly opened tab now
        all_windows = self.driver.window_handles
        new_tab = all_windows[-1]  # Assuming the new tab is the last one opened
        self.driver.switch_to.window(new_tab) 
        return None

    #method to fill the form with user1 data
    def fill_form(self,user_data):
        self.emailopt = user_data['email']
        wait = WebDriverWait(self.driver,10)
        gender_Button=wait.until(EC.visibility_of_element_located((By.XPATH,f"//input[@name='sex' and @value='{user_data['sex']}']")))
        gender_Button.click()
        status_Input= self.driver.find_element(By.XPATH,"//select[@name='statusorig']")

        #only selects the student of wwu option. needs to be changed to allow for more status options
        select = Select(status_Input)
        select.select_by_value('S-WWU')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='matnr']")))

        for x in user_data:
            self.driver.find_element(By.XPATH,f"//input[@name='{x}']").send_keys(user_data[x])

        declaration_Check = self.driver.find_element(By.XPATH,"//input[@name='tnbed']")
        declaration_Check.click()

    #method to fill form with user2 data
    def fill_form_user2(self,user_data):
        wait = WebDriverWait(self.driver,10)
        gender_Button = self.driver.find_element(By.XPATH,f"//input[@name='sex_2' and @value='{user_data['sex_2']}']")
        gender_Button.click()
        status_Input= self.driver.find_element(By.XPATH,"//select[@name='statusorig_2']")
        select = Select(status_Input)

        #only selects the student of wwu option. needs to be changed to allow for more status options
        select.select_by_value('S-WWU')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='matnr_2']")))
        for x in user_data:
            self.driver.find_element(By.XPATH,f"//input[@name='{x}']").send_keys(user_data[x])

    #method to click on the continue button after filling of form
    def continue_button(self):
        wait = WebDriverWait(self.driver, 10)
        continue_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='bs_submit']")))
        continue_Button.click()
    
    #method to click on the final submit button 
    def final_button(self):
        wait = WebDriverWait(self.driver,10)
        fee_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='kostenpflichtig buchen']")))
        fee_button.click()

    #method to deal with the case when webpage asks for email confirmation
    def optional_email(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            optional_field = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[starts-with(@name,'email_check')]")))
        except TimeoutException:
            return
        else:
            optional_field.send_keys(self.emailopt)

    