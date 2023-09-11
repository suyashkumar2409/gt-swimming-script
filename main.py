from service.data.Fetcher import Fetcher
from service.data.Parser import Parser
from service.calendar.updater import Updater
def main():
    all_events = Fetcher(Parser()).fetch()
    if all_events is None:
        print("Data fetch failed")
        return 1

    status = Updater().update(all_events)
    if status is not None:
        print("Status update failed because of "+status)
        return 1

    return 0



if __name__ == '__main__':
    main()