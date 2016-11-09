from datetime import datetime
from schedule import *

class Theater(Schedule):
    """docstring for Schedule"""
    def __init__(self, raw_tag):
        columns = raw_tag.findAll('td')
        self.title = str(columns[1].text)
        self.date = datetime.strptime(columns[0].contents[2], "%d.%m.%Y").date()
        self.show_time = datetime.strptime(columns[0].contents[-1].contents[0][-5:], "%H:%M")
        self.ticket_time = datetime.strptime(columns[0].contents[-1].contents[2][-5:], "%H:%M")

    def print_schedule(self):
        return self.title + '\n' \
                + self.date.strftime('%A, %d %B %Y') + '\n' \
                + self.show_time.strftime('Show: %H:%M') + '\n' \
                + self.ticket_time.strftime('Penukaran tiket: %H:%M') + '\n'
