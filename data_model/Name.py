import datetime

class Name:
    def __init__(self, name, take_time=True):  
        self.name = name
        if take_time:
            self.date = datetime.datetime.now()
            self.date = dict(
                year=self.date.year,
                month=self.date.month,
                day=self.date.day,
                hour=self.date.hour,
                minute=self.date.minute,
                second=self.date.second
            )
        else:
            self.date = None