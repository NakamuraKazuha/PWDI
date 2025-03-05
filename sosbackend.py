import asyncio
import websockets
import json
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
        self.countdown_seconds = 5
        self.countdown_label = None  # UI Label for countdown

    def start_countdown(self):
        """Starts the SOS countdown using a separate thread to avoid blocking UI."""
        if not self.sos_active and not self.countdown_active:
            self.countdown_active = True
            self.countdown_seconds = 5
            threading.Thread(target=self.run_countdown, daemon=True).start()

    def cancel_countdown(self):
        """Cancels the countdown before SOS is sent."""
        if not self.sos_active:  # Prevents unnecessary messages
            self.countdown_active = False
            if self.countdown_label:
                self.countdown_label.value = "SOS Canceled"
                self.update_ui_callback()

    def run_countdown(self):
        """Runs the countdown in a separate thread and triggers SOS when reaching 1."""
        while self.countdown_seconds > 1 and self.countdown_active:
            if self.countdown_label:
                self.countdown_label.value = f"{self.countdown_seconds}"
                self.update_ui_callback()
            time.sleep(1)
            self.countdown_seconds -= 1

        if self.countdown_seconds == 1 and self.countdown_active:
            self.sos_active = True
            if self.countdown_label:
                self.countdown_label.value = "Sending SOS!"
                self.update_ui_callback()
            asyncio.run(self.send_sos_callback())

            # Start a background task to show "Help is on the way!" after 5 seconds
            threading.Thread(target=self.show_help_message, daemon=True).start()

    def show_help_message(self):
        """Displays 'Help is on the way!' 5 seconds after sending SOS."""
        time.sleep(5)
        if self.countdown_label:
            self.countdown_label.value = "Help is on the way!"
            self.update_ui_callback()

    async def cancel_sos_action(self):
        """Cancels an active SOS request."""
        if self.sos_active:
            return  # Prevents canceling after SOS has been sent

        self.sos_active = False
        self.countdown_active = False
        if self.countdown_label:
            self.countdown_label.value = "SOS Canceled"
            self.update_ui_callback()  # Ensure UI updates

        await self.cancel_sos_callback()

def get_gps_location():
    return "10.2764° N, 123.8497° E"

async def cancel_sos():
    print("SOS Canceled.")
