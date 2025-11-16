struct Motor {
	const double PPR   = 92.76;
	volatile int count = 0;
	void init();
	void exec(short PWM);
	double get();
};
