from datetime import datetime, time


class SwimmingEvent:
    def __init__(self, start_time: time, end_time: time, number_of_lanes: int):
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_lanes = number_of_lanes


class SwimmingEventWithDay:
    def __init__(self, swimming_event: SwimmingEvent, day: datetime):
        self.day = day
        self.swimming_event = swimming_event

    def start_time(self) -> datetime:
        return datetime.combine(self.day, self.swimming_event.start_time)

    def end_time(self) -> datetime:
        return datetime.combine(self.day, self.swimming_event.end_time)

    def number_of_lanes(self):
        return self.swimming_event.number_of_lanes