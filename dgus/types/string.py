# TFT components
# Copyright (c) 2023 Petr Kracik
# Copyright (c) 2023 OctopusLAB

from . import Type

class String(Type):
    MAX_CHUNK_SIZE = 220

    @property
    def value(self):
        pass


    @value.setter
    def value(self, value):
        val = value.encode()

        if len(val) % 2 != 0:
            val += b'\xff'

        val += b'\xff\xff'

        for i in range(0, len(val), self.MAX_CHUNK_SIZE):
            chunk = val[i:i+self.MAX_CHUNK_SIZE]
            self._dgus.write_vp(self._vp+(i//2), chunk)
