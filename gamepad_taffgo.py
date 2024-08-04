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

print('''

 ██████╗ ██╗  ██╗██╗    ███████╗ █████╗ ██╗      █████╗ ████████╗██╗ ██████╗  █████╗
██╔════╝ ██║ ██╔╝██║    ██╔════╝██╔══██╗██║     ██╔══██╗╚══██╔══╝██║██╔════╝ ██╔══██╗
██║  ███╗█████╔╝ ██║    ███████╗███████║██║     ███████║   ██║   ██║██║  ███╗███████║
██║   ██║██╔═██╗ ██║    ╚════██║██╔══██║██║     ██╔══██║   ██║   ██║██║   ██║██╔══██║
╚██████╔╝██║  ██╗██║    ███████║██║  ██║███████╗██║  ██║   ██║   ██║╚██████╔╝██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═╝
██████╗ ████████╗███████╗     ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗
██╔══██╗╚══██╔══╝╚══███╔╝    ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
██████╔╝   ██║     ███╔╝     ██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
██╔═══╝    ██║    ███╔╝      ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
██║        ██║   ███████╗    ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
╚═╝        ╚═╝   ╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝


''')

from colorama import Back
from colorama import Fore
from colorama import Style
from pyvisca import visca
from tkinter.simpledialog import askstring
import colorama as cr
import numpy
import pygame as pg
import time

