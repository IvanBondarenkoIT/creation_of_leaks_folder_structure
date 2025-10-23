import os
import tkinter as tk
from my_classes import FileManagerApp
from settings import Settings
from menu import DictEditorApp
from json_reader import Messages

if __name__ == "__main__":
    root = tk.Tk()
    settings = Settings()
    work_folder = settings.get_work_folder_from_file()

    dict_editor = DictEditorApp(root,
                                source_file_name=settings.get_default_sources_file_name())

    dict_editor.load_dict(first_load=True)

    # Initialize with empty messages for testing
    app = FileManagerApp(root,
                         work_folder=work_folder,
                         settings=settings,
                         work_links=dict_editor.get_dict(),
                         messages={})  # Start with empty messages
    
    print("GUI initialized successfully without JSON loading")
    print("This version skips JSON file loading for testing")
    
    root.mainloop()

    settings.set_work_folder_to_file(work_folder)
