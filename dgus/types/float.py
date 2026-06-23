# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from dgus.types import Type
from struct import unpack, pack

class Float(Type):
    @property
    def value(self):
        data = self._dgus.read_vp(self._vp, 2)
        return unpack(">f", data)[0]


    @value.setter
    def value(self, value):
        data = pack(">f", value)
        self._dgus.write_vp(self._vp, data)


    def _on_change(self, data):
        val = unpack('>f', data)[0]
        for f in self._on_change_events:
            f(self, val)

