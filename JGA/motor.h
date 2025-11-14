struct Motor {
	const short PPR    = 22;
	volatile int count = 0;
	void exec(short PWM);
	double get();
};
