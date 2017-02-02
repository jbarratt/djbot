#!/usr/bin/env python
""" Encapsulates Gamepad interaction & parsing functions """

from evdev import InputDevice, categorize, ecodes, KeyEvent


class Gamepad(object):

    """ Gamepad is an object that represents DJBot's Gamepad """

    keys = {'BTN_TR2': "start",
            'BTN_TL2': "select",
            'BTN_X': "y",
            'BTN_A': "x",
            'BTN_B': "a",
            'BTN_C': "b",
            'BTN_Y': "l_shoulder",
            'BTN_Z': "r_shoulder"}

    def __init__(self):
        self.gamepad = InputDevice('/dev/input/event0')

    def get_events(self):
        """ Generator that returns a stream of events
            from the gamepad as human readable strings
            x,y,z,select,start,left,right,l_shoulder,r_shoulder, etc
        """
        for event in self.gamepad.read_loop():
            if event.type == ecodes.EV_ABS:
                value = self.convert_dpad(event)
                if value:
                    yield value
            elif event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                if keyevent.keystate != KeyEvent.key_down:
                    continue
                code = self.convert_code(keyevent.keycode)
                if code:
                    yield code

    @staticmethod
    def convert_dpad(event):
        """ Convert a dpad direction to cardinal or center """
        value = None
        if event.code == ecodes.ABS_X:
            if event.value > 200:
                value = "right"
            elif event.value < 100:
                value = "left"
            else:
                value = "center"
        elif event.code == ecodes.ABS_Y:
            if event.value > 200:
                value = "down"
            elif event.value < 100:
                value = "up"
            else:
                value = "center"
        return value

    def convert_code(self, keycode):
        """ Given a evdev keycode object, return our gamepad's key label """

        for code in self.keys:
            if code in keycode:
                return self.keys[code]

        return None
