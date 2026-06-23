# Base driver for DGUS protocol used in DWIN UART TFT displays
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from struct import pack, unpack
from time import sleep_us
from micropython import const

__version__ = "0.0.3-SNAPSHOT"
__license__ = "MIT"
__author__ = "Petr Kracik"


_HEADER = const(0x5aa5)
_WRITE_VP = const(0x82)
_READ_VP = const(0x83)
_PAGEID_REG = const(0x5a01)


class DGUS:
    def __init__(self, uart, crc=False):
        self._uart = uart
        self._crc = crc
        self._on_recv_events = []
        self._components = []
        if self._crc:
            raise NotImplementedError()


    def _read_uart(self):
        payload = b''

        read = self._uart.read()
        while read:
            payload += read
            sleep_us(10000)
            read = self._uart.read()

        return payload


    def _parse_dgus(self, payload):
        if len(payload) < 7:
            raise Exception("Unknown payload, it must have atleast 7 bytes")

        rh, rlen, rcmd, raddr, rdlen = unpack('>HBBHB', payload[0:7])

        if rh != _HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, _HEADER))

        if rlen != len(payload) - 3:
            raise Exception("Malformed reply, length does not match")

        response = dict()
        response['command'] = rcmd
        response['address'] = raddr
        response['data'] = payload[7:]

        return response


    def read_vp(self, address, length = 1):
        if length < 1 or length > 0x7c:
            raise Exception("Lenght out of range 1..124")

        # Flush RX buffer
        self._uart.read()

        self._uart.write(pack('>HBBHB', _HEADER, 4, _READ_VP, address, length))

        while not self._uart.any():
            pass

        payload = self._read_uart()
        data = self._parse_dgus(payload)

        if data['command'] != _READ_VP:
            raise Exception("Malformed reply, bad reply command")

        if data['address'] != address:
            raise Exception("Malformed reply, address does not match")

        return data['data']


    def write_vp(self, address, data):
        # Flush RX buffer
        self._uart.read()

        # pad data to be word
        if len(data) % 2 != 0:
            raise Exception("Data must dividable by 2 bytes")

        length = len(data)
        length += 3

        self._uart.write(pack('>HBBH', _HEADER, length, _WRITE_VP, address))
        self._uart.write(data)
        self._uart.flush()

        # Wait until data
        while not self._uart.any():
            pass

        data = self._read_uart()

        rh, rlen, rcmd = unpack('>HBB', data[0:4])

        if rh != _HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, _HEADER))

        if rlen != len(data) - 3:
            raise Exception("Malformed reply, length does not match")

        if rcmd != _WRITE_VP:
            raise Exception("Malformed reply, bad reply command")

        return data[4:] == b'OK'


    def set_page(self, pageid):
        payload = pack('>HH', _PAGEID_REG, pageid)
        self.write_vp(0x84, payload)


    def loop(self):
        if not self._uart.any():
            return

        payload = self._read_uart()
        data = self._parse_dgus(payload)

        self._on_recv(data)


    def _on_recv(self, data):
        for f in self._on_recv_events:
            f(data)


    def event_recv_add(self, function):
        self._on_recv_events.append(function)


    def event_recv_remove(self, function):
        if function in self._on_recv_events:
            self._on_recv_events.remove(function)
