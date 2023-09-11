from cache import load_config
from models.SwimmingEvent import SwimmingEventWithDay
import requests
from bs4 import BeautifulSoup

class Fetcher:

    def __init__(self, parser):
        self.parser = parser
        self.config = load_config()
        self.website_data = None

    def num_rows(self):
        i = 1
        while self.parser.is_valid_row(i):
            i = i+1

        len_rows = i - 1
        return len_rows

    def fetch_data(self):
        url = self.config['url']
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content,
                                 'html.parser')

            return soup

        return None

    def fetch(self):
        self.website_data = self.fetch_data()
        self.parser.initialise(self.website_data)
        num_rows = self.num_rows()

        all_events = []

        for i in range(num_rows):
            day = self.parser.parse_day_row(i+1)
            swimming_events = self.parser.parse_time_row(i+1)

            for swimming_event in swimming_events:
                all_events.append(SwimmingEventWithDay(swimming_event, day))

        return all_events