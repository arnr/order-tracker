"""
things that need fixing
------------------------

newEntry function date parameter needs to be checked out. at the moment it will only accept string
to output to the excel sheet

need to build a function that checks for the backup folder, creates it if there is not one.


"""
## library imports
from glob import escape
from importlib.util import LazyLoader
from logging import root
from operator import index
from unittest import skip
from numpy import can_cast
import openpyxl
import os
import pandas as pd
import numpy as np
import re

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from functions import *
#---------------------------------------------------


## Function calls & logic

# retrieve data from excel sheet
df = load_excel()


## button functions

def show_open_orders():
    temp = show_entries(df)
    populate_table(tree, temp)

def edit_row():
        
    #retrieve data from selected line
    focused_line = tree.focus()
    
    if "".__eq__(focused_line):
        print("no data selected")
        messagebox.showerror("ERROR", "Nothing was selected to edit!")
        return
        '''
        SOURCE:
        https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
        '''    
    
    selected_data = tree.item(focused_line,"values")
 

    edit_window = Toplevel(root)
    edit_window.title("Edit Entry")
    edit_window.geometry("350x400")

    '''CODE DEPRECATED - see note 1
    entry_boxes = {
        "status" : StringVar(),
        "ticket_num" : StringVar(), 
        "vendor" : StringVar(),
        "part_desc" : StringVar(),
        "part_num" : StringVar(),
        "order_num" : StringVar(),
        "amount" : StringVar(),
        "pay_method" : StringVar()
    }
    '''

    #store entry box data in this list
    box_entries=[]
    label_text = ["Status", "Ticket #", "Vendor", "Part Description", "Part #", "Order #", "Amount", "Payment Method"]


    for i in range(len(label_text)):
        
        # labels
        label = Label(edit_window)
        label.configure(text=label_text[i])
        label.place(relx = 0.05, rely = (i/10) + 0.1, relwidth = 0.4)
        # TO DO: the label must be left aligned to make it looke better

        '''CODE DEPRECATED - see note 1
        entry boxes
        entry_box = key + "_entrybx" 
        entry_box = Entry(edit_window, textvariable=entry_boxes[key])
        entry_box.place(relx = 0.5, rely = (i/10) + 0.1, relwidth = 0.4)
        entry_box.insert(0, selected_data[i])
        '''

        #entry boxes
        entry_box = Entry(edit_window)
        entry_box.place(relx = 0.5, rely = (i/10) + 0.1, relwidth = 0.4)
        entry_box.insert(0, selected_data[i])
        box_entries.append(entry_box)
        '''
        SOURCE: 

        Default text in entry widget
        https://www.geeksforgeeks.org/how-to-set-the-default-text-of-tkinter-entry-widget/  

        create entry boxes with loop and retrieve data from boxes
        https://www.youtube.com/watch?v=H3Cjtm6NuaQ&t

        note 1
        DEPRECATED CODE 
        Used the below tutorial to write the code as one approach to solve 
        writing multiple widgets with loop and then retrieving the info thereafter. 

        To create multiple widgets and reference them:
        https://www.youtube.com/watch?v=XerT3-rrOmQ
        END OF note 1
        '''    
    
    ## button & window functions
    def commit_changes():
        values=[]
        for entry in box_entries:
            values.append(entry.get())

        tree.item(focused_line, values=values)

        edit_window.destroy()

   # TO DO: possible solution to retrieving data https://www.youtube.com/watch?v=H3Cjtm6NuaQ
        '''
        https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview
        '''
    
    ## button definitions
    save_edit_btn = Button(edit_window, text = 'Save Changes', command=commit_changes)
    save_edit_btn.place(relx = 0.25, rely = 0.9, relwidth = 0.4, anchor=N)

    save_edit_btn = Button(edit_window, text = 'Close', command=edit_window.destroy)
    save_edit_btn.place(relx = 0.75, rely = 0.9, relwidth = 0.4, anchor=N)
    '''
    SOURCE:
    https://www.geeksforgeeks.org/how-to-close-a-window-in-tkinter/
    '''


# TO DO: the above function is to open a new window and get stuff in it.
# follow this tutorial for more guidance on that regard
# https://www.youtube.com/watch?v=H_zZiIlnB8M

# test code start


    

    '''
    reference the link
    https://pythonexamples.org/pandas-write-dataframe-to-excel-sheet/
    to write data to the sheet
    '''
    
    '''
    SOURCE
    https://stackoverflow.com/questions/56898437/method-to-get-treeview-table-into-new-dataframe
    https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column-or-row
    https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
    '''
    # TO DO:
    # thinking a bit ahead. simply saving the treeview to the dataframe has a issue. 
    # There are other functions that give filtered views of the dataframe to the tree view. 
    # Writing it back to the dataframe would result in overwriting other data and causing it to disappear.
    # One technique to solve this issue i thought of is to have a variable that tracks the view currently shown.
    # The write to dataframe operation will be different for each type of view. i.e. the if it is a 
    # filtered view then the write will try to keep the old unedited rows with then new edited rows.
    # This operation is particularly important where the treeview is from a search and show result operation. 

