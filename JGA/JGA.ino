#include "config.h"
#include "web.h"
#include "motor.h"
#include <Ticker.h>

Ticker timer;
Service api;
Motor motor;

extern void encoder();

void setup() 
{
	byte outs[6] = {LED, ENC_A, ENC_B, M_CW, M_CCW, M_PWM};
	for (byte i: outs)
		pinMode(i, OUTPUT);
	Serial.begin(115200);

	api.init();
	api.config(LED);
	attachInterrupt(digitalPinToInterrupt(ENC_A), encoder, CHANGE);
	digitalWrite(LED, LOW);
}

void loop() 
{
}

