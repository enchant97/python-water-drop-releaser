"""
tkinter gui that will allow a graphical
control over the connected serial device
"""
import tkinter as tk

from threaded_task_executor import Task_Queue

from wdr.config import get_config, write_config
from wdr.extra_math import calc_time_to_fall_in_ms
from wdr.serial_controller import SerialController, get_connected_ports
from wdr.wd_serial import WaterDropSerial

__version__ = "1.0.0"
__author__ = "enchant97"

class TkApp(tk.Tk):
    __serial = WaterDropSerial()
    __tasks = Task_Queue(True)
    def __init__(self):
        tk.Tk.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.wm_title("Water Drop Release " + __version__)
        self.wm_resizable(1, 0)
        self.wm_minsize(200, self.winfo_height())

        # the tkinter variables
        self.__drop_count = tk.IntVar(self, 1)
        self.__drop_delay = tk.IntVar(self, 0)
        self.__drop_dur = tk.IntVar(self, 200)
        self.__drop_distance = tk.IntVar(self, 1)
        self.__flash_offset = tk.IntVar(self, 0)
        self.set_defaults()

        self.port_selected = tk.StringVar(self, "NO SELECTED PORT")

        self.__port_select = tk.OptionMenu(self, self.port_selected, "NO SELECTED PORT", *get_connected_ports())
        self.__connect = tk.Button(self, text="Connect", command=self.connect)

        self.__l_drop_count = tk.Label(self, text="Drop Count:")
        self.__sb_drop_count = tk.Spinbox(self,from_=1, to=9999, textvariable=self.__drop_count)
        self.__l_drop_delay = tk.Label(self, text="Drop Delay (ms):")
        self.__sb_drop_delay = tk.Spinbox(self,from_=0, to=9999, textvariable=self.__drop_delay)
        self.__l_drop_dur = tk.Label(self, text="Drop Duration (ms):")
        self.__sb_drop_dur = tk.Spinbox(self,from_=1, to=9999, textvariable=self.__drop_dur)
        self.__l_drop_distance = tk.Label(self, text="Drop Distance (cm):")
        self.__sb_drop_distance = tk.Spinbox(self,from_=1, to=9999, textvariable=self.__drop_distance)
        self.__l_flash_offset = tk.Label(self, text="Flash Offset (ms):")
        self.__sb_flash_offset = tk.Spinbox(self,from_=0, to=9999, textvariable=self.__flash_offset)

        self.__bnt_testdrop = tk.Button(self, text="Test Water Drop", command=self.send_testdrop)
        self.__bnt_send = tk.Button(self, text="Send", command=self.load_setttings)
        self.__bnt_save = tk.Button(self, text="Save To Device", command=self.save_defaults)
        self.__bnt_start = tk.Button(self, text="Start", command=self.start_task)
        self.__l_info = tk.Label(self, text="Not Connected")

        self.__port_select.pack(fill="x")
        self.__connect.pack(fill="x")
        self.__l_drop_count.pack(fill="x")
        self.__sb_drop_count.pack(fill="x")
        self.__l_drop_delay.pack(fill="x")
        self.__sb_drop_delay.pack(fill="x")
        self.__l_drop_dur.pack(fill="x")
        self.__sb_drop_dur.pack(fill="x")
        self.__l_drop_distance.pack(fill="x")
        self.__sb_drop_distance.pack(fill="x")
        self.__l_flash_offset.pack(fill="x")
        self.__sb_flash_offset.pack(fill="x")

        self.__bnt_testdrop.pack(fill="x")
        self.__bnt_send.pack(fill="x")
        self.__bnt_save.pack(fill="x")
        self.__bnt_start.pack(fill="x")
        self.__l_info.pack(fill="x")

    def set_defaults(self):
        defaults = get_config()
        self.__drop_count.set(defaults["dropcount"])
        self.__drop_delay.set(defaults["dropdelay"])
        self.__drop_dur.set(defaults["dropduration"])
        self.__drop_distance.set(defaults["dropdistance"])
        self.__flash_offset.set(defaults["flashoffset"])

    @__tasks.add_from_func()
    def save_defaults(self):
        self.__l_info.config(text="Sending...")
        defaults = {
            "dropcount":self.__drop_count.get(),
            "dropdelay":self.__drop_delay.get(),
            "dropduration":self.__drop_dur.get(),
            "dropdistance":self.__drop_distance.get(),
            "flashoffset":self.__flash_offset.get()
        }
        self.after(0, write_config, defaults)
        self.load_setttings()
        self.__serial.save()
        self.__l_info.config(text="Sent")

    def show_message(self, message):
        self.__l_info.config(text=message)

    @__tasks.add_from_func()
    def connect(self):
        if self.port_selected.get() != "NO SELECTED PORT":
            self.__serial.new_callback(self.show_message)
            self.__serial.open_and_recv(self.port_selected.get())

    @__tasks.add_from_func()
    def start_task(self):
        self.__serial.start_task()


    @property
    def flash_delay(self):
        """
        Calculates the flash delay from the
        drop distance and adding the offset to it,
        returns -1 if invalid
        """
        delay = calc_time_to_fall_in_ms(self.__drop_distance.get()) + int(self.__flash_offset.get())
        if delay < 0:
            self.show_message("flash delay cannot be smaller than 0")
            return -1
        elif delay > 9999:
            self.show_message("flash delay cannot be greater than 9999")
            return -1
        return delay

    @__tasks.add_from_func()
    def load_setttings(self):
        if self.__serial.isopen:
            self.__l_info.config(text="Sending...")
            flash_delay = self.flash_delay
            if flash_delay > -1:
                settings_dict = {
                    "dropcount": self.__drop_count.get(),
                    "dropdelay": self.__drop_delay.get(),
                    "dropduration": self.__drop_dur.get(),
                    "flashdelay": round(flash_delay)
                }
                self.__serial.upload_settings(settings_dict)
                self.__l_info.config(text="Sent")
        else:
            self.__l_info.config(text="Not Connected")

    @__tasks.add_from_func()
    def send_testdrop(self):
        self.__serial.test_release_drop()

    def on_close(self):
        if self.__serial:
            self.__serial.close_conn()
        self.destroy()

if __name__ == "__main__":
    app = TkApp()
    app.mainloop()
