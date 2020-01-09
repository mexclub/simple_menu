import time
import ssd1306
import simple_encoder
from machine import Pin

class simple_menu():
    def __init__(self, display, rotary_enc, menu_obj, settings_obj):
        self.display = display
        self.rotary_enc = rotary_enc
        self.menu_list = menu_obj["menu_list"]
        self.menu_actions = menu_obj["menu_actions"]
        self.settings_obj = settings_obj
        self.em = simple_encoder.simple_encoder (rotary_enc['ra'], rotary_enc['rb'], rotary_enc['pin_irq'])

    def show(self):
        time.sleep_ms(500)
        self.display.fill(0)
        offset_y = 4
        row_offset = 0
        while True:
            row_offset = 0
            if self.em.counter < 0:
                self.em.counter = len(self.menu_list) - 1
            if self.em.counter >= len(self.menu_list):
                self.em.counter = 0
            if self.em.counter > 5 :
                row_offset = self.em.counter - 5
                if self.em.counter >= len(self.menu_list):
                    self.em.counter = 0
            if self.em.counter == 0:
                row_offset = 0
            emc = self.em.counter

            for row in range(row_offset, len(self.menu_list)):
                if emc == row:
                    bg_color = 1
                    fg_color = 0
                    if not self.rotary_enc['pb'].value():
                        time.sleep_ms(500)
                        if self.menu_actions[row] == '<BACK>':
                            return True
                        module = __import__(self.menu_actions[row], globals(), locals(), [self.menu_actions[row]], 0)
                        my_function = getattr(module, self.menu_actions[row])
                        my_function(self.display, self.rotary_enc, self.settings_obj)
                        self.display.fill(0)
                else:
                    bg_color = 0
                    fg_color = 1
                self.display.fill_rect(8, offset_y+(row-row_offset)*10, 120, 10, bg_color)
                self.display.text("{0}".format(self.menu_list[row]), 8, offset_y+(row-row_offset)*10, fg_color)
            self.display.show()
            time.sleep_ms(100)
