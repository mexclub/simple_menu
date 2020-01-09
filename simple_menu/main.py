import time
import ssd1306
import simple_menu
from settings import settings
from machine import SPI, I2C, Pin

rotary_enc = {"pb" : Pin(16, Pin.IN), "ra" : Pin(2, Pin.IN), "rb" : Pin(0, Pin.IN), "pin_irq" : Pin.IRQ_FALLING}
st = settings()
settings_obj = st.get_settings()

i2c_obj = I2C(-1, Pin(14), Pin(13))
addr = i2c_obj.scan()
if 0x3C in addr:
    display = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c_obj, addr=0x3C, external_vcc=False)
else:
    display = ssd1306.SSD1306_SPI(width=128, height=64, spi=SPI(1), dc=Pin(4), res=Pin(5), cs=Pin(15), external_vcc=False)

menu_list = ['back', 'clock', 'alarm', 'wifi connect', 'wifi server', 'settings', 'reset', 'alphabet']
menu_actions = ['<BACK>', 'clock', 'alarm', 'wificonnect', 'wifiserver', 'settings', 'reset', 'simple_alphabet']
menu_obj = {"menu_list": menu_list, "menu_actions": menu_actions}

menu = simple_menu.simple_menu(display, rotary_enc, menu_obj, settings_obj)

while True:
    display.fill_rect(0,0,128,64,0)
    display.text("{: ^16s}".format("WELCOME"),0,0,1)
    display.text("{: ^16s}".format("PRESS START"),0,30,1)
    display.show()

    if not rotary_enc['pb'].value():
        menu.show()
    time.sleep_ms(100)
