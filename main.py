import tkinter as tk
from my_classes import FileManagerApp
from settings import Settings

if __name__ == "__main__":
    root = tk.Tk()
    settings = Settings()
    work_folder = settings.get_work_folder_from_file()
    app = FileManagerApp(root, work_folder, settings)
    root.mainloop()
    settings.set_work_folder_to_file(work_folder)
