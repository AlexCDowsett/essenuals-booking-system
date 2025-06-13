#
# Author: Alex Dowsett
#
# Last updated: 25/06/2018
#
#--------------------------------------------------------------------------------------
version = '0.2'
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import sqlite3
import time
import datetime

# Options:
width_login = 540 # Width of login window (in pixels).
height_login = 360 # Height of login window (in pixels).
bg_colour = '#E7E8EA' # Blackground colour in hexadecimal.
text_colour = '#000000' # Text colour in hexadecimal.
colour_1 = '#A09D9C' # Defines a string that holds the 1st colour in hexadecimal.
colour_2 = '#343038' # Defines a string that holds the 2nd colour in hexadecimal.
font_1 = 'Helvetica' # Defines a string that holds the first font.
font_2 = 'Courier' # Defines a string that holds the second font.

class Login:
    """A login window for security. A username and password is required to acess the system."""
    def __init__(self, root): # Defines the function that initialises the class.
        root.title("Essentials Booking System Login (Version {})".format(version)) # Sets window's title.
        x = (root.winfo_screenwidth()-width_login)//2 # Finds center x co-ord.
        y = (root.winfo_screenheight()-height_login)//2 # Finds center y co-ord.
        root.geometry('{}x{}+{}+{}'.format(width_login, height_login, x, y))  # Sets window geometry & centers the window.
        root.resizable(False, False) # Sets the window so it cannot be resized.
        root.wm_iconbitmap("icon.ico") # Sets icon.
        root.config(bg=bg_colour) # Sets background colour of window.
        
        # Visual labels
        self.topLabel = tk.Label(root, bg=colour_1) # Defines a Tkinter label.
        self.topLabel.place(x=0, y=0, w=width_login, h=60) # Set's the label's geometry.
        self.bottomLabel = tk.Label(root, bg=colour_2, fg='#FFFFFF', text="Programmed by Alex Dowsett", font=(font_1+' 7')) # Defines a Tkinter label.
        self.bottomLabel.place(x=0, y=height_login-35, w=width_login, h=35) # Set's the label's geometry.
        self.title_small = tk.PhotoImage(file='title_small.png') # Defines a Tkinter photo image to hold the image for the header.
        self.imageLabel = tk.Label(root, bg=colour_1, image=self.title_small) # Defines a Tkinter label.
        self.imageLabel.place(x=240, y=5, w=281, h=50) # Set's the label's geometry.
        self.imageLabel.image = self.title_small # Set's the label's image to Tkinter photo image.
        
        # Text labels & entry boxes
        self.staffID = tk.StringVar() # Defines a Tkinter string variable.
        self.password = tk.StringVar() # Defines a Tkinter string variable.
        self.staffIDLabel = tk.Label(root, text="Staff ID:", bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter label.
        self.staffIDLabel.place(x=100, y=120, w=80, h=25) # Set's the label's geometry.
        self.passwordLabel = tk.Label(root, text="Password:", bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter label.
        self.passwordLabel.place(x =100, y=160, w=80, h=25) # Set's the label's geometry.
        self.staffIDEntry = tk.Entry(root, textvariable=self.staffID, fg=text_colour, font=font_2) # Defines a Tkinter entry box.
        self.staffIDEntry.place(x=200, y=120, w=200, h=25) # Set's the entry boxes' geometry.
        self.staffIDEntry.bind("<Return>", lambda x: self.passwordEntry.focus()) # Binds the following function to the return/enter key.
        self.staffIDEntry.bind("<Escape>", lambda x: self.staffIDEntry.nametowidget(".").focus()) # Unfocuses this widget when the user presses the escape key.
        self.staffIDEntry.focus() # Set's the focus on this entry box.
        self.passwordEntry = tk.Entry(root, textvariable=self.password, fg=text_colour, font=font_2, show="*") # Defines a Tkinter entry box.
        self.passwordEntry.place(x=200, y=160, w=200, h=25) # Set's the entry boxes' geometry.
        self.passwordEntry.bind("<Return>", lambda x: self.login(root)) # Binds the login function to the return/enter key while this widget is focused.
        self.passwordEntry.bind("<Escape>", lambda x: self.passwordEntry.nametowidget(".").focus()) # Unfocuses this widget when the user presses the escape key.
        
        # Buttons & clickable labels
        self.loginButton = tk.Button(root, text="Login", command=lambda: self.login(root), bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter button.
        self.loginButton.place(x=320, y=200, w=80, h=30) # Set's the button's geometry.
        self.loginButton.bind("<Return>", lambda x: self.login(root)) # Binds the login function to the return/enter key while this button is focused.
        self.loginButton.bind("<Escape>", lambda x: self.loginButton.nametowidget(".").focus()) # Unfocuses this widget when the user presses the escape key.
        self.helpLabel = tk.Label(root, text="Do not know your details?", bg=bg_colour, fg=text_colour, font=(font_1+' 12')) # Defines a Tkinter label.
        self.helpLabel.place(x=100, y=202, w=180, h=25) # Set's the label's geometry.
        self.helpLabel.bind("<Button-1>", self.login_info) # Runs the login_info function when this label is left clicked.
        self.helpLabel.bind("<Enter>", lambda x: self.helpLabel.configure(font=(font_1+' 12 underline'))) # Underlines the text that this label displays when the cursor is over the label.
        self.helpLabel.bind("<Leave>", lambda x: self.helpLabel.configure(font=(font_1+' 12'))) # Revert the text to the original when the cursor leaves this label.

        #SQL startup
        conn = sqlite3.connect('bookings.db') # Starts a connection to the database.
        c = conn.cursor() # Starts an interaction with the database.
        c.execute('CREATE TABLE IF NOT EXISTS Staff(StaffID INTEGER PRIMARY KEY, FirstName VARCHAR(255) NOT NULL, LastName VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL, IsAdmin BIT DEFAULT 0)') #  Creates the Staff Table.
        conn.commit() # Commits the change to the database.
        c.execute('SELECT COUNT(*) FROM Staff') # Retrieves the amount of records in the Staff Table.
        if c.fetchone()[0] == 0: # If no records are found (in other words, the database has just been created).
            print("Database not found. Creating a new one.") # Print a message to the console.
            c.execute("INSERT INTO Staff (FirstName, LastName, Password, isAdmin) VALUES('admin', 'admin', 'ess19', 1)") # Insert a record into staff so you can log in.
            c.execute('CREATE TABLE Options(OptionID INTEGER PRIMARY KEY, OptionName VARCHAR(255) NOT NULL, OptionValue VARCHAR(255) NOT NULL)') # Create a Options table.
        conn.commit() # Commits the change to the database.
        c.close() # Closes the interaction.
        conn.close() # Closes the connection to the database.
        
    def login_info(self, root): # Defines a function that is run when the user needs help with logging in.
        tk.messagebox.showinfo("Login details", "Ask your manager for your login details\n or view 'README.txt'.") # Displays a Tkinter information window (popup).

    def login(self, root): # Defines a function that is run when the user clicks the login button. The function compares the inputted Staff ID and password to the ones in the database and acts accordingly.
        global ID # Makes the ID variable global.
        ID = self.staffID.get() # Defines ID, a string found in the corresponding Tkinter string variable.
        p = self.password.get() # Defines password, a string found in the corresponding Tkinter string variable.
        if ID == '' or p == '': # If either of the strings are empty.
            tk.messagebox.showerror("Empty field(s)", "Please ensure you have entered both your Staff ID and password.") # Displays a Tkinter error window (popup).
            self.staffIDEntry.delete(0, tk.END) # Clears the content of this entry box.
            self.passwordEntry.delete(0, tk.END) # Clears the content of this entry box.
            self.staffIDEntry.focus() # Sets the focus on this entry box.
            return # End this function early.
        staff_details = None # Otherwise define a new variable with an unspecified datatype.
        if ID.isdigit(): # If the ID consists of only digits.
            conn = sqlite3.connect('bookings.db') # Starts a connection to the database.
            c = conn.cursor() # Starts an interaction with the database.
            c.execute('SELECT * FROM Staff WHERE StaffID=?', (ID,)) # Retrieve the record that has a Staff ID of 'ID'.
            staff_details = c.fetchone() # Fetch that record.
            c.close() # Closes the interaction. 
            conn.close() # Closes the connection to the database.
        if not staff_details == None and p == staff_details[3]: # If the record exists and the password matches.
            first_name = staff_details[1] # Defines a new string.
            last_name = staff_details[2] # Defines a new string.
            if staff_details[3] == 0: # If the user is not an admin.
                staff_details[3] = False # Convert it to a boolean.
            elif staff_details[3] == 1: # If the user is an admin.
                staff_details[3] = True # Convert it to a boolean.
            root.destroy() # Destroy the login window.
            master = tk.Tk() # Define a new Tkinter window to be used in the main window.
            main_window = Main(master) # Creates an instance of the class 'Main'.
            master.mainloop() # Waits for the master window to close before proceeding.
        else:
            tk.messagebox.showerror("Incorrect login details", "Your ID or password is incorrect. Please check your details and try again.") # Displays a Tkinter error window (popup).
            self.staffIDEntry.delete(0, tk.END) # Clears the content of this entry box.
            self.passwordEntry.delete(0, tk.END) # Clears the content of this entry box.
            self.staffIDEntry.focus() # Focuses this entry box.

class Main():
    def __init__(self, main): # Creates a new Tkinter window named root.
        main.title("Essentials Booking System (Version {})".format(version)) # Sets the window's title.
        main.state('zoomed') # Set the state of this window as zoomed.
        main.wm_iconbitmap("icon.ico") # Set's the window's icon.
        main.config(bg=bg_colour) # Sets background colour of window.
        
        # Visual labels
        self.topLabel = tk.Label(main, bg=colour_1) # Defines a Tkinter label.
        self.topLabel.place(x=0, y=0, w=main.winfo_width(), h=80) # Set's the label's geometry.
        self.bottomLabel = tk.Label(main, bg=colour_2, fg='#FFFFFF', text="Programmed by Alex Dowsett", font=(font_1+' 7')) # Defines a Tkinter label.
        self.bottomLabel.place(x=0, y=main.winfo_height()-40, w=main.winfo_width(), h=40) # Set's the label's geometry.
        self.title_large = tk.PhotoImage(file='title_large.png') # Defines a Tkinter photo image that contains the header image.
        self.imageLabel = tk.Label(main, bg=colour_1, image=self.title_large) # Set's the label's to the Tkinter photo image just defined.
        self.imageLabel.place(x=(main.winfo_width()-405), y=6, w=382, h=68) # Set's the label's geometry.
        self.imageLabel.image = self.title_large # Set's the label's image to the header image.

        self.settings_light = tk.PhotoImage(file='settings_light.png') # Defines a new Tkinter photo image.
        self.settings_dark = tk.PhotoImage(file='settings_dark.png') # Defines a new Tkinter photo image.
        self.settingsLabel = tk.Label(main, bg=colour_1, image=self.settings_light) # Set's the label's image to the light version of the settings icon.
        self.settingsLabel.place(x=15, y=15, w=50, h=50) # Set's the label's geometry.
        self.settingsLabel.image = self.settings_light # Sets the label's image.
        self.settingsLabel.bind("<Enter>", lambda x: self.change_settings_dark()) # When the cursor enters this label the following function is called.
        self.settingsLabel.bind("<Leave>", lambda x: self.change_settings_light()) # When the cursor leaves this label the following function is called.
        self.settingsLabel.bind("<Button-1>", lambda x: self.settings(main)) # Runs the following function when this label is left clicked.
        
        tab_font = font.Font(family='Courier', size=12) # Defines a Tkinter font.
        style = ttk.Style() # Defines a Tkinter style.
        style.configure('.', font=tab_font, background=bg_colour) # Configure the defined style to have a font of 'tab_font'
        current_theme =style.theme_use() # Retrieve the current theme used.
        style.theme_settings( current_theme, {  # Set's this theme's style to the
                "TNotebook.Tab": {		# style we defined for Tkinter notebook tabs.
                    "configure": {"padding": [(main.winfo_screenwidth()//25), 5] } } } ) # Add padding to the tabs so they cover the whole table.
        style.theme_use(current_theme) # Set the current theme to the theme we just edited.
        
        appointments = ttk.Notebook(main) # Defines a Tkinter notebook.
        appointments.place(x=main.winfo_screenwidth()//25, y=main.winfo_screenheight()//25 + 80, w=main.winfo_screenwidth()//1.5, h=main.winfo_screenheight()// 1.2 - 100) # Set's the notebook's geometry.
        num_of_appointments = 5 # Defines an integer.
        i = 0 # Defines a integer to be used as a counter for loops.
        columns = [] # Defines an array.
        pages = [] # Defines an array.
        trees = [] # Defines an array.
        scrolls = [] # Defines an array.
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"] # Defines an array.
        data = [ ["val1", "val2", "val3"], # Defines a 2D array to hold example values.
                 ["asd1", "asd2", "asd3"],
                 ["bbb1", "bbb3", "bbb4"],
                 ["ccc1", "ccc3", "ccc4"],
                 ["ddd1", "ddd3", "ddd4"],
                 ["eee1", "eee3", "eee4"] ]
        for i in range(num_of_appointments+1): # For all appointments.
            columns.append(i+1) # Add a integer value of (I+1).
        for i in range(6): # Loop 6 times.
            pages.append(ttk.Frame(appointments)) # Appends a Tkinter frame to this array.
            appointments.add(pages[i], text=days[i]) # Add this frame as a tab to the notebook.
            #pages[i].pack(fill = 'both', expand = 1, padx = 10, pady = 10) # Expand the frame to fill the whole notebook while a boarder of 10 pixels around this frame.
            trees.append(ttk.Treeview(pages[i], columns = columns, height = 5, show = "headings")) # Appends a Tkinter tree view (table) to this array.
            trees[i].pack(side = 'left', fill="both", expand=True) # Pack the table to fill the whole frame.
            for j in range(num_of_appointments+1): # For all appointments + 1
                if j == 1: # If its the first column.
                    trees[i].heading(1, text="Time") # Set the column heading to 'Time' (as the first column holds all the appointment times).
                else:
                    trees[i].heading(j, text=j) # Otherwise set the column heading to the value of j.
                trees[i].column(j, width = (pages[i].winfo_width()//(num_of_appointments+1))) # Set the columns width evenly.
            scrolls.append(ttk.Scrollbar(pages[i], orient="vertical", command=trees[i].yview)) # Append a Tkinter scrollbar to this array.
            scrolls[i].pack(side='right', fill='y') # Pack the scroll bar to the right side and make it fill the y axis.
            trees[i].configure(yscrollcommand=scrolls[i].set) # Link the yview of the table to corresponding scroll bar.
            for val in data: # For all values (1D arrays) in 'data' (2D array).
                trees[i].insert('', 'end', values = (val[0], val[1], val[2]) ) # Insert that 1D array as a row in the table.
            trees[i].insert('', 'end', values = (days[i], days[i], i) ) # Add more temporary values to show the table filled.

        self.searchBar = tk.Entry(main, font=font_1) # Defines a Tkinter entry box.
        self.searchBar.place(x=3*main.winfo_screenwidth()//4-20,y=100,w=main.winfo_screenwidth()//4,h=25) # Set's the entry boxes' geometry.
        self.search_icon = tk.PhotoImage(file='searchbar_icon.png') # Defines a Tkinter photo image to the search bar icon.
        self.searchIconLabel = tk.Label(main, bg=bg_colour, image=self.search_icon) # Defines a Tkinter label.
        self.searchIconLabel.place(x=3*main.winfo_screenwidth()//4-45, y=100, w=25, h=25) # Set's the label's geometry.
        self.searchIconLabel.image = self.search_icon # Set's the label's image to the Tkinter photo image that holds the searchbar icon.


    def change_settings_light(self): # Defines a function that changes the settings image that is called when the cursor hovers over it.
        self.settingsLabel.configure(image=self.settings_light) # Configures the label's image to the light version of the settings icon.
        self.settingsLabel.image = self.settings_light # Set's the label's image to the light version of the settings icon.
    def change_settings_dark(self): # Defines a function that changes the settings image that is called when the cursor leaves it.
        self.settingsLabel.configure(image=self.settings_dark) # Configures the label's image to the dark version of the settings icon.
        self.settingsLabel.image = self.settings_dark # Set's the label's image to the dark version of the settings icon.

    def settings(self, main): # Defines the function that is called when the user clicks the settings button.
        sett = tk.Tk() # Defines a Tkinter window.
        settings_window = Settings(sett, main) # Creates an instance of the Settings class.
        sett.mainloop() # Wait for the settings window to close before proceeding.

class Settings():
    '''This window allows the user to access all the settings. This class is initialised when the user clicks the settings button in the main window.'''
    def __init__(self, sett, parent): # This function is called when an instance of this class is created.
        sett.title("Settings ({})".format(version)) # Set's the window's title.
        x = (sett.winfo_screenwidth()-width_login)//2 # Finds center x co-ord.
        y = (sett.winfo_screenheight()-height_login)//2 # Finds center y co-ord.
        sett.geometry('{}x{}+{}+{}'.format(width_login, height_login, x, y))  # Sets window geometry & centers the window.
        sett.resizable(False, False) # Set's the window so it cannot be resized.
        sett.wm_iconbitmap("icon.ico") # Set's the window's icon.
        sett.config(bg=bg_colour) # Set's the background colour of window.
        sett.attributes('-topmost', True) # Make the window appear on top of all other Tkinter windows.
        sett.focus_force() # Forces the window to maintain focus over other windows.
        sett.protocol("WM_DELETE_WINDOW", lambda: self.cancel(sett, parent)) # Runs the cancel function when this window is closed down.
        
        #Buttons
        self.cancelButton = tk.Button(sett, text="Cancel", command=lambda: self.cancel(sett, parent), bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter button.
        self.cancelButton.place(x=220, y=310, w=75, h=30) # Set's the button's geometry.
        self.cancelButton.bind("<Return>", lambda x: self.cancel(sett, parent)) # Runs the cancel function when the enter/return key is pressed while this widget is focused.
        self.cancelButton.bind("<Escape>", lambda x: self.cancelButton.nametowidget(".").focus()) # Unfocuses this widget when the escape key is pressed.
        self.applyButton = tk.Button(sett, text="Apply", command=lambda: self.save(sett), bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter button.
        self.applyButton.place(x=310, y=310, w=75, h=30) # Set's the button's geometry.
        self.applyButton.bind("<Return>", lambda x: self.save(sett)) # Runs the save function when the enter/return key is pressed while this widget is focused.
        self.applyButton.bind("<Escape>", lambda x: self.applyButton.nametowidget(".").focus()) # Unfocuses this widget when the escape key is pressed.
        self.applyButton.config(relief=tk.SUNKEN) # Config the button's state so it displays as sunken.
        self.exitButton = tk.Button(sett, text="Apply & Exit", command=lambda: self.exit(sett, parent), bg=bg_colour, fg=text_colour, font=font_1) # Defines a Tkinter button.
        self.exitButton.place(x=400, y=310, w=120, h=30) # Set's the button's geometry.
        self.exitButton.bind("<Return>", lambda x: self.exit(sett, parent)) # Runs the exit function when the enter/return key is pressed while this widget is focused.
        self.exitButton.bind("<Escape>", lambda x: self.exitButton.nametowidget(".").focus()) # Unfocuses this widget when the escape key is pressed.
        
        #                                  temp                                 #
        self.c = tk.Checkbutton(sett, text="Change", command=self.box_checked)  # Defines a Tkinter check button (radio button).
        self.c.place(x=400, y = 50)                                             # Places the check button in this window.
        tk.Label(sett, text="WIP").place(x=0,y=0,w=200,h=100)                   # Defines a Tkinter label.
    def box_checked(self):                                                      # Defines a function that's run when the checkbox is changed.
        self.applyButton.config(relief=tk.RAISED)                               # Set's this button's state to raised so it displays as raised.
        

    def save(self, sett): # Defines a function that is run when the user clicks the save button. This function will save all changes.
        if self.applyButton.cget("relief") == "raised": # If the button's state is raised.
	    #APPLY CODE HERE
            self.applyButton.config(relief=tk.SUNKEN) # Change the button's state to sunken.
            print("Settings were changed.") # Prints a message in the console.

    def need_to_save(self): # Defines a function that is run when the user makes a change in the settings window.
        self.applyButton.config(relief=tk.RAISED) # Change the button's state to raised.

    def exit(self, sett, parent): # Defines a function that is run when the user clicks the exit button. This function will save and exit.
        self.save(sett) # Calls the save function.
        sett.destroy() # Destroys this Tkinter window.

    def cancel(self, sett, parent): # Defines a function that discard all changes made by the user.
        if self.applyButton.cget("relief") == "raised": # If the button's state is raised (In other words, if there are there any changes).
            sett.attributes('-topmost', False) # No longer make this window take priority over all other windows.
            if tk.messagebox.askokcancel("Unsaved Changes", "Do you want to quit? Any unsaved changes will be lost."): # Displays a Tkinter confirmation window (popup) with two options.
                sett.destroy() # Destroy the settings window.
            else:
                sett.attributes('-topmost', True) # Make the settings window take priority over other windows again.
        else:
            sett.destroy() # Destroy the settings window.

master = tk.Tk() # Define a Tkinter window.
login_window = Login(master) # Create an instance of the class 'Login'.
master.mainloop() # Wait until the master window is closed before proceeding (ending the program).
