#include <WiFi.h>
#include <HTTPClient.h>

struct Service {
	char* ssid;
	char* pass;
	String postURI = "enc_status",
		subURI     = "motor_cmd";
	short times = 10;
	byte id, led;
	double pos;
	void init(byte id, byte led);
	void config();
	void post();
};
