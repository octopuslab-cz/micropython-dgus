# TFT components
# Copyright (c) 2026 Petr Kracik
# Copyright (c) 2026 OctopusLAB

from dgus.types import Type
from struct import unpack, pack

class _Int(Type):
    @property
    def value(self):
        data = self._dgus.read_vp(self._vp, self._words)
        return unpack(self._format, data)[0]


    @value.setter
    def value(self, value):
        self._dgus.write_vp(self._vp, pack(self._format, value))


    def _on_change(self, data):
        val = unpack(self._format, data)[0]
        for f in self._on_change_events:
            f(self, val)


class Int16(_Int):
    _format = ">h"
    _words = 1


class UInt16(_Int):
    _format = ">H"
    _words = 1


class Int32(_Int):
    _format = ">i"
    _words = 2


class UInt32(_Int):
    _format = ">I"
    _words = 2
