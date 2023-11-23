import tkinter as tk
from my_classes import FileManagerApp
from settings import Settings

if __name__ == "__main__":
    root = tk.Tk()
    settings = Settings()
    app = FileManagerApp(root, settings.get_work_folder_from_file())
    root.mainloop()
