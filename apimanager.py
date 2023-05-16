from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from event import CalEvent
    

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
PRINTLOG = False

def dev_log(words):
    if PRINTLOG:
        print(words)

class APIManager:
    def __init__(self):
        self.cred = self.get_cred()
        self.service = self.get_service()
        dev_log(f"service type: {type(self.service)}")
        self.events = []

    def get_cred(self):
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    
    def get_service(self):
        return build('calendar', 'v3', credentials=self.cred)
        
    def get_events(self, count, timemin:str= datetime.datetime.utcnow().isoformat() + 'Z', timemax:str=""):
        try:
            dev_log('Getting the upcoming events')
            #datetime.datetime(year,month,day,hour,minute).isoformat() + 'Z' # 'Z' indicates UTC time
            if timemax != "":
                events_result = self.service.events().list(calendarId='primary', timeMin=timemin,timeMax=timemax,
                                                maxResults=count, singleEvents=True,
                                                orderBy='startTime').execute()
            else:
                events_result = self.service.events().list(calendarId='primary', timeMin=timemin,
                                                    maxResults=count, singleEvents=True,
                                                    orderBy='startTime').execute()
            return events_result.get('items', [])
        except HttpError as error:
            dev_log('An error occurred: %s' % error)

    def get_event_list(self):
        return self.events

    def find_event_in_year(self,year):
        self.events = []
        t1 = datetime.datetime(year,1,1,1,30).isoformat() + 'Z'
        t2 = datetime.datetime(year+1,1,1,1,30).isoformat() + 'Z'
        dev_log(f"Requesting events between {t1} and {t2}")
        events = self.get_events(10,t1)
        for event in events:
            #print(event['start']['dateTime'])
            c_e = CalEvent(event)
            dev_log(c_e)
            self.events.append(c_e)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # python api https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html
    
    # Call the Calendar API
    #type(service) = googleapiclient.discovery.Resource
    apimanager = APIManager()
    t1 = datetime.datetime(2020,1,1,1,30).isoformat() + 'Z'
    t2 = datetime.datetime(2023,1,1,1,30).isoformat() + 'Z'
    events = apimanager.get_events(10,t1)
    for event in events:
        #print(event['start']['dateTime'])
        c_e = CalEvent(event)
        dev_log(c_e)
        
if __name__ == '__main__':
    main()