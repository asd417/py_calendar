import datetime
from PyQt6.QtWidgets import QApplication, \
    QLabel, QWidget, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout, \
    QSlider, QPushButton, QComboBox
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

PRINTLOG = False

def dev_log(words):
    if PRINTLOG:
        print(words)

class CalEvent:
    def __init__(self,event_dict : dict):

        start = event_dict['start'].get('dateTime', event_dict['start'].get('date'))
        end = event_dict['end'].get('dateTime', event_dict['start'].get('date'))

        try:
            self.start : datetime = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            self.start : datetime = datetime.datetime.strptime(start, "%Y-%m-%d")

        try:
            self.end : datetime = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            self.end : datetime = datetime.datetime.strptime(end, "%Y-%m-%d")

        self.summary=event_dict['summary']

    def __repr__(self):
        return f"Event : {self.summary}, {self.start}, {self.end}"
    
    def get_month_date(self):
        month_date : str = self.start.strftime("%m %d")
        month, date = month_date.split()
        return month, date

    def getQWidget(self) -> QWidget:
        w = QWidget()
        l = QVBoxLayout()
        l.addWidget(QLabel(self.start.strftime("%Y-%m-%dT%H:%M:%S%z")))
        l.addWidget(QLabel(self.summary))
        w.setLayout(l)
        return w

