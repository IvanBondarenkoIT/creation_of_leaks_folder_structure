import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

DEFAULT_DB_FOLDER = "E:\_WORK\db"
PAD_MAX = 10
PAD_MIN = 5
WINDOW_SIZE = "500x600"
OPTIONS = ["Combo", "Database", "Logs", "Mixed"]


class FileManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Leeks file manager")
        master.geometry("600x600")

        self.DEFAULT_DB_FOLDER = DEFAULT_DB_FOLDER
        self.db_folder = tk.StringVar(value=DEFAULT_DB_FOLDER)
        self.PAD_MAX = 10
        self.PAD_MIN = 5

        # Initialize variables
        self.selected_value = tk.StringVar(value="Combo")
        self.flag = tk.BooleanVar(value=True)
        self.file_path_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.domain_value = tk.StringVar()

        self.link_value = tk.StringVar()
        self.topic_value = tk.StringVar()

        self.readme_value = tk.StringVar()
        self.password_value = tk.StringVar()

        # Create widgets
        self.create_widgets()

        # Bind the callback function to the text_topic_link variable
        self.link_value.trace_add("write", self.update_topic_name)

        # Create widgets
        self.create_widgets()


    def create_widgets(self):
        # Listbox

        # List
        options = OPTIONS
        self.listbox = tk.Listbox(self.master, height=4)
        for option in options:
            self.listbox.insert(tk.END, option)
        self.listbox.select_set(0)
        # print(listbox.get(tk.ACTIVE))
        self.listbox.grid(padx=PAD_MAX, pady=PAD_MIN, row=0, column=0, rowspan=4, sticky=tk.W + tk.E)
        # listbox.pack(padx=20, pady=20, )

        # self.listbox = tk.Listbox(self.master, height=4, listvariable=self.selected_value, selectmode=tk.SINGLE)
        # self.listbox.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=0, rowspan=4, sticky=tk.W + tk.E)

        # Flag
        self.flag_checkbox = tk.Checkbutton(self.master, text="Is TG?", variable=self.flag)
        self.flag_checkbox.grid(row=0, column=1)

        # File Chooser
        file_button = tk.Button(self.master, text="Choose File", command=self.choose_file)
        file_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=4, column=0, sticky=tk.W + tk.E)

        self.file_name_label = tk.Label(self.master, text="")
        self.file_name_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=4, column=1, sticky=tk.W + tk.E)

        # Date Field (YYYY-MM-DD)
        date_entry = tk.Entry(self.master, textvariable=self.date_var)
        date_entry.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=1, column=1, sticky=tk.W + tk.E)

        # Date Increment and Decrement Buttons
        buttonframe = tk.Frame(self.master)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)

        date_decrement_button = tk.Button(buttonframe, text="<", command=self.decrement_date)
        date_decrement_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=0, sticky=tk.W + tk.E)

        date_increment_button = tk.Button(buttonframe, text=">", command=self.increment_date)
        date_increment_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=1, sticky=tk.W + tk.E)

        buttonframe.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=2, column=1, sticky=tk.W + tk.E)

        # Domain Entry
        domain_label = tk.Label(self.master, text="Domain name(if exist)/Folder name: ")
        domain_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=0, sticky=tk.W + tk.E)

        domain_entry = tk.Entry(self.master, width=30, textvariable=self.domain_value)
        domain_entry.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=1, sticky=tk.W + tk.E)

        # Link Entry
        topic_link_label = tk.Label(self.master, text="Forum / TG link:")
        topic_link_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=0, sticky=tk.W + tk.E)

        text_topic_link = tk.Entry(self.master, width=30, textvariable=self.link_value)
        text_topic_link.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=1, sticky=tk.W + tk.E)

        # Topic Entry
        topic_name_label = tk.Label(self.master, text="Topic name / TG channel name:")
        topic_name_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=8, column=0, sticky=tk.W + tk.E)

        text_topic_name = tk.Entry(self.master, width=30, textvariable=self.topic_value)
        text_topic_name.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=8, column=1, sticky=tk.W + tk.E)

        # Text Readme
        # text_readme = tk.Text(self.master, height=4, width=40)
        # text_readme.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=9, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Password Entry
        pass_label = tk.Label(self.master, text="Password(if exist): ")
        pass_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=0, sticky=tk.W + tk.E)

        text_pass = tk.Entry(self.master, width=30, textvariable=self.password_value)
        text_pass.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=1, sticky=tk.W + tk.E)

        # Folder Entry
        # folder_label = tk.Label(self.master, text="Data Base(db) folder path: ")
        # folder_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=11, column=0, sticky=tk.W + tk.E)
        #
        # text_folder = tk.Entry(self.master, width=30, textvariable=self.db_folder)
        # text_folder.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=11, column=1, sticky=tk.W + tk.E)

        # Submit button
        submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        submit_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=12, column=1, sticky=tk.W + tk.E)

    def update_topic_name(self):
        # Callback function to update text_topic_name when text_topic_link changes if TG flag=True
        if self.flag:
            new_value = self.link_value.get()
            self.topic_value.set(new_value.replace(str(new_value.split("/")[-1]), ""))

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_var.set(file_path)
        self.file_name_label.config(text=file_path)
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        self.domain_value.set(os.path.basename(file_name))

    def increment_date(self):
        current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        new_date = current_date + timedelta(days=1)
        self.date_var.set(new_date.strftime("%Y-%m-%d"))

    def decrement_date(self):
        current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        new_date = current_date - timedelta(days=1)
        self.date_var.set(new_date.strftime("%Y-%m-%d"))

    def submit(self):

        leak_name_folder = self.create_directory_structure()
        self.remove_file_to_leak_folder(leak_name_folder)
        messagebox.showinfo(title="Message", message="File replaced to: " + leak_name_folder)

    def is_valid_folder_name(self, name):
        # Define a regular expression for a valid folder name
        # Valid folder name should not contain special characters like / \ : * ? " < > |
        pattern = re.compile(r'^[^/\\:*?"<>|]+$')
        return bool(pattern.match(name))

    def clean_folder_name(self, name):
        # Remove invalid characters from the folder name
        return re.sub(r'[\\/:*?"<>|]', '', name)

    def if_directory_not_exist_create_new(self, folder_name):
        if not os.path.exists(folder_name):

            if self.is_valid_folder_name(folder_name):
                folder_name = self.clean_folder_name(folder_name)

            os.makedirs(folder_name)

    def create_directory_structure(self):
        selected = self.listbox.get(tk.ACTIVE)
        domain_text = self.domain_value.get()
        leak_name_value = f"{self.topic_value.get()}\n{self.link_value.get()}\n"
        pass_text = self.password_value.get()

        db_folder = self.DEFAULT_DB_FOLDER
        listbox_folder = os.path.join(db_folder, selected)
        date_folder = os.path.join(listbox_folder, self.date_var.get())
        if domain_text:
            leak_name_folder = os.path.join(date_folder, domain_text)
        else:
            leak_name_folder = os.path.join(date_folder, self.topic_value.get())

        self.if_directory_not_exist_create_new(db_folder)
        self.if_directory_not_exist_create_new(listbox_folder)
        self.if_directory_not_exist_create_new(date_folder)
        self.if_directory_not_exist_create_new(leak_name_folder)

        readme_file = os.path.join(leak_name_folder, "readme.txt")

        # Clear file
        with open(readme_file, 'w'):
            pass  # Do nothing

        # Create an empty readme file
        with open(readme_file, 'w') as file:
            if domain_text and self.listbox.get(tk.ACTIVE) == "Database":
                file.write(domain_text + '\n')

            file.write(leak_name_value)

            if pass_text:
                file.write(pass_text)

        return leak_name_folder

    def remove_file_to_leak_folder(self, leak_name_folder):
        if os.path.exists(self.file_path_var.get()):
            shutil.move(self.file_path_var.get(), leak_name_folder)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
