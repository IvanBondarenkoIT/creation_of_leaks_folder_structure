import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class DictEditorApp:
    def __init__(self, root, source_file_name):
        self.root = root
        self.root.title("Dictionary Editor")

        self.my_dict = {}
        self.source_file_name = source_file_name

        # Create Menu
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load", command=self.load_dict)
        file_menu.add_command(label="Save", command=self.save_dict)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Choose Key Menu
        self.choose_key_menu = tk.Menu(self.edit_menu, tearoff=0)
        self.edit_menu.add_cascade(label="Choose Key", menu=self.choose_key_menu)

        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Add Key-Value", command=self.add_key_value)

        self.update_key_menu()

    def update_key_menu(self):
        # Update the cascading menu with dictionary keys
        self.choose_key_menu.delete(0, tk.END)

        for key in self.my_dict.keys():
            self.choose_key_menu.add_command(label=key, command=lambda k=key: self.edit_key_value(k))

    def edit_key_value(self, key):
        # Edit the value of a specific key
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Edit Value for Key: {key}")

        # Display current value
        current_value_label = tk.Label(edit_window, text=f"Current Value: {self.my_dict[key]}")
        current_value_label.pack(padx=10, pady=5)

        # Entry widget to edit the value
        new_value_label = tk.Label(edit_window, text="New Value:")
        new_value_label.pack(pady=5)
        new_value_entry = tk.Entry(edit_window)
        new_value_entry.pack(pady=10)

        # Button to update the value
        update_button = tk.Button(edit_window, text="Update Value", command=lambda: self.update_value(key, new_value_entry.get(), edit_window))
        update_button.pack()

    def update_value(self, key, new_value, edit_window):
        # Update the value for a specific key
        if new_value:
            self.my_dict[key] = new_value
            messagebox.showinfo("Success", f"Value for key '{key}' updated.")
            edit_window.destroy()
            self.update_key_menu()
        else:
            messagebox.showwarning("Warning", "New Value cannot be empty.")

    def add_key_value(self):
        # Add a new key-value pair to the dictionary
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Add Key-Value")

        key_label = tk.Label(edit_window, text="Key:")
        key_label.grid(row=0, column=0, padx=5, pady=5)
        key_entry = tk.Entry(edit_window)
        key_entry.grid(row=0, column=1, padx=5, pady=5)

        value_label = tk.Label(edit_window, text="Value:")
        value_label.grid(row=1, column=0, padx=5, pady=5)
        value_entry = tk.Entry(edit_window)
        value_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = tk.Button(
            edit_window, text="Add to Dictionary", command=lambda: self.add_to_dict(key_entry.get(), value_entry.get(), edit_window)
        )
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_to_dict(self, key, value, edit_window):
        # Add key-value pair to the dictionary
        if key and value:
            self.my_dict[key] = value
            messagebox.showinfo("Success", "Key-Value pair added to dictionary.")
            edit_window.destroy()
            self.update_key_menu()
        else:
            messagebox.showwarning("Warning", "Both Key and Value are required.")

    def save_dict(self):
        # Save the dictionary to a CSV file
        file_path = filedialog.asksaveasfilename(initialdir=".", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                for key, value in self.my_dict.items():
                    csv_writer.writerow([key, value])
            messagebox.showinfo("Success", "Dictionary saved to CSV file.")

    def load_dict(self, first_load: bool = False):
        # Load the dictionary from a CSV file
        if first_load:
            file_path = self.source_file_name
        else:
            file_path = filedialog.askopenfilename(initialdir=".", filetypes=[("CSV files", "*.csv")])

        if file_path:
            self.my_dict = {}
            with open(file_path, "r") as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if len(row) == 2:
                        key, value = row
                        self.my_dict[key] = value
            messagebox.showinfo("Success", "Dictionary loaded from CSV file.")
            self.update_key_menu()

    def get_dict(self):
        return self.my_dict

if __name__ == "__main__":
    root = tk.Tk()
    app = DictEditorApp(root)
    root.mainloop()
