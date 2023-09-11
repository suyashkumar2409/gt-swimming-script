from service.calendar.google_calendar import GoogleCalendar
class Updater():

    def __init__(self):
        self.calendar = GoogleCalendar()

    def update(self, all_events):
        self.calendar.clear_calendar()
        for event in all_events:
            self.calendar.add_event_with_details(event)