import time
import threading

class SOSHandler:
    def __init__(self, send_sos_callback, get_gps_location, cancel_sos_callback, update_ui_callback):
        self.send_sos_callback = send_sos_callback
        self.get_gps_location = get_gps_location
        self.cancel_sos_callback = cancel_sos_callback
        self.update_ui_callback = update_ui_callback

        self.sos_active = False
        self.countdown_active = False
        self.countdown_seconds = 10
        self.countdown_label = None  # To be set by UI

    def start_countdown(self):
        if not self.sos_active:
            self.countdown_active = True
            self.countdown_seconds = 10
            threading.Thread(target=self.run_countdown, daemon=True).start()

    def cancel_countdown(self):
        if not self.sos_active:
            self.countdown_active = False
            if self.countdown_label:
                self.countdown_label.value = ""
                self.update_ui_callback()

    def run_countdown(self):
        while self.countdown_seconds > 0 and self.countdown_active:
            if self.countdown_label:
                self.countdown_label.value = f" {self.countdown_seconds}"
                self.update_ui_callback()
            time.sleep(1)
            self.countdown_seconds -= 1

        if self.countdown_seconds == 0 and self.countdown_active:
            self.send_sos_callback()
            self.sos_active = True
            if self.countdown_label:
                self.countdown_label.value = "SOS Sent!"
                self.update_ui_callback()

    def cancel_sos_action(self):
        self.sos_active = False
        self.countdown_active = False
        if self.countdown_label:
            self.countdown_label.value = "SOS Canceled"
        self.cancel_sos_callback()
        self.update_ui_callback()

# Simulated SOS functions
def send_sos():
    print("SOS Sent! Notifying emergency contacts.")

def get_gps_location():
    return "14.5995° N, 120.9842° E"

def cancel_sos():
    print("SOS Canceled.")
