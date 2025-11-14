struct Motor {
	volatile int count =   0;
	short action       =   0;
	void exec(short PWM);
	double get();
};
