from cache import load_config
from models.SwimmingEvent import SwimmingEvent
from datetime import datetime, time
import unicodedata
class Parser:

    def __init__(self):
        self.config = load_config()
        self.website_data = None

    def initialise(self, website_data):
        self.website_data = website_data
    def parse_template(self, template, i):
        return template.format(i)

    def select(self, template, i):
        return self.website_data.select(self.parse_template(self.config[template], i))

    def parse_day_row(self, i):
        day_str = self.select('day_selector', i)[0].text
        day_and_date = day_str.split(" ")

        if len(day_and_date) != 2:
            return None

        date = day_and_date[1]
        current_year = datetime.now().year
        try:
            month, day = map(int, date.split('/'))
        except ValueError:
            return None

        target_date = datetime(current_year, month, day)
        return target_date

    def remove_td(self, str):
        str = str.replace("</td>", "")
        str = str.replace("<td>", "")
        return str

    def break_str(self, str):
        return str.split("\n\t\t\t")

    def parse_hours_and_minutes(self, number):
        hours_and_minutes = number.split(":")
        if len(hours_and_minutes) == 1:
            return int(hours_and_minutes[0]), 0
        else:
            return int(hours_and_minutes[0]), int(hours_and_minutes[1])
    def get_time(self, time_str: str) -> time:
        length = len(time_str)
        last_char = time_str[length - 1]
        number = time_str[:length - 1]

        hours, minutes = self.parse_hours_and_minutes(number)

        correct_hour = int(hours)
        if hours == 12:
            correct_hour = 0

        if last_char == 'p':
            correct_hour = correct_hour + 12

        try:
            return time(correct_hour, minutes)
        except:
            pass

    def parse_event(self, time_str):
        time_str = unicodedata.normalize("NFKD", time_str)
        parts = time_str.split(" ", 1)

        if len(parts) != 2:
            return None

        # Split the first part on the hyphen
        time_info = parts[0]
        lanes_info = parts[1]

        start_and_end_time = time_info.split('-')

        if len(start_and_end_time) != 2:
            return None

        start_time = self.get_time(start_and_end_time[0])
        end_time = self.get_time(start_and_end_time[1])

        # Extract the first number from the second part
        lanes_info = lanes_info.replace('(', "")
        lanes_info = lanes_info.replace(')', "")
        lanes_info = lanes_info.strip()
        number_of_lanes = int(lanes_info.split(' ')[0].split('+')[0])

        return SwimmingEvent(start_time, end_time, number_of_lanes)
    def parse_time_row(self, i):
        all_times_str = self.select('time_selector', i)[0].text
        all_times = self.break_str(all_times_str)

        all_swimming_events = [self.parse_event(time) for time in all_times]
        return [event for event in all_swimming_events if event is not None]



    def is_valid_row(self, i):
        return len(self.select('day_selector', i)) != 0