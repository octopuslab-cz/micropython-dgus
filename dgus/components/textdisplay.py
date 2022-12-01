# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from . import Component
from ..types.string import String


SP_OFFSET_VP = 0x00
SP_OFFSET_COLOR = 0x03

class TextDisplay(Component):
    def __init__(self, dgus, sp_address):
        super().__init__(dgus, sp_address)
        vp = self._dgus.read_vp_int16(self._sp + SP_OFFSET_VP)
        self._component = String(self._dgus, vp)
        print("Initialized TextDisplay at address 0x{:02x} with VP at 0x{:02x}".format(self._sp, self._component._vp))


    def set_color(self, color):
        self._dgus.write_vp_int16(self._sp + SP_OFFSET_COLOR, color)
