# Write your code here :-)
import board
import microcontroller
import digitalio
import displayio
from adafruit_display_text import label
import terminalio
import time
import adafruit_ds3231
import adafruit_ht16k33.segments
import adafruit_uc8151d
import busio

BRIGHTNESS = 1.0 / 16.0
WHITE = 0xFFFFFF
BLACK = 0x000000

BACKGROUND_COLOR = WHITE

DISPLAY_WIDTH=296
DISPLAY_HEIGHT=128

displayio.release_displays()
time.sleep(1)

i2c = board.I2C()
ds3231 = adafruit_ds3231.DS3231(i2c)
seg = adafruit_ht16k33.segments.Seg7x4(i2c)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = False

seg.brightness = BRIGHTNESS
# https://cdn-learn.adafruit.com/assets/assets/000/120/560/original/adafruit_products_Artboard_1-100.jpg

EPD_BUSY = microcontroller.pin.GPIO16
EPD_RESET = microcontroller.pin.GPIO17
EPD_DC = microcontroller.pin.GPIO18
EPD_CS = microcontroller.pin.GPIO19
EPD_SCK = microcontroller.pin.GPIO22
EPD_MOSI = microcontroller.pin.GPIO23


epd_spi = busio.SPI(EPD_SCK, MOSI=EPD_MOSI, MISO=None)

display_bus = displayio.FourWire(epd_spi,command=EPD_DC,chip_select=EPD_CS, reset=EPD_RESET, baudrate=1000000)
time.sleep(1)

display = adafruit_uc8151d.UC8151D(
  display_bus,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,rotation=90)

g = displayio.Group()

'''
with open("/display-ruler.bmp", "rb") as f:
  pic = displayio.OnDiskBitmap(f)
  t = displayio.TileGrid(pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter()))
  print('loaded bmp')
  g.append(t)
'''
background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
palette = displayio.Palette(1)
palette[0] = WHITE
t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
g.append(t)

text = 'HELLO\nISAAC'
font = terminalio.FONT
text_area = label.Label(font,text=text,color=BLACK,scale=4)
text_area.x = 20
text_area.y = 20
g.append(text_area)


print('trying to display')
display.show(g)
display.refresh()
print('done trying.')



while True:
    time.sleep(0.5)
    t = ds3231.datetime
    s = '%02d:%02d' % (ds3231.datetime.tm_hour,ds3231.datetime.tm_min)
    seg.print(s)
    print(s)
