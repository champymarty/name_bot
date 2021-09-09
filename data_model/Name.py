import datetime

class Name:
    def __init__(self, name):  
        self.name = name
        self.date = datetime.datetime.now()
        self.date = dict(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            hour=self.date.hour,
            minute=self.date.minute,
            second=self.date.second
            )