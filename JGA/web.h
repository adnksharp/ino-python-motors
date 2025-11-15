#include <WiFi.h>
#include <HTTPClient.h>

struct Service {
	char* ssid;
	char* pass;
	String postURI = "enc_status",
		subURI     = "motor_cmd";
	short times = 10;
	byte id;
	double pos;
	void init(byte ID);
	void config();
	void post();
};
