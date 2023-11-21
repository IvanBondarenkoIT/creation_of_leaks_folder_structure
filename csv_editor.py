import tkinter as tk
from tkinter import ttk, filedialog
import csv

class CSVEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("CSV Editor")

        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("#0", "Column1", "Column2", "Column3")  # Customize column names
        self.tree.heading("#0", text="Index")
        self.tree.heading("Column1", text="Column1")
        self.tree.heading("Column2", text="Column2")
        self.tree.heading("Column3", text="Column3")

        self.tree.column("#0", width=50)  # Adjust column width as needed
        self.tree.column("Column1", width=100)
        self.tree.column("Column2", width=100)
        self.tree.column("Column3", width=100)

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.load_csv_button = tk.Button(self.master, text="Load CSV", command=self.load_csv)
        self.load_csv_button.grid(row=1, column=0, padx=10, pady=10)

        self.save_csv_button = tk.Button(self.master, text="Save CSV", command=self.save_csv)
        self.save_csv_button.grid(row=1, column=1, padx=10, pady=10)

        # Create entry widgets for editing selected cell
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_var)
        self.entry.grid(row=2, column=0, padx=10, pady=10)

        # Set up event binding to handle cell selection
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        # Data container
        self.data = []

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                header = next(csv_reader)
                self.tree["columns"] = ("#0", *header)
                self.tree.heading("#0", text="Index")
                for col in header:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100)  # Adjust column width as needed
                self.data = [row for row in csv_reader]
                self.populate_treeview()

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([col for col in self.tree["columns"][1:]])
                csv_writer.writerows(self.data)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(self.data):
            self.tree.insert("", i, values=(i, *row))

    def on_tree_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        col_index = int(column.split('#')[-1])
        value = self.tree.item(item, 'values')[col_index]
        self.entry_var.set(value)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditorApp(root)
    app.run()
