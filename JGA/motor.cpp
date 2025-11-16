#include "config.h"
#include "motor.h"

extern Motor motor;

void encoder()
{
	if(digitalRead(ENC_A) == digitalRead(ENC_B))
		motor.count++;
	else
		motor.count--;
}

void Motor::init()
{
	for (byte i = 0; i < 4; i++)
		pinMode(LEDS[i], OUTPUT);
	for (byte i = 0; i < 3; i++)
	{
		for (byte j = 0; j < 2; j++)
		{
			pinMode(M[i][j], OUTPUT);
			pinMode(ENC[i][j], INPUT);
		}
	}
	attachInterrupt(digitalPinToInterrupt(ENC_A), encoder, CHANGE);
}

void Motor::exec(short PWM)
{
	if (PWM != 0)
	{
		digitalWrite(M_CW,  PWM > 0 ? HIGH :  LOW);
		digitalWrite(M_CCW, PWM < 0 ? HIGH :  LOW);
		analogWrite(M_PWM,  PWM > 0 ? PWM  : -PWM);
	}
	else
	{
		digitalWrite(M_CW,  LOW);
		digitalWrite(M_CCW, LOW);
		analogWrite(M_PWM,  0);
	}
}

double Motor::get()
{
	return double(count) / PPR;
}
