# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from struct import pack
from . import Component
from ..types import Type


class BasicGraphics(Component):
    SP_OFFSET_POS_XE = 0x03
    SP_OFFSET_POS_YE = 0x04
    
    CMD_DOT = 0x0001
    CMD_RECT = 0x0003
    CMD_FILLRECT = 0x0004

    def __init__(self, dgus, sp_address, vp_address = None):
        super().__init__(dgus, sp_address, Type, vp_address)

        self._xe = self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_POS_XE)
        self._ye = self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_POS_YE)


    def draw_pixel(self, x, y, color):
        data = pack('>HHHHH', self.CMD_DOT, 1, self._x+x, self._y+y, color)
        self._dgus.write_vp(self._vp, data)


    def draw_rect(self, x, y, w, h, color):
        data = pack('>HHHHHHHH', self.CMD_RECT, 1, self._x+x, self._y+y, self._x + x + w, self._y + y + h, color, 0xFF00)
        self._dgus.write_vp(self._vp, data)


    def fill_rects(self, rects):
        data = pack('>HH', self.CMD_FILLRECT, len(rects))
        for rect in rects:
            data += pack('>HHHHH',
                         self._x+rect['x'],
                         self._y+rect['y'],
                         self._x + rect['x'] + rect['w'],
                         self._y + rect['y'] + rect['h'],
                         rect['color'])
        data += pack('>H', 0xFF00)

        self._dgus.write_vp(self._vp, data)


    def fill_rect(self, x, y, w, h, color):
        rect = dict()
        rect['x'] = x
        rect['y'] = y
        rect['w'] = w
        rect['h'] = h
        rect['color'] = color
        
        self.fill_rects([rect])


    @property
    def size(self):
        if self._sp == 0xFFFF:
            raise Exception("This component does not have SP address")

        return (self._xe-self._x, self._ye-self._y)


    @size.setter
    def size(self, size):
        if self._sp == 0xFFFF:
            raise Exception("This component does not have SP address")
        
        xe = self._x + size[0]
        ye = self._y + size[1]

        if not self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_POS_XE, xe):
            raise Exception("Error while setting XE position")

        if not self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_POS_YE, ye):
            raise Exception("Error while setting YE position")

        self._xe = xe
        self._ye = ye
