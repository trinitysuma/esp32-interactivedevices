import serial
import pygame
import time

pygame.mixer.init()

# music
sounds = {
    "yelena": pygame.mixer.Sound("audio/yelena.mp3"),
    "bucky": pygame.mixer.Sound("audio/bucky.mp3"),
    "redguardian": pygame.mixer.Sound("audio/redguardian.mp3"),
    "ghost": pygame.mixer.Sound("audio/ghost.mp3"),
    "walker": pygame.mixer.Sound("audio/walker.mp3"),
    "team": pygame.mixer.Sound("audio/team.mp3"),
    "team_alt": pygame.mixer.Sound("audio/avengers.mp3")  # alternate song for double tap
}

# Track playing state
playing = {key: False for key in sounds}

# Serial port
ser = serial.Serial('COM5', 115200)

# Touch range for volume mapping
MIN_TOUCH = 10
MAX_TOUCH = 60

# allows volume to be determined by touch
# higher pressure = greater volume
def map_volume(val):
    inverted = MAX_TOUCH - (val - MIN_TOUCH)
    vol = (inverted - MIN_TOUCH) / (MAX_TOUCH - MIN_TOUCH)
    vol = max(0.0, min(1.0, vol))
    vol = vol ** 3  # nonlinear scaling for stronger effect
    return vol

# Double-tap tracking for 'team'
team_last_touch_time = 0
double_tap_threshold = 0.4
team_is_touching = False  # tracks if finger is currently on pad
team_current_song = "team"


while True:
    line = ser.readline().decode().strip() # gets name:pressure

    # Handle pressure updates
    if ":" in line:
        pad, val_str = line.split(":", 1) # separates member and pressure

        try:
            val = int(val_str.strip())

            if pad == "team":
                # Detect NEW touch (not hold)
                if not team_is_touching: # not already touching
                    team_is_touching = True  # now we are!

                    now = time.time()

                    if now - team_last_touch_time < double_tap_threshold:
                        # double tap (only triggers once per touch)
                        team_current_song = "team_alt" if team_current_song == "team" else "team"

                        # stop both to reset cleanly
                        sounds["team"].stop()
                        sounds["team_alt"].stop()
                        playing["team"] = False
                        playing["team_alt"] = False

                        print("Double tap → switched to", team_current_song)

                    team_last_touch_time = now

                pad_to_play = team_current_song

            else:
                pad_to_play = pad 

            # Play + volume
            if pad_to_play in sounds:
                if not playing[pad_to_play]:
                    sounds[pad_to_play].play(-1)
                    playing[pad_to_play] = True

                sounds[pad_to_play].set_volume(map_volume(val))

        except:
            pass

    elif line.startswith("STOP_"): # press released 
        pad = line[5:]

        if pad == "team":
            team_is_touching = False  # allow next tap
            pad_to_stop = team_current_song
        else:
            pad_to_stop = pad

        if pad_to_stop in sounds and playing[pad_to_stop]:
            sounds[pad_to_stop].stop()
            playing[pad_to_stop] = False
