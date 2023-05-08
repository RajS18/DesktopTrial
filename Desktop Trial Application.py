import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Realtime Plot")

        # Create and set the chart view
        self.chart_view = QChartView(self)
        self.setCentralWidget(self.chart_view)

        # Create the chart
        self.chart = QChart()
        self.chart.setTitle("Realtime Plot")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart_view.setChart(self.chart)

        # Add and set the X-axis
        self.axis_x = QValueAxis()
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setTitleText("Time (s)")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)

        # Add and set the Y-axis
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Value")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Create the line series for the real-time plot
        self.series = QLineSeries()
        self.chart.addSeries(self.series)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)

        # Create the line series for the rolling average plot
        self.average_series = QLineSeries()
        self.chart.addSeries(self.average_series)
        self.average_series.attachAxis(self.axis_x)
        self.average_series.attachAxis(self.axis_y)

        # Initialize the rolling window and average
        self.window_size = 5
        self.window = []
        self.average = 0

        # Create the timer for the real-time plot
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update_plot)

        # Create the button to toggle the rolling average plot
        self.toggle_button = QPushButton("Show Rolling Average", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setGeometry(10, 10, 120, 30)
        self.toggle_button.clicked.connect(self.toggle_average_plot)

    def toggle_average_plot(self):
        if self.toggle_button.isChecked():
            self.average_series.show()
        else:
            self.average_series.hide()

    def update_plot(self):
        # Generate a random data point
        x = self.series.count()
        y = random.uniform(0, 1)
        self.series.append(x, y)
        self.window.append(y)
        if len(self.window) > self.window_size:
            self.window.pop(0)
        self.average = sum(self.window) / len(self.window)
        self.average_series.append(x, self.average)

        # Center the chart to the recent point
        self.chart.scroll(self.axis_x.max(), 0)
        self.chart_view.repaint()

        # Print the point to console
        print(f"({x}, {y}, {self.average:.2f})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)  # Set the initial window size
    window.show()
    window.timer.start()
    sys.exit(app.exec_())
