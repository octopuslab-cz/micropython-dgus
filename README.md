# micropython-dgus

Example usage:

ESP32:

from machine import UART
from dgus import DGUS

tftu = UART(1, 115200, rx=36, tx=4)
tft = DGUS(tftu)

tft.read_vp(0x1250)
tft.write_vp(0x1250, b'\x00\x10')


UNIX port:

from serial import Serial
from dgus import DGUS

tftu = Serial("/dev/ttyUSB0", 115200, 1)
tft = DGUS(tftu)

tft.read_vp(0x1250)
tft.write_vp(0x1250, b'\x00\x10')