cr.init()
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

    # If val == 0.004, then the joystick is at rest.
    JOYSTICK_REST_VAL = 0.000
    JOYSTICK_MIN_VAL = -1
    JOYSTICK_MAX_VAL = 1

    # PTZ blocking -- so that we won't overflow the serial.
    block_up = False
    block_down = False
    block_left = False
    block_right = False
    block_rest = False
    block_zoom_in = False
    block_zoom_out = False
    block_zoom_rest = False
    
    # Preset recalling blocking -- so that we won't overflow the serial.
    block_0 = False
    block_1 = False
    block_2 = False
    block_3 = False
    block_4 = False
    block_5 = False
    block_6 = False
    block_7 = False
    
    # Preset setting/configuration blocking -- so that we won't overflow the serial.
    block_set_0 = False
    block_set_1 = False
    block_set_2 = False
    block_set_3 = False
    block_set_4 = False
    block_set_5 = False
    block_set_6 = False
    block_set_7 = False

    done = False
    init_state = True
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
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Get count of joysticks.
        # joystick_count = pg.joystick.get_count()
        # print(f"Number of joysticks: {joystick_count}")

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            # Printing the joystick name
            name = joystick.get_name()
            if init_state:
                print()
                print(Back.YELLOW, Fore.BLACK, f"Joystick name: {name}")
                print(Style.RESET_ALL, Fore.GREEN)
                print("IF THE JOYSTICK NAME IS ANYTHING OTHER THAN 'Xbox 360 Controller'")
                print("UNPLUG THE GAMEPAD'S WIRELESS USB (DONGLE) AND PLUG IT IN AGAIN UNTIL IT IS DETECTED AS AN XBOX 360 GAMEPAD")
                print(Style.RESET_ALL)
                init_state = False

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

            # Recalling presets: right hand (presets 0-3)
            if _MENU == 0:
                
                if _BTN_Y == 1:
                    if not block_0:
                        print("Dispatched command: RECALLING PRESET 0")
                        cam.preset_recall(0)
                        block_0 = True
                elif _BTN_Y == 0:
                    if block_0:
                        print("Dispatched command: RECALLING PRESET 0 UNBLOCKING")
                        block_0 = False
                
                if _BTN_B == 1:
                    if not block_1:
                        print("Dispatched command: RECALLING PRESET 1")
                        cam.preset_recall(1)
                        block_1 = True
                elif _BTN_B == 0:
                    if block_1:
                        print("Dispatched command: RECALLING PRESET 1 UNBLOCKING")
                        block_1 = False
                
                if _BTN_A == 1:
                    if not block_2:
                        print("Dispatched command: RECALLING PRESET 2")
                        cam.preset_recall(2)
                        block_2 = True
                elif _BTN_A == 0:
                    if block_2:
                        print("Dispatched command: RECALLING PRESET 2 UNBLOCKING")
                        block_2 = False
                
                if _BTN_X == 1:
                    if not block_3:
                        print("Dispatched command: RECALLING PRESET 3")
                        cam.preset_recall(3)
                        block_3 = True
                elif _BTN_X == 0:
                    if block_3:
                        print("Dispatched command: RECALLING PRESET 3 UNBLOCKING")
                        block_3 = False

            # Recalling presets: left hand (presets 4-7)
            if _MENU == 0:
                
                if _ABS_HAT0 == (0, 1):
                    if not block_4:
                        print("Dispatched command: RECALLING PRESET 4")
                        cam.preset_recall(4)
                        block_4 = True
                
                if _ABS_HAT0 == (1, 0):
                    if not block_5:
                        print("Dispatched command: RECALLING PRESET 5")
                        cam.preset_recall(5)
                        block_5 = True
                        
                if _ABS_HAT0 == (0, -1):
                    if not block_6:
                        print("Dispatched command: RECALLING PRESET 6")
                        cam.preset_recall(6)
                        block_6 = True
                        
                if _ABS_HAT0 == (-1, 0):
                    if not block_7:
                        print("Dispatched command: RECALLING PRESET 7")
                        cam.preset_recall(7)
                        block_7 = True
                
                # Reset/ground state.
                if _ABS_HAT0 == (0, 0):
                    if block_4:
                        print("Dispatched command: RECALLING PRESET 4 UNBLOCKING")
                        block_4 = False
                    if block_5:
                        print("Dispatched command: RECALLING PRESET 5 UNBLOCKING")
                        block_5 = False
                    if block_6:
                        print("Dispatched command: RECALLING PRESET 6 UNBLOCKING")
                        block_6 = False
                    if block_7:
                        print("Dispatched command: RECALLING PRESET 7 UNBLOCKING")
                        block_7 = False

            # Setting/assigning presets: right hand (presets 0-3)
            if _MENU == 1:
                
                if _BTN_Y == 1:
                    if not block_set_0:
                        print("Dispatched command: OVERWRITING PRESET 0")
                        cam.preset_set(0)
                        block_set_0 = True
                elif _BTN_Y == 0:
                    if block_set_0:
                        print("Dispatched command: OVERWRITING PRESET 0 UNBLOCKING")
                        block_set_0 = False
                
                if _BTN_B == 1:
                    if not block_set_1:
                        print("Dispatched command: OVERWRITING PRESET 1")
                        cam.preset_set(1)
                        block_set_1 = True
                elif _BTN_B == 0:
                    if block_set_1:
                        print("Dispatched command: OVERWRITING PRESET 1 UNBLOCKING")
                        block_set_1 = False
                
                if _BTN_A == 1:
                    if not block_set_2:
                        print("Dispatched command: OVERWRITING PRESET 2")
                        cam.preset_set(2)
                        block_set_2 = True
                elif _BTN_A == 0:
                    if block_set_2:
                        print("Dispatched command: OVERWRITING PRESET 2 UNBLOCKING")
                        block_set_2 = False
                
                if _BTN_X == 1:
                    if not block_set_3:
                        print("Dispatched command: OVERWRITING PRESET 3")
                        cam.preset_set(3)
                        block_set_3 = True
                elif _BTN_X == 0:
                    if block_set_3:
                        print("Dispatched command: OVERWRITING PRESET 3 UNBLOCKING")
                        block_set_3 = False

            # Setting/assigning presets: left hand (presets 4-7)
            if _MENU == 1:
                if _ABS_HAT0 == (0, 1):
                    if not block_set_4:
                        print("Dispatched command: OVERWRITING PRESET 4")
                        cam.preset_set(4)
                        block_set_4 = True
                
                if _ABS_HAT0 == (1, 0):
                    if not block_set_5:
                        print("Dispatched command: OVERWRITING PRESET 5")
                        cam.preset_set(5)
                        block_set_5 = True
                
                if _ABS_HAT0 == (0, -1):
                    if not block_set_6:
                        print("Dispatched command: OVERWRITING PRESET 6")
                        cam.preset_set(6)
                        block_set_6 = True
                    
                if _ABS_HAT0 == (-1, 0):
                    if not block_set_7:
                        print("Dispatched command: OVERWRITING PRESET 7")
                        cam.preset_set(7)
                        block_set_7 = True
                
                # Reset/ground state.
                if _ABS_HAT0 == (0, 0):
                    if block_set_4:
                        print("Dispatched command: OVERWRITING PRESET 4 UNBLOCKING")
                        block_set_4 = False
                    if block_set_5:
                        print("Dispatched command: OVERWRITING PRESET 5 UNBLOCKING")
                        block_set_5 = False
                    if block_set_6:
                        print("Dispatched command: OVERWRITING PRESET 6 UNBLOCKING")
                        block_set_6 = False
                    if block_set_7:
                        print("Dispatched command: OVERWRITING PRESET 7 UNBLOCKING")
                        block_set_7 = False

            # Adjusting speed: pan-tilt movement
            # ---
            # Low speed
            if _L1 == 0 and _L2 == 0:
                MAX_MOVEMENT_SPEED = 1
            # Medium speed
            if _L1 == 1:
                MAX_MOVEMENT_SPEED = 7
            # Max speed
            if _L2 == 1:
                MAX_MOVEMENT_SPEED = 14
            
            # Adjusting speed: zoom movement
            # ---
            # Low speed
            if _R1 == 0 and _R2 == 0:
                MAX_ZOOM_SPEED = 1
            # Medium speed
            if _R1 == 1:
                MAX_ZOOM_SPEED = 3
            # Max speed
            if _R2 == 1:
                MAX_ZOOM_SPEED = 7

            # Movement actions (left-right panning)
            if _ABS_JOY_L_X != JOYSTICK_REST_VAL:
                val = _ABS_JOY_L_X
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    if not block_left:
                        print("Dispatched command: LEFT", f"-- Movement speed: {MAX_MOVEMENT_SPEED}")
                        i = get_speed(1.0, MAX_MOVEMENT_SPEED)
                        cam.left(round(i))
                        block_left = True
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    if not block_right:
                        print("Dispatched command: RIGHT", f"-- Movement speed: {MAX_MOVEMENT_SPEED}")
                        i = get_speed(1.0, MAX_MOVEMENT_SPEED)
                        cam.right(round(i))
                        block_right = True

            # Movement actions (up-down tilting)
            if _ABS_JOY_L_Y != 128:
                val = _ABS_JOY_L_Y
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    if not block_up:
                        print("Dispatched command: UP", f"-- Movement speed: {MAX_MOVEMENT_SPEED}")
                        i = get_speed(1.0, MAX_MOVEMENT_SPEED)
                        cam.up(round(i))
                        block_up = True
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    if not block_down:
                        print("Dispatched command: DOWN", f"-- Movement speed: {MAX_MOVEMENT_SPEED}")
                        i = get_speed(1.0, MAX_MOVEMENT_SPEED)
                        cam.down(round(i))
                        block_down = True

            # Center state (at-rest state of the pan and tilt)
            val_x = _ABS_JOY_L_X
            val_y = _ABS_JOY_L_Y
            if val_x == val_y and val_x == JOYSTICK_REST_VAL:
                if not block_rest:
                    print("Dispatched command: PAN-TILT REST")
                    cam.stop()
                    #time.sleep(MOVEMENT_STOP_DELAY)
                    block_rest = True
                    
                    # Reset the blocking states of other directions.
                    block_up = False
                    block_down = False
                    block_left = False
                    block_right = False
            else:
                if block_rest:
                    print("Dispatched command: PAN-TILT UNREST")
                    block_rest = False

            # Movement actions (zoom)
            if _ABS_JOY_R_Y != 128:
                val = _ABS_JOY_R_Y
                # Do the movement
                if val >= JOYSTICK_MIN_VAL and val < JOYSTICK_REST_VAL:
                    if not block_zoom_in:
                        print("Dispatched command: ZOOM IN", f"-- Zoom speed: {MAX_ZOOM_SPEED}")
                        i = get_speed(1.0, MAX_ZOOM_SPEED)
                        cam.zoom_in(round(i))
                        block_zoom_in = True
                elif val > JOYSTICK_REST_VAL and val <= JOYSTICK_MAX_VAL:
                    if not block_zoom_out:
                        print("Dispatched command: ZOOM OUT", f"-- Zoom speed: {MAX_ZOOM_SPEED}")
                        i = get_speed(1.0, MAX_ZOOM_SPEED)
                        cam.zoom_out(round(i))
                        block_zoom_out = True
            
            # Center state of the zoom. Used to stop the zoom command.
            val_ry = _ABS_JOY_R_Y
            if val_ry == JOYSTICK_REST_VAL:
                if not block_zoom_rest:
                    print("Dispatched command: ZOOM REST")
                    cam.zoom_stop()
                    block_zoom_rest = True
                    
                    # Reset the blocking states of the zoom.
                    block_zoom_in = False
                    block_zoom_out = False
            else:
                if block_zoom_rest:
                    print("Dispatched command: ZOOM UNREST")
                    block_zoom_rest = False

if __name__ == "__main__":
    # Prompt for the PTZ's USB serial port
    port = askstring(
        'Serial USB Input',
        'Please enter the VISCA PTZ\'s registered serial port\ne.g. Windows: "COM1", "COM2", etc.\ne.g. Linux: "/dev/ttyUSB0", "/dev/ttyUSB1", etc.',
        initialvalue='COM9'
    )

    # Fail-safe mechanism
    # To exit the program, press Ctrl+C or Ctrl+D from your terminal.
    while(True):
        try:
            main(port)
        except:
            # Wait for one second before continuing
            time.sleep(1)
            continue

    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pg.quit()
