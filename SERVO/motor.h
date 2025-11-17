#include <AS5600.h>
#include <ESP32Servo.h>

struct Motor {
	const double PWPR = 4095.0;
	const short enc_zero = 3786;
	void init();
	void set(double POS);
	double get();
};
