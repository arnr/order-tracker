from functools import partial
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
from tkcalendar import Calendar
from general_functions import *



class row_editor:

    def __init__(self, tree, dataframe, parent_window) -> None:
        self.tree = tree
        self.dataframe = dataframe
        self.parent_window = parent_window

        self.new_status='nothing'
        self.selected_date=''

    status_options = [
        'ordered',
        'reordered',
        'received',
        'ticket_compeleted',
        'return_requested',
        'return_authorized',
        'credit_memo_received'
        ]


    def editor(self):
        
        print('editor hello')
        #retrieve data from selected line
        focused_line = self.tree.focus()
        focused_index = self.tree.index(self.tree.selection())
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
        edit_window = Toplevel(self.parent_window)
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
        omit_list = ("Status", "Vendor", 'Payment Method') # so these can be made in to label box instead of entry boxes
        selected_data = self.tree.item(focused_line, "values")


        # main button & window functions 
        #

        # commits the changes typed in edit window back into the treeview
        def commit_changes():

            values=[]
            ''''''
            for entry in box_entries:
                if isinstance(entry, Entry):
                    values.append(entry.get())
                # elif isinstance(entry, Label):
                #     values.append(omit_list_label.cget("text"))
            '''
            SOURCE
            https://blog.finxter.com/how-to-determine-the-type-of-an-object-in-python/
            https://stackoverflow.com/questions/34667710/pattern-matching-tkinter-child-widgets-winfo-children-to-determine-type
            '''
            # write to treeview
            self.tree.item(focused_line, values=values)

            # close window after saving
            window_close(self.parent_window, edit_window)   

        
        # function and list to deal with the edit buttons for the labels in edit screen
        label_btn_id = [] # reference list to buttons created in loop associated with omit list
        entry_bx_id = [] # reference list to all entry boxes for later calling
        

        def call_edit_fnct(i):
            # call for status edit button
            if i == 0:
                # call function to get changed value
                self.edit_status(edit_window, box_entries[i].get())

                # display new value in entry box
                entry_bx_id[i].config(state='normal')
                entry_bx_id[i].delete(0, END)
                entry_bx_id[i].insert(0,self.new_status)
                entry_bx_id[i].config(state="disabled")
            
            # call for vendor edit button
            elif i == 2:
                # call function to get changed value
                self.edit_vendor(edit_window, box_entries[i].get())

                # display new value in entry box
                entry_bx_id[i].config(state='normal')
                entry_bx_id[i].delete(0, END)
                entry_bx_id[i].insert(0,self.new_vendor)
                entry_bx_id[i].config(state="disabled")

            # call for payment method edit button        
            elif i == 7:
                # call function to get changed value
                self.edit_paymethod(edit_window, box_entries[i].get())

                # display new value in entry box
                entry_bx_id[i].config(state='normal')
                entry_bx_id[i].delete(0, END)
                entry_bx_id[i].insert(0,self.new_paymethod)
                entry_bx_id[i].config(state="disabled")
                
            # bname.configure(text = "clicked")
            # print(i)
        
        
        # create the labels and entry boxes; populate with relevant data
        for i in range(len(label_text)):
            
            # labels
            label = Label(edit_window)
            label.place(relx = 0.03, rely = (i/10) + 0.025, relwidth = 0.33)
            label.configure(text=label_text[i])

            
            # TO DO: the label must be left aligned to make it looke better

            '''CODE DEPRECATED - see note 1
            entry boxes
            entry_box = key + "_entrybx" 
            entry_box = Entry(edit_window, textvariable=entry_boxes[key])
            entry_box.place(relx = 0.5, rely = (i/10) + 0.1, relwidth = 0.4)
            entry_box.insert(0, selected_data[i])
            '''

            # editable entry boxes 
            if label_text[i] not in omit_list:
                # draw and populate entry boxes
                entry_box = Entry(edit_window)
                entry_box.place(relx = 0.35, rely = (i/10) + 0.025, relwidth = 0.4)
                entry_box.insert(0, selected_data[i])
                entry_bx_id.append(entry_box)
                
                # save data into list
                box_entries.append(entry_box)
                label_btn_id.append("") # placeholder strings added to so numbering reference is correct   

            # unclicable label boxes to show data and corresponding edit buttons
            if label_text[i] in omit_list:
                # draw and populate labels
                # omit_list_label = Label(edit_window, bg= "white", relief= SUNKEN, anchor= "w" )
                # omit_list_label.place(relx = 0.35, rely = (i/10) + 0.025, relwidth = 0.4)
                # omit_list_label.configure(text= selected_data[i])
                
                entry_box = Entry(edit_window)
                entry_box.place(relx = 0.35, rely = (i/10) + 0.025, relwidth = 0.4)
                entry_box.insert(0, selected_data[i])
                entry_bx_id.append(entry_box)
                entry_box.config(state="disabled")

                ''' CODE DEPRECATED -- solution to get function reference by using a string
                # get the functions for the edit button. Functions names are 'edit_Status', 'edit_status' & 'edit_PaymentMethod'
                edit_function = locals().get('edit_' + remove(label_text[i]))
                '''

                # draw edit button
                label_edit_btn = Button(edit_window, text= 'Edit', command=partial(call_edit_fnct, i) )
                label_edit_btn.place(relx = 0.8, rely = (i/10) + 0.025, relwidth = 0.15)
                label_btn_id.append(label_edit_btn)
        
                # save data into list
                # box_entries.append(lambda: omit_list_label)
                box_entries.append(entry_box)

            '''SOURCE: 
            -> Default text in entry widget:  https://www.geeksforgeeks.org/how-to-set-the-default-text-of-tkinter-entry-widget/  
            -> create entry boxes with loop and retrieve data from boxes:  https://www.youtube.com/watch?v=H3Cjtm6NuaQ&t
            -> https://stackoverflow.com/questions/21495367/how-to-align-text-to-the-left
            -> Tkinter Relief styles:  https://www.tutorialspoint.com/python/tk_relief.htm
            -> Assigning functions to buttons that were created with loop: https://stackoverflow.com/questions/39447138/how-can-i-identify-buttons-created-in-a-loop
            -> https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
            -> https://www.tutorialspoint.com/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter
            
            note 1
            DEPRECATED CODE 
            Used the below tutorial to write the code as one approach to solve 
            writing multiple widgets with loop and then retrieving the info thereafter. 

            To create multiple widgets and reference them:
            https://www.youtube.com/watch?v=XerT3-rrOmQ
            END OF note 1
            '''    

            # TO DO: possible solution to retrieving data https://www.youtube.com/watch?v=H3Cjtm6NuaQ
            # '''
            # https://www.tutorialspoint.com/delete-and-edit-items-in-tkinter-treeview
            # '''
        
        
        # button definitions
        #
        
        save_edit_btn = Button(edit_window, text= 'Save Changes', command=commit_changes)
        save_edit_btn.place(relx= 0.25, rely= 0.8, relwidth= 0.4, anchor= N)

        status_history_btn = Button(edit_window, text= ' Status History', command=lambda: self.status_history_window(edit_window, focused_index))
        status_history_btn.place(relx= 0.75, rely= 0.8, relwidth= 0.4, anchor= N)

        close_btn = Button(edit_window, text= 'Close', command=lambda: window_close(self.parent_window, edit_window))
        close_btn.place(relx= 0.5, rely= 0.9, relwidth= 0.9, anchor= N)
        '''
        SOURCE:
        https://www.geeksforgeeks.org/how-to-close-a-window-in-tkinter/
        '''

        grey_out(self.parent_window)


    def get_date(self, parent_window):

        # draw window
        date_window = Toplevel(parent_window)
        date_window.title("Select Date")
        date_window.geometry("200x400")
        date_window.grab_set()

        # draw calender
        cal = Calendar(date_window, selectmode = 'day',
                year = 2020, month = 5, day = 22,
                date_pattern='MM/dd/yyyy')
        cal.pack(pady = 20)

        # button functions

        # gets the date info from calender object to the necessary variables.
        def grab_date():
            dateinfo.config(text = "Selected Date is: " + cal.get_date())
            self.selected_date = cal.get_date()
            

        # Add Button and Label
        Button(date_window, text= "Get Date", command= grab_date).pack(pady = 5)

        dateinfo = Label(date_window, text = "")
        dateinfo.pack(pady = 10)

        close_btn = Button(date_window, text = 'Save & Close', command=lambda: window_close(parent_window, date_window))
        close_btn.pack(pady= 10)

        grey_out(parent_window)

        '''SOURCE
        https://www.geeksforgeeks.org/create-a-date-picker-calendar-tkinter/
        https://www.codesdope.com/blog/article/nested-function-scope-of-variable-closures-in-pyth/
        '''


    def edit_status(self,parent_window, value):

        # Draw window
        edit_status_window = Toplevel(parent_window)
        edit_status_window.title("Edit Status")
        edit_status_window.geometry("200x250")
        edit_status_window.grab_set()        

        # Draw label
        label_status = Label(edit_status_window, bg= "white", relief= SUNKEN, anchor= "w" )
        label_status.place(relx = 0.5, rely = 0.1, relwidth = 0.9, anchor= N)
        label_status.configure(text=value)

        # drop down menu for status
        clicked = StringVar()
        clicked.set('Select Status')
        drop = OptionMenu( edit_status_window , clicked, *self.status_options )
        drop.place(relx = 0.5, rely = 0.25, relwidth = 0.91, anchor= N)


        # TO DO: check all the error messages actually trigger properly. was working but changes have rendered some of it not. I noticed in some of the runs
        def save(window):
            # validate if date and status were selected before accepting status entry
            try:
                if self.selected_date:
                    if not clicked.get() == 'Select Status':
                        self.new_status = clicked.get() + ' ' + self.selected_date
                        label_status.configure(text= self.new_status)                
                        
                        # wait for selected info to show in status label 
                        time.sleep(2)
                        window.destroy()
                    
                    else:
                        messagebox.showerror("ERROR", "Status not selected!") 
                
                else:
                    messagebox.showerror("ERROR", "Date not selected!")
            
            except AttributeError:
                messagebox.showerror("ERROR", "Date not selected!")

        # draw buttons
        date_btn = Button(edit_status_window, text='Date', command=lambda: self.get_date(edit_status_window))
        date_btn.place(relx = 0.5, rely = 0.38, relwidth = 0.9, anchor= N)

        save_btn = Button(edit_status_window, text='Save', command=lambda: save(edit_status_window))
        save_btn.place(relx = 0.5, rely = 0.55, relwidth = 0.9, anchor= N)
        
        # make the window wait till user puts data for rest of program to continure
        parent_window.wait_window(edit_status_window)

        '''SOURCE
        https://www.geeksforgeeks.org/dropdown-menus-tkinter/
        https://stackoverflow.com/questions/28388346/what-does-thewait-window-method-do
        '''


    def edit_vendor(self, parent_window, value):
        
        # Draw window
        edit_vendor_window = Toplevel(parent_window)
        edit_vendor_window.title("Edit Vendor")
        edit_vendor_window.geometry("200x250")
        edit_vendor_window.grab_set()    

        # Draw label
        label_vendor = Label(edit_vendor_window, bg= "white", relief= SUNKEN, anchor= "w" )
        label_vendor.place(relx = 0.5, rely = 0.1, relwidth = 0.9, anchor= N)
        label_vendor.configure(text=value)

        vendor_list = open('vendor list.txt').read().splitlines()
        
        clicked = StringVar()
        clicked.set('Select Vendor')
        drop = OptionMenu(edit_vendor_window , clicked, *vendor_list)
        drop.place(relx = 0.5, rely = 0.25, relwidth = 0.91, anchor= N)

        def save(window):
            if not clicked.get() == 'Select Vendor':
                self.new_vendor = clicked.get()
                label_vendor.configure(text= self.new_vendor)                
                            
                # wait for selected info to show in status label 
                time.sleep(2)
                grey_in(parent_window)
                window.destroy()        

            else:
                messagebox.showerror("ERROR", "Vendor not selected")

        def close():
            self.new_vendor = value
            grey_in(parent_window)
            edit_vendor_window.destroy()

        save_btn = Button(edit_vendor_window, text= 'Save & Close', command=lambda: save(edit_vendor_window))
        save_btn.place(relx = 0.5, rely = 0.55, relwidth = 0.9, anchor= N)    

        cls_btn = Button(edit_vendor_window, text= 'Close', command= close)
        cls_btn.place(relx = 0.5, rely = 0.70, relwidth = 0.9, anchor= N)

        # make the window wait till user puts data for rest of program to continure
        grey_out(parent_window)
        parent_window.wait_window(edit_vendor_window)


    def edit_paymethod(self, parent_window, value):
        
        # Draw window
        edit_paymethod_window = Toplevel(parent_window)
        edit_paymethod_window.title("Edit Vendor")
        edit_paymethod_window.grab_set()    

        # Draw label
        label_paymethod = Label(edit_paymethod_window, bg= "white", relief= SUNKEN, anchor= "w" )
        label_paymethod.pack(ipadx=5, ipady=5, expand=True)
        label_paymethod.configure(text="Current: " + value)

        paymethod_list = open('payment method list.txt').read().splitlines()
        selected_method = StringVar()
        
        # frame to hold the radio buttons
        rbutton_frame = Frame(edit_paymethod_window)
        rbutton_frame.pack(ipady=5, expand=True)

        # radio button definition and placement
        for a, method in enumerate(paymethod_list):
            rbutton = Radiobutton(
                rbutton_frame, 
                text= method, 
                variable=selected_method, 
                value=method, 
                command=lambda: label_paymethod.configure(text=selected_method.get())
                )
            
            rbutton.pack(ipadx=10)

        # button function
        def save(window):
            if label_paymethod.cget("text") != value:
                print("radio button selected")
                self.new_paymethod = label_paymethod.cget("text")
                                        
                # wait for selected info to show in paymethod label 
                time.sleep(2)
                grey_in(parent_window)
                window.destroy()        

            else:
                messagebox.showerror("ERROR", "Payment method not selected")

        def close():
            self.new_paymethod = value
            grey_in(parent_window)
            edit_paymethod_window.destroy()

        # button 
        save_btn = Button(edit_paymethod_window, text= 'Save & Close', command=lambda: save(edit_paymethod_window) )
        save_btn.pack(ipadx=5, ipady=10, expand=True)

        cls_btn = Button(edit_paymethod_window, text= 'Close', command= close )
        cls_btn.pack(ipadx=5, ipady=10, expand=True)

        # make the window wait till user puts data for rest of program to continue
        grey_out(parent_window)
        parent_window.wait_window(edit_paymethod_window)

        '''SOURCE
        https://www.tutorialspoint.com/python/tk_radiobutton.htm
        https://www.pythontutorial.net/tkinter/tkinter-stringvar/
        '''
    
    
    # gets status history. It can bring entire dataframe set or just one row info
    def get_status_history(self, index=-1):
        
        # regex definition
        status_regex = re.compile(r'\w+\s\d+\/\d+\/\d\d\d\d')

        # get all status histories
        if index == -1:
            data = self.dataframe['STATUS HISTORY'].tolist()
            return data

        # get status history at index row
        else:
            data = self.dataframe.iloc[index].loc['STATUS HISTORY']
            
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


    def status_history_window(self, window, index):
        # window = name of window from where this window will get called
        # dataframe and list for the get_status_history function
        
        # get data for this window; exit function if none available
        list = self.get_status_history(index)
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




    