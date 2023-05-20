# TFT components
# Copyright (c) 2023 Petr Kracik
# Copyright (c) 2023 OctopusLAB

from . import Type
from struct import unpack, pack

class Float(Type):
    @property
    def value(self):
        data = self._dgus.read_vp(self._vp)
        unpack(">f", data)[0]


    @value.setter
    def value(self, value):
        data = pack(">f", value)
        return self._dgus.write_vp(self._vp, data)


    def _on_change(self, data):
        val = unpack('>f', data)[0]
        for f in self._on_change_events:
            f(self, val)

