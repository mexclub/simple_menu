from machine import Pin

class simple_encoder():
    def __init__(self, ra, rb, pin_irq):
        self.ra = ra
        self.rb = rb
        self.counter = 0
        self.ra.irq(trigger=pin_irq, handler=self.turn)
        self.rb.irq(trigger=pin_irq, handler=self.turn)

    def turn(self, pin):
        changed = False
        enc_turn = 0
        while (not self.ra.value()) or (not self.rb.value()):
            if not changed:
                if self.ra.value() == pin.value():
                    enc_turn = 2
                    self.counter = self.counter + 1
                if self.rb.value() == pin.value():
                    enc_turn = 1
                    self.counter = self.counter - 1
                changed = True
        return True
