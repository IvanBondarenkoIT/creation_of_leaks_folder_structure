import json
from datetime import datetime


class Message:
    def __init__(self, message_data):
        self.id = message_data["id"]
        self.type = message_data["type"]
        self.date = datetime.utcfromtimestamp(
            int(message_data["date_unixtime"])
        ).strftime("%Y-%m-%d")
        # self.date = message_data["date_unixtime"]
        self.from_user = message_data["from"]
        self.file = message_data.get("file", None)
        self.text = message_data.get("text", None)

    def __str__(self):
        return f"Message ID: {self.id}\nType: {self.type}\nDate: {self.date}\nFrom: {self.from_user}\nFile: {self.file}\nText: {self.text}\n"

    def get_filename(self):
        return self.file


class Messages:
    def __init__(self, file_path: str):
        # Read the file
        # self.file_path = "Z:\_DM\_Downloads\TEST\esult.json"
        with open(file_path, "r", encoding="utf8") as file:
            data = json.load(file)


        # Extract messages
        messages_data = data["messages"]

        # Create Message objects
        self.messages = [Message(message_data) for message_data in messages_data]

        # Display messages
        # for message in self.messages:
        #     print(message)

    def get_messages(self):
        return {message.get_filename().replace("files/", ""): message for message in self.messages if message.file}