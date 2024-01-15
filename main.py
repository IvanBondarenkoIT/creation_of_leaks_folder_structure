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

    messages = Messages(file_path="Z:\_DM\_Downloads\TEST\esult.json")

    app = FileManagerApp(root,
                         work_folder=work_folder,
                         settings=settings,
                         work_links=dict_editor.get_dict(),
                         messages=messages.get_messages())
    root.mainloop()

    settings.set_work_folder_to_file(work_folder)
