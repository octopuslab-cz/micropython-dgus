# TFT components
# Copyright (c) 2022 Petr Kracik
# Copyright (c) 2022 OctopusLAB

class Component:
    def __init__(self, dgus, address):
        self._addr = address
        self._dgus = dgus
        self._dgus.event_recv_add(self._on_recv)
        self._on_change_events = list()


    def _on_change(self, data):
        print("Component {}(0x{:02x}) changed value to {}".format(self.__class__.__name__, self._addr, data))


    def _on_recv(self, data):
        # Not for us, so just let it be
        if data['address'] != self.address:
            return

        self._on_change(data['data'])


    def __str__(self):
        return "{} at 0x{:02x}".format(self.__class__.__name__, self._addr)


    def __repr__(self):
        return self.__str__()


    @property
    def address(self):
        return self._addr


    @property
    def value(self):
        raise NotImplementedError()

    def event_on_change_add(self, function):
        self._on_change_events.append(function)


    def event_on_change_remove(self, function):
        if function in self._on_change_events:
            self._on_change_events.remove(function)
