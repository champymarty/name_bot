from .Name import Name
from .Server import Server
import json
import pickle


class History:

    data_file = "data.bin"
    def __init__(self):  
        self._load_history()

    def handle_new_name(self, server_id, user_id, new_name):
        if server_id not in self.servers_index:
            self._create_server(server_id)
        self.servers[self.servers_index[server_id]].add_new_username(user_id, new_name)
        self._save_history()

    def _load_history(self):
        try:
            with open(History.data_file, 'rb') as config_dictionary_file:
                self.servers_index, self.servers = pickle.load(config_dictionary_file)
        except:
            self.servers_index = {}
            self.servers = []

    def _save_history(self):
        with open(History.data_file, 'wb') as config_dictionary_file:
            pickle.dump((self.servers_index, self.servers), config_dictionary_file)

    def toJSON(self):
        servers = {}
        for server in self.servers:
            users = {}
            for user in server.users:
                names = {}
                for name in user.names:
                    names[name.name] = name.date
                users[user.id] = names
            servers[server.id] = users
        return json.dumps(servers, indent=4)

    def _create_server(self, server_id):
        self.servers.append(Server(server_id))
        self.servers_index[server_id] = len(self.servers) - 1

