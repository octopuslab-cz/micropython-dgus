from machine import UART
from dgus import DGUS
from dgus.types.int import Int16
from dgus.types.string import String
from dgus.components.textdisplay import TextDisplay
from dgus.components.returnkeycode import ReturnKeyCode
from dgus.components.datavariablesdisplay import DataVariablesDisplay

#from dgus.components.qrcode import QRCode


def dgus_receive(payload):
    print("RAW data: {}".format(payload))


def component_value(c, val):
    print("Data from component {}: {}".format(c, val))


def type_value(c, val):
    print("Data from type {}: {}".format(c, val))


def key_press(c, val):
    print("Keypad {} - key {}".format(c, val))


ut = UART(2, 115200, rx=36, tx=4)

tft = DGUS(ut)
tft.event_recv_add(dgus_receive)

i = Int16(tft, 0x1250)
i.event_on_change_add(type_value)

s = String(tft, 0x1100)
txt = TextDisplay(tft, 0x2100)
updown = DataVariablesDisplay(tft, None, 0x1250)
updown.event_on_change_add(component_value)
#qr = QRCode(tft, 0x2300)

txt.value = "Ahoj"

rc = ReturnKeyCode(tft, 0x1600)
rc.event_on_key_press_add(key_press)


print("Running main loop")
while True:
    tft.loop()
