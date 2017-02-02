""" Handle driving the motors via a simplified interface """

import time
from robot import Robot


class Motor(object):

    """ Gives a simplified interface to a pair of motors """

    def __init__(self):

        self.robot = Robot()
        self.speed = 150
        self.last_cmd = "stop"

    def handle_command(self, cmd):
        """ Handle a string command and drive motors accordingly.
            If a speed change comes in, the previous command is re-run
            with the new speed value.
        """

        if cmd == "left":
            self.robot.left(self.speed)
            self.last_cmd = cmd
        elif cmd == "right":
            self.robot.right(self.speed)
            self.last_cmd = cmd
        elif cmd == "forward":
            self.robot.forward(self.speed)
            self.last_cmd = cmd
        elif cmd == "backward":
            self.robot.backward(self.speed)
            self.last_cmd = cmd
        elif cmd == "stop":
            self.robot.stop()
            self.last_cmd = cmd
        elif cmd == "faster":
            self.speed = min(250, self.speed + 20)
            self.handle_command(self.last_cmd)
        elif cmd == "slower":
            self.speed = max(0, self.speed - 20)
            self.handle_command(self.last_cmd)
        elif cmd.startswith("sleep"):
            try:
                seconds = float(cmd[6:])
                time.sleep(seconds)
            except ValueError:
                print "unable to get sleep time from {}".format(cmd)
