import sys
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QLineSeries, QChartView
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsSimpleTextItem

class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")  # تغییر عنوان پنجره اصلی
        self.setGeometry(100, 100, 500, 600)  

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.charts = []

        for title, color in [("CPU Usage (%)", Qt.red), ("Network (bytes)", Qt.yellow), ("Memory (%)", Qt.green), ("Disk (%)", Qt.blue)]:
            chart = QChart()
            chart.setTitle(title)
            chart.legend().hide()
            chart_view = QChartView(chart)
            layout.addWidget(chart_view)
            chart_view.setMinimumSize(300, 300)  
            self.charts.append((chart, chart_view, color))

        self.update_charts()

    def update_charts(self):
        cpu_series = QLineSeries()
        network_series = QLineSeries()
        memory_series = QLineSeries()
        disk_series = QLineSeries()

        for i in range(50):
            # Get CPU data
            cpu_percent = psutil.cpu_percent(interval=1)

            # Get network data
            network_stats = psutil.net_io_counters()
            network_sent = network_stats.bytes_sent
            network_received = network_stats.bytes_recv

            # Get memory data
            memory_stats = psutil.virtual_memory()
            memory_used = memory_stats.percent

            # Get disk data
            disk_stats = psutil.disk_usage('/')
            disk_used = disk_stats.percent

            cpu_series.append(i, cpu_percent)
            network_series.append(i, network_sent)
            memory_series.append(i, memory_used)
            disk_series.append(i, disk_used)

        for chart, chart_view, color in self.charts:
            if chart.title() == "CPU Usage (%)":
                series = cpu_series
                max_range = 100
                last_value = cpu_series.at(cpu_series.count() - 1).y()
            elif chart.title() == "Network (bytes)":
                series = network_series
                max_range = 1000
                last_value = network_series.at(network_series.count() - 1).y()
            elif chart.title() == "Memory (%)":
                series = memory_series
                max_range = 100
                last_value = memory_series.at(memory_series.count() - 1).y()
            elif chart.title() == "Disk (%)":
                series = disk_series
                max_range = 100
                last_value = disk_series.at(disk_series.count() - 1).y()

            series.setColor(QColor(color))
            chart.removeAllSeries()
            chart.addSeries(series)

            chart.createDefaultAxes()
            chart.axes(Qt.Horizontal)[0].setRange(0, 50)
            chart.axes(Qt.Vertical)[0].setRange(0, max_range)

            # Add label for last value
            last_value_label = QGraphicsSimpleTextItem(f"{chart.title()}: {last_value}%")
            last_value_label.setFont(QFont("Arial", 10))

            # Set label position
            chart_view.scene().addItem(last_value_label)
            last_value_label.setPos(chart_view.rect().topRight() - last_value_label.boundingRect().bottomRight() + QPoint(-10, 20))

            QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec_())
