from machine import UART
from dgus import DGUS
from dgus.types.int import Int16
from dgus.types.string import String
from dgus.components.textdisplay import TextDisplay
from dgus.components.datavariablesdisplay import DataVariablesDisplay
from dgus.components.qrcode import QRCode


def dgus_receive(payload):
    print("Got data from display")
    print(payload)


def component_value(c, val):
    print("Got data from component {}: {}".format(c, val))


def type_value(c, val):
    print("Got data from type {}: {}".format(c, val))


ut = UART(2, 115200, rx=36, tx=4)

tft = DGUS(ut)
tft.event_recv_add(dgus_receive)

i = Int16(tft, 0x1250)
i.event_on_change_add(type_value)

s = String(tft, 0x1100)
txt = TextDisplay(tft, 0x2100)
updown = DataVariablesDisplay(tft, 0x2250)
updown.component.event_on_change_add(component_value)

qr = QRCode(tft, 0x2300)

txt.value = "Ahoj"


while True:
    tft.loop()
