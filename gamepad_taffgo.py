# -*- coding: utf-8 -*-
# 
# Control the VISCA PTZ camera using a TaffGO XBOX 360 gamepad
# By Samarthya Lykamanuella (groaking)
# Licensed under GPL-3.0
# 
# For TaffGO XBOX 360 Joystick types
# ---
# Gamepad event listener using Python
# -> SOURCE: https://github.com/zeth/inputs/blob/master/examples/gamepad_example.py
# Multithreading tips for gamepads
# -> SOURCE: https://gist.github.com/effedebe/6cae2a5849923fb373ab749594b9ed50
# PyGame joystick control example
# -> SOURCE: https://www.pygame.org/docs/ref/joystick.html
# ---
# Controller constants can be found in:
# https://www.pygame.org/docs/ref/sdl2_controller.html#pygame._sdl2.controller.Controller.get_button

from pyvisca import visca
from tkinter.simpledialog import askstring
import numpy
import pygame as pg
import time

pg.init()

def get_speed(val, max_speed):
    '''
    Calculate the absolute speed according to the analog joystick's input voltage.
    If val == 0.004, then the joystick is at rest.
    The range of value (val) is within -1 and 1.
    '''
    i = numpy.abs( val )
    return float( max_speed * float(i) )

def main(port='COM7'):
    # This dict can be left as-is, since pygame will generate a
    # pg.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

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

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("Quitting.")
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pg.JOYBUTTONDOWN:
                # print("Joystick button pressed.")
                pass

            if event.type == pg.JOYBUTTONUP:
                # print("Joystick button released.")
                pass

            # Handle hotplugging
            if event.type == pg.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pg.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
        
        # Get count of joysticks.
        # joystick_count = pg.joystick.get_count()
        # print(f"Number of joysticks: {joystick_count}")

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()
            
            # Category of binary respond values
            _L1 = joystick.get_button(4)
            _L2 = 1 if int(joystick.get_axis(4)) == 0 else 0
            _R1 = joystick.get_button(5)
            _R2 = 1 if int(joystick.get_axis(5)) == 0 else 0
            _MENU = joystick.get_button(6)
            _START = joystick.get_button(7)
            _BTN_JOY_L = joystick.get_button(8)
            _BTN_JOY_R = joystick.get_button(9)
            _BTN_A = joystick.get_button(pg.CONTROLLER_BUTTON_A)
            _BTN_B = joystick.get_button(pg.CONTROLLER_BUTTON_B)
            _BTN_X = joystick.get_button(pg.CONTROLLER_BUTTON_X)
            _BTN_Y = joystick.get_button(pg.CONTROLLER_BUTTON_Y)
            
            # Category of analog values
            _ABS_HAT0 = joystick.get_hat(0)
            _ABS_JOY_L_X = float( str(f"{ ('%.3f' % joystick.get_axis(0)) }") )
            _ABS_JOY_L_Y = float( str(f"{ ('%.3f' % joystick.get_axis(1)) }") )
            _ABS_JOY_R_X = float( str(f"{ ('%.3f' % joystick.get_axis(2)) }") )
            _ABS_JOY_R_Y = float( str(f"{ ('%.3f' % joystick.get_axis(3)) }") )
            
            # DEBUG:
            # (Please comment out this section after use.)
            # print(_L1, _L2, _R1, _R2, _MENU, _START, _BTN_JOY_L, _BTN_JOY_R, _BTN_A, _BTN_B, _BTN_X, _BTN_Y, _ABS_HAT0, _ABS_JOY_L_X, _ABS_JOY_L_Y, _ABS_JOY_R_X, _ABS_JOY_R_Y)

            # Recalling presets: left hand
            if _ABS_HAT0 == (0, 1) and _MENU == 0:
                cam.preset_recall(4)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (1, 0) and _MENU == 0:
                cam.preset_recall(5)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (0, -1) and _MENU == 0:
                cam.preset_recall(6)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (-1, 0) and _MENU == 0:
                cam.preset_recall(7)
                _ABS_HAT0 = (0, 0)  # --- blocking
            
            # Recalling presets: right hand
            if _BTN_Y == 1 and _MENU == 0:
                cam.preset_recall(0)
                _BTN_Y = 0  # --- blocking
            if _BTN_B == 1 and _MENU == 0:
                cam.preset_recall(1)
                _BTN_B = 0  # --- blocking
            if _BTN_A == 1 and _MENU == 0:
                cam.preset_recall(2)
                _BTN_A = 0  # --- blocking
            if _BTN_X == 1 and _MENU == 0:
                cam.preset_recall(3)
                _BTN_X = 0  # --- blocking
            
            # Setting/assigning presets: left hand
            if _ABS_HAT0 == (0, 1) and _MENU == 1:
                cam.preset_set(4)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (1, 0) and _MENU == 1:
                cam.preset_set(5)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (0, -1) and _MENU == 1:
                cam.preset_set(6)
                _ABS_HAT0 = (0, 0)  # --- blocking
            if _ABS_HAT0 == (-1, 0) and _MENU == 1:
                cam.preset_set(7)
                _ABS_HAT0 = (0, 0)  # --- blocking
            
            # Setting/assigning presets: right hand
            if _BTN_Y == 1 and _MENU == 1:
                cam.preset_set(0)
                _BTN_Y = 0  # --- blocking
            if _BTN_B == 1 and _MENU == 1:
                cam.preset_set(1)
                _BTN_B = 0  # --- blocking
            if _BTN_A == 1 and _MENU == 1:
                cam.preset_set(2)
                _BTN_A = 0  # --- blocking
            if _BTN_X == 1 and _MENU == 1:
                cam.preset_set(3)
                _BTN_X = 0  # --- blocking
            
            # Adjusting speed
            # ---
            # Low speed
            if _R1 == 0 and _R2 == 0:
                MOVEMENT_STOP_DELAY = 0.0001
                MOVEMENT_STOP_DELAY_LONG = 0.05
                MAX_ZOOM_SPEED = 1
                MAX_MOVEMENT_SPEED = 1
            # Medium speed
            if _R1 == 1:
                MOVEMENT_STOP_DELAY = 0.05
                MOVEMENT_STOP_DELAY_LONG = 0.1
                MAX_ZOOM_SPEED = 4
                MAX_MOVEMENT_SPEED = 3
            # Max speed
            if _R2 == 1:
                MOVEMENT_STOP_DELAY = 0.3
                MOVEMENT_STOP_DELAY_LONG = 0.5
                MAX_ZOOM_SPEED = 7
                MAX_MOVEMENT_SPEED = 14
            
            # Movement actions (left-right panning)
            if _ABS_JOY_L_X != JOYSTICK_REST_VAL:
                val = _ABS_JOY_L_X
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
            if _ABS_JOY_L_Y != 128:
                val = _ABS_JOY_L_Y
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
            if _ABS_JOY_R_Y != 128:
                val = _ABS_JOY_R_Y
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
            if _BTN_JOY_L == 1:
                cam.home()
                _BTN_JOY_L = 0  # --- blocking
            # Perform autofocus
            if _BTN_JOY_R == 1:
                cam.autofocus_sens_low()
                _BTN_JOY_R = 0  # --- blocking
            
            # Prevent too fast a movement
            time.sleep(MOVEMENT_REDUNDANT_DELAY)

            '''
            print(f"Joystick {jid}")

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            print(f"Joystick name: {name}")

            guid = joystick.get_guid()
            print(f"GUID: {guid}")

            power_level = joystick.get_power_level()
            print(f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            print(f"Number of axes: {axes}")

            for i in range(axes):
                axis = joystick.get_axis(i)
                print(f"Axis {i} value: {axis:>6.3f}")

            buttons = joystick.get_numbuttons()
            print(f"Number of buttons: {buttons}")

            for i in range(buttons):
                button = joystick.get_button(i)
                print(f"Button {i:>2} value: {button}")

            hats = joystick.get_numhats()
            print(f"Number of hats: {hats}")

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                print(f"Hat {i} value: {str(hat)}")
            
            time.sleep(0.1)
            '''

if __name__ == "__main__":
    # Prompt for the PTZ's USB serial port
    port = askstring(
        'Serial USB Input',
        'Please enter the VISCA PTZ\'s registered serial port\ne.g. Windows: "COM1", "COM2", etc.\ne.g. Linux: "/dev/ttyUSB0", "/dev/ttyUSB1", etc.',
        initialvalue='COM9'
    )

    # Fail-safe mechanism
    # To exit the program, press Ctrl+C or Ctrl+D from your terminal.
    while(true):
        try:
            main(port)
        except:
            # Wait for one second before continuing
            time.sleep(1)
            continue
    
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pg.quit()
