# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from . import Component
from struct import unpack

class Int16(Component):
    @property
    def value(self):
        return self._dgus.read_vp_int16(self._addr)


    @value.setter
    def value(self, value):
        self._dgus.write_vp_int16(self._addr, value)


    def _on_change(self, data):
        val = unpack('>H', data)[0]
        for f in self._on_change_events:
            f(self, val)
