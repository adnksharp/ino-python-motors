#include <Arduino.h>
#define LED   RGB_BUILTIN

const byte LEDS[4] = {11, 12, 13, 14};
const byte M[3][2] = {
	{17,18},
	{10, 9},
	{8, 3}
}, ENC[3][2] = {
	{5, 4},
	{6, 7},
	{16, 15}
};

#define ENC_A 15
#define ENC_B 16

#define M_PWM  8
#define M_CW   3
#define M_CCW  9
