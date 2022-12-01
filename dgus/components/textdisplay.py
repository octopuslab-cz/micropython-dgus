# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from . import Component
from ..types.string import String


class TextDisplay(Component):
    def __init__(self, dgus, sp_address):
        super().__init__(dgus, sp_address, String)


    def set_color(self, color):
        self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_COLOR, color)
