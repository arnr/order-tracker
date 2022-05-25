import os
from tkinter import CENTER, ttk
import openpyxl
import pandas as pd







class order:

    def __init__(self) -> None:
        self.df = self.load_excel()
    

    # gets data from main excel sheet and puts it into a pandas dataframe. 
    # Dataframe is processed to show only wanted data.
    def load_excel(self):

        cwd = os.getcwd()
        file_directory = os.path.join(cwd, 'program','files')
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

    # show rows for formated for proper displaying
    # if index_list is given then it will show only the rows corresponding to the number in index list
    def clean_df(self, index_list=[]):
        
        if index_list != []:
            result = self.df.loc[index_list].loc[:,self.df.columns != 'STATUS HISTORY']
        else:
            result = self.df.loc[:,self.df.columns != 'STATUS HISTORY']
        
        return result


    # takes the treeview object (table) and populates it with data from provided dataframe (dataframe) 
    @staticmethod
    def load_table(table:ttk.Treeview, dataframe:pd.DataFrame): 

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

    #show rows based on a term 'searchTerm' down a CURRENT STATUS column
    def sort_by_status(self, search_term):

        df = self.df
        col_name = "CURRENT STATUS"

        if search_term == "ordered":
            search1 = df[df[col_name].str.contains(search_term)]
            index_list1 = search1.index.values

            search2 = df[df[col_name].str.contains("reordered")]
            index_list2 = search1.index.values

            return list(set(index_list1) - set(index_list2)) + list(set(index_list2) - set(index_list1))

        else:
            search = df[df[col_name].str.contains(search_term)]
            return search.index.values

        