# test code start

# def save():
#     # final_df = saveable_dataframe(df,tree)
#     # #print(final_df)
#     # write_to_excel(final_df)
#     # messagebox.showinfo("SUCCESS", "Data saved to Excel sheet")
#     escape()

# test code end


#use below function to search and show result. map update() function to a button
ggg = search(df, 'PART #', '1')
mylist=ggg.index.values

def update():
    test1 = show_entries(df,mylist)
    populate_table(tree,test1)
####




# GUI code


## root window definition

root = Tk()
root.title('Order Tracker')
root.geometry("1000x700")
root.eval('tk::PlaceWindow . center')
'''
SOURCE
https://www.tutorialspoint.com/how-to-center-a-window-on-the-screen-in-tkinter
'''

def reshow_root_window():
    root.deiconify()

root.withdraw()
root.after(3100,reshow_root_window)
'''
SOURCE
https://stackoverflow.com/questions/1406145/how-do-i-get-rid-of-python-tkinter-root-window
'''

''' below function (splash()) seems to conflict with function edit_row(). 
    The error message that is called once treeview selection is checked opens another window for some reason.
    Placing this code after root window is called seems to fix the issue. Hence the location.
'''
splash()

#---------------------------------------------------


## Styling info

window_style = ttk.Style()
window_style.theme_use('clam')
'''
SOURCE
https://www.tutorialspoint.com/how-can-i-set-the-row-height-in-tkinter-treeview
'''
#---------------------------------------------------

#TO DO: use this tutorial to position the window towards the middle of the screen
#https://yagisanatode.com/2018/02/23/how-do-i-change-the-size-and-position-of-the-main-window-in-tkinter-and-python-3/
#---------------------------------------------------



## Root window contents / frame definitions

#top frame holds main buttons
top_frame = Frame(root, bg ='#80c1ff' )
top_frame.place(relx=.5, rely=0.03, relwidth=0.97, relheight=0.10, anchor='n')

#table frame holds the treeview and data
table_frame = Frame(root, bg='#80c1ff')
table_frame.place(relx=.5, rely=0.14, relwidth=0.97, relheight=0.42, anchor='n')

#bottom frame holds editing buttons
bottom_frame = Frame(root, bg='#80c1ff')
bottom_frame.place(relx=.5, rely=0.57, relwidth=0.97, relheight=0.20, anchor='n')
#---------------------------------------------------


## Top frame contents

open_orders_btn = Button(top_frame, text = 'Open Orders', command=show_open_orders)
open_orders_btn.place(relx = 0.05, rely = 0.2, relwidth = 0.1)

#TO DO: this button is usless for now. but placed here as a way to see dimenions and look. Please repurpose code or delete
nw_btn = Button(top_frame, text="new window", command=lambda: open_lvl2_window("Edit Row", root,"400x400"))
nw_btn.place(relx =0.2, rely = 0.2, relwidth = 0.1)
#---------------------------------------------------


## table frame contents

# treeview object to display table data from dataframe
window_style.configure('Treeview', rowheight=25)
tree = ttk.Treeview(table_frame, height=10)
tree.place(relx=.5, rely=0.01, relwidth=0.97, anchor='n')
#---------------------------------------------------


## bottom frame contents

edit_btn = Button(bottom_frame, text = 'Edit', command=edit_row)
edit_btn.place(relx=0.5, rely=0.1, relwidth=0.97, anchor='n')

close_btn = Button(bottom_frame, text = 'Save & Close')
close_btn.place(relx=0.5, rely=0.35, relwidth=0.97, anchor='n')
#---------------------------------------------------

global holder

def test_func():
    global holder
    holder = tree.selection()

#edit2_btn = Button(table_frame, text = 'test_func', command=test_func)
#edit2_btn.place(relx=.5, rely=0.7, relwidth=0.97, anchor='n')



    




#open_orders_btn3 = Button(lala, text = 'Open Orders', command=lambda: open_lvl2_window("lala", "test", root,"200x400"))
#open_orders_btn3.place(relx = 0.05, rely = 0.4, relwidth = 0.1)

# widgets definitions
#howEntries_button = Button(table_frame, text = 'Show orders', command=openorders)
#showEntries_button.place(relx=.5, rely=0.03, relwidth=0.97, anchor='n')

#delete_button = Button(table_frame, text = 'Update', command=update)
#delete_button.place(relx=.5, rely=0.08, relwidth=0.97, anchor='n')

#test code

#myLabel1 = Label(frame, text='hello world test')
#myLabel2 = Label(root, text='how are you doing?')


# widget calls
#showEntries_button.grid(row=0, column=1)
#myLabel1.grid(row=0, column=0)
#myLabel2.grid(row=1, column=0, columnspan=2)

####

root.mainloop()
















# test funcitions here

#test code

#newEntry('123','2/2/2022','tvpt','main','bn44-00098c', 'urigj894845', 25, 'paypal') # testing line onlyu - delete in final version
#updateStatus('received' , '3/29/2022', 7, 1)
#save('test3.xlsx')

####







