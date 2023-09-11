import datetime

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar as _GC
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from models.SwimmingEvent import SwimmingEventWithDay

from beautiful_date import Sept, Apr
from cache import load_secret, load_config
class GoogleCalendar:
    def __init__(self):
        self.secret = load_secret()
        self.calendar = _GC(self.secret['calendar_email'], credentials_path="credentials.json")
        self.config = load_config()

    def add_event(self, event):
        self.calendar.add_event(event)
        print("Added event " + str(event))

    def add_event_with_details(self, swimming_event_with_day: SwimmingEventWithDay):
        if self.config['add_event']:
            event = Event(
                'GT: Swimming',
                start=swimming_event_with_day.start_time(),
                end=swimming_event_with_day.end_time(),
                description="McAuley Swimming pool is open with {} lanes".format(swimming_event_with_day.number_of_lanes()),
                minutes_before_email_reminder=15,
            )
            self.add_event(event)

    def clear_calendar(self):
        for event in self.calendar.get_events(datetime.datetime(datetime.datetime.now().year, 1, 1),
                                              datetime.datetime(datetime.datetime.now().year+1, 1, 1),
                                              order_by='updated'):
            print("Deleting event "+str(event))
            self.calendar.delete_event(event)


