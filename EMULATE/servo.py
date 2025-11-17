import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

Ra = 3.69
Kb = 0.151
Kv = 0.00519
Jm = 10e-6
Kt = 0.151
pos_des = 0.25

Km = Kt / (Ra * Jm)
a = (Ra * Kv + Kt * Kb) / (Ra * Jm)

Ks_fact = 0.7
Kd_est = 0.01
A2 = a + Km * Kd_est
Kp_est = a * 0.00012
KI_max_Routh = Kp_est * A2 / Km
Ki_est = KI_max_Routh * Ks_fact

if Ki_est <= 0:
    Ki_est = 0.001

print(f"Ganancias Estables: Kp={Kp_est:.4f}, {Ki_est:.4f}, {Kd_est:.4f}")

A3 = 1
A2_lc = A2
A1_lc = Km * Kp_est
A0_lc = Km * Ki_est

P_s_coef_est = [A3, A2_lc, A1_lc, A0_lc]
num_lc_est = [Km * Kd_est, Km * Kp_est, Km * Ki_est]

s = ctrl.TransferFunction([1, 0], [1])
N = 100

G_motor_pos_raw = ctrl.TransferFunction([Km], [1, a, 0])

sys_controlador_p = Kp_est
sys_controlador_i = Ki_est / s
sys_controlador_d = Kd_est * (N * s / (s + N))
sys_controlador = sys_controlador_p + sys_controlador_i + sys_controlador_d
sys_controlador = ctrl.minreal(sys_controlador, verbose=False)

sys_est = ctrl.feedback(sys_controlador * G_motor_pos_raw)
sys_est = ctrl.minreal(sys_est, verbose=False)

sys_voltage = sys_controlador * (1 - sys_est)
sys_voltage = ctrl.minreal(sys_voltage, verbose=False)

sys_current = (sys_voltage - Kb * s * sys_est) / Ra
sys_current = ctrl.minreal(sys_current, verbose=False)

T_end = 50
time = np.linspace(0, T_end, T_end * 100)

T_pos, Y_pos = ctrl.step_response(sys_est, time)
T_volt, Y_volt = ctrl.step_response(sys_voltage, time)
T_curr, Y_curr = ctrl.step_response(sys_current, time)

Y_pos *= pos_des
Y_volt *= pos_des
Y_curr *= pos_des

polos_estables = ctrl.poles(sys_est)
print("\nPolos del Sistema (Estable):")
print(polos_estables)

"""
plt.figure(figsize=(10, 8))
plt.suptitle('Respuesta del Servomotor SG90 (Modelo Simplificado + PID)', fontsize=16)

# Posición
plt.subplot(3, 1, 1)
plt.plot(T_pos, Y_pos, label='Posición Theta(t)')
plt.plot(T_pos, np.full_like(Y_pos, pos_des), 'r--', label='Referencia')
plt.title('Posición Angular')
plt.ylabel('Posición (rad)')
plt.grid()

# Voltaje
plt.subplot(3, 1, 2)
plt.plot(T_volt, Y_volt, label='Voltaje $V_a(t)$')
plt.title('Voltaje de Armadura')
plt.ylabel('Voltaje (V)')
plt.grid()

# Corriente
plt.subplot(3, 1, 3)
plt.plot(T_curr, Y_curr, label='Corriente $I_a(t)$')
plt.title('Corriente de Armadura')
plt.xlabel('Tiempo (s)')
plt.ylabel('Corriente (A)')
plt.grid()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
"""
