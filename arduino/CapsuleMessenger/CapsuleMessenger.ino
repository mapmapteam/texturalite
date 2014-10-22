#include <Messenger.h>

// Constants: (pins)
#define MOTOR_OUT 10
#define FAN_OUT   12
#define HANDS_IN  3

// Constants: (baud rate)
#define BAUD_RATE 115200

// Constants: (messaging protocol - ASCII characters plus new lines)
#define MSG_TYPE_READ      'R'
#define MSG_TYPE_MOTOR_ON  'M'
#define MSG_TYPE_MOTOR_OFF 'm'
#define MSG_TYPE_FAN_ON    'F'
#define MSG_TYPE_FAN_OFF   'f'
#define MSG_HANDS_ON       'y'
#define MSG_HANDS_OFF      'n'

Messenger messenger('\n');

boolean readHands() {
// Reduces appearance of false positives.
#define READ_HANDS_N_SAMPLES 1000
#define READ_HANDS_N_SAMPLES_THRESHOLD 900
  int sum = 0;
  for (int i=0; i<READ_HANDS_N_SAMPLES; i++)
    sum += digitalRead(HANDS_IN) == LOW ? 1 : 0;
  return (sum > READ_HANDS_N_SAMPLES_THRESHOLD - 100);
}

// Create the callback function
void messageReady()
{
  // Loop through all the available elements of the message
  while (messenger.available())
  {
    char c = messenger.readChar();
    switch (c)
    {
      case MSG_TYPE_MOTOR_ON:
        digitalWrite(MOTOR_OUT, HIGH);
        break;
      case MSG_TYPE_MOTOR_OFF:
        digitalWrite(MOTOR_OUT, LOW);
        break;
      case MSG_TYPE_FAN_ON:
        digitalWrite(FAN_OUT, HIGH);
        break;
      case MSG_TYPE_FAN_OFF:
        digitalWrite(FAN_OUT, LOW);
        break;
      case MSG_TYPE_READ:
      default :
        // Hands ground the circuit so LOW == ON
        Serial.println(readHands() ? MSG_HANDS_ON : MSG_HANDS_OFF);
    }
  }
}

void setup()
{
  Serial.begin(BAUD_RATE);
  
  messenger.attach(messageReady);
  
  pinMode(MOTOR_OUT, OUTPUT);
  pinMode(FAN_OUT,   OUTPUT);
  pinMode(HANDS_IN,  INPUT);
}

void loop()
{
  while (Serial.available())
  {
    messenger.process(Serial.read());
  }
}

