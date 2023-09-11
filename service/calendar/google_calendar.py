import datetime

from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar as _GC
from gcsa.calendar import Calendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA
from models.SwimmingEvent import SwimmingEventWithDay

from beautiful_date import Sept, Apr
from cache import load_secret, load_config, update_secret_with_calendar_id
class GoogleCalendar:
    def __init__(self):
        self.secret = load_secret()
        self.calendar_id = None
        self.calendar = _GC(self.secret['calendar_email'], credentials_path="credentials.json")
        self.config = load_config()

        self.create_calendar_if_not_exists()

    def exists_calendar(self):
        calendar_id = self.secret['calendar_id']
        if calendar_id == "":
            return False
        calendar = self.calendar.get_calendar(calendar_id)
        if calendar is None:
            return False
        return True

    def create_calendar(self):
        calendar = Calendar(
            'GT Swimming pool Calendar',
            description='Calendar for tracking swimming pool times'
        )
        calendar = self.calendar.add_calendar(calendar)
        return calendar

    def update_config(self, calendar_id):
        update_secret_with_calendar_id(calendar_id)

    def create_calendar_if_not_exists(self):
        if not self.exists_calendar():
            calendar = self.create_calendar()
            self.update_config(calendar.calendar_id)

    def add_event(self, event):
        self.calendar.add_event(event, calendar_id=self.secret['calendar_id'])
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


