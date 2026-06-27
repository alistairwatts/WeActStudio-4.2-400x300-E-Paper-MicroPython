from machine import Pin, SPI
import time


class EPD420:
    WIDTH = 400
    HEIGHT = 300
    BUFFER_SIZE = WIDTH * HEIGHT // 8

    def __init__(
        self,
        spi_bus=2,
        sck_pin=18,
        mosi_pin=23,
        cs_pin=5,
        dc_pin=17,
        rst_pin=16,
        busy_pin=4,
        baudrate=2000000,
    ):
        self.cs = Pin(cs_pin, Pin.OUT, value=1)
        self.dc = Pin(dc_pin, Pin.OUT, value=1)
        self.rst = Pin(rst_pin, Pin.OUT, value=1)
        self.busy = Pin(busy_pin, Pin.IN)
        self.spi = SPI(
            spi_bus,
            baudrate=baudrate,
            polarity=0,
            phase=0,
            sck=Pin(sck_pin),
            mosi=Pin(mosi_pin),
        )
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.buffer = bytearray(self.BUFFER_SIZE)
        self.has_partial = True
        self._initialized = False

    def reset(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

    def wait_until_idle(self):
        while self.busy.value() == 1:
            time.sleep_ms(1)

    def send_command(self, command):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([command]))
        self.cs.value(1)

    def send_data(self, data):
        self.cs.value(0)
        self.dc.value(1)
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.cs.value(1)

    def set_position(self, x, y):
        x_byte = x // 8
        self.send_command(0x4E)
        self.send_data(x_byte)
        self.send_command(0x4F)
        self.send_data(bytearray([y & 0xFF, (y >> 8) & 0x01]))

    def address_set(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44)
        self.send_data(bytearray([x_start // 8, x_end // 8]))
        self.send_command(0x45)
        self.send_data(bytearray([
            y_start & 0xFF,
            (y_start >> 8) & 0xFF,
            y_end & 0xFF,
            (y_end >> 8) & 0xFF,
        ]))

    def power_on(self):
        self.send_command(0x22)
        self.send_data(0xE0)
        self.send_command(0x20)
        self.wait_until_idle()

    def power_off(self):
        self.send_command(0x22)
        self.send_data(0x83)
        self.send_command(0x20)
        self.wait_until_idle()

    def init(self):
        self.reset()
        self.wait_until_idle()
        self.send_command(0x12)
        time.sleep_ms(100)
        self.wait_until_idle()

        self.send_command(0x21)
        self.send_data(bytearray([0x40, 0x00]))

        self.send_command(0x01)
        self.send_data(bytearray([0x2B, 0x01, 0x00]))

        self.send_command(0x3C)
        self.send_data(0x01)

        self.send_command(0x11)
        self.send_data(0x03)

        self.address_set(0, 0, self.width - 1, self.height - 1)

        self.send_command(0x18)
        self.send_data(0x80)

        self.set_position(0, 0)
        self.power_on()
        self._initialized = True
        return True

    def init_partial(self):
        self.init()
        self.send_command(0x3C)
        self.send_data(0x80)
        self.send_command(0x21)
        self.send_data(bytearray([0x00, 0x00]))
        self._initialized = True
        return True

    def update(self):
        self.send_command(0x22)
        self.send_data(0xF7)
        self.send_command(0x20)
        self.wait_until_idle()

    def update_fast(self):
        self.send_command(0x22)
        self.send_data(0xC7)
        self.send_command(0x20)
        self.wait_until_idle()

    def update_partial(self):
        self.send_command(0x22)
        self.send_data(0xFF)
        self.send_command(0x20)
        self.wait_until_idle()

    def write_image(self, data):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(data)
        self.cs.value(1)

    def display_frame(self):
        self.set_position(0, 0)
        self.send_command(0x26)
        self.write_image(self.buffer)
        self.set_position(0, 0)
        self.send_command(0x24)
        self.write_image(self.buffer)
        self.update()

    def display_partial(self):
        self.set_position(0, 0)
        self.send_command(0x24)
        self.write_image(self.buffer)
        self.update_partial()
        self.set_position(0, 0)
        self.send_command(0x26)
        self.write_image(self.buffer)

    def clear_buffer(self, color=1):
        fill_byte = 0xFF if color else 0x00
        for i in range(len(self.buffer)):
            self.buffer[i] = fill_byte

    def sleep(self):
        self.power_off()
        self.send_command(0x10)
        self.send_data(0x01)
        self._initialized = False
