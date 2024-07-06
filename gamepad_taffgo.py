# -*- coding: utf-8 -*-
# 
# Control the VISCA PTZ camera using a TaffGO XBOX 360 gmepad
# By Samarthya Lykamanuella (groaking)
# Licensed under GPL-3.0
# 
# For Microntek USB Joystick types
# ---
# Gamepad event listener using Python
# -> SOURCE: https://github.com/zeth/inputs/blob/master/examples/gamepad_example.py
# Multithreading tips for gamepads
# -> SOURCE: https://gist.github.com/effedebe/6cae2a5849923fb373ab749594b9ed50

# SOURCE: https://www.pygame.org/docs/ref/joystick.html
import pygame
pygame.init()

from pyvisca import visca
from threading import Thread
from tkinter import messagebox
from tkinter.simpledialog import askstring
import numpy
import sys
import time

class GPad(Thread):
    ''' This class listens to the gamepad event without blocking the main code (using multithreading). '''
    
    def __init__(self):
        Thread.__init__(self)
        self.ABS_HAT0 = (0, 0)
        self.ABS_JOY_R_Y = 128
        self.ABS_JOY_L_X = 128
        self.ABS_JOY_L_Y = 128
        self.ABS_JOY_R_X = 128
        self.BTN_JOY_L = 0
        self.BTN_JOY_R = 0
        self.BTN_B = 0
        self.BTN_A = 0
        self.L1 = 0
        self.L2 = 0
        self.MENU = 0
        self.R1 = 0
        self.R2 = 0
        self.BTN_X = 0
        self.START = 0
        self.BTN_Y = 0
    
    def run(self):

        # This dict can be left as-is, since pygame will generate a
        # pygame.JOYDEVICEADDED event for every joystick connected
        # at the start of the program.
        joysticks = {}
        
        try:
            while True:
                # Event processing step.
                # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
                # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
                for event in pygame.event.get():
                    # Handle hotplugging
                    if event.type == pygame.JOYDEVICEADDED:
                        # This event will be generated when the program starts for every
                        # joystick, filling up the list without needing to create them manually.
                        joy = pygame.joystick.Joystick(event.device_index)
                        joysticks[joy.get_instance_id()] = joy
                        print(f"Joystick {joy.get_instance_id()} connected")\
                
                for joystick in joysticks.values():
                    
                    # Category of binary respond values
                    self.L1 = joystick.get_button(4)
                    self.L2 = 1 if int(joystick.get_axis(2)) == 0 else 0
                    self.R1 = joystick.get_button(5)
                    self.R2 = 1 if int(joystick.get_axis(5)) == 0 else 0
                    self.MENU = joystick.get_button(6)
                    self.START = joystick.get_button(7)
                    self.BTN_JOY_L = joystick.get_button(9)
                    self.BTN_JOY_R = joystick.get_button(10)
                    self.BTN_B = joystick.get_button(1)
                    self.BTN_A = joystick.get_button(0)
                    self.BTN_X = joystick.get_button(2)
                    self.BTN_Y = joystick.get_button(3)
                    
                    # DEBUG:
                    # (Please comment out this section after use.)
                    # print(self.BTN_A, self.BTN_B, self.BTN_X, self.BTN_Y, self.L2, self.R2, int(joystick.get_axis(2)), int(joystick.get_axis(5)))
                    
                    # Category of analog values
                    self.ABS_HAT0 = joystick.get_hat(0)
                    self.ABS_JOY_L_X = float( str(f"{ ('%.3f' % joystick.get_axis(0)) }") )
                    self.ABS_JOY_L_Y = float( str(f"{ ('%.3f' % joystick.get_axis(1)) }") )
                    self.ABS_JOY_R_X = float( str(f"{ ('%.3f' % joystick.get_axis(3)) }") )
                    self.ABS_JOY_R_Y = float( str(f"{ ('%.3f' % joystick.get_axis(4)) }") )
        except Exception as e:
            messagebox.showerror('Unknown gamepad error', f'Unknown error is detected. Please check your gamepad console connection: {e}')
            sys.exit()

def get_speed(val, max_speed):
    '''
    Calculate the absolute speed according to the analog joystick's input voltage.
    If val == 0.004, then the joystick is at rest.
    The range of value (val) is within -1 and 1.
    '''
    i = numpy.abs( val )
    return float( max_speed * float(i) )

