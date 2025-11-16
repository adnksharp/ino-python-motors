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
			neopixelWrite(LED, 10, 10, 10);
		else
			neopixelWrite(LED, 255, 200, 0);
		http.end();
	}
	else
	{
		neopixelWrite(LED, 255, 0, 100);
		WiFi.disconnect();
		WiFi.reconnect();
		api.verify();
	}
}

void Service::init(byte ID)
{
	id = ID;
	ssid = SSID;
	pass = PASS;
	postURI = SERVER + postURI;
	subURI = SERVER + subURI;
	WiFi.begin(ssid, pass);
	verify();
	Serial.println(WiFi.localIP());
}

void Service::verify()
{
	neopixelWrite(LED, 255, 0, 0);
	while(WiFi.status() != WL_CONNECTED) { delay(100); }
	neopixelWrite(LED, 0, 0, 0);
}
