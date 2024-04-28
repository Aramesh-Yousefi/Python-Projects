import tkinter as tk
from tkinter import ttk
import psutil

class SystemHealthChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("System Health Checker")

        self.cpu_label = ttk.Label(root, text="CPU Usage:")
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.cpu_usage = ttk.Label(root, text="")
        self.cpu_usage.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.memory_label = ttk.Label(root, text="Memory Usage:")
        self.memory_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.memory_usage = ttk.Label(root, text="")
        self.memory_usage.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.disk_label = ttk.Label(root, text="Disk Usage:")
        self.disk_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.disk_usage = ttk.Label(root, text="")
        self.disk_usage.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.network_label = ttk.Label(root, text="Network Usage:")
        self.network_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.network_usage = ttk.Label(root, text="")
        self.network_usage.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.update_values()

    def update_values(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        network_percent = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        self.cpu_usage.config(text=f"{cpu_percent:.2f}%")
        self.memory_usage.config(text=f"{memory_percent:.2f}%")
        self.disk_usage.config(text=f"{disk_percent:.2f}%")
        self.network_usage.config(text=f"{network_percent / (1024 * 1024):.2f} MB")

        self.root.after(1000, self.update_values)

def main():
    root = tk.Tk()
    app = SystemHealthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
