# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from micropython import const
from dgus.components import Component
from dgus.types.string import String


_SP_OFFSET_UNIT_PIXELS = const(0x03)
_SP_OFFSET_FIX_MODE = const(0x05)


class QRCode(Component):
    def __init__(self, dgus, sp_address, vp_address = None):
        super().__init__(dgus, sp_address, String, vp_address)


    @property
    def unit_pixels(self):
        return self._read_u16(self._sp + _SP_OFFSET_UNIT_PIXELS)


    @unit_pixels.setter
    def unit_pixels(self, value):
        self._write_u16(self._sp + _SP_OFFSET_UNIT_PIXELS, value)


    @property
    def fix_mode(self):
        return self._read_u16(self._sp + _SP_OFFSET_FIX_MODE)


    @fix_mode.setter
    def fix_mode(self, value):
        self._write_u16(self._sp + _SP_OFFSET_FIX_MODE, value)
