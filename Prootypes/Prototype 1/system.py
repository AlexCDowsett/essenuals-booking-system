#Imports
from tkinter import * # Imports Tkinter module.
from tkinter import ttk # Imports the ttk part of the Tkinter module.
from datetime import * # Imports the datetime module.
bgColour = '#F5EEEE' # Defines a string that contains the background colour in hexadecimal.
fgColour = '#F5EEEE' # Defines a string that contains the foreground colour in hexadecimal. 

#Functions
def settingsFunc(): # Defines a function that is run when the settings button is pressed.
    settings = Tk() # Defines a new Tkinter window.
    settings.title("Settings") # Sets a title for the window.
    settings.geometry("720x540") # Set's the window's geometry.
    settings.config(bg = bgColour) # Set's the window's background colour to the colour stored in bicolour.
    settings.wm_iconbitmap("icon.ico") # Set's the window's icon.
    var1 = IntVar() # Defines a Tkinter integer variable.
    Checkbutton(settings, text="Tickbox", variable=var1).grid(row=0, sticky=W) # Defines a Tkinter check button.
    viewDatabaseButton1 = Button(settings, text="View Booking Database", command=viewDatabase)  # Defines a Tkinter button.
    viewDatabaseButton1.place(x = 10, y = 100, w = 150, h = 30) # Set's the geometry of the button.
    viewDatabaseButton2 = Button(settings, text="View Client Database", command=viewDatabase)  # Defines a Tkinter button.
    viewDatabaseButton2.place(x = 10, y = 140, w = 150, h = 30) # Set's the geometry of the button.
    viewDatabaseButton3 = Button(settings, text="View Hairdresser Database", command=viewDatabase)  # Defines a Tkinter button.
    viewDatabaseButton3.place(x = 10, y = 180, w = 150, h = 30) # Set's the geometry of the button.
    print(var1) # Prints a variable to the console.
    
def viewDatabase(): # Defines a work in progress function.
    "" 
           

root = Tk() # Defines a Tkinter window.
root.title("Booking System (0.1)") # Set's the window's title.
root.geometry("1080x720") # Set's the window's geometry.
root.config(bg = bgColour) # Set's the window's background colour.
root.wm_iconbitmap("icon.ico") # Set's the window's icon.
root.resizable(False, False) # Makes the window unable to be resized.

#Variables
search = StringVar() # Defines a Tkinter string variable.

#Labels
searchBar = Entry(root, textvariable = search) # Defines a Tkinter entry box.
searchBar.place(x = 640, y = 15, w = 400, h = 25) # Set's the entry boxes' geometry.
searchBar.focus() # Sets the focuses the entry box.

searchBarIcon = Label(root) # Defines a Tkinter label.
searchBarIcon.place(x=1040, y = 15, w = 25, h = 25) # Set's the geometry of the label.
searchBarImage = PhotoImage(file = "searchbar_icon.png") # Defines a tkinter photo image variable to hold the image to be displayed within this label.
searchBarIcon.config(image = searchBarImage, bg = bgColour, fg = fgColour) # Configures the colour and image of this label.

settingsButton=Button(root, command = settingsFunc) # Binds the following function to the button.
settingsButton.place(x=1000, y=640, w = 60, h = 60) # Set's the button's geometry.
settingsIcon=PhotoImage(file = "settings.png") # Defines a tkinter photo image variable to hold the image to be displayed within this button.
settingsButton.config(image = settingsIcon, bg = bgColour, fg = fgColour) # Configures the colour and image of this button.


data = [ ["13:30", "Deborah", "Lewis", "00:30", "Haircut"], # Defines a 2D array.
         ["14:00", "Peter", "Tim", "00:30", "Haircut"],
         ["14:00", "Emma", "Joe", "01:00", "Colouring"],
         ["14:30", "Michelle", "Emma", "00:30","Haircut"] ]


frame = Frame(root) # Defines a Tkinter frame.
frame.pack() # Packs the frame.
tree = ttk.Treeview(frame, columns = (1,2,3,4,5), height = 15, show = "headings") # Defines a Tkinter tree view (table).
frame.place(x=100, y=150) # Places the frame in the window.
tree.pack(side = 'left') # Pack the table to favour the left side of the frame.

tree.heading(1, text="Time") # Set's a column name for the table.
tree.heading(2, text="Client's Name") # Set's a column name for the table.
tree.heading(3, text="Hairdresser") # Set's a column name for the table.
tree.heading(4, text="Duration") # Set's a column name for the table.
tree.heading(5, text="Notes") # Set's a column name for the table.

tree.column(1, width = 150) # Set's the width of the column.
tree.column(2, width = 150) # Set's the width of the column.
tree.column(3, width = 150) # Set's the width of the column.
tree.column(4, width = 150) # Set's the width of the column.
tree.column(5, width = 150) # Set's the width of the column.

scroll = ttk.Scrollbar(frame, orient = "vertical", command = tree.yview) # Defines a Tkinter scrollbar and binds it to the following function.
scroll.pack(side = 'right', fill = 'y') # Packs the scroll bar to favour the right side and fill the y axis.

tree.configure(yscrollcommand = scroll.set) # Set's the table's yview to match the yview of the scrollbar.

for val in data: # For all values (1D arrays) in the array 'data' (2D array).
    tree.insert('', 'end', values = (val[0], val[1], val[2], val[3], val[4]) ) # Insert that 1D arrays into the table.
root.mainloop() # Wait until the window is closed before proceeding.
