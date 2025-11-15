#include "config.h"
#include "web.h"
//#include "motor.h"
#include <Ticker.h>

byte ID = 0;
Ticker times;
Service api;
//Motor motor;

//extern void encoder();
extern void post();

void setup() 
{
	Serial.begin(115200);
	delay(1100);
	byte outs[6] = {LED, ENC_A, ENC_B, M_CW, M_CCW, M_PWM};
	for (byte i = 0; i < sizeof(outs) / sizeof(outs[0]); i++)
		pinMode(i, OUTPUT);

	Serial.print("Start API");
	api.init(ID);
	Serial.println("...");
	api.config();
	Serial.print("Start Threads");
	//attachInterrupt(digitalPinToInterrupt(ENC_A), encoder, CHANGE);
	Serial.println("...");
	times.attach_ms(api.times, post);
	Serial.println("Sketch corriendo!");
}

void loop() 
{
	//Serial.println("Running...");
	//delay(5000);
}

