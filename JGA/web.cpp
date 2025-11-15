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
		
		String pos = "0.00";//String(motor.get());
		String httpRequestData = "{\"id\":\"0\",\"position\":" + pos + "}";

		int httpResponseCode = http.POST(httpRequestData);

		if (httpResponseCode > 0) 
			neopixelWrite(LED, 0, 50, 50);
		else
			neopixelWrite(LED, 255, 200, 0);
		http.end();
	}
	else
		neopixelWrite(LED, 255, 50, 0);
}

void Service::init(byte ID)
{
	id = ID;
	ssid = SSID;
	pass = PASS;
	postURI = SERVER + postURI;
	subURI = SERVER + subURI;
}

void Service::config()
{
	  WiFi.begin(ssid, pass);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}
