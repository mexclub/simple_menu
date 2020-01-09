import time
import ssd1306
import simple_encoder
from machine import Pin

class simple_alphabet():
    def __init__(self, display, rotary_enc, settings_obj):
        self.display = display
        self.rotary_enc = rotary_enc
        self.alphanumeric_list = list('\b'+'\n'+settings_obj[0]['ALPHABET'])
        self.em = simple_encoder.simple_encoder (rotary_enc['ra'], rotary_enc['rb'], rotary_enc['pin_irq'])
        self.show()

    def show(self):
        self.display.fill(0)
        self.display.text("{0}".format("SELECT LETTER: "), 0, 0, 1)
        self.display.fill_rect(0,36,128,12,1)
        str_push = ""
        self.em.counter = 3
        while True:
            if self.em.counter < 0:
                self.em.counter = len(self.alphanumeric_list) - 1
            if self.em.counter >= len(self.alphanumeric_list):
                self.em.counter = 0

            self.display.fill_rect(0,12,128,12,0)
            actual_char = self.alphanumeric_list[self.em.counter]
            if actual_char == '\b':
                actual_char = '<BACKSPACE>'
            if actual_char == '\n':
                actual_char = '<END>'
            self.display.text("{0}".format(actual_char), 0, 12, 1)

            if not self.rotary_enc["pb"].value():
                if actual_char == '<BACKSPACE>':
                    actual_char = ''
                    if len(str_push) > 0:
                        str_push = str_push[:-1]
                    else:
                        str_push = ''
                if actual_char == '<END>':
                    time.sleep_ms(500)
                    return str_push
                str_push = str_push + str(actual_char)
                self.display.fill_rect(0,36,128,12,1)
                self.display.text("{0:>16}".format(str_push[-16:]), 0, 36, 0)
                # str_to_return = str_push
                time.sleep_ms(500)

            self.display.show()
            time.sleep_ms(100)

