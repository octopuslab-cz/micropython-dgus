# Base driver for DGUS protocol used in DWIN UART TFT displays
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from struct import pack, unpack

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Petr Kracik"


class Component:
    def __init__(self, dgus, address):
        self._dgus = dgus
        self._addr = address


    def __str__(self):
        return "{} at 0x{:02x}".format(self.__class__.__name__, self._addr)


    def __repr__(self):
        return self.__str__()


    @property
    def address(self):
        return self._addr


    @property
    def value(self):
        raise NotImplementedError()


class Int16(Component):
    @property
    def value(self):
        return self._dgus.read_vp_int16(self._addr)


    @value.setter
    def value(self, value):
        self._dgus.write_vp_int16(self._addr, value)


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


    def _parse_dgus(self, payload):
        rh, rlen, rcmd, raddr, rdlen = unpack('>HBBHB', payload[0:7])

        if rh != self.HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, HEADER))

        if rlen != len(payload) - 3:
            raise Exception("Malformed reply, length does not match")

        response = dict()
        response['command'] = rcmd
        response['address'] = raddr
        response['data'] = payload[7:]

        return response


    def read_vp(self, address, length = 1):
        if length < 1 and length > 0x7c:
            raise Exception("Lenght out of range 1..124")

        # Flush RX buffer
        self._uart.read()

        self._uart.write(pack('>HBBHB', self.HEADER, 4, self.READ_VP, address, length))

        while not self._uart.any():
            pass

        payload = self._uart.read()
        data = self._parse_dgus(payload)

        if data['command'] != self.READ_VP:
            raise Exception("Malformed reply, bad reply command")

        if data['address'] != address:
            raise Exception("Malformed reply, address does not match")

        return data['data']


    def read_vp_int16(self, address):
        data = self.read_vp(address, 1)
        return unpack(">h", data)[0]


    def read_vp_uint16(self, address):
        data = self.read_vp(address, 1)
        return unpack(">H", data)[0]


    def write_vp(self, address, data):
        # Flush RX buffer
        self._uart.read()

        # pad data to be word
        if len(data) % 2 != 0:
            raise Exception("Data must dividable by 2 bytes")

        length = len(data)
        length += 3


        self._uart.write(pack('>HBBH', self.HEADER, length, self.WRITE_VP, address))
        self._uart.write(data)

        while not self._uart.any():
            pass

        data = self._uart.read()
        rh, rlen, rcmd = unpack('>HBB', data[0:4])

        if rh != self.HEADER:
            raise Exception("Malformed reply, HEADER mismatch {} != {}".format(rh, HEADER))

        if rlen != len(data) - 3:
            raise Exception("Malformed reply, length does not match")

        if rcmd != self.WRITE_VP:
            raise Exception("Malformed reply, bad reply command")

        return data[4:] == b'OK'


    def write_vp_int16(self, address, value):
        data = pack(">H", value)
        return self.write_vp(address, data)


    def write_vp_int32(self, address, value):
        data = pack(">I", value)
        return self.write_vp(address, data)


    def loop(self):
        if not self._uart.any():
            return
        payload = self._uart.read()

        self._on_recv(self._parse_dgus(payload))


    def _on_recv(self, data):
        for f in self._on_recv_events:
            f(data)


    def event_recv_add(self, function):
        self._on_recv_events.append(function)


    def event_recv_remove(self, function):
        if function in self._on_recv_events:
            self._on_recv_events.remove(function)
