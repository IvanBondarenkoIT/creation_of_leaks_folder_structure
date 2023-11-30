SETTINGS_FILE_NAME = "settings.cfg"
DEFAULT_SOURCES_FILE_NAME = "sources.csv"


class Settings:
    def __init__(self, ):
        self.work_folder_path = SETTINGS_FILE_NAME
        self.sources_file_name = DEFAULT_SOURCES_FILE_NAME

    def get_work_folder_from_file(self):
        with open(self.work_folder_path, "r") as file:
            return file.read()

    def set_work_folder_to_file(self, work_folder: str):
        with open(self.work_folder_path, "w") as file:
            return file.write(work_folder)

    def get_default_sources_file_name(self):
        return self.sources_file_name
