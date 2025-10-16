import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta

from json_reader import Message, Messages

DEFAULT_DB_FOLDER = "E:\\_WORK\\db"
PAD_MAX = 10
PAD_MIN = 5
WINDOW_SIZE = "530x600"
OPTIONS = ["Combo", "Database", "Logs", "Mixed"]


class FileManagerApp:
    def __init__(self, master, work_folder=DEFAULT_DB_FOLDER, settings=None, work_links: dict = None, messages: dict[str, Message] = None):
        self.messages = messages or {}
        print(self.messages)

        self.master = master
        master.title("Leeks file manager")
        master.geometry(WINDOW_SIZE)

        self.settings = settings or {}
        self.work_links = work_links or {}
        self.DEFAULT_DB_FOLDER = work_folder
        self.db_folder = tk.StringVar(value=DEFAULT_DB_FOLDER)
        self.PAD_MAX = 10
        self.PAD_MIN = 5

        # Initialize variables
        self.selected_value = tk.StringVar(value="Combo")
        self.flag = tk.BooleanVar(value=True)

        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.domain_value = tk.StringVar()

        self.file_path_var = tk.StringVar()
        self.file_name_label = tk.Label(self.master, text="")

        self.messages_file_path_var = tk.StringVar()
        self.messages_file_path_label = tk.Label(self.master, text="")

        self.link_value = tk.StringVar()
        self.topic_value = tk.StringVar()

        self.readme_value = tk.StringVar()
        self.password_value = tk.StringVar()

        self.combobox_value = tk.StringVar()

        # Create widgets
        self.create_widgets()

        # Bind the callback function to the text_topic_link variable
        self.link_value.trace_add("write", self.update_topic_name)
        self.combobox_value.trace_add("write", self.update_topic_name_by_combobox)

    def create_widgets(self):
        combobox_label = tk.Label(self.master, text="Select Option:")
        combobox_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=0, sticky=tk.W)

        self.combobox = ttk.Combobox(self.master, textvariable=self.selected_value, values=OPTIONS, state="readonly")
        self.combobox.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=1, sticky=tk.W + tk.E)
        self.combobox.current(0)
        self.combobox.grid(row=1, column=0)

        flag_checkbox = tk.Checkbutton(self.master, text="Autofill", variable=self.flag)
        flag_checkbox.grid(row=0, column=1)

        file_button = tk.Button(self.master, text="Choose File", command=self.choose_file)
        file_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=4, column=0, sticky=tk.W + tk.E)
        self.file_name_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=4, column=1, sticky=tk.W + tk.E)

        date_entry = tk.Entry(self.master, textvariable=self.date_var)
        date_entry.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=1, column=1, sticky=tk.W + tk.E)

        buttonframe = tk.Frame(self.master)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)

        date_decrement_button = tk.Button(buttonframe, text="<", command=self.decrement_date)
        date_decrement_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=0, sticky=tk.W + tk.E)

        date_increment_button = tk.Button(buttonframe, text=">", command=self.increment_date)
        date_increment_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=1, sticky=tk.W + tk.E)

        buttonframe.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=2, column=1, sticky=tk.W + tk.E)

        domain_label = tk.Label(self.master, text="Domain name(if exist)/Folder name: ")
        domain_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=0, sticky=tk.W + tk.E)

        domain_entry = tk.Entry(self.master, width=40, textvariable=self.domain_value)
        domain_entry.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=1, sticky=tk.W + tk.E)

        topic_link_label = tk.Label(self.master, text="Forum link / TG link:")
        topic_link_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=0, sticky=tk.W + tk.E)

        text_topic_link = tk.Entry(self.master, width=40, textvariable=self.link_value)
        text_topic_link.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=1, sticky=tk.W + tk.E)

        link_button = tk.Button(self.master, text="+1", command=self.link_plus_one)
        link_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=3, sticky=tk.W + tk.E)

        topic_name_label = tk.Label(self.master, text="Topic name / TG channel:")
        topic_name_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=8, column=0, sticky=tk.W + tk.E)

        text_topic_name = tk.Entry(self.master, width=40, textvariable=self.topic_value)
        text_topic_name.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=8, column=1, sticky=tk.W + tk.E)

        pass_label = tk.Label(self.master, text="Password(if exist): ")
        pass_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=0, sticky=tk.W + tk.E)

        text_pass = tk.Entry(self.master, width=40, textvariable=self.password_value)
        text_pass.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=1, sticky=tk.W + tk.E)

        label = tk.Label(self.master, text="Choose source: ")
        label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=12, column=0, sticky=tk.W + tk.E)

        work_links_keys = list(self.work_links.keys())
        combobox = ttk.Combobox(textvariable=self.combobox_value, values=work_links_keys)
        combobox.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=12, column=1, sticky=tk.W + tk.E)

        chose_messages_file_button = tk.Button(self.master, text="JSON messages File", command=self.choose_messages_file)
        chose_messages_file_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=13, column=0, sticky=tk.W + tk.E)

        self.messages_file_path_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=13, column=1, sticky=tk.W + tk.E)

        submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        submit_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=15, column=1, sticky=tk.W + tk.E)

        chain_submit_button = tk.Button(self.master, text="Chain Submit", command=self.chain_submit)
        chain_submit_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=16, column=1, sticky=tk.W + tk.E)

    def update_topic_name(self, *args):
        if self.flag.get():
            new_value = self.link_value.get()
            self.topic_value.set(new_value.replace(str(new_value.split("/")[-1]), ""))

    def update_topic_name_by_combobox(self, *args):
        new_value = self.work_links[self.combobox_value.get()]
        self.topic_value.set(new_value)

    def choose_messages_file(self):
        messages_file_path = filedialog.askopenfilename()
        self.messages_file_path_var.set(messages_file_path)
        self.messages_file_path_label.config(text=messages_file_path)
        if messages_file_path:
            messages = Messages(file_path=messages_file_path)
            self.messages = messages.get_messages()

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_var.set(file_path)
        self.file_name_label.config(text=file_path)
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        self.domain_value.set(os.path.basename(file_name))

        if file_name + file_extension in self.messages.keys():
            print(self.messages[file_name + file_extension])

            self.date_var.set(self.messages[file_name + file_extension].date)

            new_value = self.link_value.get()
            self.link_value.set(
                new_value.replace(str(new_value.split("/")[-1]), str(self.messages[file_name + file_extension].id))
            )

    def increment_date(self):
        current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        new_date = current_date + timedelta(days=1)
        self.date_var.set(new_date.strftime("%Y-%m-%d"))

    def decrement_date(self):
        current_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d")
        new_date = current_date - timedelta(days=1)
        self.date_var.set(new_date.strftime("%Y-%m-%d"))

    def link_plus_one(self):
        new_value = self.link_value.get()
        link_number_plus_one = int(new_value.split("/")[-1]) + 1
        self.link_value.set(new_value.replace(str(new_value.split("/")[-1]), f"{link_number_plus_one}"))

    def submit(self):
        leak_name_folder = self.create_directory_structure()
        self.remove_file_to_leak_folder(leak_name_folder)
        messagebox.showinfo(title="Message", message="File replaced to: " + leak_name_folder)

    def is_valid_folder_name(self, name):
        pattern = re.compile(r'^[^/\\:*?"<>|]+$')
        return bool(pattern.match(name))

    def clean_folder_name(self, name):
        return re.sub(r'[\\/:*?"<>| ]', "", name)

    def if_directory_not_exist_create_new(self, folder_name):
        if not os.path.exists(folder_name):
            if self.is_valid_folder_name(folder_name):
                folder_name = self.clean_folder_name(folder_name)
            os.makedirs(folder_name)

    def create_directory_structure(self):
        selected = self.combobox.get()
        domain_text = self.domain_value.get().strip()  # Trim leading/trailing spaces
        topic_text = self.topic_value.get().strip()    # Trim leading/trailing spaces
        leak_name_value = f"{topic_text}\n{self.link_value.get()}\n"
        pass_text = self.password_value.get()

        db_folder = self.DEFAULT_DB_FOLDER
        listbox_folder = os.path.join(db_folder, selected)
        date_folder = os.path.join(listbox_folder, self.date_var.get())
        if domain_text:
            leak_name_folder = os.path.join(date_folder, domain_text)
        else:
            leak_name_folder = os.path.join(date_folder, topic_text)

        self.if_directory_not_exist_create_new(db_folder)
        self.if_directory_not_exist_create_new(listbox_folder)
        self.if_directory_not_exist_create_new(date_folder)
        self.if_directory_not_exist_create_new(leak_name_folder)

        readme_file = os.path.join(leak_name_folder, "readme.txt")

        with open(readme_file, "w"):
            pass

        with open(readme_file, "w") as file:
            if domain_text and selected == "Database":
                file.write(domain_text + "\n")
            file.write(leak_name_value)
            if pass_text:
                file.write(pass_text)

        return leak_name_folder

    def remove_file_to_leak_folder(self, leak_name_folder):
        if os.path.exists(self.file_path_var.get()):
            shutil.move(self.file_path_var.get(), leak_name_folder)

    def chain_submit(self):
        folder_path = filedialog.askdirectory(title="Choose Folder with Files")
        if not folder_path:
            return

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                self.file_path_var.set(file_path)
                self.file_name_label.config(text=file_path)

                file_name_only, file_extension = os.path.splitext(os.path.basename(file_path))
                self.domain_value.set(os.path.basename(file_name_only))

                full_file_name = file_name_only + file_extension
                if full_file_name in self.messages:
                    msg = self.messages[full_file_name]
                    self.date_var.set(msg.date)
                    new_value = self.link_value.get()
                    self.link_value.set(
                        new_value.replace(str(new_value.split("/")[-1]), str(msg.id))
                    )

                leak_name_folder = self.create_directory_structure()
                self.remove_file_to_leak_folder(leak_name_folder)

        messagebox.showinfo(title="Chain Submit", message="All files processed.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
