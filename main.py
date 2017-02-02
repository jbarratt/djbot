#!/usr/bin/env python

from Queue import Queue
from threading import Thread
import signal
import sys
from sound import Sound
from gamepad import Gamepad
from motor import Motor
from screen import Face
from logic import Brain


def motor(q):
    """ motor takes a Queue as input and runs forever running commands. """
    print "motor starting up"
    m = Motor()
    while True:
        cmd = q.get()
        m.handle_command(cmd)
        q.task_done()


def screen(q):
    """ screen takes a Queue and runs forever running commands. """
    print "screen starting up"
    face = Face("/dev/ttyAMA0")
    while True:
        cmd = q.get()
        face.handle_command(cmd)
        q.task_done()


def sound(q):
    """ sound takes a Queue and runs forever running commands. """
    print "sound starting up"
    snd = Sound()
    while True:
        cmd = q.get()
        print "sound: {}".format(cmd)
        snd.handle_command(cmd)
        q.task_done()


def gamepad(q):
    """ gamepad takes a Queue and puts all events on it """
    print "gamepad starting up"
    gp = Gamepad()
    for event in gp.get_events():
        print "gamepad: read {} and queued".format(event)
        q.put(event)


def brain(gamepad_q, motor_q, screen_q, sound_q):
    """ main game loop. Takes input from gamepad and sends commands
        to device queues per output. """

    print "starting main game loop"

    djbot = Brain(motor_q, screen_q, sound_q)
    djbot.startup()

    while True:
        print "waiting on gamepad:"
        cmd = gamepad_q.get()
        djbot.handle_command(cmd)
        gamepad_q.task_done()


def handle_sigint():
    """ Gracefully exit """
    sys.exit(1)


def main():
    """ Set up all the workers and queues, then kick off
        the main loop. """

    gamepad_q = Queue(maxsize=0)
    w = Thread(target=gamepad, args=(gamepad_q,))
    w.setDaemon(True)
    w.start()

    motor_q = Queue(maxsize=0)
    w = Thread(target=motor, args=(motor_q,))
    w.setDaemon(True)
    w.start()

    screen_q = Queue(maxsize=0)
    w = Thread(target=screen, args=(screen_q,))
    w.setDaemon(True)
    w.start()

    sound_q = Queue(maxsize=0)
    w = Thread(target=sound, args=(sound_q,))
    w.setDaemon(True)
    w.start()

    signal.signal(signal.SIGINT, handle_sigint)

    brain(gamepad_q, motor_q, screen_q, sound_q)


if __name__ == '__main__':
    main()
