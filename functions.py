# All functions 

#from curses import window
#from msilib import datasizemask
from tkinter import CENTER
from glob import escape
from numpy import can_cast
import openpyxl
import os
import pandas as pd
import numpy
import re
from tkinter import *
from tkinter import ttk
from functions import *
from tkinter import messagebox

def new_order(worksheet, ticket_num, date, vendor, part_name, part_num, order_num, amount, pay_method ):
    # enters new data row into sheet

    ref_row = worksheet.max_row + 1
    data = [ticket_num, vendor, part_name, part_num, order_num, amount, pay_method]

    worksheet.cell(row=ref_row, column=1).value = 'ordered ' + date +';'

    for i in range(2,9):
        worksheet.cell(row = ref_row, column = i).value = data[i-2]
    
    return worksheet
    # TO DO:
    # this function may need to be rewritten due to using openpyxl. if changes are made the dataframe 
    # object will not have the data. essentially program will have to pull the sheet again. not optimal
   

def updateStatus(df, newStatus, date, rowNum):
    #ws.cell(row = rowNum, column = columnNum).value = newStatus + date +'; ' + ws.cell(row = rowNum, column = columnNum).value 
    if df.at[rowNum, 'CURRENT STATUS'] != None:
        df.at[rowNum, 'STATUS HISTORY'] = df.at[rowNum, 'CURRENT STATUS'] + '; ' + df.at[rowNum, 'STATUS HISTORY'] 

    df.at[rowNum, 'CURRENT STATUS'] = newStatus + ' ' + date


def search(df, colName, searchTerm,):
    #show rows based on a term 'searchTerm' down a particular column 'colName'
     result = df[df[colName].str.contains(searchTerm)]
     return result





def save(wb, filename):
    wb.save(filename)


def show(df):
    print(df)


## TO DO: use below function for reference. delete in final version
## help to select and edit rows data in treeview
def edit(tree):
   # Get selected item to Edit
   selected_item = tree.selection()[0]
   tree.item(selected_item, text="blub", values=("foo", "bar"))

## TO DO: delete in final code. just placed for ease of navigation in outline mode in vscode
def PLACE_HOLDER():
    escape



#deleting and editing rows in treeview: see below tutorial
#https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview

    
## Data related functions
##


# gets data from main excel sheet and puts it into a pandas dataframe. 
# Dataframe is processed to show only wanted data.
def load_excel():

    cwd = os.getcwd()
    file_directory = os.path.join(cwd, 'program', 'files')
    os.chdir(file_directory)
    wb = openpyxl.load_workbook('order tracking.xlsx')
    ws = wb['ORDERS']
        
    # setup pandas dataframe for further processing
    df = pd.DataFrame(ws.values)

    ## make sure that first row is actually the title row
    df.columns = df.iloc[0]
    df = df[1:]

    ## make sure these values treated as strings
    df['PART #'] = df['PART #'].astype(str) 
    df['ORDER #'] = df['ORDER #'].astype(str)

    return df


#show rows for formated for proper displaying
#if index_list is given then it will show only the rows corresponding to the number in index list
def show_entries(dataframe:pd.DataFrame, index_list=[]):
    
    if index_list != []:
        result = dataframe.loc[index_list].loc[:,dataframe.columns != 'STATUS HISTORY']
    else:
        result = dataframe.loc[:,dataframe.columns != 'STATUS HISTORY']
    return result


#gets status history. It can bring entire dataframe set or just one row info
def get_status_history(dataframe:pd.DataFrame, index=-1):
    
    # regex definition
    status_regex = re.compile(r'\w+\s\d+\/\d+\/\d\d\d\d')

    # get all status histories
    if index == -1:
        data = dataframe['STATUS HISTORY'].tolist()
        return data

    # get status history at index row
    else:
        data = dataframe.iloc[index].loc['STATUS HISTORY']
        
        try:
            list = status_regex.findall(data)
            
        except TypeError:
            list = []


        if list == []:
            messagebox.showinfo("No History", "This record has no history")

        return list
        
    '''
    SOURCE
    https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column-or-row
    https://stackoverflow.com/questions/28754603/indexing-pandas-data-frames-integer-rows-named-columns
    '''


# function to save the edited treeview data back to dataframe for further saving
def saveable_dataframe(original_dataframe, tree):
    # origianl dataframe = dataframe that was loaded in to the treeview before any editing.
    # tree = treeview object with all the edited data. 

    # pull data from treeview widget and pass to dataframe.
    values = []
    for child in tree.get_children():
        values.append(tree.item(child)["values"])
    
    df_to_write = pd.DataFrame(values)
    
    # status history and add it back to dataframe
    list = get_status_history(original_dataframe)
    df_to_write.insert(1,"STATUS HISTORY", list, False)
    
    return df_to_write


