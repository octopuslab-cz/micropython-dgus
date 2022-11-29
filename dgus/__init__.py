# Base driver for DGUS protocol used in DWIN UART TFT displays
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from struct import pack, unpack

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Petr Kracik"


class DGUS:
    HEADER=0x5aa5
    WRITE_VP=0x82
    READ_VP=0x83


    def __init__(self, uart, crc=False):
        self._uart = uart
        self._crc = crc
        self._on_recv_events = []
        if self._crc:
            raise NotImplementedError()



    def read_vp(self, address, length = 1):
        # Flush RX buffer
        self._uart.read()

        self._uart.write(pack('>HBBHB', HEADER, 4, READ_VP, address, length))
        while not self._uart.any():
            pass

        data = self._uart.read()
        rh, rlen, rcmd, raddr, rdlen = unpack('>HBBHB', data[0:7])

        if rh != HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, HEADER))

        if rlen != len(data) - 3:
            raise Exception("Malformed reply, length does not match")

        if rcmd != READ_VP:
            raise Exception("Malformed reply, bad reply command")

        if raddr != address:
            raise Exception("Malformed reply, address does not match")

        rdata = unpack('>{}H'.format(rdlen), data[7:])

        return rdata


    def write_vp(self, address, data):
        # Flush RX buffer
        self._uart.read()

        # pad data to be word
        if len(data) % 2 != 0:
            data += b'\x00'

        length = len(data)
        length += 3


        self._uart.write(pack('>HBBH', HEADER, length, WRITE_VP, address))
        self._uart.write(data)

        while not self._uart.any():
            pass

        data = self._uart.read()
        rh, rlen, rcmd = unpack('>HBB', data[0:4])

        if rh != HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, HEADER))

        if rlen != len(data) - 3:
            raise Exception("Malformed reply, length does not match")

        if rcmd != WRITE_VP:
            raise Exception("Malformed reply, bad reply command")

        return data[4:] == b'OK'


    def loop(self):
        if not self._uart.any():
            return


    def _on_recv(self, data):
        for f in self._on_recv_events:
            f(data)


    def event_recv_add(self, function):
        self._on_recv_events.append(function)


    def event_recv_remove(self, function):
        if function in self._on_recv_events:
            self._on_recv_events.remove(function)
