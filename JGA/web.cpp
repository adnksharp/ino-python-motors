#include "config.h"
#include "motor.h"
#include "credentials.h"
#include "web.h"

extern Service api;
extern Motor motor;

void post(void * parameter)
{
	while(1)
	{
		if (WiFi.status() == WL_CONNECTED)
		{
			HTTPClient http;

			http.begin(api.postURI); 
			http.addHeader("Content-Type", "application/json"); 
			api.request = "{\"id\":\"0\",\"position\":" + String(motor.get()) + "}";
			api.code = http.POST(api.request);

			if (api.code == 200)
			{
				api.response = http.getString();
				StaticJsonDocument<200> doc;
				DeserializationError error = deserializeJson(doc, api.response);

				if (error) 
					neopixelWrite(LED, 255, 100, 0);
				else 
				{
					motor.set(doc["voltage"] | 0.0); 
					neopixelWrite(LED, 10, 10, 10);
				}
			}
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
	while(WiFi.status() != WL_CONNECTED)
		continue;
	neopixelWrite(LED, 0, 0, 0);
}
