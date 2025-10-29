import json
import os

class AccountManager:
    def __init__(self, file_path="users.json"):
        self.file_path = file_path
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_users(self):
        with open(self.file_path, "w") as f:
            json.dump(self.users, f, indent=4)

    def register(self, username, password):
        if username in self.users:
            return False, "⚠️ Username already exists!"
        self.users[username] = password
        self.save_users()
        return True, "✅ Registration successful!"

    def login(self, username, password):
        if username not in self.users or self.users[username] != password:
            return False, "❌ Invalid username or password."
        return True, "✅ Login successful!"
