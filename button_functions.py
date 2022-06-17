import row_editor
import orders


data = orders.order()


# edit a selected row
def edit_row(tree, root):

    new_row = row_editor.row_editor(tree, data.df, root)
    new_row.editor()


def populate_table(tree, view_type=""):
    # view_type must be one of the current status types so as to display that type of orders in the treeview
    if view_type:
        index = data.sort_by_status(view_type)
        data.load_table(tree, data.clean_df(index))
    else:
        data.load_table(tree,data.clean_df())


def selective_populate():
    pass


def test(tree, view_type):
    # index = data.sort_by_status(view_type)
    # print(index)

    df = data.df
    col_name = "CURRENT STATUS"
    # test_str=view_type
    # print(type(test_str))
    # print(test_str)
    # search1 = df[df[col_name].str.contains(view_type)]
    # search1 = df[df[col_name].str.contains("ordered")]
    # index_list1 = search1.index.values

    # print(index_list1)

    filt = df[col_name].str.contains("ordered") & (~df[col_name].str.contains("reordered"))
    df1=df[filt]
    df1_index = df1.index.values
    print(df1)
    



    df2= data.clean_df(df1_index)
    data.load_table(tree,df2)

def test2(tree, search_term):
    index = data.search(search_term)
    # cleaned_data = data.clean_df(index)
    # print(cleaned_data)
    data.load_table(tree, index)