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

    # Initialize with empty messages first to show GUI immediately
    app = FileManagerApp(root,
                         work_folder=work_folder,
                         settings=settings,
                         work_links=dict_editor.get_dict(),
                         messages={})  # Start with empty messages
    
    # Load messages asynchronously after GUI is shown
    def load_messages_async():
        app.show_loading()  # Show loading indicator
        try:
            # Check if JSON file exists
            json_path = "D:\_DM\_Downloads\TEST\esult.json"
            if os.path.exists(json_path):
                messages = Messages(file_path=json_path)
                app.update_messages(messages.get_messages())
                print(f"Loaded {len(app.messages)} messages successfully")
            else:
                print(f"JSON file not found: {json_path}")
                app.update_messages({})
        except Exception as e:
            print(f"Error loading messages: {e}")
            app.update_messages({})
    
    # Schedule message loading after GUI is ready
    root.after(100, load_messages_async)
    
    root.mainloop()

    settings.set_work_folder_to_file(work_folder)
