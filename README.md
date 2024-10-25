# Hochschulsport Münster Signup Script
This script is to automate the sign up process for Uni Münster's Hochschulsports.

## Installation
The script works with Firefox browser and requires Geckodriver to be installed. Other required packages are Selenium and Tkinter.

## Usage
On running the program, you will see the following interface
<img width="560" alt="Screenshot 2024-10-25 at 21 48 25" src="https://github.com/user-attachments/assets/9bbb5c51-5c32-4d6e-873a-394ffa304762">

After entering all the user details, you have the option to save your data. If you decide to save your data, the next time you open the program, you will be able to select users based on the first name from the drop down menu of existing users.

Next thing you need to enter is the url of the course website you are registering for. For example if you want to register for the Salsa course, you need to enter the url of the webpage with the actual course offerings which looks like this
<img width="961" alt="Screenshot 2024-10-25 at 22 01 38" src="https://github.com/user-attachments/assets/ce8fdb68-a59a-4e77-bea1-453de99aa531">

Now from the given course offerings, you need to select the course number you want to register for and enter in the user data interface. Some courses like Salsa require you to sign up in pairs. So in the user data interface, you have the option of selecting a two person course which opens up entry fields to enter the user data of the second person.
<img width="560" alt="Screenshot 2024-10-25 at 22 06 29" src="https://github.com/user-attachments/assets/96d29059-dde9-4ad7-8277-60568d992218">

If the course is already available for booking, after pressing the submit button the program should open up a browser window with the course and click on the 'buchen' button and fill out the form with the user(s) details and click the relevant buttons for the final booking.

In case the registration is not yet open, the program shows a countdown timer for the registration to open up and 30 seconds before the start of registration, it opens the webpage and checks for the 'buchen' button by refreshing the page every 5 seconds
