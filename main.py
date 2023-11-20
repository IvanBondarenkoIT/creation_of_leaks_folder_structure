import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime, timedelta
import os
import shutil

DEFAULT_DB_FOLDER = "E:\_WORK\TESTS"
PAD_MAX = 10
PAD_MIN = 5
WINDOW_SIZE = "500x600"


def submit():
    selected = listbox.get(tk.ACTIVE)
    # flag_status = flag.get()
    file_path = file_path_var.get()
    file_name = file_name_label.cget("text")
    date_value = date_var.get()
    text1_content = text_readme.get("1.0", tk.END)
    text2_content = text_pass.get()
    text3_content = text_domein.get()


    print("Selected from list:", selected)
    # print("Flag status:", flag_status)
    print("File path:", file_path)
    print("File name:", file_name)
    print("Date:", date_value)
    print("Text 1 content:", text1_content)
    print("Text 2 content:", text2_content)
    print("Text 3 content:", text3_content)

    leak_name_folder = create_directory_structure(selected, date_value, text1_content, text2_content, text3_content)
    print(leak_name_folder)
    remove_file_to_leak_folder(file_path, leak_name_folder)
    result_message = leak_name_folder
    messagebox.showinfo(title="Message", message="File replaced to: " + result_message)


def choose_file():
    file_path = filedialog.askopenfilename()
    file_path_var.set(file_path)
    file_name_label.config(text=file_path)
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    domein_value.set(os.path.basename(file_name))


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


def create_directory_structure(selected_value, date_value, leak_name_value, pass_text, domain_text):
    db_folder = DEFAULT_DB_FOLDER
    listbox_folder = os.path.join(db_folder, selected_value)
    date_folder = os.path.join(listbox_folder, date_value)
    if domain_text:
        leak_name_folder = os.path.join(date_folder, domain_text)
    else:
        leak_name_folder = os.path.join(date_folder, leak_name_value.split("\n")[0])

    if_directory_not_exist_create_new(db_folder)
    if_directory_not_exist_create_new(listbox_folder)
    if_directory_not_exist_create_new(date_folder)
    if_directory_not_exist_create_new(leak_name_folder)

    readme_file = os.path.join(leak_name_folder, "readme.txt")

    #
    # # Remove file if exists
    # if os.path.exists(readme_file):
    #     os.remove(readme_file)
    # Clear file
    file = open(readme_file, 'w')
    file.close()

    # Create an empty readme file
    with open(readme_file, 'w') as file:

        if domain_text and listbox.get(tk.ACTIVE) == "Database":
            file.write(domain_text+'\n')

        file.write(leak_name_value)

        if pass_text:
            file.write(pass_text)

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
root.geometry(WINDOW_SIZE)

# List
options = ["Combo", "Database", "Logs", "Mixed"]
listbox = tk.Listbox(root, height=4)
for option in options:
    listbox.insert(tk.END, option)
listbox.select_set(0)
print(listbox.get(tk.ACTIVE))
listbox.grid(padx=PAD_MAX, pady=PAD_MIN, row=0, column=0, rowspan=4, sticky=tk.W+tk.E)
# listbox.pack(padx=20, pady=20, )

# Flag
# flag = tk.BooleanVar()
# flag_checkbox = tk.Checkbutton(root, text="Is TG", variable=flag)
# flag_checkbox.grid(row=4, column=0)
# flag_checkbox.pack()

# File Chooser
file_path_var = tk.StringVar()
file_button = tk.Button(root, text="Choose File", command=choose_file)
file_button.grid(padx=PAD_MAX, pady=PAD_MIN, row=4, column=0, sticky=tk.W+tk.E)
# file_button.pack()

file_name_label = tk.Label(root, text="")
file_name_label.grid(padx=PAD_MAX, pady=PAD_MIN, row=4, column=1, sticky=tk.W+tk.E)
# file_name_label.pack()

# Date Field (YYYY-MM-DD)
date_var = tk.StringVar()
date_var.set(datetime.now().strftime("%Y-%m-%d"))
date_entry = tk.Entry(root, textvariable=date_var)
date_entry.grid(padx=PAD_MAX, pady=PAD_MIN,row=1, column=1, sticky=tk.W+tk.E)


# Date Increment and Decrement Buttons
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)

date_decrement_button = tk.Button(buttonframe, text="<", command=decrement_date)
date_decrement_button.grid(padx=PAD_MAX, pady=PAD_MIN,row=0, column=0, sticky=tk.W+tk.E)

date_increment_button = tk.Button(buttonframe, text=">", command=increment_date)
date_increment_button.grid(padx=PAD_MAX, pady=PAD_MIN,row=0, column=1, sticky=tk.W+tk.E)

buttonframe.grid(padx=PAD_MAX, pady=PAD_MIN,row=2, column=1, sticky=tk.W+tk.E)

# Text Fields
domein_label = tk.Label(root, text="Domein name(if exist)\Folder name: ")
domein_label.grid(padx=PAD_MAX, pady=PAD_MIN,row=6, column=0, sticky=tk.W+tk.E)


domein_value = tk.StringVar()
text_domein = tk.Entry(root,  width=30, textvariable=domein_value)
text_domein.grid(padx=PAD_MAX, pady=PAD_MIN,row=6, column=1, sticky=tk.W+tk.E)

readme_file_label = tk.Label(root, text="Readme File Content: ")
readme_file_label.grid(padx=PAD_MAX, pady=PAD_MIN,row=7, column=0, sticky=tk.W+tk.E)

text_readme = tk.Text(root, height=4, width=40)
text_readme.grid(padx=PAD_MAX, pady=PAD_MIN,row=9, column=0, columnspan=2, sticky=tk.W+tk.E)

pass_label = tk.Label(root, text="Password(if exist): ")
pass_label.grid(padx=PAD_MAX, pady=PAD_MIN, row=10, column=0, sticky=tk.W+tk.E)

text_pass = tk.Entry(root,  width=30)
text_pass.grid(padx=PAD_MAX, pady=PAD_MIN, row=10, column=1, sticky=tk.W+tk.E)
#
# text3 = tk.Text(root, height=2, width=30)
# text3.pack()

folder_label = tk.Label(root, text="Data Base(db) folder path: ")
folder_label.grid(padx=PAD_MAX, pady=PAD_MIN, row=11, column=0, sticky=tk.W+tk.E)

text_folder = tk.Entry(root,  width=30)
text_folder.grid(padx=PAD_MAX, pady=PAD_MIN, row=11, column=1, sticky=tk.W+tk.E)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(padx=PAD_MAX, pady=PAD_MIN,row=12, column=1, sticky=tk.W+tk.E)

root.mainloop()
