from src import actions
from pynput.keyboard import Key


def OverlaySetter():  # gets replaced
    pass


def NewOverlay(overlay):
    print("New overlay: " + type(overlay).__name__)
    OverlaySetter(overlay)
    pass


class AbstractOverlay:
    def __init__(self):
        self.pressActions = None
        self.releaseActions = None
        self.texts = None

    def setActions(self, texts, pressActions, releaseActions):
        self.texts = texts
        self.pressActions = pressActions
        self.releaseActions = releaseActions

    def getActions(self):
        return self.texts, self.pressActions, self.releaseActions


BaseOverlay = AbstractOverlay()
SceneOverlay = AbstractOverlay()
OBSOverlay = AbstractOverlay()
TwitchOverlay = AbstractOverlay()
CoolOverlay = AbstractOverlay()
VoiceModOverlay = AbstractOverlay()
EmergencyConfirmOverlay = AbstractOverlay()

BaseOverlay.setActions(
    [],
    [
        [NewOverlay, SceneOverlay],
        [NewOverlay, OBSOverlay],
        [NewOverlay, TwitchOverlay],
        [actions.write, (Key.f14, 1)],
        [NewOverlay, CoolOverlay],
        [NewOverlay, VoiceModOverlay],
        [NewOverlay, EmergencyConfirmOverlay],
        [actions.write, (Key.f13, 1)]
    ],
    [
        [None, None],
        [None, None],
        [None, None],
        [actions.write, (Key.f14, 0)],
        [None, None],
        [None, None],
        [None, None],
        [actions.write, (Key.f13, 0)],
    ])

SceneOverlay.setActions(
    [
        "",
        "Start",
        "End",
        "Chat",
        "Game",
        "Display",
        "Elgato",
        "WOS"
    ],
    [
        [None, None],
        [actions.obsScene, "Start"],
        [actions.obsScene, "End"],
        [actions.obsScene, "Icon & Chatting"],
        [actions.obsScene, "Gameplay - game"],
        [actions.obsScene, "Gameplay - display"],
        [actions.obsScene, "Gameplay - elgato"],
        [actions.obsScene, "Words on Stream"],

    ],
    [
        [NewOverlay, BaseOverlay],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None]
    ])

OBSOverlay.setActions(
    [
        "Capture",
        "",
        "obs2",
        "obs3",
        "obs4",
        "obs5",
        "obs6",
        "Mute"
    ],
    [
        [actions.write, (Key.f20, 1)],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [actions.obsMute, None]

    ],
    [
        [actions.write, (Key.f20, 0)],
        [NewOverlay, BaseOverlay],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None]
    ])

TwitchOverlay.setActions(
    [
        "clip",
        "obs2",
        "",
        "emote on",
        "obs4",
        "obs5",
        "obs6",
        "emote off"
    ],
    [
        [actions.sendTwitchMessage, ("!clip")],
        [None, None],
        [None, None],
        [actions.sendTwitchMessage, ("/emoteonly")],
        [None, None],
        [None, None],
        [None, None],
        [actions.sendTwitchMessage, ("/emoteonlyoff")]

    ],
    [
        [None, None],
        [None, None],
        [NewOverlay, BaseOverlay],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None]
    ])

CoolOverlay.setActions(
    [
        "Start/Split",
        "Reset",
        "cool3",
        "cool4",
        "",
        "cool5",
        "cool6",
        "cool7"
    ],
    [
        [actions.write, (Key.f15, 1)],
        [actions.write, (Key.f16, 1)],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None]

    ],
    [
        [actions.write, (Key.f15, 0)],
        [actions.write, (Key.f16, 0)],
        [None, None],
        [None, None],
        [NewOverlay, BaseOverlay],
        [None, None],
        [None, None],
        [None, None]
    ])

VoiceModOverlay.setActions(
    [
        "vol1",
        "vol2",
        "vol3",
        "vol4",
        "vol5",
        "",
        "vol6",
        "vol7"
    ],
    [
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None]

    ],
    [
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [NewOverlay, BaseOverlay],
        [None, None],
        [None, None]
    ])

EmergencyConfirmOverlay.setActions(
    [
        "Alert",
        "-",
        "-",
        "-",
        "-",
        "-",
        "",
        "-"
    ],
    [
        [actions.streamEmergency, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
    ],
    [
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [None, None],
        [NewOverlay, BaseOverlay],
        [None, None],
    ]
)
