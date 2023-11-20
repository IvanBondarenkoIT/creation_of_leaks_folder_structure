import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta


class FileManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Leeks file manager")
        master.geometry("500x600")

        self.DEFAULT_DB_FOLDER = "E:/_WORK/TESTS"
        self.PAD_MAX = 10
        self.PAD_MIN = 5

        # Initialize variables
        self.selected_value = tk.StringVar(value="Combo")
        self.file_path_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.domain_value = tk.StringVar()
        self.text1_content = tk.StringVar()
        self.text2_content = tk.StringVar()
        self.text3_content = tk.StringVar()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Listbox
        self.listbox = tk.Listbox(self.master, height=4, listvariable=self.selected_value, selectmode=tk.SINGLE)
        self.listbox.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=0, column=0, rowspan=4, sticky=tk.W + tk.E)

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
        domein_label = tk.Label(self.master, text="Domain name(if exist)/Folder name: ")
        domein_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=0, sticky=tk.W + tk.E)

        domein_entry = tk.Entry(self.master, width=30, textvariable=self.domain_value)
        domein_entry.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=6, column=1, sticky=tk.W + tk.E)

        # Text Readme
        readme_file_label = tk.Label(self.master, text="Readme File Content: ")
        readme_file_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=7, column=0, sticky=tk.W + tk.E)

        text_readme = tk.Text(self.master, height=4, width=40)
        text_readme.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=9, column=0, columnspan=2, sticky=tk.W + tk.E)

        # Password Entry
        pass_label = tk.Label(self.master, text="Password(if exist): ")
        pass_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=0, sticky=tk.W + tk.E)

        text_pass = tk.Entry(self.master, width=30, textvariable=self.text2_content)
        text_pass.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=10, column=1, sticky=tk.W + tk.E)

        # Folder Entry
        folder_label = tk.Label(self.master, text="Data Base(db) folder path: ")
        folder_label.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=11, column=0, sticky=tk.W + tk.E)

        text_folder = tk.Entry(self.master, width=30)
        text_folder.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=11, column=1, sticky=tk.W + tk.E)

        # Submit button
        submit_button = tk.Button(self.master, text="Submit", command=self.submit)
        submit_button.grid(padx=self.PAD_MAX, pady=self.PAD_MIN, row=12, column=1, sticky=tk.W + tk.E)

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
        selected = self.listbox.get(tk.ACTIVE)
        file_path = self.file_path_var.get()
        date_value = self.date_var.get()
        text1_content = self.text1_content.get()
        text2_content = self.text2_content.get()
        text3_content = self.domain_value.get()

        print("Selected from list:", selected)
        print("File path:", file_path)
        print("Date:", date_value)
        print("Text 1 content:", text1_content)
        print("Text 2 content:", text2_content)
        print("Text 3 content:", text3_content)

        leak_name_folder = self.create_directory_structure(selected, date_value, text1_content, text2_content, text3_content)
        print(leak_name_folder)
        self.remove_file_to_leak_folder(file_path, leak_name_folder)
        result_message = leak_name_folder
        messagebox.showinfo(title="Message", message="File replaced to: " + result_message)

    def if_directory_not_exist_create_new(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def create_directory_structure(self, selected_value, date_value, leak_name_value, pass_text, domain_text):
        db_folder = self.DEFAULT_DB_FOLDER
        listbox_folder = os.path.join(db_folder, selected_value)
        date_folder = os.path.join(listbox_folder, date_value)
        if domain_text:
            leak_name_folder = os.path.join(date_folder, domain_text)
        else:
            leak_name_folder = os.path.join(date_folder, leak_name_value.split("\n")[0])

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

    def remove_file_to_leak_folder(self, file_path, leak_name_folder):
        if file_path and os.path.exists(file_path):
            shutil.move(file_path, leak_name_folder)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
