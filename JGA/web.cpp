#include "config.h"
#include "credentials.h"
#include "web.h"

extern Service api;


void Service::init()
{
	api.ssid = SSID;
	api.pass = PASS;
	api.postURI = SERVER + api.postURI;
	api.subURI = SERVER + api.subURI;
}

void Service::config(byte led)
{
	WiFi.begin(api.ssid, api.pass);
	while (WiFi.status() != WL_CONNECTED) 
	{
		delay(50);
		digitalWrite(led, !digitalRead(led));
	}
}

void Service::post(byte id, byte led, double pos)
{
	if (WiFi.status() == WL_CONNECTED)
	{
		HTTPClient http;

		http.begin(api.postURI); 
		http.addHeader("Content-Type", "application/json"); 

		String httpRequestData = "{\"id\":\"0\",\"position\":" + String(pos) + "}";

		int httpResponseCode = http.POST(httpRequestData);

		if (httpResponseCode > 0) 
			digitalWrite(led, LOW);
		else
			digitalWrite(led, HIGH);
		http.end();
	}
	else
		digitalWrite(led, HIGH);
}

