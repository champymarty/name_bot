from data_model.Name import Name


class User:
    def __init__(self, user_id: str):  
        self.id: str = user_id
        self.names = []

    def __eq__(self, other):
        return self.id == other.id and self.names == other.names

    def add_name(self, new_name: str):
        self.names.append(Name(new_name))