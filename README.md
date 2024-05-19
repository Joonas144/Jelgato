## Background

A goofy python "driver" with a goofy arduino that makes for a goofy custom keyboard with different action layouts


Unfortunately I've lost the PCB design for this project, However the project was heavily inspired from
[this project](https://www.partsnotincluded.com/diy-stream-deck-mini-macro-keyboard/)
where both the 3d model and arduino source code originated. However the arduino source code was modified to fit my specific needs, and the method for handling arduino inputs into real actions is completely different, using TKinter for a layout-based design turning an 8-action macro keyboard into one with theoretically infinite actions by segmenting each set of actions in it's own layout - which can further contain new layouts et cetera.

The current configurations in overlays.py contain 1 base overlay and 6 custom overlays, for a total of 44 possible actions. 

Actions can be added to the action.py file

## configuration
The .env file expects

```.env
# Twitch
token = [twitch token]
channel = [twitch channel name]

# OBS
host = [obs ip address]
port = [obs port]
password = [obs password]
```