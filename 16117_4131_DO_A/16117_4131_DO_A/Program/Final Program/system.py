version = '1.0'
#                               Created by Alex Dowsett                                
#--------------------------------------------------------------------------------------
#                        CONFIGURATION (READ USER GUIDE FIRST!)                        
first_appointment_time = '07:00' # The time of the first appointment of the day in a 'hh:mm' format.
last_appointment_time = '20:00' # The time of the last appointment of the day in a 'hh:mm' format.
appointment_intervals = 15 # Time in minutes for each appointment slot. If this value is changed, keep it as a factor of 15.
working_days = [1, 2, 3, 4, 5, 6] # Where Monday = 1, Tuesday = 2... Sunday = 7. For example: If the working days are Monday, Wednesday and Sunday then workings_days = [1, 3, 7].
bg_colour = '#E7E8EA' # Blackground colour in hexadecimal.                            
text_colour = '#343038' # Text colour in hexadecimal.                             
primary_colour = '#A09D9C' # 1st colour in hexadecimal.                                 
secondary_colour = '#343038' # 2nd colour in hexadecimal.                               
primary_font = 'Helvetica' # A font to be used primarily.                            
secondary_font = 'Courier' # A font to be used secondarily.                            
tertiary_font = 'Trebuchet MS' # A font to be used tertiarily.
database_file = 'bookings.db' # Name of database file.
main_window_zoomed = True # If 'True' the main window will be zoomed on startup.       
main_window_width_relative_size = 0.95 # The percentage of the width that the main window will fill on startup. Only applies if main_window_zoomed = False.
main_window_height_relative_size = 0.90 # The percentage of the height that the main window will fill on startup. Only applies if main_window_zoomed = False.
#
#--------------------------------------------------------------------------------------

# IMPORTS
import tkinter as tk # Imports the tkinter module. Any functions from this module will be start with a 'tk.' to show what module it came from.
import tkinter.ttk as ttk # Imports the tkk part of the tkinter module. Any functions from this module will be start with a 'ttk.' to show what module it came from.
from tkinter import messagebox # Imports tkinter messageboxes seperately otherwise they will encounter errors when being used outside of Python IDLE.
import sqlite3 # Imports the sqlite3 module. This module is used to communicate with the datebase file (datebase.db).
import time # Imports the time module.
import datetime # Imports the datetime module.

# VARIABLES
root = tk.Tk() # Defines the variable 'root' as a tkinter window.
screen_width = root.winfo_screenwidth() # Defines a new integer that holds the width of the screen in pixels.
screen_height = root.winfo_screenheight() # Defines a new integer that holds the height of the screen in pixels.
main_window_width = round(screen_width * main_window_width_relative_size) # Calculates the inital width of the main window in pixels.
main_window_height = round(screen_height * main_window_height_relative_size) # Calculates the inital height of the main window in pixels.
first_appointment_time = int(first_appointment_time.split(':')[0]) * 60 + int(first_appointment_time.split(':')[1]) # This calculation converts the time hh:mm to minutes from midnight.
last_appointment_time = int(last_appointment_time.split(':')[0]) * 60 + int(last_appointment_time.split(':')[1]) # This calculation converts the time hh:mm to minutes from midnight.

# GLOBAL FUNCTIONS
def main():
    '''This function is run when the program starts.'''
    login_window = Login(root) # Creates an instance of the class Login with the tkinter window 'root' as a parameter.
    root.mainloop() # Wait until the tkinter window 'root' is closed.
    
def add_date_suffix(day):
    '''This function adds the corresponding date suffix to the end of a number.'''
    day = int(day) # Converts variable to integer.
    suffix = '' # Defines a string called 'suffix'.
    if 4 <= day <= 20 or 24 <= day <= 30: # If variable 'day' in the stated range.
        suffix = 'th' # Change 'suffix' value.
    elif day in {1, 21, 31}: # If variable 'day' is one of the following values.
        suffix = 'st' # Change 'suffix' value.
    elif day in {2, 22}: # If variable 'day' is one of the following values.
        suffix = 'nd' # Change 'suffix' value.
    elif day in {3, 23}: # If variable 'day' is one of the following values.
        suffix = 'rd' # Change 'suffix' value.
    return str(day) + suffix # Return 'day' followed by the suffix as a string value.

def log(statement):
    '''This function simply prints a string with the date and time as a prefix.'''
    print('[{}] {}'.format(time.strftime('%d/%m/%y|%H:%M:%S'), statement)) # Prints message to the console.

def db_open():
    '''This function opens the connection and cursor to the database.'''
    global c, conn # Makes these variable global and therefore accessible in all functions.
    conn = sqlite3.connect('db/' + database_file) # Starts a connection to the database named 'bookings.db' within the /db/ folder. 
    c = conn.cursor() # Defines a cursor to interact with the database.

def db_close():
    '''This function closes the connection and cursor to the database.'''
    c.close() # Stops interaction.
    conn.close() # Closes connection with database.

    
