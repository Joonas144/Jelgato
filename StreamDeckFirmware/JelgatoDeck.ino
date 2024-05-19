

// ---------------------------------
// Key definitions
/*#define BUTTON_KEY1 KEY_F13
#define BUTTON_KEY2 KEY_F14
#define BUTTON_KEY3 KEY_F15
#define BUTTON_KEY4 KEY_F16
#define BUTTON_KEY5 KEY_F17
#define BUTTON_KEY6 KEY_F18
#define BUTTON_KEY7 KEY_F19
#define BUTTON_KEY8 KEY_F20
*/

// Key definitions
#define BUTTON_KEY1 '0'
#define BUTTON_KEY2 '1'
#define BUTTON_KEY3 '2'
#define BUTTON_KEY4 '3'
#define BUTTON_KEY5 '4'
#define BUTTON_KEY6 '5'
#define BUTTON_KEY7 '6'
#define BUTTON_KEY8 '7'

#define BUTTON_OSU_KEY1 'D'
#define BUTTON_OSU_KEY2 'F'
#define BUTTON_OSU_KEY3 'J'
#define BUTTON_OSU_KEY4 'K'
#define BUTTON_OSU_KEY5 'X'
#define BUTTON_OSU_KEY6 'Z'
#define BUTTON_OSU_KEY7 'X'
#define BUTTON_OSU_KEY8 'Z'

// Pin definitions
#define BUTTON_PIN1 9
#define BUTTON_PIN2 6
#define BUTTON_PIN3 4
#define BUTTON_PIN4 2
#define BUTTON_PIN5 8
#define BUTTON_PIN6 7
#define BUTTON_PIN7 5
#define BUTTON_PIN8 3
// ---------------------------------


#include "Keyboard.h"

bool osuMode = false;

// Button helper class for handling press/release and debouncing
class button {
  public:
    const char key;
    const char altKey;
    const uint8_t pin;
    bool pressed = 0;

    button(uint8_t k, uint8_t o, uint8_t p) : key(k), altKey(o), pin(p) {}

    void press(boolean state) {
      if (state == pressed || (millis() - lastPressed  <= debounceTime)) {
        return; // Nothing to see here, folks
      }

      lastPressed = millis();
      
      //state ? Keyboard.press(key) : Keyboard.release(key);
      if (osuMode) {
        state ? Keyboard.press(altKey) : Keyboard.release(altKey);
      } else {
        state ? Serial.println(key) : Serial.println(key+20);
      }
      pressed = state;
    }

    void update() {
      press(!digitalRead(pin));
    }

  private:
    const long debounceTime = 30;
    unsigned long lastPressed;

} ;

// Button objects, organized in array
button buttons[] = {
  {BUTTON_KEY1, BUTTON_OSU_KEY1, BUTTON_PIN1},
  {BUTTON_KEY2, BUTTON_OSU_KEY2, BUTTON_PIN2},
  {BUTTON_KEY3, BUTTON_OSU_KEY3, BUTTON_PIN3},
  {BUTTON_KEY4, BUTTON_OSU_KEY4, BUTTON_PIN4},
  {BUTTON_KEY5, BUTTON_OSU_KEY5, BUTTON_PIN5},
  {BUTTON_KEY6, BUTTON_OSU_KEY6, BUTTON_PIN6},
  {BUTTON_KEY7, BUTTON_OSU_KEY7, BUTTON_PIN7},
  {BUTTON_KEY8, BUTTON_OSU_KEY8, BUTTON_PIN8},
};

const uint8_t NumButtons = sizeof(buttons) / sizeof(button);
const uint8_t ledPin = 17;


int startPressed;
int endPressed;
int previousState = 0;
int held = 0;
const int holdThreshold = 1000;

void setup() {
  // Safety check. Ground pin #1 (RX) to cancel keyboard inputs.
  pinMode(1, INPUT_PULLUP);
  if (!digitalRead(1)) {
    failsafe();
  }

  // Set LEDs Off. Active low.
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  TXLED0;

  for (int i = 0; i < NumButtons; i++) {
    pinMode(buttons[i].pin, INPUT_PULLUP);
  }

  Serial.begin(9600);
  Serial.write("Ready");
}

void(* resetFunc) (void) = 0;//declare reset function at address 0

void loop() {
  for (int i = 0; i < NumButtons; i++) {
    buttons[i].update();
  }

  int buttonState = (
      buttons[0].pressed &&
      buttons[3].pressed &&
      buttons[4].pressed &&
      buttons[7].pressed
     );
     
  if (previousState != buttonState) {
    previousState = buttonState;
    if (buttonState == HIGH) {
      Keyboard.releaseAll();
      startPressed = millis();
    } else {
      int holdTime = millis() - startPressed;
        osuMode = !osuMode;
      }
    }
  
  //for (int i = 0; i < NumButtons; i++) {
  //Serial.write( (uint8_t*)buttons, sizeof(buttons));
  //}

}

void failsafe() {
  for (;;) {} // Just going to hang out here for awhile :D
}
