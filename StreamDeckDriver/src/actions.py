from dotenv import load_dotenv
from obswebsocket import obsws, requests, exceptions, events
from os import environ as config
from pynput.keyboard import Controller
from pywitch import PyWitchTMI
import threading

# Env files
load_dotenv()

# Keyboard
keyboard = Controller()

# Twitch
tmi = PyWitchTMI(
    channel=config.get("channel"),
    token=config.get("token"),
    verbose=True
)
obs = obs = obsws(config.get("host"),
                  config.get("port"),
                  config.get("password"))


def obsConnection(*args):
    try:
        obs.connect()
    except exceptions.ConnectionFailure as Error:
        print("Obs is sleeping... We'll try to connect again after a minute")

        timer = threading.Timer(10.0, obsConnection)
        timer.start()


def on_exit(message):
    obs.disconnect()
    obs.connect()


obs.register(on_exit, events.Exiting)


def setupActions():
    obsConnection()


def streamEmergency():
    sendTwitchMessage('/emoteonly', '/clear', '/commercial 60', 'It seems we\'re getting hate-raided, stay tuned :D')


def sendTwitchMessage(*args):
    tmi.start()
    for msg in args:
        tmi.send(msg)
    tmi.stop()


def obsScene(name):
    obs.connect()
    obs.call(requests.SetCurrentScene(name))


def obsMute():
    isCurrentlyMuted = obs.call(requests.GetMute("Microphone")).datain.get("muted")
    obs.call(requests.SetMute("Microphone", not isCurrentlyMuted))
    pass


def write(string, wasJustPressed):
    print(str(string) + " was just pressed" if wasJustPressed else " was just released")
    if wasJustPressed:
        keyboard.press(string)

    if not wasJustPressed:
        keyboard.release(string)


setupActions()
