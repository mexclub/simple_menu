import time
import ssd1306
from machine import Pin, RTC
import math

class clock():
    def __init__(self, display, rotary_enc, settings_obj):
        self.display = display
        self.rotary_enc = rotary_enc
        self.settings_obj = settings_obj

        led = Pin(2, Pin.OUT)
        led.on()

        self.display.fill(0)
        self.display.text("",0,0,1)
        self.display.text("",0,12,1)
        self.display.text("",0,24,1)
        self.display.text("",0,36,1)
        self.display.text("",0,48,1)

        ICON = [
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
            [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
            [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
            [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
        ]

        for y, row in enumerate(ICON):
            for x, c in enumerate(row):
                self.display.pixel(x+118, y+0, c)
        self.display.show()

        iterations = 210
        radio = 32
        for i in range(iterations):
            my_sin = math.sin(i*2*math.pi/iterations)
            my_cos = math.cos(i*2*math.pi/iterations)
            self.display.pixel(96+int(radio*my_cos),32+int(radio*my_sin),1)

        px_second = 0
        py_second = 0
        px_minute = 0
        py_minute = 0
        px_hour = 0
        py_hour = 0

        dicmonths= ('NaN','Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic')
        rtc = RTC()
        rtc.datetime((2019, 12, 27, 6, 18, 33, 0, 0)) # set a specific date and time
        while True:
            dt = rtc.datetime() # get date and time
            self.display.fill_rect(0,0,72,12,0)
            self.display.fill_rect(0,12,64,24,0)
            self.display.text("{day:02} de {month}".format(month=dicmonths[dt[1]], day=dt[2]),0,0,1)
            self.display.text("{hour:02}:{minute:02}:{second:02}".format(hour=dt[4], minute=dt[5], second=dt[6]),0,12,1)

            x_hour = math.cos((dt[4]-3 + (dt[5]-15)/60 )*2*math.pi/12)
            y_hour = math.sin((dt[4]-3 + (dt[5]-15)/60 )*2*math.pi/12)
            x_minute = math.cos((dt[5]-15)*2*math.pi/60)
            y_minute = math.sin((dt[5]-15)*2*math.pi/60)
            x_second = math.cos((dt[6]-15)*2*math.pi/60)
            y_second = math.sin((dt[6]-15)*2*math.pi/60)

            self.display.pixel(96+int(radio*0.95*px_second), 32+int(radio*0.95*py_second), 0)
            self.display.pixel(96+int(radio*0.95*x_second), 32+int(radio*0.95*y_second), 1)
            px_second = x_second
            py_second = y_second

            self.display.line(96, 32, 96+int(radio*0.8*px_minute), 32+int(radio*0.8*py_minute), 0)
            self.display.line(96, 32, 96+int(radio*0.8*x_minute), 32+int(radio*0.8*y_minute), 1)
            px_minute = x_minute
            py_minute = y_minute

            self.display.line(96, 32, 96+int(radio*0.5*px_hour), 32+int(radio*0.5*py_hour), 0)
            self.display.fill_rect(96-1+int(radio*0.5*px_hour), 32-1+int(radio*0.5*py_hour), 3, 3, 0)
            self.display.line(96, 32, 96+int(radio*0.5*x_hour), 32+int(radio*0.5*y_hour), 1)
            self.display.fill_rect(96-1+int(radio*0.5*x_hour), 32-1+int(radio*0.5*y_hour), 3, 3, 1)
            px_hour = x_hour
            py_hour = y_hour

            if not rotary_enc['pb'].value():
                time.sleep_ms(500)
                return None

            self.display.show()
            time.sleep_ms(100)