#======================================================================================
#                                        LOGIN WINDOW                                  
#======================================================================================
class Login: # Defines a class that will represent the login window.
    '''This class is a login window for security. A username and password is required to access the system.''' # Class Information.
    def __init__(self, master): # Initializes this function when an instance of the class is created.
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Defines the varaible master as an attribute to self (main_window).
        self.id_var = tk.StringVar() # Defines a tkinter string variable that stores the staff ID as an attribute of self (main_window).
        self.p_var = tk.StringVar() # Defines a tkinter string variable that stores the password as an attribute of self (main_window).
        
    ### TKINTER WINDOW CONFIG
        self.master.title('Essensuals Booking System Login (Version {})'.format(version)) # Sets title of the window.
        self.master.geometry('540x360+{}+{}'.format(((screen_width-540)//2), ((screen_height-360)//2)))  # Sets window geometry and centers the window.
        self.master.resizable(False, False) # Disables resizing for the window.
        self.master.wm_iconbitmap('resources/icon.ico') # Sets window icon.
        self.master.config(bg=bg_colour) # Sets background colour of window.
        
    ### TKINTER LABELS
        self.header_label = tk.Label(self.master, bg=primary_colour) # Defines a label.
        self.header_label.place(x=0, y=0, w=540, h=60) # Sets the geometry of the label.
        
        self.footer_label = tk.Label(self.master, bg=secondary_colour, fg='#FFFFFF', text='Programmed by Alex Dowsett', font=(primary_font,  7)) # Defines a label.
        self.footer_label.place(x=0, y=325, w=540, h=35) # Sets the geometry of the label.
        
        self.title_image = tk.PhotoImage(file='resources/title_small.png') # Defines a tkinter variable that contains an image. 
        self.title_label = tk.Label(self.master, bg=primary_colour, image=self.title_image) # Defines a label that will contain the image.
        self.title_label.place(x=240, y=5, w=281, h=50) # Sets the geometry of the label.
        self.title_label.image = self.title_image # Sets the label's image to the tkinter image 'title_image'.

        self.id_label = tk.Label(self.master, text='Staff ID:', bg=bg_colour, fg=text_colour, font=primary_font) # Defines a label.
        self.id_label.place(x=100, y=120, w=80, h=25) # Sets the geometry of the label.
        
        self.p_label = tk.Label(self.master, text='Password:', bg=bg_colour, fg=text_colour, font=primary_font) # Defines a label.
        self.p_label.place(x=100, y=160, w=80, h=25) # Sets the geometry of the label.

    ### TKINTER ENTRY BOXES
        self.id_entry = tk.Entry(self.master, textvariable=self.id_var, fg=text_colour, font=secondary_font) # Defines an entry box that allows the user to enter their staff ID. The value entered is stored in the variable created earlier.
        self.id_entry.place(x=200, y=120, w=200, h=25) # Sets the entry box's geometry.
        self.id_entry.bind('<Return>', lambda event: self.p_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the password entry.
        self.id_entry.bind('<Escape>', lambda event: self.master.focus()) # When pressing the escape key while this widget is focued, will force focus off this widget.
        self.id_entry.focus() # Focuses this widget so the user can type their ID without having to click the entry box first.

        self.p_entry = tk.Entry(self.master, textvariable=self.p_var, fg=text_colour, font=secondary_font, show='*')# Defines an entry box that allows the user to enter their password. The value entered is stored in the variable created earlier. The password is also hidden from view by showing ever character as '*'s.                                                        
        self.p_entry.place(x=200, y=160, w=200, h=25) # Sets the entry box's geometry.
        self.p_entry.bind('<Return>', lambda event: self.log_in()) # When pressing the return key while this widget is focused, will run the 'log_in' function. 
        self.p_entry.bind('<Escape>', lambda event: self.master.focus()) # When pressing the escape key while this widget is focued, will force focus off this widget.
        
    ### TKINTER BUTTONS
        self.login_button = tk.Button(self.master, text='Log In', command=self.log_in, bg=bg_colour, fg=text_colour, font=primary_font) # Defines a button which when pressed, runs the function 'log_in'.
        self.login_button.place(x=320, y=200, w=80, h=30) # Sets the geometry of the button.
        self.login_button.bind('<Return>', lambda event: self.log_in()) # When pressing the return key while this widget is focused, will run the 'log_in' function.
        self.login_button.bind('<Escape>', lambda event: self.master.focus()) # When pressing the escape key while this widget is focued, will force focus off this widget.

        self.help_button = tk.Label(self.master, text='Do not know your details?', bg=bg_colour, fg=text_colour, font=(primary_font, 12)) # Defines a label that contains text coloured 'text_colour' in the font 'font_1' sized 12.
        self.help_button.place(x=100, y=202, w=180, h=25) # Sets the geometry of the label.
        self.help_button.bind('<Button-1>', lambda event: messagebox.showinfo('Information: Login Help', 'Ask your manager for your login details\nor for first time use, read the User Guide\nor view the "README.txt" text file.')) # Makes the label clickable, that when clicked runs the function 'info'.
        self.help_button.bind('<Enter>', lambda event: self.help_button.configure(font=(primary_font, 12, 'underline'))) # When the mouse cursor is hovering above this label, the text becomes underlined to indicate it's clickable.
        self.help_button.bind('<Leave>', lambda event: self.help_button.configure(font=(primary_font, 12))) # When the mouse cursor is no longer hovering above this label, the text is no longer underlined.        

    ### GENERATES A DATABASE IF NONE EXISTS
        db_open() # Creates connection and interaction to the database.
        c.execute('CREATE TABLE IF NOT EXISTS Staff(StaffID INTEGER PRIMARY KEY, FirstName VARCHAR(255) NOT NULL, LastName VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL, IsAdmin BIT DEFAULT 0)') # Creates Staff table in the database.
        conn.commit() # Processes the SQL command.
        c.execute('SELECT COUNT(*) FROM Staff') # Retrieves the amount of records in the Staff table.
        
        if c.fetchone()[0] == 0: # If the Staff table is empty. (In other words if the table has just been created). 
            log('Database not found. Creating a new one.') # Logs a message to the console to record that a new database was created.
            c.execute('INSERT INTO Staff(FirstName, LastName, Password, IsAdmin) VALUES("Jim", "Shaw", "ess19", 1)') # Inserts a temporary admin login into the staff table for the admins in order to access the program. 
            c.execute('CREATE TABLE Clients(ClientID INTEGER PRIMARY KEY, FirstName VARCHAR(255) NOT NULL, LastName VARCHAR(255) NOT NULL, Mobile VARCHAR(255), Home VARCHAR(255))') # Creates Client table in the database.
            c.execute('CREATE TABLE Haircuts(HaircutID INTEGER PRIMARY KEY, Haircut VARCHAR(255) NOT NULL, Price REAL NOT NULL, EstimatedTime INTEGER)') # Creates Haircut table in the database.
            c.execute('CREATE TABLE Hairdressers(StaffID INTEGER NOT NULL, Rate INTEGER DEFAULT 100)') # Creates Hairdressers table in the database.
            c.execute('CREATE TABLE Appointments(AppointmentID INTEGER PRIMARY KEY, StaffID INTEGER NOT NULL, ClientID INTEGER NOT NULL, HaircutID INTEGER NOT NULL, StartTime INTEGER NOT NULL, Duration INTEGER NOT NULL, Date VARCHAR(255) NOT NULL, AmountPaid REAL)') # Creates Appointment table in the database.   
            conn.commit() # Processes the SQL commands.
        db_close() # Closes connection and interaction to the database.
        
### 'LOGIN' CLASS FUNCTIONS
    def log_in(self): # Defines a function called 'login' (This function performs the login process).
        '''The function ran when the user has inputted a Staff ID and password and then pressed enter or clicked the log in button. The function compares the inputted values to the ones in the database and then performs accordingly.'''
        self.id = self.id_var.get() # Retrieves the value in the tkinter variable linked to the 'staffID' entry box, and stores it as 'users_ID'.
        self.p = self.p_var.get() # Retrieves the value in the tkinter variable linked to the 'password' entry box, and stores it as 'p'.
        if self.id == '' or self.p == '': # Checks that neither entry boxes were empty.
            messagebox.showerror('Error: Empty field(s)', 'Please ensure you have entered both your Staff ID and password.') # If one of them was, an tkinter error window is displayed informing the user on their mistake.
            
        else:
            db_open() # Opens the connection and interaction to the database
            c.execute('SELECT * FROM Staff WHERE StaffID=?', (self.id,)) # Retrieves the staff's details of the staff with ID 'users_ID'.
            global user
            user = list(c.fetchone()) # Fetches the result.
            db_close() # Closes connection and interaction to the database.
            
            if not user == None and self.p == user[3]: # Condition: If the staff ID is within the database and the password matches.    
                log('{} {} logged in.'.format(user[1], user[2])) # Log the following string.
                global main_window # Defines the main window as global so it can be used outside this function.
                main_window = Main(root) # Creates a new instance of the class 'Main' called 'main_window'.
                root.mainloop() # Once the instance (main window) is created, stop until the window is closed. Then the program will run the next line of code.
                return # End function early.
            
            else:
                messagebox.showerror('Error: Incorrect login details', 'Your ID or password is incorrect. Please check your details and try again.') # Displays a Tkinter error window informing the user the login details are incorrect.
                
        self.id_entry.delete(0, tk.END) # Clears the 'StaffID' entry box.
        self.p_entry.delete(0, tk.END) # Clears the 'password' entry box.
        self.id_entry.focus() # Refocuses the 'StaffID' entry box.

        
#======================================================================================
#                                        MAIN WINDOW  
#======================================================================================
class Main(): # Defines a class that will be used for the main window.
    '''The main window of the program that contains the booking system.'''
    def __init__(self, master): # Initializes the following code when an instance of a class is created.
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Make the variable 'master' an attribute to the Main class.
        self.width = main_window_width # Make the variable an attribute to the Main class.
        self.height = main_window_height # Make the variable an attribute to the Main class.
        self.update = False # Define a new attribute.

    ### TKINTER WINDOW CONFIG
        for widget in self.master.winfo_children(): # For all widgets in the tkinter window.
            widget.destroy() # Destroy it.
            
        self.master.title('Essensuals Booking System (Version {})'.format(version)) # Sets title.
        self.master.geometry('{}x{}+0+10'.format(self.width, self.height)) # Sets windows geometry.
        self.master.resizable(True, True) # Sets the window so it cannot be resized.
        self.master.bind('<Configure>', self.on_resize) # Bind the function 'on_resize' to trigger whenever the windows geometry is altered.
        self.master.bind('<Left>', lambda event: self.move_day(False)) # Bind the function 'move_day' with parameter False when the left arrow key is pressed.
        self.master.bind('<Right>', lambda event: self.move_day(True)) # Bind the function 'move_day' with parameter True when the right arrow key is pressed.

    ### TKINTER LABELS
        self.header_label = tk.Label(self.master, bg=primary_colour) # Defines the header label which is coloured 'primary_colour'.
        self.header_label.place(x=0, y=0, w=screen_width, h=80) # Sets the geometry of the header.

        self.footer_label = tk.Label(self.master, bg=secondary_colour, fg='#FFFFFF', text='Programmed by Alex Dowsett', font=(primary_colour+' 7')) # Defines the footer which is coloured 'colour_2'. It also adds some centered, white text in the font 'font_1'.
        self.footer_label.place(x=0, h=40) # Sets the geometry of the footer label.

        self.time_label = tk.Label(self.master, bg=primary_colour, fg=bg_colour, font=(tertiary_font, 20, 'bold'), anchor='w') # Defines the following Tkinter label.
        self.time_label.place(x=235,y=5,w=120, h=40) # Sets the geometry of the label.
        
        self.date_label = tk.Label(self.master, bg=primary_colour, fg=bg_colour, font=(tertiary_font, 20, 'bold'), anchor='e') # Defines the following Tkinter label.
        self.date_label.place(x=100,y=5,w=135, h=40) # Sets the geometry of the label.

        self.welcome_label = tk.Label(self.master, bg=primary_colour, fg=bg_colour, text='Welcome {}.'.format(user[1]), font=(tertiary_font, 20, 'bold'), anchor='w') # Defines the following tkinter label.
        self.welcome_label.place(x=100, y=35, w=400, h=40) # Sets the geometry of the label.
        
        self.week_label = tk.Label(self.master, bg=bg_colour, fg=text_colour, font=(tertiary_font, 26, 'bold')) # Defines the following Tkinter label.
        self.week_label.place(x=0, y=80) # Sets the geometry of the label.
        
        self.title_image = tk.PhotoImage(file='resources/title_large.png') # Imports a photo file as an attribute named 'title_large'.
        self.title_label = tk.Label(self.master, bg=primary_colour, image=self.title_image) # Defines a label that will contain the image stored in the attribute 'title_large'.
        self.title_label.place(y=6, w=382, h=68) # Sets the geometry of the label.
        self.title_label.image = self.title_image # Sets the image in 'title_large' to an attribute of the new label.
        
    ### TKINTER BUTTONS
        self.logout_button = tk.Label(self.master, bg=bg_colour, fg=primary_colour, text='Log Out', font=(primary_font, 12)) # Defines the following Tkinter button.
        self.logout_button.place(y=80, w=80, h=30)
        self.logout_button.bind('<Button-1>', lambda event: self.log_out()) # Makes the label clickable, that when clicked runs the function 'info'.
        self.logout_button.bind('<Enter>', lambda event: self.logout_button.configure(font=(primary_font, 12, 'underline'))) # When the mouse cursor is hovering above this label, the text becomes underlined to indicate it's clickable.
        self.logout_button.bind('<Leave>', lambda event: self.logout_button.configure(font=(primary_font, 12))) # When the mouse cursor is no longer hovering above this label, the text is reverted to its normal state.

        self.settings_light_image = tk.PhotoImage(file='resources/settings_light.png') # Imports a photo file as an attribute named 'settings_light'.
        self.settings_dark_image = tk.PhotoImage(file='resources/settings_dark.png') # Imports a photo file as an attribute named 'settings_dark'.
        self.settings_button = tk.Label(self.master, bg=primary_colour, image=self.settings_light_image) # Defines a label that contains the image stored in the variable 'settings_light'.
        self.settings_button.place(x=15, y=15, w=50, h=50) # Sets the geometry of the label.
        self.settings_button.image = self.settings_light_image # Sets the image in 'settings_light' to an attribute of the label.
        self.settings_button.bind('<Button-1>', lambda event: self.open_settings_window()) # Makes the label clickable, that when clicked runs the function 'settings'.
        self.settings_button.bind('<Enter>', lambda event: self.on_hover(0)) # When the mouse cursor is hovering above this label, the function 'change_settings_dark' is ran.
        self.settings_button.bind('<Leave>', lambda event: self.on_hover(1)) # When the mouse cursor is no longer hovering above this label, the function 'change_settings_dark' is ran.

        self.arrow_left_light_image = tk.PhotoImage(file='resources/arrow_left_light.png') # Imports a photo file as an attribute named 'title_large'.
        self.arrow_left_dark_image = tk.PhotoImage(file='resources/arrow_left_dark.png') # Imports a photo file as an attribute named 'title_large'.
        self.arrow_left_button = tk.Label(self.master, bg=bg_colour, image=self.arrow_left_dark_image) # Defines a label that will contain the image stored in the attribute 'title_large'.
        self.arrow_left_button.place(y=80, w=70) # Sets the geometry of the label.
        self.arrow_left_button.image = self.arrow_left_dark_image # Sets the image in 'title_large' to an attribute of the new label.
        self.arrow_left_button.bind('<Button-1>', lambda event: self.move_week(False)) # Makes the label clickable, that when clicked runs the function 'settings'.
        self.arrow_left_button.bind('<Enter>', lambda event: self.on_hover(2)) # When the mouse cursor is hovering above this label, the function 'change_settings_dark' is ran.
        self.arrow_left_button.bind('<Leave>', lambda event: self.on_hover(3)) # When the mouse cursor is no longer hovering above this label, the function 'change_settings_dark' is ran.

        self.arrow_right_light_image = tk.PhotoImage(file='resources/arrow_right_light.png') # Imports a photo file as an attribute named 'title_large'.
        self.arrow_right_dark_image = tk.PhotoImage(file='resources/arrow_right_dark.png') # Imports a photo file as an attribute named 'title_large'.
        self.arrow_right_button = tk.Label(self.master, bg=bg_colour, image=self.arrow_right_dark_image) # Defines a label that will contain the image stored in the attribute 'title_large'.
        self.arrow_right_button.place(y=80, w=70) # Sets the geometry of the label.
        self.arrow_right_button.image = self.arrow_right_dark_image # Sets the image in 'title_large' to an attribute of the new label.
        self.arrow_right_button.bind('<Button-1>', lambda event: self.move_week(True)) # Makes the label clickable, that when clicked runs the function 'settings'.
        self.arrow_right_button.bind('<Enter>', lambda event: self.on_hover(4)) # When the mouse cursor is hovering above this label, the function 'change_settings_dark' is ran.
        self.arrow_right_button.bind('<Leave>', lambda event: self.on_hover(5)) # When the mouse cursor is no longer hovering above this label, the function 'change_settings_dark' is ran.

    ### TKINTER STYLE
        # This section of code sets a default style used for tkinter widgets. This style however will only apply for the tabs within the tkinter notebook we will define later on.
        self.style = ttk.Style() # Define the style
        self.style.configure('.', bg=bg_colour, fg=text_colour, font=primary_font) # Adds the font just defined to the style. Also sets the background colour to 'bg_colour'.
        self.current_theme = self.style.theme_use() # Retrieves the current theme being used.
        self.style.theme_settings (self.current_theme, { # Configures the current theme by adding padding to the tabs in the widget 'TNotebook'.
                'TNotebook.Tab': {
                    'configure': {'padding': [5, 10] } } } ) # The padding around the text within the notebook tab (Increases the size of the tabs slightly).
        self.style.theme_use(self.current_theme) # Enforces the new theme that's been configured.
        
        # These 3 lines of code define a variable that contains padding for the tabs in the notebook. Adding this padding to the tabs ensures they take up all the space they are allowed.
        self.padding = [] # Defines an array.
        for i in range(100): # Loops the following code 100 times.
            self.padding.append(' ') # Adds a space character to the array.

    ### CLOCK
        # Starts a recursive function that calls itself every 0.2 seconds. This function checks the displayed time and date against the real time and date and updates the displayed values if neccessary.
        self.time = '' # Defines the time as an empty string so it has to be updated on the first call of the function.
        self.date = '' # Defines the date as an empty string so it has to be updated on the first call of the function.
        self.tick() # Calls the tick function.

    ### CALCULATING THE WORKING DATES
        # This section of code converts the working days of the week to actual dates. These dates are used for the notebook/table tabs and the text above the notebook/table stating what working week it is.
        day_of_the_week = int(time.strftime('%w')) # Retrieves the day of the week it is today. Between 0-6 where 0 is Sunday.
        if day_of_the_week == 0: # If 0.
            day_of_the_week = 7 # Change to 7.
        global working_dates # Defines a variable and makes it global.
        working_dates = [] # Defines the variable as an array.
        for i in range(len(working_days)): # Loop i amount of times, where i is the number of days the company is open in a week.
            working_dates.append(datetime.date.today() + datetime.timedelta(days=(working_days[i] - day_of_the_week))) # Calculates the dates for this working week.

    ### FETCHES HAIRDRESSERS' DETAILS FROM THE DATABASE
        # This section of code fetches all the hairdressers' details from the database.
        db_open()
        c.execute('SELECT StaffID, FirstName, LastName FROM Staff WHERE StaffID IN (SELECT StaffID FROM Hairdressers)') # Retrieve the staff information for all hairdressers.
        self.hairdressers = c.fetchall() # Fetch all records that match the above SQL statement.
        db_close()
        
        # These 3 lines of code convert the list of tuples to a list of lists (2D list).
        for i in range(len(self.hairdressers)): # Loop for each hairdresser.
            self.hairdressers[i] = list(self.hairdressers[i]) # Converts tuple to array/list.
            self.hairdressers[i].append('') # Adds a string value onto the end of the array.
        
            
    ### ENSURES HAIRDRESSER NAMES ARE UNIQUE 
        # Ensures all hairdressers have unique names displayed. If two hairdressers share the same first name then the first letter of their surnames will also be displayed.
        # If their names still clash the next letter will be displayed. In the case their surnames also match it will displayed both their full name. An admin may add a
        # number or other unique identifier to their name if both of the same names being displayed is not suitable.
        for i in range(len(self.hairdressers)): # Loop for each hairdresser.
            surname_clash = [] # Defines an array.
            while not surname_clash == [i]: # Loop until no surname clash.
                surname_clash = [i] # Sets value of variable.
                for j in range(len(self.hairdressers)): # Loop for all hairdressers.
                    if i != j and str(self.hairdressers[i][1]) + str(self.hairdressers[i][3]) == str(self.hairdressers[j][1]) + str(self.hairdressers[j][3]) and self.hairdressers[j][2] != '': # If surname clash and not a clash with self.
                        surname_clash.append(j) # Add index which clashed with.
                if len(surname_clash) != 1: # If clash is not just self.
                    for j in range(len(surname_clash)): # Loop for each clash.
                        self.hairdressers[surname_clash[j]][3] += str(self.hairdressers[surname_clash[j]][2][0]) # Move first character of string to last index (index 3) of array.
                        self.hairdressers[surname_clash[j]][2] = self.hairdressers[surname_clash[j]][2][1:] # Remove first character of string from index 2.
                        
    ### NOTEBOOK/TABLE                  
        self.nb = ttk.Notebook(self.master) # Defines a Tkinter notebook widget.
        self.nb.bind('<Escape>', lambda event: self.master.focus()) # If user presses Escape key the program will unfocus all widgets.
        
    ### MORE VARIABLES
        # Defines variables to be used in the appoinments table.
        self.tabs = [] # Defines an array that will contain the 6 pages (a page for each working day).
        self.lbs = [] # This 2d array will contain the listboxes for each page. We need a listbox for each hairdresser and we need a set of listboxes for each page in the notebook.
        self.names_frame = [] # Defines an array that will contain a frame that will contain the names of the hairdressers. There will be a frame per day.
        self.names = [] # This 2d array will contain the canvases to display the hairdressers' names. We use a canvas instead to display the text vertically to save space. We need a set of canvases for each page.
        self.scrolls = [] # Defines an array that will contain the 6 scroll bars (a scrollbar for each page).
        self.clock_image = tk.PhotoImage(file='resources/clock.png') # Defines a new variable to hold a Tkinter image of 'clock.png'.

        for i in range(len(working_days)): # Loop for all working days in a week.
            self.names.append([]) # Add array to names array.
            self.lbs.append([]) # Add array to list boxes array.
            
        ### TABS
            self.tabs.append(tk.Frame(self.nb)) # Add frame for each working day of the week.
            self.tabs[i].rowconfigure(1, weight=1) # Add a weight to the frame (Takes piority of space over weightless widgets).
            self.tabs[i].bind('<Visibility>', lambda event: [self.on_resize(), self.update_table(), self.master.focus()]) # When the tab is changed in the notebook run the following functions.
            self.nb.add(self.tabs[i]) # Add the tab to the notebook.
            
        ### FRAMES
            # A frame to contain all the canvasses which display the hairdressers' names.
            self.names_frame.append(tk.Frame(self.tabs[i], height=64)) # Adds a frame to contain hairdressers' names inside the tab frame for each working day of the week.
            self.names_frame[i].grid(row=0, column=0, sticky='new', columnspan=len(self.hairdressers)+1) # Set geometry for frame.

        ### SCROLLBARS
            # The scrollbar is used to scroll thought the list boxes containing all the appointments.
            self.scrolls.append(ttk.Scrollbar(self.tabs[i], orient='vertical', command=self.on_scroll_by_bar)) # Add a Tkinter scrollbar for each tab.
            self.scrolls[i].grid(row=0, column = len(self.hairdressers)+1, sticky='ns', rowspan = 2) # Sets geometry and sets it to last column of tab frame.
            
            for j in range(len(self.hairdressers)+1): # Loop for each hairdresser.
            ### CANVASSES
                # The canvesses hold the names of the haidressers as column headings. Theses are displayed on canvasses instead of labels to allow them to be rotated 90 degrees.
                self.tabs[i].columnconfigure(j, weight=1) # Sets a weight for all columns except last (scrollbar column).
                self.names[i].append(tk.Canvas(self.names_frame[i])) # Add canvas for hairdresser's name.
                self.names[i][j].place(y=0, h=64) # Sets the canvas' geometry.
                
                if j == 0: # If first column (If the column that contains the appointment times).
                    self.names[i][0].clock = self.names[i][0].create_image(0, 0, anchor='nw', image=self.clock_image) # Add image to canvas.
                    self.names[i][0].image = self.clock_image # Set canvas attribute 'image' to 'clock_image'.
                    
                else:
                    self.names[i][j].create_text(24, 56, anchor='sw', angle=90, text=self.hairdressers[j-1][1], fill=text_colour, font=(primary_font, 10)) # Add hairdresser's name at 90 degree angle.
                    if not self.hairdressers[j-1][3] == '': # If another hairdresser shares this name.
                        self.names[i][j].create_text(40, 56, anchor='sw', angle=90, text=self.hairdressers[j-1][3], fill=text_colour, font=(primary_font, 10)) # Add the first part of the hairdresser's surname aswell.
                        
            ### LISTBOXES
                # Each listbox is a column a table. As there are multiple tables (one for each day) there is a 2D array of listboxes.
                self.lbs[i].append(tk.Listbox(self.tabs[i], yscrollcommand=self.on_scroll_by_wheel, fg=text_colour, font=(secondary_font, 9))) # Add a listbox below the hairdresser's name.
                self.lbs[i][j].tab = i # Add an attribute to the list box so we know what tab is belongs in.
                self.lbs[i][j].lb = j # Add an attribute to the list box so we know which list box it is from left to right.
                self.lbs[i][j].grid(row=1, column=j, sticky='nesw') # Set geometry of list box and make it expand in all directions in the frame.
                self.lbs[i][j].bind('<<ListboxSelect>>', self.open_appointments_window) # If the list box is clicked run the following function.
                self.lbs[i][j].bind('<FocusIn>', lambda event: self.master.focus()) # Makes the listbox unfocusable.
                
    ### RESIZING WIDGETS
        # Resizes the widgets to appropriate sizes depending on the screen size. Also sets the window in a zoomed state if enabled.
        # Zooming the window naturally triggers self.on_resize() because the tkinter window is set to run that function whenever the windows width of height is altered (set on line 186).
        # Therefore the function is only required to be run if the window is not set to be in a zoomed state on start up.
        if main_window_zoomed == True:
            self.master.state('zoomed') # Maximises window to fullscreen.
        else:
            self.on_resize() # Run the function 'on_resize'.
        
### 'MAIN' CLASS FUNCTIONS
    def on_resize(self, event=None):
        '''The function called when the geometry of the main window is altered. This function adjusts the geometry any widgets that depend on the height and width of the main window.'''
        if self.width != self.master.winfo_width() or event == None:  # This code is run if the width has changed, or an 'event' value was not provided.
            self.width = self.master.winfo_width() # Get the new width of the main window in pixels.

            self.week_label.place(w=self.width) # Alter the width of the label to equal the new width.
            self.logout_button.place(x=self.width-80) # Alter the position of the log out button based on the new width.
            self.arrow_left_button.place(x=self.width*0.5-320) # Alter the position of the left arrow button based on the new width.
            self.arrow_right_button.place(x=self.width*0.5+250) # Alter the position of the right arrow button based on the new width.
            self.title_label.place(x=self.width-405) # Alter the position of the label based on the new width.
            self.footer_label.place(w=self.width) # Alter the position of the label based on the new width.
            self.nb.place(x=(self.width-10)*0.03+5, w=(self.width-10)*0.94) # Alter the position and width of the notebook based on the new width.
            self.names_frame[self.nb.index(self.nb.select())].update_idletasks() # Update geometry of the name frame of the current tab in the notebook.
            for i in range(len(self.hairdressers)+1): # For each hairdresser.
                self.names[self.nb.index(self.nb.select())][i].place(x=self.names_frame[self.nb.index(self.nb.select())].winfo_width()*i/(len(self.hairdressers)+1), w=self.names_frame[self.nb.index(self.nb.select())].winfo_width()/(len(self.hairdressers)+1)) # Alter the position and width of the canvas in the name frame.
            self.names[self.nb.index(self.nb.select())][0].coords(self.names[self.nb.index(self.nb.select())][0].clock, (self.names_frame[self.nb.index(self.nb.select())].winfo_width()/(len(self.hairdressers)+1)/2)-16, 24) # Alter the position of the clock image in the first canvas.

        if self.height != self.master.winfo_height() or event == None: # This code is run if the height has changed, or an 'event' value was not provided.
            self.height = self.master.winfo_height() # Get the new height of the main window in pixels.

            self.week_label.place(h=(self.height-165)*0.04+40) # Alter the height of the label based on the new height.
            self.arrow_left_button.place(h=(self.height-165)*0.04+40) # Alter the height of the left arrow button based on the new height.
            self.arrow_right_button.place(h=(self.height-165)*0.04+40) # Alter the height of the right arrow button based on the new height.
            self.footer_label.place(y=self.height-40) # Alter the postition of the label based on the new height.
            self.nb.place(y=(self.height-165)*0.04+120, h=(self.height-165)*0.93-5) # Alter the position and width of the notebook based on the new height.

    def on_hover(self, hover):
        '''This function is triggered when the windows cursor hovers or unhovers over any interactable labels.''' 
        if hover == 0: # If the cursor hovers over the settings button.
            self.settings_button.configure(image=self.settings_dark_image) # Change image to darker version.
            self.settings_button.image = self.settings_dark_image # Change 'image' attribute to darker version.
        elif hover == 1: # If the cursor unhovers over the settings button.
            self.settings_button.configure(image=self.settings_light_image) # Change image to lighter version.
            self.settings_button.image = self.settings_light_image # Change 'image' attribute to lighter version.
            
        elif hover == 2: # If the cursor hovers over the left arrow (previous week) button.
            self.arrow_left_button.configure(image=self.arrow_left_light_image) # Change image to lighter version.
            self.arrow_left_button.image = self.arrow_left_light_image # Change 'image' attribute to lighter version.
        elif hover == 3: # If the cursor unhovers over the left arrow (previous week) button.
            self.arrow_left_button.configure(image=self.arrow_left_dark_image) # Change image to darker version.
            self.arrow_left_button.image = self.arrow_left_dark_image # Change 'image' attribute to darker version.

        elif hover == 4: # If the cursor hovers over the right arrow (next week) button.
            self.arrow_right_button.configure(image=self.arrow_right_light_image) # Change image to lighter version.
            self.arrow_right_button.image = self.arrow_right_light_image # Change 'image' attribute to lighter version.
        elif hover == 5: # If the cursor unhovers over the right arrow (next week) button.
            self.arrow_right_button.configure(image=self.arrow_right_dark_image) # Change image to darker version.
            self.arrow_right_button.image = self.arrow_right_dark_image # Change 'image' attribute to darker version.

    def log_out(self):
        '''This function is called when the user clicks the log out button. The function prepares the window to be converted back into a log in window and then converts it.'''
        for widget in self.master.winfo_children(): # For all widgets in the tkinter window.
            widget.destroy() # Destroy it.
        self.master.unbind('<Configure>') # Unbind the 'on_resize' function.
        self.master.state('normal') # Unzooms the window.
            
        global login_window # Defines the main window as global so it can be used outside this function.
        log('{} {} logged out.'.format(user[1], user[2])) # Logs the following string.
        login_window = Login(root) # Creates a new instance of the class 'Main' called 'main_window'.
        root.mainloop() # Once the instance (main window) is created, stop until the window is closed. Then the program will run the next line of code.

    def move_day(self, direction):
        '''This function is called when the tab is changed or needs to be changed.'''
        if direction == True: # If direction is left (next day).
            if self.nb.index(self.nb.select()) == len(working_days)-1: # If last day of week.
                self.move_week(True) # Move to next week.
                self.nb.select(0) # Select first tab (day) of new week.
            else:
                self.nb.select(self.nb.index(self.nb.select())+1) # Otherwise move to next day.
        elif direction == False: # If direction is right (previous day).
            if self.nb.index(self.nb.select()) == 0: # If first day of week.
                self.move_week(False) # Move to previous week.
                self.nb.select(len(working_days)-1) # Select last tab (day) of new week.
            else:
                self.nb.select(self.nb.index(self.nb.select())-1) # Otherwise move to previous day.
            
        self.on_resize() # Set new widgets' initial geometry.
        self.update_table() # Update / repopulate table as it's a new day.
        self.master.focus() # Unfocus all widgets.
        
    def move_week(self, direction):
        '''This function allows the user to navigate through the weeks in the table.'''
        global working_dates # Makes the variable global.
        
        if direction == False: # Move back a week.
            for i in range(len(working_dates)): # For all working dates.
                working_dates[i] -= datetime.timedelta(days=7) # Minus 7 days from the date.
                
        elif direction == True: # Move forward a week.
            for i in range(len(working_dates)): # For all working dates.
                working_dates[i] += datetime.timedelta(days=7) # Add 7 days to the date.
                
        self.update_table() # Updates the appointments table. Repopulates the list boxes with appointments.

    def tick(self):
        '''This function compares real time and date to the displayed time and date and updates them where necessary. This function calls itself after every 0.2 seconds.'''
        if self.time != time.strftime('%H:%M:%S'): # If displayed time does not equal real time.
            self.time = time.strftime('%H:%M:%S') # Then update the displayed time variable.
            self.time_label.config(text=self.time) # Redisplay displayed time.
            
            if self.date != time.strftime('%d/%m/%y'): # If displayed date does not equal real date.
                self.date = time.strftime('%d/%m/%y') # Then update the displayed time variable.
                self.date_label.config(text=self.date + '|') # Redisplay displayed date.
                
        self.time_label.after(200, self.tick) # Call this function again in 0.2 seconds.

    def on_scroll_by_bar(self, *args):
        '''This function is triggered when the user scrolls using the scroll bar. This sets all the listboxes 'yview' to equal the 'yview' of the scrollbar. In simplier words, the function syncs the yview of the listboxes to the scrollbar.'''
        for i in range(len(self.hairdressers)+1): # For all listboxes.
            self.lbs[self.nb.index(self.nb.select())][i].yview(*args) # Update yview of list box to match the yview of scrollbar.
            
    def on_scroll_by_wheel(self, *args):
        '''This function is triggered when the user scrolls using the scroll wheel on a listbox. This sets all the other listboxes 'yview' to the 'yview' of the scrolled listbox. It also synces the scrollbar 'yview' to the 'yview' of the scrolled listbox.'''
        for i in range(len(self.hairdressers)+1): # For all listboxes.
            self.lbs[self.nb.index(self.nb.select())][i].yview_moveto(args[0]) # Update yview of list box to match the yview of the list box that was scrolled.
        self.scrolls[self.nb.index(self.nb.select())].set(*args) # Updates the yview of the scrollbar to match the list box that was scrolled.

    def update_table(self):
        '''This function populates the table thats currently being displayed. This function is called whenever any changes are made to appointments or when the user changes the displayed day or week.'''
    ### CLEARING CONTENTS OF LIST BOXES
        for i in range(len(self.hairdressers)+1): # For all listboxes.
            self.lbs[self.nb.index(self.nb.select())][i].delete(0, tk.END) # Clears the listbox's content (so it can be repopulated).
            if i != 0: # If not the first listbox (that holds time)
                self.lbs[self.nb.index(self.nb.select())][i].appointment_id = [] # Adds an attribute to the listbox to hold the appointment ids corresponding to the appointments stored in this list box.

    ### UPDATING DISPLATED DATES
        for i in range(len(working_dates)): # For all working days.
            self.nb.tab(i, text=(working_dates[i].strftime('%a') + ' ' + add_date_suffix(working_dates[i].strftime('%d')) + ' ' + working_dates[i].strftime('%b') + ' ' + working_dates[i].strftime('%Y') + ''.join(self.padding))) # Display working date in the tab.
            
        self.lbs[self.nb.index(self.nb.select())][0].bindtags((self.lbs[i][0], self.tabs[i], 'all')) # Makes first listbox (that holds the times) unclickable.
        self.week_label.config(text='{} {} - {} {}'.format(working_dates[0].strftime('%A'), add_date_suffix(working_dates[0].strftime('%d')), working_dates[len(working_dates)-1].strftime('%A'), add_date_suffix(working_dates[len(working_dates)-1].strftime('%d')))) # Updates the label that displayed week above the table.

    ### REPOPULATING LIST BOXES
        db_open() 
        for i in range((last_appointment_time - first_appointment_time)//appointment_intervals+1): # For all appointment slots per hairdresser.
            start_time = time.strftime('%M:%S', time.gmtime(first_appointment_time + i * appointment_intervals)) # Calculate time of the appointment.
            self.lbs[self.nb.index(self.nb.select())][0].insert(tk.END, start_time) # Add that time to the first list box.
            
            c.execute('SELECT AppointmentID, StaffID, ClientID, Duration FROM Appointments WHERE Date=? AND StartTime=?', ((working_dates[self.nb.index(self.nb.select())].strftime('%d/%m/%Y')), start_time)) # Retrieve any appointments at that time.
            self.appointments = c.fetchall() # Fetch all those appointments at that time.
            
            for j in range(len(self.hairdressers)): # For all hairdressers.
                for k in range(len(self.appointments)): # For all appointments.
                    self.appointments[k] = list(self.appointments[k]) # Convert tuple to array/list.
                    
                    if self.hairdressers[j][0] == self.appointments[k][1]: # If hairdresser id for hairdresser equals hairdresser id in appointment record.
                        c.execute('SELECT FirstName FROM Clients WHERE ClientID=?', (self.appointments[k][2],)) # Retrieve first name of the client that this appointment is for.
                        client = c.fetchone() # Fetch the first name.
                        
                        for l in range(self.appointments[k][3]//15): # For the amount of slots the appointment takes.
                            self.lbs[self.nb.index(self.nb.select())][j+1].insert(tk.END, client) # Insert client's first name into listbox for that time.
                            self.lbs[self.nb.index(self.nb.select())][j+1].appointment_id.append(self.appointments[k][0]) # Insert appointment id into the list boxes' attribute (array).
                            
                if self.lbs[self.nb.index(self.nb.select())][j+1].size() <= i: # If the size of the listbox does not match the appointment time we are on.
                    self.lbs[self.nb.index(self.nb.select())][j+1].insert(tk.END, ' -') # Add '-' string (make it an empty slot).
                    self.lbs[self.nb.index(self.nb.select())][j+1].appointment_id.append(-1) # Append a null appointment id to represent it is empty.  
        db_close()
        
    def open_settings_window(self):
        '''This function opens a popup (Tkinter toplevel) window so the user can config the settings.'''
        popup = tk.Toplevel(self.master) # Defines a Tkinter toplevel window.
        global settings_window # Make the tkinter window global.
        settings_window = Settings(popup) # Creates a new instance of the class 'Settings'.
        popup.mainloop() # Wait until the settings window is closed.

    def open_appointments_window(self, event):
        '''This function is triggered when the user clicks on a list box. It works out the column and row that was clicked then creates an instance of Appointments with that information.'''
        popup = tk.Toplevel(self.master) # Defines a Tkinter toplevel window.
        global appointments_window # Makes the tkinter window global.
        appointments_window = Appointments(popup, (event.widget.lb-1), int(event.widget.curselection()[0])) # Creates a new instance of the class 'Appointments' with the coords of the appointment that was clicked.
        popup.mainloop() # Wait until the settings window is closed.
        
        
#======================================================================================
#                                     SETTINGS WINDOW  
#======================================================================================
class Settings():
    def __init__(self, master):
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Make 'master' an attribute of the 'Settings' class.
        self.tables_var = tk.StringVar() # Defines a Tkinter string variable.

    ### TKINTER WINDOW CONFIG
        self.master.title('Settings (Version {})'.format(version)) # Sets title
        self.master.geometry('270x180+{}+{}'.format(((screen_width-270)//2), ((screen_height-180)//2)))  # Sets window geometry & centers the window.
        self.master.resizable(False, False) # Sets the window so it cannot be resized
        self.master.wm_iconbitmap('resources/icon.ico') # Sets icon
        self.master.config(bg=bg_colour) # Sets background colour of window
        self.master.protocol('WM_DELETE_WINDOW', lambda: [self.master.destroy(), self.update_main_window()])
        
        self.master.focus_set() # Sets focus on this tkinter window.
        self.master.grab_set() # Sets grab on this tkinter window (so no other windows can be focused).
        
    ### TKINTER LABELS
        self.tables_label = tk.Label(self.master, text="To add, manage or remove any clients, staff,\nhairdressers or haircuts select a table in the\ndropdown menu (Admin access required).", bg=bg_colour, fg=text_colour, font=(primary_font, 10)) # Defines a tkinter label.
        self.tables_label.place(x=0, y=40, w=270, h=50) # Sets the geometry of the label.

    ### TKINTER COMBOBOX (DROP-DOWN MENU)
        self.tables_box = ttk.Combobox(self.master, textvariable=self.tables_var, font=(secondary_font, 9), state='readonly') # Defines a tkinter combobox.
        self.tables_box['values'] = ['Hairdressers/Staff', 'Clients', 'Haircuts'] # Defines the array that contains the data that the drop-down menu will contain.
        self.tables_box.place(x=50, y=10, w=170, h=30) # Sets drop-down menu's geometry.
        self.tables_box.bind('<Return>', lambda event: self.tables_box.event_generate('<Down>')) # Makes the drop-down menu drop down when the enter key is pressed when this widget is focused.
        self.tables_box.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        self.tables_box.bind('<<ComboboxSelected>>', lambda event: self.open_tables_window()) # When a option is selected from the drop-down menu, call the following function.
        
    ### TKINTER BUTTONS
        self.change_password_button = tk.Button(self.master, text='Change password', command=lambda: self.open_change_password_window(), bg=bg_colour, fg=text_colour, font=primary_font) # Defines a tkinter button.
        self.change_password_button.place(x=50, y=100, w=170, h=30) # Sets buttons's geometry.
        self.change_password_button.bind('<Return>', lambda event: self.open_change_password_window()) # Call the following function when the enter key is pressed when this widget is focused.
        self.change_password_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        
        self.dismiss_button = tk.Button(self.master, text='Dismiss', command=lambda: [self.master.destroy(), self.update_main_window()], bg=bg_colour, fg=text_colour, font=primary_font) # Defines a tkinter button.
        self.dismiss_button.place(x=185, y=140, w=75, h=30) # Sets button's geometry.
        self.dismiss_button.bind('<Return>', lambda event: [self.master.destroy(), self.update_main_window()]) # Call the following functions when the enter key is pressed when this widget is focused.
        self.dismiss_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.

### 'SETTINGS' CLASS FUNCTIONS
    def open_change_password_window(self):
        '''This function opens the tkinter window that allows the user to change their password. This function is called when the user clicks the change passsword button.'''
        popup = tk.Toplevel(self.master) # Defines a tkinter toplevel window.
        global change_password_window # Makes this variable global.
        change_password_window = ChangePassword(popup) # Creates a instance of the ChangePassword class.
        popup.mainloop() # Wait until this window is closed down.

    def open_tables_window(self):
        '''This function opens the tkinter window that allows the user to edit the database. This function is called when the user selects an option from the drop-down menu.'''
        if user[4] == True: # If the user is an admin.
            popup = tk.Toplevel(self.master) # Defines a tkinter toplevel window.
            global tables_window # Make this variable global.
            tables_window = Tables(popup, self.tables_box.current()) # Creates a instance of the Tables class.
            self.tables_box.set('') # Unselects the option in the drop-down menu.
            popup.mainloop() # Wait until this window is closed down.
            
        else:
            messagebox.showerror('Error: Access Denied', 'You must be an admin to edit the tables.') # Display a tkinter errror popup with the following message.
            self.tables_box.set('') # Unselects the option in the drop-down menu.

    def update_main_window(self):
        '''This function is called when the settings window is closed and the main window is refocused/re-grabbed. If any hairdressers have been added or removed from the database, the window will need to be rebuild to account for the change of list boxes, canvases, etc.'''
        if main_window.update == True: # If the main window needs updating.
            main_window.master.unbind('<Configure>') # Unbinds the 'on_resize' function from the window.
            main_window.master.state('normal') # Unzooms the window.
            for tab in main_window.tabs: # For all tabs in the notebook within the main window.
                tab.unbind('<Visibility>') # Unbind the 'on_resize' function from the tab.
            
            main_window.__init__(main_window.master) # Reinitialise the instance of the class.
            main_window.update = False # Set the boolean to show the main window no longer needs to be updated.
            

#======================================================================================
#                                CHANGE PASSWORD WINDOW  
#======================================================================================        
class ChangePassword(): # Defines a class that represents the window that lets users change their password.
    '''This window lets the user change their password. The window is opened when the user clicks the change password button in the settings window.'''
    def __init__(self, master): # This function is run when a instance of the class is initialised.
        '''This function is run when the class is initialised.'''
        self.master = master # Makes the variable 'master' an attribute of this class.
        self.current_p_var = tk.StringVar() # Defines a new Tkinter string variable.
        self.new_p_var = tk.StringVar() # Defines a new Tkinter string variable.
        self.new_p_confirm_var = tk.StringVar() # Defines a new Tkinter string variable.

    ### TKINTER WINDOW CONFIG
        self.master.title('Change Password (Version {})'.format(version)) # Sets title of the window.
        self.master.geometry('270x180+{}+{}'.format(((screen_width-270)//2), ((screen_height-180)//2)))  # Sets window geometry and centers the window.
        self.master.resizable(False, False) # Sets the window so it cannot be resized.
        self.master.wm_iconbitmap('resources/icon.ico') # Sets icon.
        self.master.config(bg=bg_colour) # Sets background colour of window.
        self.master.protocol('WM_DELETE_WINDOW', lambda: [self.master.destroy(), settings_window.master.focus_set(), settings_window.master.grab_set()]) # Runs the following functions when the window is closed down.
        
        settings_window.master.grab_release() # Release the grab of the settings windows so it can be transferred to the change password window.
        self.master.focus_set() # Sets the focus on this window.
        self.master.grab_set() # Sets the grab on this window (so other windows cannot take focus).

    ### TKINTER LABELS
        self.current_p_label = tk.Label(self.master, text='Current\nPassword:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.current_p_label.place(x=0, y=10, w=90, h=35) # Sets the label's geometry.

        self.new_p_label = tk.Label(self.master, text='New\npassword:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.new_p_label.place(x=0, y=50, w=90, h=35) # Sets the label's geometry.

        self.new_p_confirm_label = tk.Label(self.master, text='Re-enter\npassword:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.new_p_confirm_label.place(x=0, y=90, w=90, h=35) # Sets the label's geometry.
                                            
    ### TKINTER ENTRY BOXES
        self.current_p_entry = tk.Entry(self.master, textvariable=self.current_p_var, fg=text_colour, font=(secondary_font, 9), show='*') # Defines a Tkinter entry box.
        self.current_p_entry.place(x=95, y=15, w=150, h=25) # Sets the entry boxes' geometry.
        self.current_p_entry.bind('<Return>', lambda event: self.new_p_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.current_p_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed while this widget is focused.
        self.current_p_entry.focus()

        self.new_p_entry = tk.Entry(self.master, textvariable=self.new_p_var, fg=text_colour, font=(secondary_font, 9), show='*') # Defines a Tkinter entry box.
        self.new_p_entry.place(x=95, y=55, w=150, h=25) # Sets the entry boxes' geometry.
        self.new_p_entry.bind('<Return>', lambda event: self.new_p_confirm_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.new_p_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed while this widget is focused.

        self.new_p_confirm_entry = tk.Entry(self.master, textvariable=self.new_p_confirm_var, fg=text_colour, font=(secondary_font, 9), show='*') # Defines a Tkinter entry box.
        self.new_p_confirm_entry.place(x=95, y=95, w=150, h=25) # Sets the entry boxes' geometry.
        self.new_p_confirm_entry.bind('<Return>', lambda event: self.change_password()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.new_p_confirm_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed while this widget is focused.

    ### TKINTER BUTTONS
        self.change_p_button = tk.Button(self.master, text='Change Password', command=lambda: self.change_password(), bg=bg_colour, fg=text_colour, font=primary_font) # Defines a tkinter button.
        self.change_p_button.place(x=110, y=140, w=140, h=30) # Sets the button's geometry.
        self.change_p_button.bind('<Return>', lambda event: self.change_password()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.change_p_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed while this widget is focused.

        self.cancel_button = tk.Button(self.master, text='Cancel', command=lambda: [self.master.destroy(), settings_window.master.focus_set(), settings_window.master.grab_set()], bg=bg_colour, fg=text_colour, font=primary_font) # Defines a tkinter button.
        self.cancel_button.place(x=30, y=140, w=65, h=30) # Sets the button's geometry.
        self.cancel_button.bind('<Return>', lambda event: [self.master.destroy(), settings_window.master.focus_set(), settings_window.master.grab_set()]) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.cancel_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed while this widget is focused.

### 'CHANGE PASSWORD' CLASS FUNCTIONS
    def change_password(self):
        '''This function checks the if the inputted password matches the password in the database. If it does it will overwrite it with the new password. This function is called when the user presses the change password button in this window.'''
        current_p = self.current_p_var.get() # Get the string value in the tkinter string varaible.
        new_p = self.new_p_var.get() # Get the string value in the tkinter string varaible.
        new_p_confirm = self.new_p_confirm_var.get() # Get the string value in the tkinter string varaible.

        if current_p == '' or new_p == '' or new_p_confirm == '': # If any entry boxes are empty.
            messagebox.showerror('Error: Empty field(s)', 'Please ensure there are no empty field(s).') # Display a Tkinter error window (popup).

        elif current_p != user[3]: # If the current password does not match the one in the database.
            messagebox.showerror('Error: Password Incorrect', 'The current password was incorrect. Please try again.') # Display a Tkinter error window (popup).

        elif new_p != new_p_confirm: # If the new password does not match in both entry boxes.
            messagebox.showerror('Error: New passwords do not match', 'The new passwords do not match. Please re-enter the passwords.') # Display a Tkinter error window (popup).

        elif current_p == new_p: # If the password is not new.
            messagebox.showerror('Error: Password must be new', 'Your new password matches the old password. Please ensure it is different.') # Display a Tkinter error window (popup).

        elif len(new_p) < 8: # If the password's length is not atleast 8 characters.
            messagebox.showerror('Error: Password too weak', 'The password must contain atleast 8 characters.') # Display a Tkinter error window (popup).

        else:
            for i in range(len(new_p)): # For all characters in the new password.
                if list(new_p)[i].isalpha(): # If the character is alphabetical (a-z or A-Z).
                    
                    for j in range(len(new_p)): # For all characters in the new password.
                        if list(new_p)[j].isdigit(): # If the character is a digit (0-9).
                            
                            db_open()
                            c.execute('UPDATE Staff SET Password=? WHERE StaffID=?', (new_p, user[0])) # Update the password to the new password if the user id equals the one that's logged in.
                            conn.commit() # Commit the database change.
                            db_close()
                            user[3] = new_p # Update the password for the user logged in Python.
                            log('{} {} updated their password.'.format(user[1], user[2])) # Log the change.

                            self.master.destroy() # Destroy the change password window.
                            settings_window.master.focus_set() # Set focus back to the settings window.
                            settings_window.master.grab_set() # Set grab back to the settings window.
                            return # Exit the function early.
                                              
                    messagebox.showerror('Error: Password too weak', 'The password must contain atleast 1 digit.') # Display a Tkinter error window (popup).
                    break # Exit the for loop as no characters are digits therefore the password is already invalid.
                
            messagebox.showerror('Error: Password too weak', 'The password must contain atleast 1 alphabetical character.') # Display a Tkinter error window (popup).
                                    
        self.current_p_entry.delete(0, tk.END) # If unsuccessful, clear the entry box.
        self.new_p_entry.delete(0, tk.END) # If unsuccessful, clear the entry box.
        self.new_p_confirm_entry.delete(0, tk.END) # If unsuccessful, clear the entry box.


#======================================================================================
#                                           TABLES WINDOW  
#======================================================================================
class Tables():
    '''This window allows admins to access the database within Python. This function is called when a table is selected in the drop-down menu within the settings window. The window will then display the table selected.'''
    def __init__(self, master, table):
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Sets the variable 'master' to an attribute of the class.
        self.table = table # The table selected (between 0-2).
        self.entry = None # The variable to hold the Tkinter entry box that will be defined when a field in the table is clicked.
        self.entry_var = tk.StringVar() # Defines a Tkinter string variable.
        self.changes = [] # Defines an array.

    ### TKINTER WINDOW CONFIG
        self.master.title('Edit {} Tables (Version {})'.format(settings_window.tables_var.get(), version)) # Sets window's title.
        self.master.geometry('540x360+{}+{}'.format(((screen_width-540)//2), ((screen_height-360)//2)))  # Sets window geometry & centers the window.
        self.master.resizable(False, False) # Sets the window so it cannot be resized.
        self.master.wm_iconbitmap('resources/icon.ico') # Sets window's icon.
        self.master.config(bg=bg_colour) # Sets background colour of window.
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.cancel()) # Runs the following function when the window is exited.
        self.master.bind('<Button-1>', lambda event: self.hide_entry(click=True)) # Runs the following function when user left clickes anywhere within the window.
        self.master.focus_set() # Sets focus on the window.
        self.master.grab_set() # Sets grab on the window (so other windows cannot be focused).

    ### TKINTER BUTTONS
        self.add_button = tk.Button(self.master, text='Add', command=lambda: self.add_record(), bg=bg_colour, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter button.
        self.add_button.place(x=40, y=310, w=50, h=20) # Sets button's geometry.
        self.add_button.bind('<Return>', lambda event: self.add_record()) # Runs the following function when the enter key is pressed while this widget is focused.
        self.add_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.

        self.remove_button = tk.Button(self.master, text='Remove', command=lambda: self.remove_record(), bg=bg_colour, fg=text_colour, font=(secondary_font, 9))  # Defines a Tkinter button.
        self.remove_button.place(x=90, y=310, w=50, h=20) # Sets button's geometry.
        self.remove_button.bind('<Return>', lambda event: self.remove_record()) # Runs the following function when the enter key is pressed while this widget is focused.
        self.remove_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        
        self.cancel_button = tk.Button(self.master, text='Cancel', command=lambda: self.cancel(), bg=bg_colour, fg=text_colour, font=primary_font)  # Defines a Tkinter button.
        self.cancel_button.place(x=220, y=320, w=75, h=30) # Sets button's geometry.
        self.cancel_button.bind('<Return>', lambda event: self.cancel()) # Runs the following function when the enter key is pressed while this widget is focused.
        self.cancel_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        
        self.apply_button = tk.Button(self.master, text='Apply', command=lambda: self.apply(), bg=bg_colour, fg=text_colour, font=primary_font, relief=tk.SUNKEN)  # Defines a Tkinter button.
        self.apply_button.place(x=310, y=320, w=75, h=30) # Sets button's geometry.
        self.apply_button.bind('<Return>', lambda event: self.apply()) # Runs the following function when the enter key is pressed while this widget is focused.
        self.apply_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        
        self.exit_button = tk.Button(self.master, text='Apply & Exit', command=lambda: self.exit_(), bg=bg_colour, fg=text_colour, font=primary_font)  # Defines a Tkinter button.
        self.exit_button.place(x=400, y=320, w=120, h=30) # Sets button's geometry.
        self.exit_button.bind('<Return>', lambda event: self.exit_()) # Runs the following function when the enter key is pressed while this widget is focused.
        self.exit_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses the widget when the escape key is pressed.
        
    ### GETTING RECORDS AND FIELDS OF TABLE
        db_open()
        if self.table == 0: # If Staff table.
            self.fields = ['StaffID', 'FirstName', 'LastName', 'Password', 'IsAdmin', 'IsHairdresser', 'Rate'] # Defines an array that contains the table's fields.
            self.field_descs = ['First name of the staff member.'] # Defines an array that contains the fields' descriptions.
            self.field_descs.append('Last name of the staff member.') # Adds a description to the array.
            self.field_descs.append('Password for the staff member to log into the booking system.') # Adds a description to the array.
            self.field_descs.append('Will this staff member have admin controls where False = 0 and True = 1.') # Adds a description to the array.
            self.field_descs.append('Will this staff member be a hairdresser. (Will clients be about to book appointments with this staff member.') # Adds a description to the array.
            self.field_descs.append('The rate of the hairdressers prices in percentage, where 100% is default. For example, 200% means the hairdresser charges double the normal rate/price.') # Adds a description to the array.
            c.execute('SELECT * FROM Staff') # Retrieves the data from the table.
            self.records= list(c.fetchall()) # Fetches the data.
            self.new_record = [-1, '', '', '', 0, 0, 100] # Defines an array that contains the default values of a record within this table.
            self.record_required = [True, True, True, True, True, True] # Defines an array that contains booleans that represent if the field is required.
            
        elif self.table == 1: # If Client table.
            self.fields = ['ClientID', 'FirstName', 'LastName', 'Mobile', 'Home']  # Defines an array that contains the table's fields.
            self.field_descs = ['First name of client.'] # Defines an array that contains the fields' descriptions.
            self.field_descs.append('Last name of client.') # Adds a description to the array.
            self.field_descs.append('Mobile phone number to contact the client.') # Adds a description to the array.
            self.field_descs.append('Home phone number to contact the client.') # Adds a description to the array.
            c.execute('SELECT * FROM Clients') # Retrieves the data from the table.
            self.records= list(c.fetchall()) # Fetches the data.
            self.new_record = [-1, '', '', '', ''] # Defines an array that contains the default values of a record within this table.
            self.record_required = [True, True, False, False] # Defines an array that contains booleans that represent if the field is required.
            
        elif self.table == 2: # If Haircut table.
            self.fields = ['HaircutID', 'Haircut', 'Price', 'EstimatedTime']  # Defines an array that contains the table's fields.
            self.field_descs = ['The name of the haircut.'] # Defines an array that contains the fields' descriptions.
            self.field_descs.append('The price of the haircut at normal rate, where £1 = 1.0') # Adds a description to the array.
            self.field_descs.append('Estimated time the appointment will take in factor of 15 where 15 minutes = 15.') # Adds a description to the array.
            c.execute('SELECT * FROM Haircuts') # Retrieves the data from the table.
            self.records= list(c.fetchall()) # Fetches the data.
            self.new_record = [-1, '', '', ''] # Defines an array that contains the default values of a record within this table.
            self.record_required = [True, True, True] # Defines an array that contains booleans that represent if the field is required.

        self.id_labels = [] # Defines an array that will contain the ids of the records.
        for i in range(len(self.records)): # For all records.
            self.records[i] = list(self.records[i]) # Convert tuple to array/list.
            if self.table == 0: # If Staff table.
                c.execute('SELECT Rate FROM Hairdressers WHERE StaffID=?', (self.records[i][0],)) # Retrieve the hairdresser's rate for this staff member.
                result = c.fetchone() # Fetch the data.
                if result == None: # If this staff member isn't a hairdresser.
                    self.records[i].append(0) # Set the isHairdresser coloumn to False (0).
                    self.records[i].append('') # Set the rate to empty.
                else:
                    self.records[i].append(1) # Set the isHairdresser coloumn to True (1).
                    self.records[i].append(result[0]) # Set the rate to the rate retrieved from the database.
            self.id_labels.append(tk.Label(self.master, text=self.records[i][0], bg=bg_colour, fg=text_colour, font=(primary_font, 9), anchor='e')) # Add label that contains the id for this record.
            if i <= 16: # If the record is within the first 16.
                self.id_labels[i].place(x=20, w=20, h=16, y=16*i+40) # Place the label next to the corresponding record.
            else:
                self.id_labels[i].place(x=20, w=20, h=16, y=360) # Place the label outside the window.
        db_close()
        
    ### TKINTER FRAMES
        self.table_frame = tk.Frame(self.master) # Defines a Tkinter frame.
        self.table_frame.place(x=40, y=10, w=480, h=300) # Sets the frame's geometry.
        self.table_frame.rowconfigure(1, weight=1) # Adds a weight to the first row in the frame.
        
        self.fields_frame = tk.Frame(self.table_frame, height=20) # Defines a Tkinter frame.
        self.fields_frame.grid(row=0, column=0, sticky='new', columnspan=len(self.fields)-1) # Sets the frame's geometry.

    ### TKINTER LABEL
        self.id_label = tk.Label(self.master, bg=bg_colour, fg=text_colour, text='ID', font=(primary_font, 9)) # Defines a Tkinter label.
        self.id_label.place(x=20, y=10, w=20, h=20) # Sets label's geometry.

        self.remove_info_label = tk.Label(self.master, bg=bg_colour, fg=text_colour, font=(primary_font, 7), text='', anchor='w') # Defines a Tkinter label.
        self.remove_info_label.place(x=0, y=330, w=200, h=30) # Sets label's geometry.

    ### SCROLLBAR
        self.scroll = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.on_scroll_by_bar) # Defines a Tkinter scrollbar.
        self.scroll.grid(row=0, column = len(self.fields)-1, sticky='ns', rowspan = 2) # Set's the scrollbar's geometry.
        
    ### POPULATING TKINTER FRAMES WITH LISTBOXES AND LABELS 
        self.field_labels = [] # Defines an array that will contain the field headings.
        self.lbs = [] # Defines an array that will contain the list boxes.
        for i in range(len(self.fields)-1): # For each field excluding the id.
            self.table_frame.columnconfigure(i, weight=1) # Give it a weight.
            self.fields_frame.update_idletasks() # Update the geometry of the frame.
            self.field_labels.append(tk.Label(self.fields_frame, text=self.fields[i+1], bg=bg_colour, fg=text_colour, font=(primary_font, 9))) # Appends a Tkinter label to the array.
            self.field_labels[i].place(x=self.fields_frame.winfo_width()*i/(len(self.fields)-1), y=0, w=self.fields_frame.winfo_width()/(len(self.fields)-1), h=20) # Sets the label's geometry.
            self.field_labels[i].field = i # Adds an attribute to the label that contains the field.
            self.field_labels[i].bind('<Button-1>', lambda event: messagebox.showinfo(('Info: Help with ' + self.fields[event.widget.field+1]), self.field_descs[event.widget.field])) # Displays a Tkinter information window (popup) when the field's heading it left clicked.
            self.field_labels[i].bind('<Enter>', lambda event: event.widget.configure(font=(primary_font, 9, 'underline'))) # When the mouse cursor is hovering above this label, the text becomes underlined to indicate it's clickable.
            self.field_labels[i].bind('<Leave>', lambda event: event.widget.configure(font=(primary_font, 9))) # When the mouse cursor is no longer hovering above this label, the text is reverted to its normal state.        
            
        ### TKINTER LISTBOXES
            self.lbs.append(tk.Listbox(self.table_frame, yscrollcommand=self.on_scroll_by_wheel, fg=text_colour, font=(secondary_font, 9))) # Appends a Tkinter list box to the array.
            self.lbs[i].grid(row=1, column=i, sticky='nesw') # Set's the list boxes' geometry.
            self.lbs[i].bind('<<ListboxSelect>>', lambda event: self.force_show_entry(event)) # Run the following functions when the list box is left clicked.
            self.lbs[i].bind('<FocusIn>', lambda event: self.focus_fix()) # Run the 'focus_fix' function when the list box is focused.
            self.lbs[i].field = i # Adds an attribute to the list box that contains the field.

            for j in range(len(self.records)): # For all records.
                if self.records[j][i+1] == None: # If the field of this record is empty.
                    self.records[j][i+1] = '' # Set it to an empty string instead.
                    self.lbs[i].insert(tk.END, 'None') # Insert the string 'None' into the list box.
                    self.lbs[i].itemconfig(j, foreground=primary_colour) # Change the colour of 'None' to show it's not a value.
                else:
                    self.lbs[i].insert(tk.END, self.records[j][i+1]) # Otherwise insert the data into the list box.

    ### TKINTER ENTRY BOXES
        self.entry = tk.Entry(self.master, textvariable=self.entry_var, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter entry box.
        self.entry.bind('<FocusOut>', lambda event: self.focus_fix()) # Run the 'focus_fix' function when the entry box loses focus.
        self.entry.bind('<Escape>', lambda event: self.hide_entry(cancel=True)) # Run the following function when the escape key is pressed while the entry box is focused.
        self.entry.bind('<Return>', lambda event: self.hide_entry()) # Run the following function when the return key is pressed while the entry box is focused.
        self.entry.bind('<Enter>', lambda event: self.on_hover(True)) # Run the following function when the cursor hovers over the entry box.
        self.entry.bind('<Leave>', lambda event: self.on_hover(False)) # Run the following function when the cursor leaves the entry box.
        self.entry.hover = False # Defines a boolean.
        self.entry.hidden = True # Defines a boolean.
        self.entry.forced = None # Defines a boolean.

### 'TABLES' CLASS FUNCTIONS
    def on_hover(self, hover):
        '''This function runs when the cursor moves over the entry box. It is required so when the user left clicks we know if they've left clicked the entry box.'''
        self.entry.hover = hover

    def focus_fix(self):
        '''This function fixes which widget is focused depending on if the entry box is present. This function is a fix to a bug.'''
        if self.entry.hidden == True:
            self.master.focus()
        else:
            self.entry.focus()

    def force_show_entry(self, event):
        '''This function forces the entry box to appear when hide_entry is next called (which is called straight after by the left click binding). This is required so the entry box is not hidden straight away. This function is a fix to a bug.'''
        if self.entry.hidden == True: # If the entry's attribute 'hidden' is True.
            self.entry.forced = event # Set the entry's attribute 'forced' to the event of the widget that called this function.

    def hide_entry(self, cancel=False, click=False):
        '''This function hides the entry box and checks if the new value is valid data for this field. This function is called when the user clicks off the entry box or presses escape or enter.'''
        if self.entry.forced != None: # If the entry needs to be forced to show.
            lb = self.entry.forced.widget # Gets the widget from the event.
            if not(self.table == 0 and lb.field == 5 and self.records[int(lb.curselection()[0])][5] == 0): # If the clicked listbox is not rates for a staff member that isn't a hairdresser.
                self.show_entry(self.entry.forced) # Calls the function to show the entry box.
            lb.selection_clear(0, tk.END) # Clears the selection of the listbox.
            self.entry.forced = None # Makes the entry box no longer be forced to show.
            
        elif (click == False or self.entry.hover == False) and self.entry.hidden == False: # If entry box is not hidden and the left click that called this function was not on the entry box.
            self.entry.lower(self.table_frame) # Hide the entry box under the table frame.
            self.entry.hidden = True # Mark the entry box as hidden (change entry boxes' attribute).
            new_val = self.entry_var.get() # Retrieve the string value from the Tkinter string variable.
            if self.table != 0 or self.entry.field != 2: # If the selected field isn't the password.
                new_val = new_val.replace(' ', '').lower() # Remove all space characters and then make all character lower case.
            for lb in self.lbs: # For all list boxes.
                lb.selection_clear(0, tk.END) # Clear the selection.
            self.entry.delete(0, tk.END) # Clear the contents of the entry box.

            if cancel == True or new_val == str(self.records[self.entry.record][self.entry.field+1]): # If the user clicked escape on the entry box or the value is equal to the value that was there before.
                return # Exit function early.
            elif new_val == '': # If the new value is nothing.
                self.records[self.entry.record][self.entry.field+1] = new_val # Update the records with this new value.
                self.lbs[self.entry.field].delete(self.entry.record) # Remove the old value from the list box.
                if self.record_required[self.entry.field] == True: # If this field is required.
                    self.lbs[self.entry.field].insert(self.entry.record, 'Required') # Add 'Required' to the list box in place of the old value.
                    self.lbs[self.entry.field].itemconfig(self.entry.record, foreground='red') # Make 'Required' red to show it's not a value.
                    return # Exit function early.
                else:
                    self.lbs[self.entry.field].insert(self.entry.record, 'None') # Add 'None' to the list box in place of the old value.
                    self.lbs[self.entry.field].itemconfig(self.entry.record, foreground=primary_colour) # Make 'None' a different colour to show it's not a value.
                    return # Exit function early.
    ### VALIDATION
        ### IF FIELD IS NAME
            elif (self.table in {0, 1} and self.entry.field in {0, 1}) or (self.table == 2 and self.entry.field == 0): # If the field is a name.
                if new_val.isalpha(): # Check that the string only consists of alphabetical characters (a-z or A-Z).
                    new_val = new_val.title() # Capitalise the first character of the string.
                    if new_val == self.records[self.entry.record][self.entry.field+1]: # If the new value is equal to the old value.
                        return # Exit function early.
                else:
                    messagebox.showerror('Error: Incorrect data type', 'This field must only contain alphabetical characters.') # Displays a tkinter error window (popup) with the following message.
                    return # Exit function early.
        ### IF FIELD IS PASSWORD
            elif self.table == 0 and self.entry.field == 2: # If the field is the password.
                if len(new_val) < 8: # If length of the password is less than 8 characters.
                    messagebox.showerror('Error: Password too weak', 'The password must contain atleast 8 characters.') # Displays a tkinter error window (popup) with the following message.
                    return # Exit function early.
                else:
                    alpha_exists = False # Defines a boolean to keep track if there is atleast one alphabetical character.
                    digit_exists = False # Defines a boolean to keep track if there is atleast one digit.
                    for i in range(len(new_val)): # For all characters in the password.
                        if list(new_val)[i].isalpha(): # If the character is alphabetical (a-z or A-Z).
                            alpha_exists = True # Set the boolean to True.
                            break # End the loop early.
                    for j in range(len(new_val)): # For all characters in the password.
                        if list(new_val)[j].isdigit(): # If the character is a digit (0-9).
                            digit_exists = True # Set the boolean to True.
                            break # End the loop early.
                    if alpha_exists == False: # If there was no alphabetical characters.        
                        messagebox.showerror('Error: Password too weak', 'The password must contain atleast 1 digit.') # Displays a tkinter error window (popup) with the following message.
                        return # Exit function early.
                    elif digit_exists == False: # If there was no digits.
                        messagebox.showerror('Error: Password too weak', 'The password must contain atleast 1 alphabetical character.') # Displays a tkinter error window (popup) with the following message.
                        return # Exit function early.
        ### IF FIELD IS BOOLEAN
            elif self.table == 0 and self.entry.field in {3, 4}: # If Staff Table and a boolean field.
                if new_val in {'1', 'true', 'yes'}: # If value is one of the following.
                    if self.records[self.entry.record][self.entry.field+1] == 1: # If the value has not changed.
                        return # Exit function early.
                    new_val = 1 # Otherwise set new value to 1.
                elif new_val in {'0', 'false', 'no'}: # If value is one of the following.
                    if self.records[self.entry.record][self.entry.field+1] == 0: # If the value has not changed.
                        return # Exit function early.
                    if self.entry.field == 3: # If the field is 'isAdmin'.
                    ### CHECK FOR ATLEAST ONE OTHER ADMIN
                        admins = 0 # Counter for the amount of admins.
                        for record in self.records: # For all records.
                            if record[4] == 1: # If record is admin.
                                admins += 1 # Add one to counter.
                                if admins == 2: # When counter reaches two.
                                    break # End for loop early.
                        if admins < 2: # If there is not atleast two admins.
                            messagebox.showerror('Error: Atleast one admin must exist', 'There must be atleast one admin.') # Displays a tkinter error window (popup) with the following message.
                            return # Exit function early.
                    new_val = 0 # If there is atleast two admins, then set new value to 0.
                else:
                    messagebox.showerror('Error: Incorrect data type', 'This field must be a boolean.') # Displays a tkinter error window (popup) with the following message.
                    return # Exit function early.
        ### IF FIELD IS NUMBER
            elif (self.table == 0 and self.entry.field == 5) or (self.table == 1 and self.entry.field in {2,3}) or (self.table == 2 and self.entry.field == 2): # If field consisting of only digits.
                if new_val.isdigit(): # If new value consists of only digits.
                    if self.table != 1 or not self.entry.field in {2,3}: # If field is not Clients' phone numbers.
                        new_val = int(new_val) # Convert string to integer.
                    if new_val == self.records[self.entry.record][self.entry.field+1]: # If the value has not changed.
                        return # Exit function early.
                    if self.table == 2 and self.entry.field == 2 and new_val % 15 != 0: # If the field is appointment time and isn't factor of 15.
                        messagebox.showerror('Error: Incorrect data type', 'This field must be a factor of 15.') # Displays a tkinter error window (popup) with the following message.
                        return # Exit function early.
                else:
                    messagebox.showerror('Error: Incorrect data type', 'This field must only contain digits.') # Displays a tkinter error window (popup) with the following message.
                    return # Exit function early.
        ### IF FIELD IS FLOAT/REAL
            elif self.table == 2 and self.entry.field == 1: # If table is Haircuts and field is price.
                try: # Try the following code.
                    new_val = float(new_val) # Convert the new value to a float. If successful no errors will be produced.
                    if new_val == self.records[self.entry.record][self.entry.field+1]: # If the value has not changed.
                        return # Exit function early.
                    if new_val < 0: # If value is negative.
                        messagebox.showerror('Error: Incorrect data type', 'This float must be postive.') # Displays a tkinter error window (popup) with the following message.
                        return # Exit function early.
                except TypeError: # If an error was produced when converting the new value to a float (In other words, the variable was not a float/real).
                    messagebox.showerror('Error: Incorrect data type', 'This field must be a float.') # Displays a tkinter error window (popup) with the following message.
                    return # Exit function early.
        ### IF NEW VALUE PASSES ALL VALIDATION
            self.records[self.entry.record][self.entry.field+1] = new_val # Update records with new value.
            self.changes.append(['update', self.records[self.entry.record][0], self.entry.field, new_val]) # Add the change to the changes array to be applied when the user chooses to.
            self.apply_button.config(relief=tk.RAISED) # Set button's state to raised.
            self.lbs[self.entry.field].delete(self.entry.record) # Delete the old value from the list box.
            self.lbs[self.entry.field].insert(self.entry.record, new_val) # Insert the new value into the list box in place of the old.
            if self.table == 0 and self.entry.field == 4 and new_val == 1: # If Staff table, field is 'isHairdresser' and value is 1.
                self.records[self.entry.record][6] = 100 # Make 'Rate' field equal to 1.
                self.lbs[5].delete(self.entry.record) # Delete the old value from the list box.
                self.lbs[5].insert(self.entry.record, 100) # Insert the new value into the list box in place of the old.
            elif self.table == 0 and self.entry.field == 4 and new_val == 0: # If Staff table, field is 'isHairdresser' and value is 0.
                self.records[self.entry.record][6] = '' # Make 'Rate' field equal to empty string.
                self.lbs[5].delete(self.entry.record) # Delete the old value from the list box.
                self.lbs[5].insert(self.entry.record, '') # Insert the new value into the list box in place of the old.
                       
            
    def show_entry(self, event):
        '''This function is called when the user wants to edit a record. It summons an entry box over the record so the user can edit the value.'''
        self.entry.field = event.widget.field # Get field of from list boxes' attribute.
        self.entry.record = int(event.widget.curselection()[0]) # Get the record that is selected in the list box.
        
    ### IF RECORD NEEDS TO BE REMOVED
        if self.remove_button['relief'] == tk.SUNKEN: # If the button's state is sunken:
            self.remove_button.config(relief=tk.RAISED) # Set the button's state to raised.
            self.remove_info_label.config(text='') # Empty the string containing information on how to remove.
            for i in range(len(self.records)): # For all records.
                if self.table != 0 or (self.records[i][4] == 1 and self.entry.record != i): # If atleast one other admin exists and it's not itself. 
                    self.id_labels[self.entry.record].destroy() # Destroy the label that displays the record's primary key.
                    self.id_labels.remove(self.id_labels[self.entry.record]) # Remove the label from the array that contained it.
                    self.changes.append(['remove', self.records[self.entry.record][0]]) # Add the change to the changes array to be applied when the user chooses to.
                    self.apply_button.config(relief=tk.RAISED) # Set button's state to raised.
                    self.records.remove(self.records[self.entry.record]) # Remove this record from the 2D array.
                    for lb in self.lbs: # For all list boxes.
                        lb.delete(self.entry.record) # Remove this record.
                    return # End function early.
            messagebox.showerror('Error: Atleast one admin must exist', 'There must be atleast one admin.') # Displays a tkinter error window (popup) with the following message.
    ### IF RECORD IS BEING EDITED
        else:
            self.entry.lift(self.table_frame) # Lift the entry box that was hidding behind the table frame.
            self.entry.hidden = False # Set it's attribute to no longer being hidden.
            self.entry.yview = self.lbs[0].yview() # Take note of the list box.
            self.entry_var.set(self.records[self.entry.record][self.entry.field+1]) # Set the value of the entry box to the value of the record where the entry box will be placed.
        
            y = int(self.entry.record-self.entry.yview[0]*len(self.records))*16+30 # Calculate the y position that the entry box needs to be plaed at.
            self.entry.place(x=self.fields_frame.winfo_width()*self.entry.field/(len(self.fields)-1)+40, y=y, w=self.fields_frame.winfo_width()/(len(self.fields)-1), h=16) # Set's the entry boxes' geometry.
            self.entry.icursor(tk.END) # Set's the cursor at the end of the entry box.

    def add_record(self):
        '''This function is called when the user clicks the add record button. It adds a record at the bottom of the table and adds it to the record array with that table's default values for each field.'''
    ### CALCULATES THE NEW PRIMARY KEY FOR THE RECORD.
        self.records.append([self.new_record[0]]) # Adds an array to the records array (2D array).
        for i in range(len(self.records)-1): # For all records excluding self.
            if self.records[len(self.records)-1][0] < self.records[i][0]: # If this record has a higher primary key than the new record.
                self.records[len(self.records)-1][0] = self.records[i][0] # Set the new record's primary key equal to that record.
        self.records[len(self.records)-1][0] += 1 # Add one to the highest primary key to ensure it's unique.
        self.id_labels.append(tk.Label(self.master, text=self.records[len(self.records)-1][0], bg=bg_colour, fg=text_colour, font=(primary_font, 9), anchor='e')) # Defines a Tkinter label that contains this new record's primary key.
        self.id_labels[len(self.id_labels)-1].place(x=20, w=20, h=16, y=360) # Set's the record's geometry.
        self.changes.append(['add', self.records[len(self.records)-1][0]]) # Add the change to the changes array to be applied when the user chooses to.
        self.apply_button.config(relief=tk.RAISED) # Set's the button's state as raised as there's unsaved changes.
        
        for i in range(len(self.fields)-1): # For all fields excluding the first.
            self.records[len(self.records)-1].append(self.new_record[i+1]) # Add the field to the new record.
            if self.table == 0 and i == 5: # If Staff table and 'isHairdresser' field.
                self.lbs[i].insert(tk.END, '') # Insert empty string.
            elif self.new_record[i+1] == '' and self.record_required[i] == True: # If field is empty and required.
                self.lbs[i].insert(tk.END, 'Required') # Set list box to show 'Required'.
                self.lbs[i].itemconfig(len(self.records)-1, foreground='red') # Change the colour to red to show it's not a value.
            elif self.new_record[i+1] == '': # If field is empty and not required.
                self.lbs[i].insert(tk.END, 'None') # Set list box to show 'None'.
                self.lbs[i].itemconfig(len(self.records)-1, foreground=primary_colour) # Change the colour of this to show it's not a value.
            else:
                self.lbs[i].insert(tk.END, self.records[len(self.records)-1][i+1]) # Otherwise insert the record value into the list box.

        self.on_scroll_by_wheel(1.0-16/len(self.records), 1.0) # Set the yview of all the listboxes down by a record to account for the new record at the bottom.

    def remove_record(self):
        '''This function is run when the remove button is clicked by the user. This will cause the next record to be pressed to be deleted. This button is toggleable.'''
        if self.remove_button['relief'] == tk.RAISED: # If the button's in a raised state.
            self.remove_button.config(relief=tk.SUNKEN) # Set the button's state to sunken.
            self.remove_info_label.config(text="The next record you click will be removed.\nClick 'Remove' again to cancel the removal.") # Make the label close to the button display infomation when the button is toggled on.
        else:
            self.remove_button.config(relief=tk.RAISED) # Set the button's state to raised.
            self.remove_info_label.config(text='') # Remove the information displayed by making the displayed string empty.
            
    def on_scroll_by_bar(self, *args):
        '''This function is run when the user scrolls with the scroll bar. It syncs all the listboxes to the new yview of the scroll bar.'''
        if self.entry.hidden == True: # Only scroll if the entry box is not present.
            for i in range(len(self.fields)-1): # For all fields excluding the first one.
                self.lbs[i].yview(*args) # Sync the yview of this list box to the yview of the scroll bar.
            if float(args[1]) >=0 and float(args[1]) + 16/len(self.records) <= 1: # If the primary keys need re-syncing with the records.
                for i in range(len(self.id_labels)): # For all primary key labels.
                    if i - float(args[1]) * len(self.records) <= 16: # If the corresponding record is on screen.
                        self.id_labels[i].place(y=int(i-float(args[1])*len(self.records))*16+30) # Place the primary key label next to the corresponding record.
                    else:
                        self.id_labels[i].place(y=360) # Otherwise place the primary key label off screen (outside the window).
            
    def on_scroll_by_wheel(self, *args):
        '''This function is triggered when the user scrolls using the scroll wheel on a list box. This sets all the other list boxes yview to the yview of the scrolled list box.'''
        if len(self.lbs) + 1 == len(self.fields): # If the list box is one of the fields.
            if self.entry.hidden == True: # If the entry box is currently hidden.
                yview = args[0] # Define a new float with the value of the first argument/parameter.
                self.scroll.set(*args) # Set/sync the scrollbar's yview to the new yview of the list box.
            else:
                yview = self.entry.yview[0] # Else undo the change in yview of the list box that called this function.
            for i in range(len(self.fields)-1): # For all listboxes.
                self.lbs[i].yview_moveto(yview) # Move the yview by the change in yview caused by the scroll.
            for i in range(len(self.id_labels)): # For all primary key labels.
                line = int(i - float(yview) * len(self.records)) # Calculate the line of the record where the first record is 1 and the nth record is n.
                if line >= 0 and line <= 16: # If in the first 16 records (In other words, if the corresponding record is no screen).
                    self.id_labels[i].place(y=line*16+30) # Place the primary key label next to the corresponding label.
                else:
                    self.id_labels[i].place(y=360) # Otherwise, place the primary key label off screen (outside the window).
                                              
        

    def apply(self):
        '''This function is called when the user clicks the apply button. It applies all the changes made in the table to the database.'''
        if self.apply_button['relief'] == tk.RAISED: # If the apply button is raised (In other words, if there are any unsaved changes).
            for i in range(len(self.fields)-1): # For all fields excluding the first one.
                for j in range(len(self.records)): # For all records.
                    if self.lbs[i].get(j) == 'Required' and self.records[j][i+1] == '': # If the listbox contains an empty field that is required.
                        messagebox.showerror('Error: Required Fields', 'There are required fields are are empty. Please fill these in before continuing.') # Displays a Tkinter message window (popup).
                        return False # End the function early with the boolean value False to show it was unsuccessful.

            if self.table == 0: # If Staff Table.
                table_name = 'Staff' # Define a string with the following value.
            elif self.table == 1: # If Staff Table.
                table_name = 'Clients' # Define a string with the following value.
            elif self.table == 2: # If Staff Table.
                table_name = 'Haircuts' # Define a string with the following value.
                
            db_open()
            for i in range(len(self.changes)): # For all changes made to the table.
                if self.changes[i][0] == 'add': # If the change is a new record.
                    if self.table == 0: # If Staff Table.
                        c.execute('INSERT INTO Staff (StaffID, FirstName, LastName, Password, IsAdmin) VALUES (?, "placeholder", "placeholder", "placeholder", 0)', (self.changes[i][1],)) # Insert a new record.
                    elif self.table == 1: # If Client Table.
                        c.execute('INSERT INTO Clients (ClientID, FirstName, LastName) VALUES (?, "placeholder", "placeholder")', (self.changes[i][1],)) # Insert a new record.
                    elif self.table == 2: # If Haircut Table.
                        c.execute('INSERT INTO Haircuts (HaircutID, Haircut, Price, EstimatedTime) VALUES (?, "placeholder", 1.0, 15)', (self.changes[i][1],)) # Insert a new record.
                if self.changes[i][0] == 'remove': # If the change is removing an existing record.
                    c.execute('DELETE FROM {} WHERE {} = {}'.format(table_name, self.fields[0], self.changes[i][1])) # Delete a record.
                    if self.table == 0: # If Staff Table.
                        c.execute('SELECT * FROM Hairdressers WHERE StaffID = ?', (self.changes[i][1],)) # Delete a record.
                        if c.fetchone() != None: # If this staff member is a hairdresser.
                            c.execute('DELETE FROM Hairdressers WHERE StaffID = ?', (self.changes[i][1],)) # Delete a record.
                            main_window.update = True # Set the main_window to be updated after returning back to the main window.
                if self.changes[i][0] == 'update': # If the change is a change in value of a field in a record.
                    if self.table == 0 and self.changes[i][2] == 4: # If Staff table and field is 'isHairdresser'.
                        if self.changes[i][3] == 0: # If the value of 'isHairdresser' is 0.
                            c.execute('DELETE FROM Hairdressers WHERE StaffID = ?', (self.changes[i][1],)) # Delete a record.
                        elif self.changes[i][3] == 1: # If the value of 'isHairdresser' is 1.
                            c.execute('INSERT INTO Hairdressers (StaffID, Rate) VALUES (?, 100)', (self.changes[i][1],)) # Add a record.
                        main_window.update = True # Set the main_window to be updated after returning back to the main window
                    elif self.table == 0 and self.changes[i][2] == 5: # If Staff table and field is 'Rate'.
                            c.execute('UPDATE Hairdressers SET Rate = ? WHERE StaffID = ?', (self.changes[i][3], self.changes[i][1])) # Change a value of the 'Rate' field where Staff ID another value.
                    else:
                        if isinstance(self.changes[i][3], str): # If the value is a instance of the class string/str (In other words, is this variable a string).
                            self.changes[i][3] = ('"{}"'.format(self.changes[i][3])) # Surround the string in quotations so mysqlite3 knows it's a string.
                        c.execute('UPDATE {} SET {} = {} WHERE {} = {}'.format(table_name, self.fields[self.changes[i][2]+1], self.changes[i][3], self.fields[0], self.changes[i][1])) # Change a value of a field in a record.
                   
                conn.commit() # Commit the changes to the database.
            db_close()
            self.changes = [] # Defines an empty array.
            self.apply_button.config(relief=tk.SUNKEN) # Set the button's state as sunken.
            log('Database was updated by {} {}.'.format(user[1], user[2])) # Log that the database was altered by an admin.
        return True # End the function early with the boolean value True to show it was successful.

    def exit_(self): # This function is called 'exit_' as 'exit' is a reserved function for Python.
        '''This function is called when the user clicks the exit button. It applies changes and then closes the tables window.'''
        if self.apply(): # If apply is successful (returns True).
            self.master.destroy() # Destroy the tables window.
            settings_window.master.focus_set() # Set the focus to the settings window.
            settings_window.master.grab_set() # Set the grab to the settings window, so no other windows can take focus.

    def cancel(self):
        '''This function is called when the user clicks the cancel button. It discards all changes and then closes the tables window.'''
        if self.apply_button['relief'] == tk.RAISED: # If the button's state is raised.
            if not messagebox.askokcancel('Confirmation: Unsaved Changes', 'Do you want to quit? Any unsaved changes will be lost.'): # Display a Tkinter window (popup) to confirm the user wants to discard the changes.
                return # End the function early.
        self.master.destroy() # Destroy the tables window.
        settings_window.master.focus_set() # Set the focus to the settings window.
        settings_window.master.grab_set() # Set the grab to the settings window, so no other windows can take focus.
        
#======================================================================================
#                          ADDING / MANAGING APPOINTMENTS WINDOW  
#======================================================================================
class Appointments():
    def __init__(self, master, lb, line):
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Defines variable 'master' as attribute of the Appointments class.
        self.lb = lb # Defines variable 'lb' as attribute of the Appointments class.
        self.line = line # Defines variable 'line' as attribute of the Appointments class.
        global main_window # Declare the variable 'main_window' as global.
        self.day = main_window.nb.index(main_window.nb.select()) # Define an integer as the working day of the week selected (In other words, the tab from left to right).
        self.id = main_window.lbs[self.day][self.lb+1].appointment_id[self.line] # Retrieves the appointment id from the list boxes' attributes.
        
    ### TKINTER WINDOW CONFIG
        self.master.geometry('540x360+{}+{}'.format(((screen_width-540)//2), ((screen_height-360)//2)))  # Sets window geometry and centers the window.
        self.master.resizable(False, False) # Sets the window so it cannot be resized.
        self.master.wm_iconbitmap('resources/icon.ico') # Sets the window's icon.
        self.master.config(bg=bg_colour) # Sets background colour of window.
        self.master.focus_set() # Sets the focus on this window.
        self.master.grab_set() # Sets the grap on this window, so other windows cannot take the focus.
        self.master.protocol('WM_DELETE_WINDOW', lambda: [self.master.destroy(), main_window.lbs[self.day][self.lb+1].selection_clear(0, tk.END)]) # Run the following functions when the user closes the window.
        
    ### CONNECTION TO DATABASE
        db_open()

        c.execute('SELECT Rate FROM Hairdressers') # Retrieve all the rate from the Hairdressers table.
        self.rate = c.fetchall()[self.lb][0] # Fetch the rate for this hairdresser from the query.

        c.execute('SELECT ClientID, FirstName, LastName FROM Clients') # Retrives the ClientID, FirstName, LastName from the Clients table.
        self.clients = c.fetchall() # Fetch the results from the query.

        c.execute('SELECT HaircutID, Haircut, Price, EstimatedTime FROM Haircuts') # Retrieve all records from the Haircuts table.
        self.haircuts = c.fetchall() # Fetch the results from the query.
        
    ### ADDING NEW APPOINTMENT
        if self.id == -1: # If there is no appointment in this appointment slot.
            db_close()
            
        ### MORE TKINTER WINDOWS CONFIG
            self.master.title('Add Appointment (Version {})'.format(version)) # Sets window's title.

        ### VARIABLES
            self.client_names = [] # Defines an array.
            self.haircut_names = [] # Defines an array.
            self.durations = [15, 30, 45, 60, 75, 90, 105, 120] # Defines an array.

            self.client_var = tk.StringVar() # Defines a Tkinter string variable.
            self.haircut_var = tk.StringVar() # Defines a Tkinter string variable.
            self.duration_var = tk.StringVar() # Defines a Tkinter string variable.

        ### POPULATING LISTS
            for i in range(len(self.clients)): # For all clients.
                self.client_names.append('{} {}'.format(self.clients[i][1], self.clients[i][2])) # Put the client's first name and surname together to make it an option for a drop-down menu.
            self.client_names.append('--- Add new client ---') # Add a last option to add a new client.

            for i in range(len(self.haircuts)): # For all haircuts.
                self.haircut_names.append(self.haircuts[i][1] + ' (Estimated Price: £' + '{:0.2f}'.format(self.haircuts[i][2] * self.rate * 0.01) + ')') # Put's the haircut name, price and hairdresser's rate together to make it an option for a drop-down menu.

            for i in range(len(self.durations)): # For all durations.
                self.durations[i] = str(self.durations[i]) + ' minutes' # Makes each duration an option for a drop-down menu.
                
        ### TKINTER LABELS
            self.time_label = tk.Label(self.master, text='Start Time:', bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='e') # Defines a Tkinter label.
            self.time_label.place(x=0, y=20, w=165, h=30) # Sets the geometry of the label.
            self.time_ans_label = tk.Label(self.master, text=time.strftime('%M:%S', time.gmtime(first_appointment_time + self.line * appointment_intervals)), bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='w') # Defines a Tkinter label.
            self.time_ans_label.place(x=170, y=20, w=250, h=30) # Sets the geometry of the label.
            
            self.hairdresser_label = tk.Label(self.master, text='Hairdresser:', bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='e') # Defines a Tkinter label.
            self.hairdresser_label.place(x=0, y=70, w=165, h=30) # Sets the geometry of the label.
            self.hairdresser_ans_label = tk.Label(self.master, text=(main_window.hairdressers[self.lb][1] + ' ' + main_window.hairdressers[self.lb][3] + main_window.hairdressers[self.lb][2]), bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='w') # Defines a Tkinter label.
            self.hairdresser_ans_label.place(x=170, y=70, w=250, h=30) # Sets the geometry of the label.
            
            self.client_label = tk.Label(self.master, text='Client:', bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='e') # Defines a Tkinter label.
            self.client_label.place(x=0, y=120, w=165, h=30) # Sets the geometry of the label.

            self.haircut_label = tk.Label(self.master, text='Haircut:', bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='e') # Defines a Tkinter label.
            self.haircut_label.place(x=0, y=170, w=165, h=30) # Sets the geometry of the label.

            self.duration_label = tk.Label(self.master, text='Duration:', bg=bg_colour, fg=text_colour, font=(primary_font, 12), anchor='e') # Defines a Tkinter label.
            self.duration_label.place(x=0, y=220, w=165, h=30) # Sets the geometry of the label.
            
        ### TKINTER COMBOBOXES (DROPDOWN MENUS)
            self.client_box = ttk.Combobox(self.master, textvariable=self.client_var, font=(secondary_font, 9), state='readonly') # Defines a Tkinter combo box (drop-down menu).
            self.client_box['values'] = self.client_names # Sets the options of this drop-down menu to the values in the following array.
            self.client_box.place(x=170, y=120, w=250, h=30) # Sets the drop-down menu's geometry.
            self.client_box.bind('<Return>', lambda event: self.client_box.event_generate('<Down>')) # Make the drop-down menu drop down when the user presses the enter/return key while this widget is focused.
            self.client_box.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.
            self.client_box.bind('<<ComboboxSelected>>', lambda event: self.open_add_client_window(False)) # Runs the following function when the user presses the enter/return key while this widget is focused.
               
            self.haircut_box = ttk.Combobox(self.master, textvariable=self.haircut_var, font=(secondary_font, 9), state='readonly') # Defines a Tkinter combo box (drop-down menu).
            self.haircut_box['values'] = self.haircut_names # Sets the options of this drop-down menu to the values in the following array.
            self.haircut_box.place(x=170, y=170, w=250, h=30) # Sets the drop-down menu's geometry.
            self.haircut_box.bind('<Return>', lambda event: self.haircut_box.event_generate('<Down>')) # Make the drop-down menu drop down when the user presses the enter/return key while this widget is focused.
            self.haircut_box.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.
            self.haircut_box.bind('<<ComboboxSelected>>', lambda event: self.duration_box.current(int((self.haircuts[self.haircut_box.current()][3])/appointment_intervals)-1))  # Runs the following function when the user presses the enter/return key while this widget is focused.
            
            self.duration_box = ttk.Combobox(self.master, textvariable=self.duration_var, font=(secondary_font, 9), state='readonly') # Defines a Tkinter combo box (drop-down menu).
            self.duration_box['values'] = self.durations # Sets the options of this drop-down menu to the values in the following array.
            self.duration_box.place(x=170, y=220, w=250, h=30) # Sets the drop-down menu's geometry.
            self.duration_box.bind('<Return>', lambda event: self.duration_box.event_generate('<Down>')) # Make the drop-down menu drop down when the user presses the enter/return key while this widget is focused.
            self.duration_box.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        ### TKINTER BUTTONS
            self.add_client_button = tk.Button(self.master, text='+', command= lambda: self.open_add_client_window(True), bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
            self.add_client_button.place(x=420, y=120, w=30, h=30) # Sets the button's geometry.
            self.add_client_button.bind('<Return>', lambda event: self.open_add_client_window(True)) # Runs the following function when the user presses the enter/return key while this widget is focused.
            self.add_client_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

            self.add_appointment_button = tk.Button(self.master, text='Add appointment', command=self.add_appointment, bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
            self.add_appointment_button.place(x=380, y=310, w=140, h=30) # Sets the button's geometry.
            self.add_appointment_button.bind('<Return>', lambda event: self.add_appointment()) # Runs the following function when the user presses the enter/return key while this widget is focused.
            self.add_appointment_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

            self.cancel_appointment_button = tk.Button(self.master, text='Cancel', command=lambda: [self.master.destroy(), main_window.lbs[self.day][self.lb+1].selection_clear(0, tk.END)], bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
            self.cancel_appointment_button.place(x=290, y=310, w=75, h=30) # Sets the button's geometry.
            self.cancel_appointment_button.bind('<Return>', lambda event: self.master.destroy()) # Runs the following function when the user presses the enter/return key while this widget is focused.
            self.cancel_appointment_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

    ### MANAGING EXISTING APPOINTMENT    
        else:
            
        ### MORE TKINTER WINDOW CONFIG
            self.master.title('Manage Appointment (Version {})'.format(version)) # Sets the window's title.

        ### FETCHING DATA FROM DATABASE
            c.execute('SELECT ClientID, HaircutID, StartTime, Duration, Date, AmountPaid FROM Appointments WHERE AppointmentID=?', (self.id,)) # Retrieves the appointment information for the appointment with matching id.
            self.appointment = c.fetchone() # Fetches the result from the query.
            
            c.execute('SELECT FirstName, LastName FROM Clients WHERE ClientID=?', (self.appointment[0],)) # Retrieves the first and last name for the client with matching id.
            self.client = c.fetchone() # Fetches the result from the query.
            
            c.execute('SELECT Haircut, Price FROM Haircuts WHERE HaircutID=?', (self.appointment[1],)) # Retrieves the haircut name and price for the haircut with matching id.
            self.haircut = c.fetchone() # Fetches the result from the query.
            
            db_close()
            
        ### TKINTER LABELS
            self.time_label = tk.Label(self.master, text='Time:', bg=bg_colour , fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.time_label.place(x=0, y=20, w=165, h=30) # Sets the label's geometry.
            self.time_ans_label = tk.Label(self.master, text=(self.appointment[2] + ' to ' + time.strftime('%M:%S', time.gmtime(int(self.appointment[2].split(':')[0]) * 60 + int(self.appointment[2].split(':')[1]) + self.appointment[3]))), bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.time_ans_label.place(x=170, y=20, w=250, h=30) # Sets the label's geometry.

            self.date_label = tk.Label(self.master, text='Date:', bg=bg_colour, fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.date_label.place(x=0, y=50, w=165, h=30) # Sets the label's geometry.
            self.date_ans_label = tk.Label(self.master, text=self.appointment[4], bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.date_ans_label.place(x=170, y=50, w=250, h=30) # Sets the label's geometry.
            
            self.hairdresser_label = tk.Label(self.master, text='Hairdresser:', bg=bg_colour, fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.hairdresser_label.place(x=0, y=80, w=165, h=30) # Sets the label's geometry.
            self.hairdresser_ans_label = tk.Label(self.master, text=(main_window.hairdressers[self.lb][1] + ' ' + main_window.hairdressers[self.lb][3] + main_window.hairdressers[self.lb][2]), bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.hairdresser_ans_label.place(x=170, y=80, w=250, h=30) # Sets the label's geometry.
            
            self.client_label = tk.Label(self.master, text='Client:', bg=bg_colour, fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.client_label.place(x=0, y=110, w=165, h=30) # Sets the label's geometry.
            self.client_ans_label = tk.Label(self.master, text=(self.client[0] + ' ' +  self.client[1]), bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.client_ans_label.place(x=170, y=110, w=250, h=30) # Sets the label's geometry.

            self.haircut_label = tk.Label(self.master, text='Haircut:', bg=bg_colour, fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.haircut_label.place(x=0, y=140, w=165, h=30) # Sets the label's geometry.
            self.haircut_ans_label = tk.Label(self.master, text=self.haircut[0], bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.haircut_ans_label.place(x=170, y=140, w=250, h=30) # Sets the label's geometry.

            self.amount_to_pay_label = tk.Label(self.master, bg=bg_colour, fg=text_colour, font=primary_font, anchor='e') # Defines a Tkinter label.
            self.amount_to_pay_label.place(x=0, y=170, w=165, h=30) # Sets the label's geometry.
            self.amount_to_pay_ans_label = tk.Label(self.master, bg=bg_colour, fg=text_colour, font=primary_font, anchor='w') # Defines a Tkinter label.
            self.amount_to_pay_ans_label.place(x=170, y=170, w=250, h=30) # Sets the label's geometry.

        ### TKINTER BUTTONS
            self.cancel_appointment_button = tk.Button(self.master, text='Cancel Appointment', command=self.cancel_appointment, bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
            self.cancel_appointment_button.place(x=360, y=310, w=160, h=30) # Sets the geometry of the button.
            self.cancel_appointment_button.bind('<Return>', lambda event: self.cancel_appointment()) # Runs the following function when the user presses the enter/return key while this widget is focused.
            self.cancel_appointment_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

            self.dismiss_button = tk.Button(self.master, text='Dismiss', command=lambda: [self.master.destroy(), main_window.lbs[self.day][self.lb+1].selection_clear(0, tk.END)], bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
            self.dismiss_button.place(x=270, y=310, w=75, h=30)# Sets the geometry of the button.
            self.dismiss_button.bind('<Return>', lambda event: self.master.destroy()) # Runs the following function when the user presses the enter/return key while this widget is focused.
            self.dismiss_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        ### IF APPOINTMENT NOT PAID
            if self.appointment[5] == None: # If appointment is not paid.
                
            ### MORE TKINTER LABELS
                self.amount_to_pay_label.configure(text='Amount to pay:') # Defines a Tkinter label.
                self.amount_to_pay_ans_label.configure(text='£') # Configure an existing label's displayed text.

            ### TKINTER ENTRY BOX
                self.amount_to_pay_var = tk.StringVar() # Defines a Tkinter string variable.
                self.amount_to_pay_entry = tk.Entry(self.master, textvariable=self.amount_to_pay_var, fg=text_colour, font=secondary_font) # Defines a Tkinter entry box.
                self.amount_to_pay_entry.insert(tk.END, '{:0.2f}'.format(self.haircut[1] * self.rate * 0.01)) # Insert the amount to pay as a string into the entry box (in X.YY format where X is a number and Y are digits).
                self.amount_to_pay_entry.place(x=185, y=170, w=235, h=30) # Sets the entry boxes' geometry.
                self.amount_to_pay_entry.bind('<Return>', lambda event: self.pay_appointment()) # Runs the following function when the user presses the enter/return key while this widget is focused.
                self.amount_to_pay_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

            ### MORE TKINER BUTTONS
                self.mark_as_paid_button = tk.Button(self.master, text='Mark appointment as paid', command=lambda: self.pay_appointment(), bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
                self.mark_as_paid_button.place(x=170, y=210, w=250, h=30) # Sets the button's geometry.
                self.mark_as_paid_button.bind('<Return>', lambda event: self.pay_appointment()) # Runs the following function when the user presses the enter/return key while this widget is focused.
                self.mark_as_paid_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        ### IF APPOINTMENT PAID         
            else:
                self.amount_to_pay_label.config(text='Amount paid:') # Defines a Tkinter label.
                self.amount_to_pay_ans_label.configure(text='£{:0.2f}'.format(self.appointment[5])) # Configure an existing label's displayed text.

### 'APPOINTMENT' CLASS FUNCTIONS      
    def add_appointment(self):
        '''This function adds an appointment to the database. It will first check if any fields are empty and if the appointment overlaps with any other appointments.'''
        if self.client_var.get() == '' or self.haircut_var.get() == '': # If either of the drop-down menus are empty.
            messagebox.showinfo('Error: Empty Field(s)', 'Please ensure all the fields are filled to make an appointment.') # Displays a Tkinter error window (popup).
        else:
            haircut = self.haircut_box.current() # Defines a new variable equal to the selected option's index in the array.
            duration = self.duration_box.current() # Defines a new variable equal to the selected option's index in the array.
            client = self.client_box.current() # Defines a new variable equal to the selected option's index in the array.
            
            for i in range(duration): # Loop for index of selected duration.
                if main_window.lbs[self.day][self.lb+1].appointment_id[self.line+i+1] != -1: # If the appointment slot is already booked.
                    messagebox.showerror('Error: Overlapping Appointments', 'This appointment cannot be made because it overlaps with another. Please reschedule or if possible shorten the duration of the appointment.') # Displays a Tkinter error window (popup).
                    return # End the function early.
                           
            db_open() # Creates a connection and cursor with the database.
            c.execute('INSERT INTO Appointments(StaffID, ClientID, HaircutID, StartTime, Duration, Date) VALUES(?, ?, ?, ?, ?, ?)', (main_window.hairdressers[self.lb][0], self.clients[client][0], self.haircuts[haircut][0], time.strftime('%M:%S', time.gmtime(first_appointment_time + self.line * appointment_intervals)), ((duration+1)*appointment_intervals), working_dates[self.day].strftime('%d/%m/%Y'))) # Insert a new appointment into the Appointments table.
            conn.commit() # Commit the change to the database.
            db_close() # Closes the connection and cursor with the database.
            
            self.master.destroy() # Destroy the appointments window.
            main_window.update_table() # Update the table in main window to show the new appointment.
            log('{} {} booked the following appointment: {} for {} booked with {} {}{} at {} on {}.'.format(user[1], user[2], self.haircuts[haircut][1], self.client_var.get(), main_window.hairdressers[self.lb][1], main_window.hairdressers[self.lb][3], main_window.hairdressers[self.lb][2], time.strftime('%M:%S', time.gmtime(first_appointment_time + self.line * appointment_intervals)), working_dates[self.day].strftime('%d/%m/%Y'))) # Log the new appointment in the console.

    def pay_appointment(self):
        '''This function is called when the user clicks the pay appointment button. It will mark the appointment paid with the amount in the entry box.'''
        amount_to_pay = self.amount_to_pay_var.get() # Define a new string equal to the value in the corresponding entry box.
        try: # Try the following code.
            float(amount_to_pay) # Convert the variable to a float.
        except ValueError: # If the variable could not be converted to a float.
            messagebox.showerror('Error: Must be a float value', 'The value you entered is not number or a float value.') # Displays a Tkinter error window (popup).
            return # End the function early.
        
        if float(amount_to_pay) < 0: # If negative.
            messagebox.showerror('Error: Negative Payment', 'The amount to pay cannot be negative.') # Displays a Tkinter error window (popup).
            return # End the function early.
        
        db_open() # Creates a connection and cursor with the database.
        c.execute('UPDATE Appointments SET AmountPaid=? WHERE AppointmentID=?', (amount_to_pay, self.id)) # Edit the record to show it's paid.
        conn.commit() # Commit the change to the database.
        db_close() # Closes the connection and cursor with the database.

        self.amount_to_pay_label.configure(text='Amount paid:') # Change the text in the label to show it's paid.
        self.amount_to_pay_ans_label.configure(text='£{:0.2f}'.format(float(amount_to_pay))) # Show the amount paid by a label.

        self.amount_to_pay_entry.destroy() # Destroy the entry box as it's no longer needed.
        self.mark_as_paid_button.config(relief=tk.SUNKEN) # Set the button's state to sunken as it's no longer needed.
        

    def cancel_appointment(self):
        '''This function is called when the user clicks the cancel appointment button. It will remove the appointment from the database.'''
        db_open()  # Creates a connection and cursor with the database.
        c.execute('SELECT AmountPaid FROM Appointments WHERE AppointmentID=?', (self.id,)) # Retieve the amount paid for the appointment.
        if c.fetchone()[0] != 0: # If the appointment has been paid.
            db_close() # Closes the connection and cursor with the database.
            if not messagebox.askyesno('Confimation: Appointment has been paid', 'This appointment has been paid for. Please refund the client before cancelling. Do you want to continue?'): # Displays a Tkinter confirmation window (popup).
                return # Ends the function early.
        else:
            db_close() # Closes the connection and cursor with the database.
        if messagebox.askyesno('Confirmation: Cancel appointment', 'Are you sure you want to cancel this appointment? This change cannot be undone. Do you want to continue?'): # Displays a Tkinter confirmation window (popup). 
            db_open()  # Creates a connection and cursor with the database.
            c.execute('DELETE FROM Appointments WHERE AppointmentID=?', (self.id,)) # Deletes the appointment from the database.
            conn.commit() # Commits the change to the database.
            db_close() # Closes the connection and cursor with the database.
            self.master.destroy() # Destroy the appointments window.
            main_window.update_table() # Update the table in the main window.
            log('{} {} cancelled the following appointment: {} for {} {} booked with {} {}{} at {} on {}.'.format(user[1], user[2], self.haircut[0], self.client[0], self.client[1], main_window.hairdressers[self.lb][1], main_window.hairdressers[self.lb][3], main_window.hairdressers[self.lb][2], time.strftime('%M:%S', time.gmtime(first_appointment_time + self.line * appointment_intervals)), working_dates[self.day].strftime('%d/%m/%Y'))) # Log who deleted the appointment in the console.

    def open_add_client_window(self, called_by_button):
        '''This function is called when the user clicks the button or selects the last option in the client drop-down menu. It opens the AddClient window.'''
        if self.client_var.get() == '--- Add new client ---' or called_by_button == True: # If last option of the client drop-down menu is selected or the function was called by the button.
            self.client_box.set('') # Unselect any options selected in the client's drop-down menu.
            
            popup = tk.Toplevel(self.master) # Defines a Tkinter toplevel window (popup window).
            global add_client_window # Declare the variable 'add_client_window' globally.
            add_client_window = AddClient(popup) # Create an instance of the AddClient class.
            popup.mainloop() # Wait until the add client window is closed until proceeding.

#======================================================================================
#                                   ADDING CLIENTS WINDOW 
#======================================================================================
class AddClient():
    '''This window consists of entry boxes allowing the user to add a client to the database. This is a quicker way to add clients without going into the client table. It also does not require admin rights to perform. This window can be opened in the appointments window by a button or by a drop-down menu.'''
    def __init__(self, master):
        '''This function is run when the class is initialised.'''
    ### VARIABLES
        self.master = master # Defines the variable 'master' as an attribute to this class.
        self.first_name_var = tk.StringVar() # Defines a Tkinter string variable.
        self.last_name_var = tk.StringVar() # Defines a Tkinter string variable.
        self.mobile_phone_var = tk.StringVar() # Defines a Tkinter string variable.
        self.home_phone_var = tk.StringVar() # Defines a Tkinter string variable.
        
    ### TKINTER WINDOW CONFIG
        self.master.title('Add Client (Version {})'.format(version)) # Sets window's title.
        self.master.geometry('270x180+{}+{}'.format(((screen_width-270)//2), ((screen_height-180)//2)))  # Sets window geometry and centers the window.
        self.master.resizable(False, False) # Sets the window so it cannot be resized.
        self.master.wm_iconbitmap('resources/icon.ico') # Sets window's icon.
        self.master.config(bg=bg_colour) # Sets background colour of window.
        self.master.protocol('WM_DELETE_WINDOW', lambda: [self.master.destroy(), appointments_window.master.focus_set(), appointments_window.master.grab_set()]) # Runs the following functions when this window is closed.
        
        appointments_window.master.grab_release() # Release the grab of appointments window (to be transferred to this window).
        self.master.focus_set() # Sets focus on this window.
        self.master.grab_set() # Sets grab on this window, so other windows cannot take the focus.

        # TKINTER LABELS
        self.first_name_label = tk.Label(self.master, text='First Name:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.first_name_label.place(x=0, y=10, w=90, h=25) # Sets the label's geometry.

        self.last_name_label = tk.Label(self.master, text='Last Name:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.last_name_label.place(x=0, y=40, w=90, h=25) # Sets the label's geometry.

        self.mobile_phone_label = tk.Label(self.master, text='Mobile Phone:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.mobile_phone_label.place(x=0, y=70, w=90, h=25) # Sets the label's geometry.

        self.home_phone_label = tk.Label(self.master, text='Home Phone:', bg=bg_colour, fg=text_colour, font=(primary_font, 10), anchor='e') # Defines a Tkinter label.
        self.home_phone_label.place(x=0, y=100, w=90, h=25) # Sets the label's geometry.
                                            
        # TKINTER ENTRY BOXES
        self.first_name_entry = tk.Entry(self.master, textvariable=self.first_name_var, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter entry box.
        self.first_name_entry.place(x=95, y=10, w=150, h=25) # Sets the entry boxes' geometry.
        self.first_name_entry.bind('<Return>', lambda event: self.last_name_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.first_name_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.
        self.first_name_entry.focus()

        self.last_name_entry = tk.Entry(self.master, textvariable=self.last_name_var, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter entry box.
        self.last_name_entry.place(x=95, y=40, w=150, h=25) # Sets the entry boxes' geometry.
        self.last_name_entry.bind('<Return>', lambda event: self.mobile_phone_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.last_name_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        self.mobile_phone_entry = tk.Entry(self.master, textvariable=self.mobile_phone_var, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter entry box.
        self.mobile_phone_entry.place(x=95, y=70, w=150, h=25) # Sets the entry boxes' geometry.
        self.mobile_phone_entry.bind('<Return>', lambda event: self.home_phone_entry.focus()) # When pressing the return key while this widget is focused, will shift focus to the next widget.
        self.mobile_phone_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        self.home_phone_entry = tk.Entry(self.master, textvariable=self.home_phone_var, fg=text_colour, font=(secondary_font, 9)) # Defines a Tkinter entry box.
        self.home_phone_entry.place(x=95, y=100, w=150, h=25) # Sets the entry boxes' geometry.
        self.home_phone_entry.bind('<Return>', lambda event: self.add_client()) # When pressing the return key while this widget is focused, run the following function.
        self.home_phone_entry.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        # TKINTER BUTTONS
        self.add_client_button = tk.Button(self.master, text='Add Client', command=lambda: self.add_client(), bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
        self.add_client_button.place(x=110, y=140, w=140, h=30) # Sets the button's geometry.
        self.add_client_button.bind('<Return>', lambda event: self.add_client()) # When pressing the return key while this widget is focused, run the following function.
        self.add_client_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        self.cancel_button = tk.Button(self.master, text='Cancel', command=lambda: [self.master.destroy(), appointments_window.master.focus_set(), appointments_window.master.grab_set()], bg=bg_colour, fg=text_colour, font=primary_font) # Defines a Tkinter button.
        self.cancel_button.place(x=30, y=140, w=65, h=30) # Sets the button's geometry.
        self.cancel_button.bind('<Return>', lambda event: [self.master.destroy(), appointments_window.master.focus_set(), appointments_window.master.grab_set()]) # When pressing the return key while this widget is focused, run the following functions
        self.cancel_button.bind('<Escape>', lambda event: self.master.focus()) # Unfocuses this widget when the user presses the escape key.

        
### 'ADDCLIENT' CLASS FUNCTIONS 
    def add_client(self):
        '''This function validates the values entered into the entry boxes. If valid, will add the client to the database. This function is called by the add client button.'''
    ### VARIABLES
        first_name = self.first_name_var.get().replace(' ', '') # Defines a new string with the value in the corresponding entry box. It also removes any space characters in the process.
        last_name = self.last_name_var.get().replace(' ', '') # Defines a new string with the value in the corresponding entry box. It also removes any space characters in the process.
        mobile_phone = self.mobile_phone_var.get().replace(' ', '') # Defines a new string with the value in the corresponding entry box. It also removes any space characters in the process.
        home_phone = self.home_phone_var.get().replace(' ', '') # Defines a new string with the value in the corresponding entry box. It also removes any space characters in the process.
        
    ### EMPTY FIELD(S)
        if first_name == '' or last_name == '': # If any of the name fields are empty.
            messagebox.showerror('Error: Empty Field(s)', 'You cannot have any empty fields') # Displays a Tkinter error window (popup).
            return # Ends the function early.

    ### CHECK NAMES ARE ALPHABETICALLY
        if not ((first_name.isalpha() or first_name == '') and (last_name.isalpha()) or last_name ==''): # If the names only consist of alphabetically characters (or are blank).
            messagebox.showerror('Error: Incompatible characters', 'Names must contain only alphabetically characters. Please try again.') # Displays a Tkinter error window (popup).
            return # Ends the function early.
        
    ### CHECKS PHONE NUMBER CONTAINS ONLY DIGITS AND CORRECT AMOUNT OF DIGITS
        if not ((mobile_phone.isdigit() or mobile_phone == '') and (home_phone.isdigit()) or home_phone ==''): # If the phone numbers consist of only digits (or are blank).
            messagebox.showerror('Error: Incompatible characters', 'Phone number must contain only digits. Please try again.') # Displays a Tkinter error window (popup).
            return # Ends the function early.
            
        if not((len(mobile_phone) in {10, 11} or mobile_phone == '') and (len(home_phone) in {10, 11} or home_phone == '')): # If the phone numbers consist of 10 or 11 characters (or are blank).
            if not messagebox.askyesno('Confirmation: Phone Number(s) length(s)', 'Phone number should contain 10 or 11 digits. Do you want to continue?'): # Displays a Tkinter confirmation window (popup).
                return # Ends the function early.
    ### MORE EMPTY FIELD(S)
        if mobile_phone == '' and home_phone == '': # If any of the phone number fields are empty.
            if not messagebox.askyesno('Confirmation: No Phone Number', 'We recommended atleast one phone number to contact and inform clients of cancellations. Are you sure you want to continue?'): # Displays a Tkinter confirmation window (popup).
                return # Ends the function early.
            
    ### CHECK CLIENT DOES NOT ALREADY EXIST ON DATABASE      
        db_open()
        c.execute('SELECT Mobile, Home FROM Clients WHERE (FirstName=? AND LastName=? AND (Mobile=? OR Home=?))', (first_name, last_name, mobile_phone, home_phone)) # Retrieve any records of clients that have matching names and at least one matching phone number.
        if c.fetchone() != None: # If any matching records.
            if not messagebox.askyesno('Confirmation: Duplicates may exist!', 'There is already a client with this name who shares the same phone number(s). Please ensure this new client is not already on the database. Do you want to continue?'): # Displays a Tkinter confirmation window (popup).
                    return # Ends the function early.
        db_close()

    ### ADD CLIENT TO DATABASE
        db_open()
        if mobile_phone == '' and home_phone == '': # If no phone numbers were given.
            c.execute('INSERT INTO Clients(FirstName, LastName) VALUES(?, ?)', (first_name, last_name)) # Add a new client record with only the names provided.
        elif mobile_phone == '': # If only the home phone number was given.
            c.execute('INSERT INTO Clients(FirstName, LastName, Home) VALUES(?, ?, ?)', (first_name, last_name, home_phone)) # Add a new client record with the names and the home phone number provided.
        elif home_phone == '': # If only the mobile phone number was given.
            c.execute('INSERT INTO Clients(FirstName, LastName, Mobile) VALUES(?, ?, ?)', (first_name, last_name, mobile_phone)) # Add a new client record with the names and the mobile phone number provided.
        else: # # If both phone numbers were given.
            c.execute('INSERT INTO Clients(FirstName, LastName, Mobile, Home) VALUES(?, ?, ?, ?)', (first_name, last_name, mobile_phone, home_phone)) # Add a new client record with the names and phone numbers provided.
        conn.commit() # Commit the change to the database.
        
        c.execute('SELECT ClientID, FirstName, LastName FROM Clients') # Retrive the new client records.
        appointments_window.clients = c.fetchall() # Update the client records of the 2D array stored as an attribute of the appointments window.
        db_close()
        
        appointments_window.client_names = [] # Redefines the variable as an empty array.
        for i in range(len(appointments_window.clients)): # For all clients.
            appointments_window.client_names.append('{} {}'.format(appointments_window.clients[i][1], appointments_window.clients[i][2])) # Put the client's first name and surname together to make it an option for a drop-down menu.
        appointments_window.client_names.append('--- Add new client ---') # Add a last option to add a new client.
        appointments_window.client_box['values'] = appointments_window.client_names # Resets the options of this drop-down menu to the values in the following array.
        appointments_window.client_box.current(len(appointments_window.client_names)-2) # Set the currently selected client as the one just added.
        
        self.master.destroy() # Destroys the add client window.
        appointments_window.master.focus_set() # Sets focus back on the appointments window.
        appointments_window.master.grab_set() # Sets the grab back on the appointments window, so other windows cannot take focus.
            
            
if __name__ == '__main__': # Only runs the following code if the program is the main program and is not imported into another.
    main() # Calls the main function.
