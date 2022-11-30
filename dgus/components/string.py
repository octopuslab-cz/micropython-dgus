# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

from . import Component

class String(Component):
    @property
    def value(self):
        pass


    @value.setter
    def value(self, value):
        val = value.encode()

        if len(val) % 2 != 0:
            val += b'\x00'

        val += b'\xff\xff'

        self._dgus.write_vp(self._addr, val)
