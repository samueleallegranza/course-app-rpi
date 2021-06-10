from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from time import sleep

class Display:
    def __init__(self, port, address):
        serial = i2c(port=port, address=address)
        self.device = sh1106(serial)

    def connected(self):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "CONNECTED", fill="white")

    def denied(self):
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "ACCESS DENIED", fill="white")

    def granted(self, response):
        direction = "IN" if response["direction"] == 1 else "OUT"
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "ACCESS GRANTED", fill="white")
            draw.text((10, 20), response["student_name"], fill="white")
            draw.text((10, 30), "Direction: " + direction, fill="white")
