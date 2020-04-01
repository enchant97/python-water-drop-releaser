"""
Allows for simple control over serial using pyserial
"""
import serial
from serial.tools import list_ports

__author__ = "enchant97"

def get_connected_ports():
    """
    returns a tuple of all
    connected serial ports
    """
    ports = []
    for port in list_ports.comports():
        ports.append(port.device)
    return tuple(ports)

class SerialController:
    """
    Allows for simple messages
    to be sent through serial
    """
    __isopen = False
    def __init__(self, port=None, budrate=9600, timeout=None, callback=None):
        """
        To use callback the function must accept 1 argument
        which will be returned message.

        Args:
            port: port for serial connection if None will have to use open_conn()
            budrate: the budrate
            timeout: the amount of time to wait for reply
            callback: function to call when there is a reply
        """
        self.new_callback(callback)
        self.open_conn(port, budrate, timeout)

    @property
    def isopen(self):
        return self.__isopen

    def __run_callback(self, message):
        if self.__callback:
            self.__callback(message)

    def recv_to_callback(self):
        self.__run_callback(self.serial.readline().decode())

    def send(self, message):
        """
        Will convert message into bytes and send to serial,
        adding \\n at end of sent message.
        """
        message += "\n"
        self.serial.write(message.encode())

    def send_and_recv(self, message):
        """
        sends message using self.send(),
        then run callback with recieved message as string,
        """
        self.send(message)
        self.recv_to_callback()

    def new_callback(self, callback):
        self.__callback = callback

    def open_and_recv(self, port, budrate=9600, timeout=None):
        """
        Opens connection and waits for message
        """
        self.open_conn(port, budrate, timeout)
        self.recv_to_callback()

    def open_conn(self, port, budrate=9600, timeout=None):
        """
        Opens a new serial connection,
        closes if one already exists.
        """
        if self.isopen:
            self.close_conn()
        self.serial = serial.Serial(port, budrate, timeout=timeout)
        if port:
            self.__isopen = True

    def close_conn(self):
        self.serial.close()
        self.__isopen = False
