# Base driver for DGUS protocol used in DWIN UART TFT displays
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Petr Kracik"


class DGUS:
    HEADER=b"\x0a\xa5"

    def __init__(self, uart):
        self._uart = uart

    def read_vp(self, address, length = 1):
        pass

    def write_vp(self, address, data):
        pass

    def loop(self):
        pass

    def on_recv(self):
        pass

    def add_on_recv_event(self, f):
        pass
