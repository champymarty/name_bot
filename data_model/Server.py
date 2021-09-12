from data_model.User import User
import json

class Server:

    def __init__(self, server_id):  
        self.id = server_id
        self.users = []
        self.users_index = {}

    def add_new_username(self, user_id, new_name, old_name):
        if user_id not in self.users_index:
            self._add_user(user_id, old_name)
        self.users[self.users_index[user_id]].add_name(new_name)
        
    def _add_user(self, user_id, old_name):
        self.users.append(User(user_id))
        self.users_index[user_id] = len(self.users) - 1
        self.users[-1].add_name(old_name, take_time=False)

    def get_history(self, user_id, old_name):
        if user_id not in self.users_index:
            self._add_user(user_id, old_name)
        return self.users[self.users_index[user_id]].names
