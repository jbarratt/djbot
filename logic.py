""" Main game logic, takes inputs, decides on outputs """

import time
import random
import subprocess


class Brain(object):

    """ The brain does the thinkin' """

    def __init__(self, motor_q, screen_q, sound_q):
        self.emotions = ['mad', 'sad', 'regular']
        self.utterances = {'mad': "I'm so mad",
                           'sad': "I am sad. Wah.",
                           'regular': "I feel just fine"}
        self.emotion = 'regular'
        self.motor = motor_q
        self.screen = screen_q
        self.sound = sound_q
        self.game = None
        self.b_presses = []

    def startup(self):
        """ What to do on first boot """
        self.screen.put("regular")
        self.sound.put("say D J Bot")
        self.sound.put("djbeat")
        self.sound.put("say Select plays a game")
        self.sound.put("say Start changes my mood")

    def handle_command(self, cmd):
        """ Handle gamepad events """

        if self.game is not None and self.game.complete:
            self.game = None

        # The first block of commands are all about
        # navigation. They happen at all times, regardless
        # of game mode.
        if cmd == "center":
            self.motor.put("stop")
        elif cmd == "left":
            self.motor.put("right")
        elif cmd == "right":
            self.motor.put("left")
        elif cmd == "up":
            self.motor.put("forward")
        elif cmd == "down":
            self.motor.put("backward")
        elif cmd == "l_shoulder":
            self.motor.put("slower")
        elif cmd == "r_shoulder":
            self.motor.put("faster")
        else:
            if not self.game:
                self.main_command(cmd)
            else:
                self.game.handle_command(cmd)

    def main_command(self, cmd):
        """ Handle gamepad keys in the non-game mode """

        if cmd == "start":
            # choose any other emotion than the one we have now
            self.emotion = random.choice([x for x in self.emotions
                                          if x != self.emotion])
            self.screen.put(self.emotion)
            self.sound.put("say {}".format(self.utterances[self.emotion]))
            self.sound.put("djbeat")
        elif cmd == "select":
            self.game = RockPaperScissors(self.motor, self.screen, self.sound)
            self.game.startup()
        elif cmd == "b":
            self.handle_b_press()

    def handle_b_press(self):
        """ Store a 'b' press. If we get 3 in rapid fire, shut the
            computer down """
        now = time.time()
        self.b_presses.append(now)
        # remove any list items > 2 seconds old
        self.b_presses = [x for x in self.b_presses if now - x < 2.0]
        if len(self.b_presses) >= 3:
            self.sound.put("say you pressed B 3 times. Powering down.")
            subprocess.call("sudo shutdown now -h", shell=True)


class RockPaperScissors(object):

    """ Implements basic Rock Paper Scissors """

    WEAPONS = {
        'y': 'paper',
        'x': 'scissors',
        'a': 'rock'
    }

    BEATS = {
        'paper': 'rock',
        'scissors': 'paper',
        'rock': 'scissors'
    }

    def __init__(self, motor_q, screen_q, sound_q):
        self.motor = motor_q
        self.screen = screen_q
        self.sound = sound_q
        self.complete = False
        self.robot_wins = 0
        self.player_wins = 0

    def startup(self):
        """ run this when the game begins """
        self.sound.put("say Welcome to DJ Bot Rock Paper Scissors")
        self.sound.put("say Press Select to Quit")
        self.sound.put("say EX is Rock, WHY is Paper, AEE is Scissors")
        self.sound.put("say Best of 3. Press a key.")

    def handle_command(self, cmd):
        """ Handles an RPS command """
        if cmd == "select":
            self.sound.put("say thank you for playing")
            self.complete = True
        elif cmd in self.WEAPONS:
            mine = random.choice(self.BEATS.keys())
            player = self.WEAPONS[cmd]
            if mine == player:
                self.sound.put("say we both had {}, do over!".format(mine))
            elif self.BEATS[player] == mine:
                self.sound.put(
                    "say {} beats {}, you get a point".format(
                        player,
                        mine))
                self.screen.put("blink")
                self.player_wins += 1
            else:
                self.sound.put(
                    "say My {} beats your {}, I win I win I win".format(
                        mine,
                        player))
                self.sound.put("djbeat")
                self.motor.put("forward")
                self.motor.put("sleep 0.1")
                self.motor.put("backward")
                self.motor.put("sleep 0.1")
                self.motor.put("stop")
                self.robot_wins += 1
        if self.player_wins >= 2:
            self.sound.put("say You won! Congratulations!")
            self.complete = True
        elif self.robot_wins >= 2:
            self.sound.put("say I won! 2 out of 3!")
            self.sound.put("djbeat")
            self.complete = True
