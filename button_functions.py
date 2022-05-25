import row_editor
import orders

# varaible to hold the current working dataframe for the various functions
working_df =""



# edit a selected row
def edit_row(tree, root):
    global working_df
    new_row = row_editor.row_editor(tree, working_df, root)
    new_row.editor()


def load_data(tree):
    data = orders.order()
    index = data.sort_by_status("received")
    data.load_table(tree, data.clean_df(index))

    global working_df
    working_df = data.df

    
def test():
    def Diff(li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
 
    # Driver Code
    li1 = [10, 15, 20, 25, 30, 35, 40]
    li2 = [25, 40, 35]
    print(Diff(li1, li2))