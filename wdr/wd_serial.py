"""
Allows for serial communication with the water drop controller arduino,

Requires serial_controller
"""
from .serial_controller import SerialController

__author__ = "enchant97"

class WaterDropSerial(SerialController):
    def test_release_drop(self):
        if self.isopen:
            self.send_and_recv("TESTDROP")

    def test_release_flash(self):
        if self.isopen:
            self.send_and_recv("TESTFLASH")

    def start_task(self):
        if self.isopen:
            self.send_and_recv("START")

    def save(self):
        if self.isopen:
            self.send_and_recv("SAVECURRENT")

    def upload_settings(self, settings_dict):
        """
        args:
            settings_dict : the settings that will be sent as a dictionary
                possible keys:
                    - dropdelay
                    - dropcount
                    - dropduration
                    - flashdelay
        """
        if self.isopen:
            self.send_and_recv(f"dropdelay={settings_dict.get('dropdelay', 0)}")
            self.send_and_recv(f"dropcount={settings_dict.get('dropcount', 1)}")
            self.send_and_recv(f"dropduration={settings_dict.get('dropduration', 200)}")
            self.send_and_recv(f"flashdelay={settings_dict.get('flashdelay', 0)}")
