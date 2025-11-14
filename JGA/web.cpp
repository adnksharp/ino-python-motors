#include "config.h"
#include "motor.h"
#include "credentials.h"
#include "web.h"

extern Service api;
extern Motor motor;

void post()
{
	if (WiFi.status() == WL_CONNECTED)
	{
		HTTPClient http;

		http.begin(api.postURI); 
		http.addHeader("Content-Type", "application/json"); 
		
		String pos = String(motor.get());
		String httpRequestData = "{\"id\":\"0\",\"position\":" + pos + "}";

		int httpResponseCode = http.POST(httpRequestData);

		if (httpResponseCode > 0) 
			digitalWrite(api.led, LOW);
		else
			digitalWrite(api.led, HIGH);
		http.end();
	}
	else
		digitalWrite(api.led, HIGH);
}

void Service::init(byte id, byte led)
{
	api.ssid = SSID;
	api.pass = PASS;
	api.postURI = SERVER + api.postURI;
	api.subURI = SERVER + api.subURI;
}

void Service::config()
{
	WiFi.begin(api.ssid, api.pass);
	while (WiFi.status() != WL_CONNECTED) 
	{
		delay(50);
		digitalWrite(led, !digitalRead(led));
	}
}
