#include <WiFi.h>
#include <HTTPClient.h>

struct Service {
	char* ssid;
	char* pass;
	String postURI = "enc_status",
		subURI     = "motor_cmd";
	short times = 10;
	void init();
	void config(byte led);
	void post(byte id, byte led, double pos);
};
