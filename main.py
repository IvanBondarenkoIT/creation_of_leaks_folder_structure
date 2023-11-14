import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
import os
import shutil

DEFAULT_DB_FOLDER = "DB"


def submit():
    selected = listbox.get(tk.ACTIVE)
    # flag_status = flag.get()
    file_path = file_path_var.get()
    file_name = file_name_label.cget("text")
    date_value = date_var.get()
    text1_content = text_readme.get("1.0", tk.END)
    text2_content = text_pass.get("1.0", tk.END)
    # text3_content = text3.get("1.0", tk.END)

    print("Selected from list:", selected)
    # print("Flag status:", flag_status)
    print("File path:", file_path)
    print("File name:", file_name)
    print("Date:", date_value)
    print("Text 1 content:", text1_content)
    print("Text 2 content:", text2_content)
    # print("Text 3 content:", text3_content)

    leak_name_folder = create_directory_structure(selected, date_value, text1_content.replace("\n", ""))
    print(leak_name_folder)
    remove_file_to_leak_folder(file_path, leak_name_folder)


def choose_file():
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)
    file_name_label.config(text=file_path)


def increment_date():
    current_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
    new_date = current_date + timedelta(days=1)
    date_var.set(new_date.strftime("%Y-%m-%d"))


def decrement_date():
    current_date = datetime.strptime(date_var.get(), "%Y-%m-%d")
    new_date = current_date - timedelta(days=1)
    date_var.set(new_date.strftime("%Y-%m-%d"))


def if_directory_not_exist_create_new(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def create_directory_structure(selected_value, date_value, leak_name_value):
    db_folder = DEFAULT_DB_FOLDER
    listbox_folder = os.path.join(db_folder, selected_value)
    date_folder = os.path.join(listbox_folder, date_value)
    leak_name_folder = os.path.join(date_folder, leak_name_value)

    if_directory_not_exist_create_new(db_folder)
    if_directory_not_exist_create_new(listbox_folder)
    if_directory_not_exist_create_new(date_folder)
    if_directory_not_exist_create_new(leak_name_folder)

    readme_file = os.path.join(leak_name_folder, "readme.txt")

    #
    # # Remove file if exists
    # if os.path.exists(readme_file):
    #     os.remove(readme_file)

    # Create an empty readme file
    with open(readme_file, 'w') as file:
        file.write(leak_name_value)

    return leak_name_folder


def remove_file_to_leak_folder(file_path, leak_name_folder):
    if file_path and os.path.exists(file_path):
        # db_folder = "DB"
        # selected_value = listbox.get(tk.ACTIVE)
        # date_value = date_var.get()
        # date_folder = os.path.join(db_folder, selected_value, date_value)
        # leak_name_folder = os.path.join(date_folder, leak_name_value)
        shutil.move(file_path, leak_name_folder)


root = tk.Tk()
root.title("Leeks file manager")
root.geometry("400x320")

# List
options = ["Combo", "Database", "Logs", "Mixed"]
listbox = tk.Listbox(root, height=4)
for option in options:
    listbox.insert(tk.END, option)
listbox.grid(padx=10, pady=10, row=0, column=0, rowspan=4, sticky=tk.W+tk.E)
# listbox.pack(padx=20, pady=20, )

# Flag
# flag = tk.BooleanVar()
# flag_checkbox = tk.Checkbutton(root, text="Is TG", variable=flag)
# flag_checkbox.grid(row=4, column=0)
# flag_checkbox.pack()

# File Chooser
file_path_var = tk.StringVar()
file_button = tk.Button(root, text="Choose File", command=choose_file)
file_button.grid(padx=10, pady=10,row=4, column=0, sticky=tk.W+tk.E)
# file_button.pack()

file_name_label = tk.Label(root, text="Selected File: ")
file_name_label.grid(padx=10, pady=10,row=5, column=0, columnspan=2, sticky=tk.W+tk.E)
# file_name_label.pack()

# Date Field (YYYY-MM-DD)
date_var = tk.StringVar()
date_var.set(datetime.now().strftime("%Y-%m-%d"))
date_entry = tk.Entry(root, textvariable=date_var)
date_entry.grid(padx=10, pady=10,row=1, column=1, sticky=tk.W+tk.E)


# Date Increment and Decrement Buttons
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)


date_increment_button = tk.Button(buttonframe, text="<", command=increment_date)
date_increment_button.grid(padx=10, pady=10,row=0, column=0, sticky=tk.W+tk.E)

date_decrement_button = tk.Button(buttonframe, text=">", command=decrement_date)
date_decrement_button.grid(padx=10, pady=10,row=0, column=1, sticky=tk.W+tk.E)

buttonframe.grid(padx=10, pady=10,row=2, column=1, sticky=tk.W+tk.E)

# Text Fields
readme_file_label = tk.Label(root, text="Readme File Content: ")
readme_file_label.grid(padx=10, pady=10,row=6, column=0, sticky=tk.W+tk.E)

text_readme = tk.Text(root, height=4, width=40)
text_readme.grid(padx=10, pady=10,row=7, column=0, columnspan=2, sticky=tk.W+tk.E)

pass_label = tk.Label(root, text="Password(if exist): ")
pass_label.grid(padx=10, pady=10,row=8, column=0, sticky=tk.W+tk.E)

text_pass = tk.Entry(root,  width=30)
text_pass.grid(padx=10, pady=10,row=8, column=1, sticky=tk.W+tk.E)
#
# text3 = tk.Text(root, height=2, width=30)
# text3.pack()

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(padx=10, pady=10,row=9, column=1, sticky=tk.W+tk.E)

root.mainloop()