def main(port='/dev/ttyUSB0'):
    ''' Actually controls the VISCA PTZ camera using joystick/gamepad. '''
    
    try:
        # Establish the non-blocking multithreading for analog input
        game_pad = GPad()
        game_pad.start()
        
        # Establish and initialize the VISCA object
        # (Change the port value according to your system's availability.)
        cam = visca.PTZ(port)
        
        # Set the max speed (pixel per 100 ms) of the X-Y joystick movement
        MAX_MOVEMENT_SPEED = 7
        MAX_ZOOM_SPEED = 7
        
        # Set the delay time for movement speed
        MOVEMENT_REDUNDANT_DELAY = 0.01
        
        # Set the delay time after each movement, before stopping any continuous command
        MOVEMENT_STOP_DELAY = 0.0005
        MOVEMENT_STOP_DELAY_LONG = 0.5
        
        # If val == 0.004, then the joystick is at rest.
        JOYSTICK_REST_VAL = 0.000
        JOYSTICK_MIN_VAL = -1
        JOYSTICK_MAX_VAL = 1
        
        # Fail-safe error catching with infinite loop
        while True:
            
            # Recalling presets: left hand
            if game_pad.ABS_HAT0 == (0, 1) and game_pad.MENU == 0:
                cam.preset_recall(4)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (1, 0) and game_pad.MENU == 0:
                cam.preset_recall(5)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (0, -1) and game_pad.MENU == 0:
                cam.preset_recall(6)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (-1, 0) and game_pad.MENU == 0:
                cam.preset_recall(7)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            
            # Recalling presets: right hand
            if game_pad.BTN_Y == 1 and game_pad.MENU == 0:
                cam.preset_recall(0)
                game_pad.BTN_Y = 0  # --- blocking
            if game_pad.BTN_B == 1 and game_pad.MENU == 0:
                cam.preset_recall(1)
                game_pad.BTN_B = 0  # --- blocking
            if game_pad.BTN_A == 1 and game_pad.MENU == 0:
                cam.preset_recall(2)
                game_pad.BTN_A = 0  # --- blocking
            if game_pad.BTN_X == 1 and game_pad.MENU == 0:
                cam.preset_recall(3)
                game_pad.BTN_X = 0  # --- blocking
            
            # Setting/assigning presets: left hand
            if game_pad.ABS_HAT0 == (0, 1) and game_pad.MENU == 1:
                cam.preset_set(4)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (1, 0) and game_pad.MENU == 1:
                cam.preset_set(5)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (0, -1) and game_pad.MENU == 1:
                cam.preset_set(6)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            if game_pad.ABS_HAT0 == (-1, 0) and game_pad.MENU == 1:
                cam.preset_set(7)
                game_pad.ABS_HAT0 = (0, 0)  # --- blocking
            
            # Setting/assigning presets: right hand
            if game_pad.BTN_Y == 1 and game_pad.MENU == 1:
                cam.preset_set(0)
                game_pad.BTN_Y = 0  # --- blocking
            if game_pad.BTN_B == 1 and game_pad.MENU == 1:
                cam.preset_set(1)
                game_pad.BTN_B = 0  # --- blocking
            if game_pad.BTN_A == 1 and game_pad.MENU == 1:
                cam.preset_set(2)
                game_pad.BTN_A = 0  # --- blocking
            if game_pad.BTN_X == 1 and game_pad.MENU == 1:
                cam.preset_set(3)
                game_pad.BTN_X = 0  # --- blocking
            
            # Adjusting speed
            # ---
            # Low speed
            if game_pad.R1 == 0 and game_pad.R2 == 0:
                MOVEMENT_STOP_DELAY = 0.0001
                MOVEMENT_STOP_DELAY_LONG = 0.05
                MAX_ZOOM_SPEED = 1
                MAX_MOVEMENT_SPEED = 1
            # Medium speed
            if game_pad.R1 == 1:
                MOVEMENT_STOP_DELAY = 0.05
                MOVEMENT_STOP_DELAY_LONG = 0.1
                MAX_ZOOM_SPEED = 4
                MAX_MOVEMENT_SPEED = 3
            # Max speed
            if game_pad.R2 == 1:
                MOVEMENT_STOP_DELAY = 0.3
                MOVEMENT_STOP_DELAY_LONG = 0.5
                MAX_ZOOM_SPEED = 7
                MAX_MOVEMENT_SPEED = 14
            
            # Movement actions (left-right panning)
            if game_pad.ABS_JOY_L_X != JOYSTICK_REST_VAL:
                val = game_pad.ABS_JOY_L_X
                i = get_speed(val, MAX_MOVEMENT_SPEED)
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    cam.left(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY)
                    cam.stop()
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    cam.right(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY)
                    cam.stop()
            
            # Movement actions (up-down tilting)
            if game_pad.ABS_JOY_L_Y != 128:
                val = game_pad.ABS_JOY_L_Y
                i = get_speed(val, MAX_MOVEMENT_SPEED)
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    cam.up(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY)
                    cam.stop()
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    cam.down(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY)
                    cam.stop()
            
            # Movement actions (zoom)
            if game_pad.ABS_JOY_R_Y != 128:
                val = game_pad.ABS_JOY_R_Y
                i = get_speed(val, MAX_ZOOM_SPEED)
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    cam.zoom_in(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY_LONG)
                    cam.zoom_stop()
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    cam.zoom_out(round(i))
                    time.sleep(MOVEMENT_STOP_DELAY_LONG)
                    cam.zoom_stop()
            
            # Analog center button press actions
            # ---
            # Move camera to home/default position
            if game_pad.BTN_JOY_L == 1:
                cam.home()
                game_pad.BTN_JOY_L = 0  # --- blocking
            # Perform autofocus
            if game_pad.BTN_JOY_R == 1:
                cam.autofocus_sens_low()
                game_pad.BTN_JOY_R = 0  # --- blocking
            
            # Prevent too fast a movement
            time.sleep(MOVEMENT_REDUNDANT_DELAY)
        
        # Wait until the end of the game_pad thread
        game_pad.joint()
    
    except Exception as e:
        messagebox.showerror('Unknown error', f'Unknown error is detected. Please check your PTZ connection: {e}')
        sys.exit()
    
if __name__ == "__main__":
    # Prompt for the PTZ's USB serial port
    port = askstring(
        'Serial USB Input',
        'Please enter the VISCA PTZ\'s registered serial port\ne.g. Windows: "COM1", "COM2", etc.\ne.g. Linux: "/dev/ttyUSB0", "/dev/ttyUSB1", etc.'
    )
    
    main(port)