# function to write the final data from a dataframe to the excel sheet
def write_to_excel(edited_dataframe:pd.DataFrame):
    #edited_dataframe: the dataframe with all the edits in it. The final data should be here.
   
    writer = pd.ExcelWriter('order tracking test.xlsx')
    edited_dataframe.to_excel(writer,sheet_name='ORDERS',index=False)
    writer.close()

#---------------------------------------------------


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



## GUI buttons functions
##

# level 2 windows hold secondary data or do seconday activities and are called from the main window. 
# main_window is the name of window from which this window will be called. usually it will be 'root' window
def open_lvl2_window(new_window, window_title:str, main_window:Tk, size="200x200"):

    new_window = Toplevel(main_window)
    new_window.title(window_title)
    new_window.geometry(size)

    return new_window


# level 3 window shows history of statuses of selected row
def status_history_window(window, dataframe, index):
    # window = name of window from where this window will get called
    # dataframe and list for the get_status_history function
    
    # get data for this window; exit function if none available
    list = get_status_history(dataframe, index)
    if list == []:
        return
     
    
    # draw window
    status_window = Toplevel(window)
    status_window.title("Status History")
    status_window.geometry("250x300")
    status_window.grab_set()

    # box for data 
    listbox = Listbox(status_window)    
    listbox.place(relx = 0.5, rely = 0.1, relwidth = 0.9, relheight=0.8, anchor=N)

    # button function
    # def window_close():
    #     status_window.grab_release()
    #     grey_in(window)
    #     status_window.destroy()
    
    # button
    close_btn = Button(status_window, text = 'Close', command=lambda: window_close(window, status_window))
    close_btn.place(relx=0.5, rely=0.85, relwidth=0.9, anchor=N)

    # populate box
    for count, item in enumerate(list):
       listbox.insert(count, item)

    # grey out the parent window
    grey_out(window)


# level 2 window to show and edit one row from the treeview
def edit_row(tree, dataframe, parent_window):
        
    #retrieve data from selected line
    focused_line = tree.focus()
    focused_index = tree.index(tree.selection())
    '''
    SOURCE:
    https://stackoverflow.com/questions/68508694/how-do-i-get-the-index-of-selected-row-in-tkinter-treeview
    '''
    
    # check if a row was selected before moving on.
    if "".__eq__(focused_line):
        print("no data selected")
        messagebox.showerror("ERROR", "Nothing was selected to edit!")
        return
        '''
        SOURCE:
        https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
        '''    
     
    # GUI related
    #
    edit_window = Toplevel(parent_window)
    edit_window.title("Edit Entry")
    edit_window.geometry("350x400")
    edit_window.grab_set()

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
    # store entry box data in these lists
    box_entries=[]
    label_text = ["Status", "Ticket #", "Vendor", "Part Description", "Part #", "Order #", "Amount", "Payment Method"]
    selected_data = tree.item(focused_line, "values")

    # create the labels and entry boxes; populate with relevant data
    for i in range(len(label_text)):
        
        # labels
        label = Label(edit_window)
        label.configure(text=label_text[i])
        label.place(relx = 0.05, rely = (i/10) + 0.025, relwidth = 0.4)
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
        entry_box.place(relx = 0.5, rely = (i/10) + 0.025, relwidth = 0.4)
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
    

    # button & window functions
    #
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
    
    # button definitions
    #
    save_edit_btn = Button(edit_window, text= 'Save Changes', command=commit_changes)
    save_edit_btn.place(relx= 0.25, rely= 0.8, relwidth= 0.4, anchor= N)

    #save_edit_btn = Button(edit_window, text = 'Close', command=edit_window.destroy)
    save_edit_btn = Button(edit_window, text= ' Status History', command=lambda: status_history_window(edit_window, dataframe,focused_index))
    save_edit_btn.place(relx= 0.75, rely= 0.8, relwidth= 0.4, anchor= N)

    close_btn = Button(edit_window, text= 'Close', command=lambda: window_close(parent_window, edit_window))
    close_btn.place(relx= 0.5, rely= 0.9, relwidth= 0.9, anchor= N)
    '''
    SOURCE:
    https://www.geeksforgeeks.org/how-to-close-a-window-in-tkinter/
    '''

    grey_out(parent_window)
#---------------------------------------------------



'''
to take data from treeview to dataframe 
https://stackoverflow.com/questions/56898437/method-to-get-treeview-table-into-new-dataframe


to edit and delete items in treeview
https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview



'''
# def backup():
#    #this function will create a backup of the main excel sheet before any changes are made. 
#     #Furthermore it will check how many backups are there and delete the oldest ones so as to control number of copies kept