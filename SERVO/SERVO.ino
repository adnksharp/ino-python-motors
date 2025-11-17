#include "config.h"
#include "web.h"
//#include "motor.h"

byte ID = 1;

Service api;

extern void post(void * parameter);
/*

Motor motor;

extern void encoder();
*/
void setup() 
{
	Serial.begin(115200);
	while (!Serial)
		continue;

	api.init(ID);
	//motor.init();
	xTaskCreatePinnedToCore(post, "PubThread", 10000, NULL, 3, NULL, 1);
}

void loop()
{}
