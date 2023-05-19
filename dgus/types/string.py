# TFT components
# Copyright (c) 2023 Petr Kracik
# Copyright (c) 2023 OctopusLAB

from . import Type

class String(Type):
    @property
    def value(self):
        pass


    @value.setter
    def value(self, value):
        val = value.encode()

        if len(val) % 2 != 0:
            val += b'\xff'

        val += b'\xff\xff'

        # send in chunks
        for i in range(0, len(val), 220):
            chunk = val[i:i+220]
            self._dgus.write_vp(self._vp+(i//2), chunk)
