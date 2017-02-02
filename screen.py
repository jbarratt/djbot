""" Robot face orchestration """

import serial
import random
import time


class Face(object):

    """
    Represents a robot's face (connected with serial)
    """

    TOP = 55
    BOTTOM = 10
    LL = 20
    LR = 54
    RL = 72
    RR = 107

    def __init__(self, port):
        self.conn = serial.Serial(port, "115200")
        self.clear_display()
        self.regular_face()
        self.faces = ["sad", "mad", "regular"]

    def handle_command(self, cmd):
        """ Handle text based commands """
        if cmd == "blink":
            for _ in range(3):
                self.set_backlight(0)
                time.sleep(0.2)
                self.set_backlight(200)
        else:
            self.set_face(cmd)

    def random(self):
        """ Set the face to a random face """
        face = random.choice(self.faces)
        self.set_face(face)

    def set_face(self, face):
        """ Given a string representation of the faces we know, select one """
        if face == "sad":
            self.sad_face()
        elif face == "mad":
            self.mad_face()
        elif face == "regular":
            self.regular_face()

    def set_backlight(self, pct):
        """ Set the backlight to an integer percentage of intensity 0-100 """
        self.conn.write("|\x02"+chr(pct))

    def clear_display(self):
        """ Clear the display """
        self.conn.write("      ")
        self.conn.write("|\x00")

    def draw_box(self, x1, y1, x2, y2):
        """ Draw a box from (x1, y1) to (x2, y2) """
        self.conn.write("|\x0f"+chr(x1)+chr(y1)+chr(x2)+chr(y2))

    def draw_line(self, x1, y1, x2, y2):
        """ Draw a line from (x1, y1) -> (x2, y2) """
        self.conn.write("|\x0c"+chr(x1)+chr(y1)+chr(x2)+chr(y2)+chr(1))

    def eye_outline(self):
        """ Draw the boxes for a standard eyeball """
        self.draw_box(self.LL, self.BOTTOM, self.LR, self.TOP)
        self.draw_box(self.RL, self.BOTTOM, self.RR, self.TOP)

    def eyebrows(self):
        """ Draw the basic eyebrows for the sad/normal face """
        self.draw_line(self.LL, self.TOP+5, self.LR, self.TOP+5)
        self.draw_line(self.RL, self.TOP+5, self.RR, self.TOP+5)

    def sad_face(self):
        """ Draws a sad face on the screen """
        self.clear_display()
        self.eye_outline()
        self.eyebrows()
        for x in range(1, 6):
            top = self.BOTTOM+(x*2)
            bottom = top-1
            self.draw_box(self.LL+4, bottom, self.LR-4, top)
            self.draw_box(self.RL+4, bottom, self.RR-4, top)

    def regular_face(self):
        """ Draw the standard face """
        self.clear_display()
        self.eye_outline()
        self.eyebrows()
        for x in range(1, 6):
            top = self.BOTTOM+15+(x*2)
            bottom = top-1
            self.draw_box(self.LL+4, bottom, self.LR-4, top)
            self.draw_box(self.RL+4, bottom, self.RR-4, top)

    def mad_face(self):
        """ Draw the angry face """
        self.clear_display()

        # mad eye outline
        self.draw_box(self.LL, self.BOTTOM, self.LR, self.TOP-10)
        self.draw_box(self.RL, self.BOTTOM, self.RR, self.TOP-10)

        # mad eyebrows
        self.draw_line(self.LR-15, self.TOP, self.LR+5, self.TOP-10)
        self.draw_line(self.RL-5, self.TOP-10, self.RL+15, self.TOP)

        for x in range(1, 6):
            top = self.BOTTOM+10+(x*2)
            bottom = top-1
            self.draw_box(self.LL+4, bottom, self.LR-4, top)
            self.draw_box(self.RL+4, bottom, self.RR-4, top)
