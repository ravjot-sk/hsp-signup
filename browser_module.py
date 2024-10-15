import time
import re
from selenium import webdriver #importing webdriver
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By #to locate elements
from selenium.webdriver.support.ui import Select, WebDriverWait #to get select objects
from selenium.webdriver.support import expected_conditions as EC #for condition fulfillment
from selenium.common.exceptions import NoSuchElementException, TimeoutException #exception handling
from selenium.webdriver.firefox.service import Service

class webpage_handling:
    def __init__(self) -> None:
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        options.set_preference("general.useragent.override", userAgent)
        self.driver = webdriver.Firefox(options=options)
        #geckodriver_path = "./geckodriver"
        #service = Service(geckodriver_path)
        #self.driver = webdriver.Firefox(options=options,service=service)

    def openWebpage(self,url,course_number):
        self.driver.get(url)
        wait = WebDriverWait(self.driver,10)
        our_row = f"//tr[td[@class='bs_sknr' and text()='{course_number}']]"
        
        #need to add if else here in case button not found
        while True:
            try:
                target_row=wait.until(EC.visibility_of_element_located((By.XPATH,our_row)))
                button_path = f"{our_row}//input[@class='bs_btn_buchen']"
                booking_button = target_row.find_element(By.CSS_SELECTOR, "input.bs_btn_buchen")
                #booking_button = wait.until(EC.presence_of_element_located((By.XPATH,button_path)))
                break
            except NoSuchElementException:
                print("Button not found, refreshing...")
                self.driver.refresh()
                time.sleep(5) 
        #booking_button = target_row.find_element(By.CSS_SELECTOR, "input.bs_btn_buchen")
        booking_button.click()
        original_window = self.driver.current_window_handle
        all_windows = self.driver.window_handles
        new_tab = all_windows[-1]  # Assuming the new tab is the last one opened
        self.driver.switch_to.window(new_tab) 

    def fillForm(self,user_data):
        self.emailopt = user_data['email']
        wait = WebDriverWait(self.driver,10)
        gender_Button=wait.until(EC.visibility_of_element_located((By.XPATH,f"//input[@name='sex' and @value='{user_data['sex']}']")))
        gender_Button.click()
        status_Input= self.driver.find_element(By.XPATH,"//select[@name='statusorig']")
        select = Select(status_Input)
        select.select_by_value('S-WWU')
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='matnr']")))

        for x in user_data:
            self.driver.find_element(By.XPATH,f"//input[@name='{x}']").send_keys(user_data[x])

        declaration_Check = self.driver.find_element(By.XPATH,"//input[@name='tnbed']")
        declaration_Check.click()

    def continueButton(self):
        wait = WebDriverWait(self.driver, 10)
        continue_Button = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='bs_submit']")))
        continue_Button.click()
    
    def finalButton(self):
        wait = WebDriverWait(self.driver,10)
        fee_button = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='kostenpflichtig buchen']")))
        fee_button.click()

    def optionalEmail(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            optional_field = wait.until(EC.visibility_of_element_located((By.XPATH,"//input[starts-with(@name,'email_check')]")))
        except TimeoutException:
            return
        else:
            optional_field.send_keys(self.emailopt)
#start_time_data = target_row.find_element(By.CSS_SELECTOR,"span.bs_btn_autostart").text
#                match = re.search(r"(\d{2}\.\d{2}\.),\s(\d{2}:\d{2})", start_time_data)
#                if match:
#                    date = match.group(1)  # "17.10."
#                    time = match.group(2)  # "19:30"
#                    print(f"Date: {date}, Time: {time}")"""