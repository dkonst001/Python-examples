#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""
Test play sounds. (June 3, 2015)

Piece of SimpleGUICS2Pygame.
https://bitbucket.org/OPiMedia/simpleguics2pygame

GPLv3 --- Copyright (C) 2015 Olivier Pirson
http://www.opimedia.be/
"""

import time

try:
    import simplegui

    SIMPLEGUICS2PYGAME = False
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    SIMPLEGUICS2PYGAME = True


TEST = 'test sound'

sound_jump_ogg = simplegui.load_sound('eatpellet.ogg')

if SIMPLEGUICS2PYGAME:
 #   local_sound_chirp_wav = simplegui._load_local_sound('_snd/chirp_1s.wav')
 local_sound_chirp_wav = simplegui._load_local_sound('eatpellet.ogg')
 


def wait(seconds):
    """
    Wait during `seconds` seconds.

    :param seconds: (int or float) >= 0
    """
    assert isinstance(seconds, int) or isinstance(seconds, float), \
        type(seconds)

    start = time.time()
    while time.time() - start < seconds:
        pass


# Main
wait(1)

print('Play "jump.ogg"')
sound_jump_ogg.play()
wait(1)

print (SIMPLEGUICS2PYGAME)

if SIMPLEGUICS2PYGAME:
    print('Play local "chirp_1s.wav"')
    local_sound_chirp_wav.play()
    wait(local_sound_chirp_wav._get_length())
