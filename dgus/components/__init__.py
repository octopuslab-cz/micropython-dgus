# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

SP_OFFSET_VP = 0x00
SP_OFFSET_COLOR = 0x03

class Component:
    def __init__(self, dgus, sp_address, component):
        self._sp = sp_address
        self._dgus = dgus
        self._vp = self._dgus.read_vp_int16(self._sp + SP_OFFSET_VP)
        self._component = component(self._dgus, self._vp)
        print("Initialized {} at address 0x{:02x} with VP at 0x{:02x}".format(self.__class__.__name__, self._sp, self._vp))


    @property
    def component(self):
        return self._component


    @property
    def value(self):
        if self._component is None:
            raise Exception("Component is not net")
        
        return self._component.value


    @value.setter
    def value(self, value):
        self._component.value = value
