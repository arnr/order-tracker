from tkinter import *
from tkinter import ttk
import pandas as pd

## General GUI related functions
##


def grey_out(window):
    # window is name of window/widget to "greyed out"
    
    try:
        for child in window.winfo_children():
            wtype = child.winfo_class()
            
            if wtype not in ('Frame','Labelframe'):
                child.configure(state='disable')
            
            else:
                grey_out(child)
   
    except TclError:
        pass


def grey_in(window):
    # window is name of window/widget to "greyed in"
    
    try:
        for child in window.winfo_children():
            wtype = child.winfo_class()
            
            if wtype not in ('Frame', 'Labelframe'):
                child.configure(state= 'normal')
            
            else:
                grey_in(child)
   
    except:
        pass
    '''
    SOURCE
    https://stackoverflow.com/questions/24942760/is-there-a-way-to-gray-out-disable-a-tkinter-frame
    https://www.tutorialspoint.com/getting-every-child-widget-of-a-tkinter-window
    https://www.tutorialspoint.com/how-to-gray-out-disable-a-tkinter-frame
    '''


# function for the close button
def window_close(parent_window, child_window):
    child_window.grab_release()
    grey_in(parent_window)
    child_window.destroy()


# creates a 3 second splash screen
def splash():
    splash_screen = Tk()
    splash_screen.geometry("300x200")
    
    splash_screen.overrideredirect(True) # removes the top window handle bar
    splash_screen.eval('tk::PlaceWindow . center') # center window to screen
    
    splash_label = Label(splash_screen, text="Splash text welcome")
    splash_label.place(relx=.5, rely=0.5, anchor='n')

    splash_screen.after(3000,splash_screen.destroy) # close window after 3 seconds
    '''
    SOURCE
    https://www.youtube.com/watch?v=LTVvHObxc4E 
    '''
    # TO DO: this is a basic splash screen. You need to put logo or picture or some decoration on it to finalize this section


# takes the treeview object (table) and populates it with data from provided dataframe (dataframe) 
def populate_table(table:ttk.Treeview, dataframe:pd.DataFrame): 

    #clear table of old data
    table.delete(*table.get_children())

    #defining the columns
    table["column"] = list(dataframe.columns)
    table["show"] = "headings"
        
    #formatting the columns
    for col in table['column']:
        table.column(col,anchor=CENTER, width=40)
        table.heading(col, text=col)
    
    #testing code
    for col in table['columns']:
        table.column(col, width=118)
    ## TO DO: please read
    #https://stackoverflow.com/questions/64477453/how-to-view-partial-area-of-a-treeview-and-horizontal-scrollable-in-tkinter


    #populate table with data from dataframe
    df_rows = dataframe.to_numpy().tolist()
    for row in df_rows:
        table.insert("","end", values=row)
    
    return table
    
#---------------------------------------------------
