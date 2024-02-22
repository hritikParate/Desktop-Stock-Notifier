import datetime
import time
import yfinance as yf
from plyer import notification
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from threading import Thread

# Global variable to control the notification loop
notification_active = True

def show_notification(stock_symbol, interval_hours):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.info

        notification_title = f"{data['shortName']} - {datetime.date.today()}"
        notification_message = (
            f"Current Price = {data['currentPrice']}\n"
            f"DayLow = {data['dayLow']}\n"
            f"DayHigh = {data['dayHigh']}"
        )

        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon="icons/notification_icon.ico",
            timeout=5
        )

        # Sleep for the specified interval in seconds
        time.sleep(interval_hours * 60 * 60)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        # Stop the notification loop in case of an error
        stop_notifications()

def start_notifications(stock_symbol, interval_hours):
    while notification_active:
        show_notification(stock_symbol, interval_hours)

def get_user_input():
    stock_symbol = entry_stock.get()
    interval_hours = entry_interval.get()

    try:
        # Check if the interval is a valid positive number
        interval_hours = float(interval_hours)
        if interval_hours <= 0:
            raise ValueError("Interval should be a positive number")

        # Minimize the window
        root.iconify()

        # Start a thread for continuous notifications
        notification_thread = Thread(target=start_notifications, args=(stock_symbol, interval_hours))
        notification_thread.start()

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number for the interval.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def stop_notifications():
    global notification_active
    notification_active = False
    root.withdraw()  # Hide the window instead of closing it

# Create themed tkinter window with the 'plastik' theme
root = ThemedTk(theme="plastik")

root.title("Stock Notification App")

# Create and place themed widgets
label_stock = ttk.Label(root, text="Stock Symbol:")
label_stock.grid(row=0, column=0, padx=10, pady=10)

entry_stock = ttk.Entry(root)
entry_stock.grid(row=0, column=1, padx=10, pady=10)

label_interval = ttk.Label(root, text="Notification Interval (hours):")
label_interval.grid(row=1, column=0, padx=10, pady=10)

entry_interval = ttk.Entry(root)
entry_interval.grid(row=1, column=1, padx=10, pady=10)

button_start = ttk.Button(root, text="Start Notifications", command=get_user_input)
button_start.grid(row=2, column=0, pady=20)

button_stop = ttk.Button(root, text="Stop Notifications", command=stop_notifications)
button_stop.grid(row=2, column=1, pady=20)

# Start the themed tkinter main loop
root.mainloop()
