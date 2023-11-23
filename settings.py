SETTINGS_FILE_NAME = "settings.cfg"


class Settings:
    def __init__(self, ):
        self.work_folder_path = SETTINGS_FILE_NAME

    def get_work_folder_from_file(self):
        with open(self.work_folder_path, "r") as file:
            return file.read()


