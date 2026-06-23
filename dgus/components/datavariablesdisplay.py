# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from dgus.components import Component, _SP_OFFSET_COLOR
from dgus.types.int import Int16


class DataVariablesDisplay(Component):
    def __init__(self, dgus, sp_address, vp_address = None, datatype=Int16):
        super().__init__(dgus, sp_address, datatype, vp_address)


    def set_color(self, color):
        self._dgus.write_vp_int16(self._sp + _SP_OFFSET_COLOR, color)
