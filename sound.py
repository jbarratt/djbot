""" Sound handling functions of DJBot """

import os
import sys
import glob
import random
import subprocess


class Sound(object):

    """ Handles dispatching sounds to the robot speakers """

    def __init__(self):
        pathname = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.audio_files = glob.glob(pathname + '/audio/*.wav')

    def handle_command(self, cmd):
        """ Parses and handles command """

        if cmd.startswith("say "):
            self.say(cmd[4:])
        elif cmd == "djbeat":
            self.random_beat()
        else:
            print "Unknown command: '{}'".format(cmd)

    def random_beat(self):
        """ Plays a random beat from the disk array """
        wav = random.choice(self.audio_files)
        subprocess.call(['aplay', wav])

    @staticmethod
    def say(text):
        """ Says the given phrase using flite """
        subprocess.call(['flite', '-t', text])
