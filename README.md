# micropython-dgus

Example usage:

ESP32:

from machine import UART
from dgus import DGUS
from dgus.components.int import Int16

def component_value(c, val):
    print("Got data from component {}: {}".format(c, val))


tftu = UART(1, 115200, rx=36, tx=4)
tft = DGUS(tftu)

tft.read_vp(0x1250)
tft.write_vp(0x1250, b'\x00\x10')

number = Int16(tft, 0x1250)
print(number.value)
number.value = 123

number.event_on_change_add(component_value)

while True:
    tft.loop()
