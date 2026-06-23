# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from dgus.types import Type
from struct import unpack, pack

class Int16(Type):
    @property
    def value(self):
        data = self._dgus.read_vp(self._vp, 1)
        return unpack(">h", data)[0]


    @value.setter
    def value(self, value):
        self._dgus.write_vp(pack(">h", value), self._vp, 1)


    def _on_change(self, data):
        val = unpack('>h', data)[0]
        for f in self._on_change_events:
            f(self, val)


class UInt16(Type):
    @property
    def value(self):
        data = self._dgus.read_vp(self._vp, 1)
        return unpack(">H", data)[0]


    @value.setter
    def value(self, value):
        self._dgus.write_vp(pack(">H", value), self._vp, 1)


    def _on_change(self, data):
        val = unpack('>H', data)[0]
        for f in self._on_change_events:
            f(self, val)
