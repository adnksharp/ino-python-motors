#include "config.h"
#include "motor.h"
#include "credentials.h"
#include "web.h"

extern Service api;
extern Motor motor;

String httpRequestData = "{\"id\":\"0\",\"position\":0.0}";
int httpResponseCode = 0;

void post(void * parameter)
{
	while(1)
	{
		if (WiFi.status() == WL_CONNECTED)
		{
			HTTPClient http;

			http.begin(api.postURI); 
			http.addHeader("Content-Type", "application/json"); 
			httpRequestData = "{\"id\":\"0\",\"position\":" + String(motor.get()) + "}";
			httpResponseCode = http.POST(httpRequestData);

			if (httpResponseCode > 0) 
				neopixelWrite(LED, 10, 10, 10);
			else
				neopixelWrite(LED, 255, 100, 0);
			http.end();
		}
		else
		{
			WiFi.disconnect();
			WiFi.reconnect();
			api.verify();
		}
		vTaskDelay(api.times / portTICK_PERIOD_MS);
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
