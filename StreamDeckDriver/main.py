from src import overlay, overlays
from src import arduino_finder
import serial

SerialPort = arduino_finder.findArduino()
SerialBaud = 9600
arduino = serial.Serial(port=SerialPort, baudrate=SerialBaud, timeout=.001)
overlay.start()


class CurrentOverlay:
    texts = []
    pressActions = []
    releaseActions = []


def SetOverlay(newOverlay):
    (CurrentOverlay.texts,
     CurrentOverlay.pressActions,
     CurrentOverlay.releaseActions) = newOverlay.getActions()

    if CurrentOverlay.texts:
        overlay.updateTexts(CurrentOverlay.texts)
        overlay.show()
        return

    overlay.hide()


overlays.OverlaySetter = SetOverlay
overlays.OverlaySetter(overlays.BaseOverlay)

print("Good to go, awaiting input...")
buttonsPressed = [0, 0, 0, 0, 0, 0, 0, 0]

while True:
    overlay.update()

    serialInput = arduino.readline().decode().strip()
    if serialInput == '': continue

    serialInput = int(serialInput)
    print("button " + ("pressed: " + str(serialInput)) if serialInput <= 20 else ("released: " + str(serialInput-68)))

    listFunction = None
    listArgs = None

    if serialInput <= 20:
        overlay.highlight(serialInput, True)
        buttonsPressed[serialInput] = 1

        listFunction, listArgs = CurrentOverlay.pressActions[serialInput]

    if serialInput >= 21:
        overlay.highlight(serialInput - 68, False)
        buttonsPressed[serialInput - 68] = 0
        listFunction, listArgs = CurrentOverlay.releaseActions[serialInput - 68]

    if listFunction is None: continue

    if listArgs is None:
        thread = Thread(target=listFunction)
        thread.start()
        continue
        # listFunction()
        # continue

    if isinstance(listArgs, overlays.AbstractOverlay):
        listFunction(listArgs)
        continue

    if isinstance(listArgs, str):
        thread = Thread(target=listFunction, args=[listArgs])
        print("type was str")
        thread.start()
        continue

    thread = Thread(target=listFunction, args=listArgs)
    thread.start()
    # listFunction(*listArgs)
