import datetime

class CalEvent:
    def __init__(self,event_dict : dict):

        start = event_dict['start'].get('dateTime', event_dict['start'].get('date'))
        end = event_dict['end'].get('dateTime', event_dict['start'].get('date'))

        try:
            self.start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            self.start = datetime.datetime.strptime(start, "%Y-%m-%d")

        try:
            self.end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            self.end = datetime.datetime.strptime(end, "%Y-%m-%d")

        self.summary=event_dict['summary']

    def __repr__(self):
        return f"Event : {self.summary}, {self.start}, {self.end}"
