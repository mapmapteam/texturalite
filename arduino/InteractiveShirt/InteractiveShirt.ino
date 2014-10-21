

#include "MovingStats.h"
#include "mapFloat.h"

const int N_INPUT_OUTPUT = 6;
const int REACTION_DELAY =  3000;
const float STATS_SAMPLES_PERIOD = 300000.0f;

const int photoPins[] = { 0, 1, 2, 3, 4, 5 };
const int ledPins[]   = { 3, 5, 6, 9, 10, 11 };

int nextLedValues[N_INPUT_OUTPUT];

MovingStats stats((STATS_SAMPLES_PERIOD/REACTION_DELAY)*N_INPUT_OUTPUT, 512, 128);

void setup() {
  for (int i=0; i<N_INPUT_OUTPUT; i++) {
    pinMode( ledPins[i], OUTPUT );
    nextLedValues[i] = 0;
  }
}

void loop() {
  for (int i=0; i<N_INPUT_OUTPUT; i++) {
    // Read photo cell.
    int val = analogRead( photoPins[i] );
    
    // Update stats.
    stats.update(val);
    
    // Normalize value with mean at 0 and stddev at 1.
    float normValue = stats.normalize(val);
    
    // Keep value within range.
    normValue = constrain(normValue, -2, 2);
    
    // Remap to [0,255] LED output.
    float remappedValue = mapFloat(normValue, -2, 2, 0, 255);
    
    // Write to LED.
    nextLedValues[i] = round(remappedValue);
  }
  
  // Add a delay.
  delay(REACTION_DELAY);

  // Write to LEDs.
  for (int i=0; i<N_INPUT_OUTPUT; i++) {
    analogWrite( ledPins[i], nextLedValues[i] );
  }
}
