import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QVBoxLayout,QHBoxLayout, QSlider, QPushButton, QStackedLayout
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import calendar

# https://realpython.com/python-pyqt-gui-calculator/

class Window(QWidget):

    def __init__(self):
        super().__init__()

        # set the title
        self.transparency = 0.5
        
        self.setWindowTitle("Calendar App")
  
        # setting  the geometry of window
        self.monthIndex = 4
        self.year = 2023
        self.today = 12
        self.thisMonthIndex = 4
        self.update_all()
    
    def show(self):
        super().show()
        print("Show called")

    def setTransparency(self, val):
        self.transparency = (float(val) / 10)
        self.setWindowOpacity(self.transparency)
    
    def setMonth(self, val):
        self.monthIndex = max(0, min(val, 11))
        self.stacked_month_layout.setCurrentIndex(self.monthIndex)
        self.year_label.setText(f"<h1>{self.year},{self.monthIndex + 1}</h1>")
        print(f"Month: {self.monthIndex + 1}")

    def topbar_widget(self):
        widget = QWidget()
        l = QHBoxLayout()
        button_prev = QPushButton("<")
        button_next = QPushButton(">")
        def button_prev_pressed():
            self.setMonth(self.monthIndex - 1)
        def button_next_pressed():
            self.setMonth(self.monthIndex + 1)

        button_prev.clicked.connect(button_prev_pressed)
        button_next.clicked.connect(button_next_pressed)
        
        self.year_label = QLabel(f"<h1>{self.year},{self.monthIndex+1}</h1>")
        self.year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        l.addWidget(button_prev)
        l.addWidget(self.year_label)
        l.addWidget(button_next)

        widget.setLayout(l)
        return widget


    def transparency_slider(self):
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)  # Set the orientation to horizontal

        # Set the minimum and maximum values
        slider.setMinimum(1)
        slider.setMaximum(10)

        # Set the tick interval (optional)
        slider.setTickInterval(1)

        # Set the slider value
        slider.setValue(5)
        def slider_value_changed(value):
            print(f"Slider value: {value}")
            self.setTransparency(value)

        slider.valueChanged.connect(slider_value_changed)
        return slider

    def update_all(self):
        self.setWindowOpacity(self.transparency)
        
        self.stacked_month_layout= QStackedLayout(self)
        for i in range(12):
            self.stacked_month_layout.addWidget(self.create_single_month(i))
        #self.stacked_month_layout.addWidget(self.create_single_month(0))
        stacked_year_widget = QWidget()
        stacked_year_widget.setLayout(self.stacked_month_layout)
        self.stacked_month_layout.setCurrentIndex(self.monthIndex)
        # show all the widgets
        v_area = QVBoxLayout()
        v_area.addWidget(self.topbar_widget())
        v_area.addWidget(stacked_year_widget)
        v_area.addWidget(self.transparency_slider())
        self.setLayout(v_area)
        self.show()
    
    def create_single_month(self, month) -> QWidget:
        """
            0 <= month <= 11
        """
        date_default_background = QPalette()
        date_default_background.setColor(QPalette.ColorRole.Window, QColor(250,250,250))

        date_today_background : QPalette = QPalette()
        date_today_background.setColor(QPalette.ColorRole.Window, QColor(200,200,200))
        month_tuple : tuple = calendar.monthrange(self.year, month+1)
        print(f"{month+1} has {month_tuple}")
        offset = (month_tuple[0] + 1) % 7
        cal_widget : QWidget = QWidget()
        grid : QGridLayout = QGridLayout()
        
        for i in range(month_tuple[1]):
            date_string = ""
            date_num = i + 1 
            dateWidget = QWidget()
            dateWidget.setAutoFillBackground(True)
            if date_num == self.today and month == self.thisMonthIndex:
                dateWidget.setPalette(date_today_background)
            else:
                dateWidget.setPalette(date_default_background)

            datelayout = QVBoxLayout()
            match (i + offset) % 7:
                case 0:
                    date_string = "Sun"
                case 1:
                    date_string = "Mon"
                case 2:
                    date_string = "Tue"
                case 3:
                    date_string = "Wed"
                case 4:
                    date_string = "Thu"
                case 5:
                    date_string = "Fri"
                case 6:
                    date_string = "Sat"
            dateLabel = QLabel(f"<h3>{date_string}, {date_num}</h3>")
            datelayout.addWidget(dateLabel)

            taskLabel = QLabel(f"<p>Task</p>")
            datelayout.addWidget(taskLabel)
            
            dateWidget.setLayout(datelayout)
            dateWidget.setMinimumWidth(100)
            dateWidget.setMinimumHeight(100)
            grid.addWidget(dateWidget,(i + offset)//7, (i + offset)%7)
        cal_widget.setLayout(grid)
        return cal_widget


def main():
    app = QApplication([])
    window = Window()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()