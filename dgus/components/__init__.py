# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

class Component:
    SP_OFFSET_VP = 0x00
    SP_OFFSET_POS_X = 0x01
    SP_OFFSET_POS_Y = 0x02
    SP_OFFSET_COLOR = 0x03

    def __init__(self, dgus, sp_address, component, vp_address=None):
        self._sp = sp_address or 0xFFFF
        self._dgus = dgus
        if vp_address is None:
            self._vp = self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_VP)
        else:
            self._vp = vp_address

        if self._sp != 0xFFFF:
            self._x = self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_POS_X)
            self._y = self._dgus.read_vp_int16(self._sp + self.SP_OFFSET_POS_Y)

        self._component = component(self._dgus, self._vp)
        print("Initialized {} at address 0x{:02x} with VP at 0x{:02x}".format(self.__class__.__name__, self._sp, self._vp))


    @property
    def component(self):
        return self._component


    @property
    def position(self):
        if self._sp == 0xFFFF:
            raise Exception("This component does not have SP address")

        return (self._x, self._y)


    @position.setter
    def position(self, pos):
        if self._sp == 0xFFFF:
            raise Exception("This component does not have SP address")

        if not self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_POS_X, pos[0]):
            raise Exception("Error while setting X position")

        if not self._dgus.write_vp_int16(self._sp + self.SP_OFFSET_POS_Y, pos[1]):
            raise Exception("Error while setting Y position")

        self._x = pos[0]
        self._y = pos[1]


    @property
    def value(self):
        if self._component is None:
            raise Exception("Component is not net")
        
        return self._component.value


    @value.setter
    def value(self, value):
        self._component.value = value
