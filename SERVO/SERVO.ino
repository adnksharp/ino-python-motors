#include "config.h"
#include "web.h"
#include "motor.h"

byte ID = 1;

AS5600 encoder;
Servo servo;
Service api;
Motor motor;

extern void post(void * parameter);

void setup() 
{
	Serial.begin(115200);
	while (!Serial)
		continue;

	api.init(ID);
	motor.init();
	xTaskCreatePinnedToCore(post, "PubThread", 10000, NULL, 3, NULL, 1);
}

void loop()
{}
