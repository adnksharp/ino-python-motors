#include "config.h"
#include "web.h"
#include "motor.h"
#include <Ticker.h>

byte ID = 0;
Ticker times;
Service api;
Motor motor;

extern void encoder();
extern void post();

void setup() 
{
	byte outs[6] = {LED, ENC_A, ENC_B, M_CW, M_CCW, M_PWM};
	for (byte i: outs)
		pinMode(i, OUTPUT);

	Serial.begin(115200);

	api.init(ID, LED);
	api.config();
	attachInterrupt(digitalPinToInterrupt(ENC_A), encoder, CHANGE);
	times.attach_ms(api.times, post);
	digitalWrite(LED, LOW);
	Serial.println("Sketch corriendo!");
}

void loop() 
{
}

