import framebuf
import time
from ssd1683 import EPD420


def center_text_x(width, text, char_width=8):
    return max((width - len(text) * char_width) // 2, 0)


def draw_start_screen(epd):
    fb = framebuf.FrameBuffer(epd.buffer, epd.width, epd.height, framebuf.MONO_HLSB)
    fb.fill(1)
    message_top = "Hello World!"
    message_bottom = "WeAct Studio"
    x_top = center_text_x(epd.width, message_top)
    x_bottom = center_text_x(epd.width, message_bottom)
    y_top = epd.height // 2 - 20
    y_bottom = epd.height // 2 + 4
    fb.text(message_top, x_top, y_top, 0)
    fb.text(message_bottom, x_bottom, y_bottom, 0)
    epd.display_frame()


def show_partial_demo(epd):
    if not epd.has_partial:
        return

    epd.init_partial()
    fb = framebuf.FrameBuffer(epd.buffer, epd.width, epd.height, framebuf.MONO_HLSB)
    box_x = 10
    box_y = 15
    box_w = 70
    box_h = 20

    for step in range(1, 11):
        fb.fill(1)
        fb.fill_rect(box_x, box_y, box_w, box_h, 1)
        fb.text("fast partial", 90, 20, 0)
        fb.text("value", 90, 34, 0)
        value_text = "{:.2f}".format(13.95 * step)
        fb.text(value_text, box_x + 2, box_y + 6, 0)
        epd.display_partial()
        time.sleep_ms(500)

    time.sleep_ms(1000)
    fb.fill(1)
    fb.text("Partial demo done!", 10, 20, 0)
    epd.display_frame()


def main():
    epd = EPD420(
        spi_bus=2,
        sck_pin=18,
        mosi_pin=23,
        cs_pin=5,
        dc_pin=17,
        rst_pin=16,
        busy_pin=4,
    )

    if not epd.init():
        raise RuntimeError("Failed to initialize SSD1683 display")

    print('Drawing start screen...')
    draw_start_screen(epd)
    print('Sleeping for 1 second')
    time.sleep_ms(1000)

    print('Showing partial demo...')
    show_partial_demo(epd)
    time.sleep_ms(1000)
    print('Sleeping for 1 second')

    print('Putting display to sleep...')
    epd.sleep()
    print('Display is now in sleep mode. Exiting program.')
    while True:
        time.sleep_ms(10000)


if __name__ == "__main__":
    main()
