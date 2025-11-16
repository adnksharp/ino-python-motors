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
	Serial.begin(115200);
	delay(1100);

	Serial.println("Start API...");
	api.init(ID);
	Serial.println("Start Motor");
	motor.init();
	times.attach_ms(api.times, post);
	Serial.println("OK");
}

void loop() 
{
	//Serial.println("Running...");
	//delay(5000);
}

