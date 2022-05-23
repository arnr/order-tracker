import row_editor


# edit a selected row
def edit_row(tree, df, root):
    new_row = row_editor.row_editor(tree, df, root)
    new_row.editor()