# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

class Component:
    def __init__(self, dgus, sp_address):
        self._sp = sp_address
        self._dgus = dgus
        self._component = None

    @property
    def component(self):
        return self._component


    #component.setter
    def component(self, value):
        self._compoment = value


    @property
    def value(self):
        if self._component is None:
            raise Exception("Component is not net")
        
        return self._compoment.value


    @value.setter
    def value(self, value):
        self._component.value = value
