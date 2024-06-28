"""
Important: This file is imported from the DWIN_T5UIC1_LCD
repository available on (https://github.com/odwdinc/DWIN_T5UIC1_LCD)
with no to minimal changes. All credits go to the original author.
"""
# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

from gpiozero import Button


class Encoder:
    def __init__(self, dial_left_pin, dial_right_pin, callback=None):
        self.dial_left_pin = dial_left_pin
        self.dial_right_pin = dial_right_pin
        self.value = 0
        self.state = "00"
        self.direction = None
        self.callback = callback

        self.dial_left_button = Button(dial_left_pin)
        self.dial_left_button.when_pressed = self.transitionOccurred
        self.dial_left_button.when_released = self.transitionOccurred

        self.dial_right_button = Button(dial_right_pin)
        self.dial_right_button.when_pressed = self.transitionOccurred
        self.dial_right_button.when_released = self.transitionOccurred

    def transitionOccurred(self, channel):
        dial_left_state = '1' if self.dial_left_button.is_pressed else '0'
        dial_right_state = '1' if self.dial_right_button.is_pressed else '0'
        newState = dial_left_state + dial_right_state

        if self.state == "00":  # Resting position
            if newState == "01":  # Turned right 1
                self.direction = "R"
            elif newState == "10":  # Turned left 1
                self.direction = "L"

        elif self.state == "01":  # R1 or L3 position
            if newState == "11":  # Turned right 1
                self.direction = "R"
            elif newState == "00":  # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value)

        elif self.state == "10":  # R3 or L1
            if newState == "11":  # Turned left 1
                self.direction = "L"
            elif newState == "00":  # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value)

        else:  # self.state == "11"
            if newState == "01":  # Turned left 1
                self.direction = "L"
            elif newState == "10":  # Turned right 1
                self.direction = "R"
            elif (
                newState == "00"
            ):  # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value)

        self.state = newState

    def getValue(self):
        return self.value
