from machine import UART

from dgus import DGUS
from dgus.components.int import Int16


def dgus_receive(payload):
    print("Got data from display")
    print(payload)


def component_value(c, val):
    print("Got data from component {}: {}".format(c, val))


ut = UART(2, 115200, rx=36, tx=4)
tft = DGUS(ut)
tft.event_recv_add(dgus_receive)

i = Int16(tft, 0x1250)
i.event_on_change_add(component_value)

while True:
    tft.loop()
