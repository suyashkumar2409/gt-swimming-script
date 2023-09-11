import unittest
from service.data.Parser import Parser
from service.data.Fetcher import Fetcher
class TestParser(unittest.TestCase):

    def setUp(self) -> None:
        self.parser = Parser()
        fetcher = Fetcher(self.parser)
        website_data = fetcher.fetch_data()
        self.parser.initialise(website_data)

    def test_faulty_row(self):
        events = self.parser.parse_time_row(5)
        for event in events:
            self.assertIsNotNone(event, None)

if __name__ == '__main__':
    unittest.main()