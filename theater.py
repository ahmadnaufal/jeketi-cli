from datetime import datetime
from schedule import *

class Theater(Schedule):
    """docstring for Theater"""
    def __init__(self, title, date, show_time, ticket_time, purchase_periods=[]):
        self.title = title
        self.date = date
        self.show_time = show_time
        self.ticket_time = ticket_time
        self.purchase_periods = purchase_periods

    def __str__(self):
        strep = self.title + '\n' \
                    + self.date.strftime('%A, %d %B %Y') + '\n' \
                    + self.show_time.strftime('Show: %H:%M') + '\n' \
                    + self.ticket_time.strftime('Penukaran tiket: %H:%M') + '\n'

        for period in self.purchase_periods:
            strep += str(period) + '\n'

        return strep

class PurchasePeriod(object):
    """docstring for PurchasePeriod"""
    def __init__(self, id, title, start_time, end_time):
        self.id = id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    def create_from_period_string(cls, title, raw):
        strtimes = raw.split(" - ")
        start_time = datetime.strptime(" ".join(strtimes[0].split(" ")[1:3]), "%d.%m.%Y %H:%M")
        end_time = datetime.strptime(" ".join(strtimes[1].split(" ")[1:3]), "%d.%m.%Y %H:%M")

        return cls(0, title, start_time, end_time)

    def __str__(self):
        return self.title + ": " + self.start_time.strftime('%A, %d %B %Y %H:%M') + " - " + self.end_time.strftime('%A, %d %B %Y %H:%M')

