# WeAct Studio 4.2" SSD1683 E-Paper MicroPython Demo

A MicroPython implementation for the WeAct Studio 4.2" (400×300) black & white
e-paper module with SSD1683 controller. This demo achieves a similar visual
result as the Arduino example, but runs on MicroPython-compatible
microcontrollers like the ESP32.

## Features

- **Custom SSD1683 Driver**: Pure MicroPython implementation of the SSD1683
  e-paper controller
- **Full Screen Updates**: Display text and graphics with complete refresh
- **Partial Updates**: Faster screen updates in regions without full refresh
- **Hardware-Agnostic SPI**: Works with any MicroPython board supporting
  `machine.SPI`
- **Simple API**: Clean, object-oriented interface for display control

## Hardware Requirements

### Display Module
- **WeAct Studio 4.2" GDEY042T81** (or compatible SSD1683-based 400×300 panel)
- Black & white e-paper display
- SPI interface

### Microcontroller
- **ESP32** (tested) or other MicroPython-compatible board
- SPI support via `machine.SPI`
- GPIO pins for control signals

### Wiring (ESP32 Default Pinout)

Connect the e-paper module to ESP32:

| E-Paper Pin | ESP32 Pin | Pin No. |
|:-----------:|:---------:|--------:|
| CS          | GPIO5     |       5 |
| SCK         | GPIO18    |      18 |
| MOSI        | GPIO23    |      23 |
| DC          | GPIO17    |      17 |
| RST         | GPIO16    |      16 |
| BUSY        | GPIO4     |       4 |
| GND         | GND       |       – |
| VCC         | 3.3V      |       – |

### Optional Modifications

To use different pins, modify the pin parameters when instantiating `EPD420`:

```python
epd = EPD420(
    spi_bus=2,
    sck_pin=18,
    mosi_pin=23,
    cs_pin=5,
    dc_pin=17,
    rst_pin=16,
    busy_pin=4,
)
```

## Installation & Setup

This assumes you have MicroPython running on your device and `main.py` and
`ssd1783.py` have been copied to the device.

### Run the Demo

Connect via serial console and execute:

```python
import main
```

Or, if `main.py` is set as `boot.py`, it will run automatically on startup.

## Usage

### Basic Example

```python
from ssd1683 import EPD420
import framebuf

# Initialize the display
epd = EPD420()
epd.init()

# Create a framebuffer
fb = framebuf.FrameBuffer(epd.buffer, epd.width, epd.height, framebuf.MONO_HLSB)

# Draw on the framebuffer
fb.fill(1)  # Fill white
fb.text("Hello!", 10, 10, 0)  # Draw black text

# Update the display
epd.display_frame()
```

### Full Screen Update

```python
epd.display_frame()  # Triggers a full screen refresh
```

### Partial Update

```python
epd.init_partial()
# ... modify epd.buffer ...
epd.display_partial()  # Faster refresh without
```

### Power Management

```python
epd.sleep()  # Deep sleep mode; wake requires full reset
epd.power_off()  # Turn off voltage supplies
epd.power_on()  # Reactivate power
```

## Demo Behavior

The included `main.py` demonstrates:

1. **Initialization**: Sets up SPI, GPIO, and the SSD1683 controller
2. **Full Screen Display**: Shows centered "Hello World!" and "WeAct Studio" text
3. **Partial Update Demo**: Cycles through 10 values in a small box region using fast partial updates
4. **Sleep Mode**: Places the display in low-power sleep at the end

### Buffer Format

- **Size**: 15,000 bytes (400 × 300 ÷ 8)
- **Format**: MONO_HLSB (monochrome, high byte first, LSB first per byte)
- **Color**: 1 = white, 0 = black

### Timing

- **Initialization**: ~2–3 seconds
- **Full Update**: ~3–5 seconds
- **Partial Update**: ~0.5–1 second
- **Sleep Entry**: ~100 ms

## Source & Attribution

This MicroPython implementation is derived from:

- **WeAct Studio E-Paper Module** repository documentation
- **Arduino GxEPD2 library** command sequences for SSD1683
- **Raspberry Pi C driver** (`epaper.c`) in the WeAct repository
- **MicroPython framebuf module** for graphics rendering

The SSD1683 command sequences and timing parameters were reverse-engineered
from the Arduino and C examples to ensure compatibility with the WeAct Studio
4.2" module.

## License

This code is provided as-is for. Please refer to the WeAct Studio repository
for original hardware design and documentation.

## References

- [WeAct Studio GitHub](https://github.com/WeActTC/WeAct-7inch-e-Paper-Module)
- [MicroPython Documentation](https://docs.micropython.org/)
- [SSD1683 Datasheet](https://www.good-display.com/product/364.html)
- [Arduino GxEPD2 Library](https://github.com/ZinggJM/GxEPD2)
