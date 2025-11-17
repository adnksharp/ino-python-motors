#include "config.h"
#include "motor.h"

extern Motor motor;
extern AS5600 encoder;
extern Servo servo;

void Motor::init()
{
	pinMode(ENC_DIR, OUTPUT);
	pinMode(ENC_GPO, OUTPUT);
	Wire.begin();
	encoder.begin();
	servo.attach(SERVO);
}

void Motor::set(double POS)
{
	int pos = POS * 360;
	pos = map(pos, 0, 180, 0, 180);
	servo.write(pos);
}

double Motor::get()
{
	int read = encoder.readAngle() - enc_zero;
	if (read < 0)
		read += PWPR;
	return double(read) / PWPR;
}
