import pandas as pd
import argparse
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
# import matplotlib.pyplot as plt 
import pandasgui as pdgui
import os

# os.environ["PANDASGUI_BACKEND"] = "PySide2"

class UnsupportedFileType(Exception):
    pass

def read_excel(path: str) -> pd.DataFrame:
    return pd.read_excel(path)

def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def read_json(path: str) -> pd.DataFrame:
    return pd.read_json(path)

def unsupported(*args) -> None:
    raise UnsupportedFileType

SUPPORTED = {".xlsx": read_excel, ".csv": read_csv, ".json": read_json, None: unsupported}

def getfilename() -> str:
    #tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return file_path

def getfiletype(path: str) -> str | None:
    filetype = pathlib.Path(path).suffix
    if filetype in SUPPORTED:
        return filetype
    else:
        None

def getdata() -> pd.DataFrame:
    path = getfilename()
    data = SUPPORTED[getfiletype(path)](path)
    return data

def showdata(data: pd.DataFrame):
    gui = pdgui.show(data , settings={'block': True})
    return gui

def load_dataframe():
    global data
    data = getdata()

    treeview = ttk.Treeview(window)
    treeview["columns"] = tuple(data.columns)
    treeview["show"] = "headings"

    for column in data.columns:
        treeview.heading(column, text=column)

    for row in data.itertuples(index=False):
        for el in row:
            treeview.insert("", "end", values=el)

    treeview.pack(expand=True)

    # Create a variable to track the currently selected item
    selected_item = ""

    # Define a function to handle item selection
    def on_select(event):
        global selected_item
        selected_item = treeview.focus()

    # Bind the item selection event to the function
    treeview.bind("<<TreeviewSelect>>", on_select)

    # Define a callback function for calculating mean
    def calculate_mean():
        selected_columns = treeview.selection()[0].split() if treeview.selection() else []
        if selected_columns:
            selected_values = [[treeview.set("", column) for column in selected_columns]]
            selected_df = pd.DataFrame(selected_values, columns=selected_columns)
            mean_values = selected_df.mean()
            print("Mean values:")
            print(mean_values)

    # Define a callback function for calculating standard deviation
    def calculate_std():
        selected_columns = treeview.selection()[0].split() if treeview.selection() else []
        if selected_columns:
            selected_values = [[treeview.set("", column) for column in selected_columns]]
            selected_df = pd.DataFrame(selected_values, columns=selected_columns)
            std_values = selected_df.std()
            print("Standard deviation values:")
            print(std_values)

    # Create buttons to calculate mean and standard deviation
    mean_button = ttk.Button(window, text="Calculate Mean", command=calculate_mean)
    mean_button.pack()

    std_button = ttk.Button(window, text="Calculate Std", command=calculate_std)
    std_button.pack()


def mean():
    selected_item = treeview.focus()

    if selected_item:
        values = treeview.item(selected_item)["values"]
        selected_column = values[colum_index]
        mean = data[selected_column].mean()
        tk.messagebox.showinfo("Mean Calculation", f"The mean of {selected_column} is {mean:.2f}.")
    else:
        tk.messagebox.showwarning("No Selection", "Please select a row in the dataframe.")



data = None
window = tk.Tk()
window.title("Dataframe Viewer")

load_button = ttk.Button(window, text="Load Dataframe", command=load_dataframe)
load_button.pack()

mean_button = ttk.Button(window, text="Calculate Mean", command=mean)
mean_button.pack()

visualise_button = ttk.Button(window, text="Visualise", command=lambda: showdata(data))
visualise_button.pack()

window.mainloop()
#import pandas as pd
#from pandasgui import show
#df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6], 'c':[7,8,9]})
#show(df , settings={'block': True})

# data = getdata()
# showdata(data)

#data = pd.read_excel("data/data.xlsx")

#print(data)
#print("\n\n------------------\n\n")
#print(list(data))