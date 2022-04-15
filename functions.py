# All functions 

#from curses import window
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
    file_directory = os.path.join(cwd, 'program\\files')
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


def get_status_history(dataframe:pd.DataFrame):
    list = dataframe['STATUS HISTORY'].tolist()
    return list
    '''
    SOURCE
    https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column-or-row
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
# def write_to_excel(edited_dataframe:pd.DataFrame):
#     # edited_dataframe: the dataframe with all the edits in it. The final data should be here.
#     # writer = pd.ExcelWriter('order tracking test.xlsx')
#     # edited_dataframe.to_excel(writer,sheet_name='ORDERS',index=False)
#     # writer.close()
#     escape()
#     #edited_dataframe.to_excel(r'files/order tracking.xlsx', sheet_name='ORDERS', index=False)
#---------------------------------------------------


## General GUI related functions
##

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
#---------------------------------------------------



'''
to take data from treeview to dataframe 
https://stackoverflow.com/questions/56898437/method-to-get-treeview-table-into-new-dataframe


to edit and delete items in treeview
https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview



'''
#def backup():

   #this function will create a backup of the main excel sheet before any changes are made. 
    #Furthermore it will check how many backups are there and delete the oldest ones so as to control number of copies kept
'''





''
regex search procedure for reference
>>>sampletext = 'closed 3/30/2022; received 3/23/2022; ordered 3/15/2022'
>>>myregex = re.compile(r'\w+\s\d+\/\d+\/\d\d\d\d')
>>>myregex.findall(sampletext)
>>>['closed 3/30/2022', 'received 3/23/2022', 'ordered 3/15/2022']
dasda
'''
