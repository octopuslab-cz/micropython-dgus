# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from micropython import const
from dgus.components import Component, _SP_OFFSET_COLOR
from dgus.types.string import String


_SP_OFFSET_TEXT_LENGTH = const(0x08)


class TextDisplay(Component):
    def __init__(self, dgus, sp_address, vp_address = None):
        super().__init__(dgus, sp_address, String, vp_address)


    def set_color(self, color):
        self._write_u16(self._sp + _SP_OFFSET_COLOR, color)


    @property
    def max_length(self):
        return self._read_u16(self._sp + _SP_OFFSET_TEXT_LENGTH)


    @max_length.setter
    def max_length(self, value):
        self._write_u16(self._sp + _SP_OFFSET_TEXT_LENGTH, value)
