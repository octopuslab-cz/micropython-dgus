# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from . import Component
from ..types.string import String


class TextDisplay(Component):
    SP_OFFSET_TEXT_LENGTH = 0x0


    def __init__(self, dgus, sp_address):
        super().__init__(dgus, sp_address, String)


    def set_color(self, color):
        self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_COLOR, color)


    @property
    def max_length(self):
        return self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_TEXT_LENGTH)


    @max_length.setter
    def max_length(self, value):
        self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_TEXT_LENGTH, value)
