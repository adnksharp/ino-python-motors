import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

Ra = 9.23
La = 0.9
Kb = 0.0269
Kv = 1.13e-5
Jm = 50e-6 
Kt = 0.0269
Ks_fact = 0.45
pos_des = 0.25

Den_a = La * Jm
Num_a3 = La * Kv + Ra * Jm
Num_a2_c = Ra * Kv + Kt * Kb

Kd_est = 0.1

KP_max_Routh_num = Num_a3 * (Kt * Kd_est + Num_a2_c)
KP_max_Routh_den = Kt * Den_a
Kp_est = (KP_max_Routh_num / KP_max_Routh_den) * Ks_fact

a2_term = Kt * Kd_est + Num_a2_c
N_KI_num = (Num_a3 / Den_a) * a2_term * (Kt * Kp_est) - (Kt * Kp_est)**2
D_KI_den = Kt * (Num_a3)**2
Ki_max_Routh = (N_KI_num * Den_a) / D_KI_den
Ki_est = Ki_max_Routh * Ks_fact

if Ki_est <= 0:
    Ki_est = 0.001

print(f"Ganancias Estables: Kp={Kp_est:.4f}, {Ki_est:.4f}, {Kd_est:.4f}")

a4 = Den_a
a3 = Num_a3
a2 = Kt * Kd_est + Num_a2_c
a1 = Kt * Kp_est
a0 = Kt * Ki_est

P_s_coef_est = [a4, a3, a2, a1, a0]
num_lc_est = [Kt * Kd_est, Kt * Kp_est, Kt * Ki_est]

s = ctrl.TransferFunction([1, 0], [1])
N = 100

sys_controlador_p = Kp_est
sys_controlador_i = Ki_est / s
sys_controlador_d = Kd_est * (N * s / (s + N))

sys_controlador = sys_controlador_p + sys_controlador_i + sys_controlador_d
sys_controlador = ctrl.minreal(sys_controlador, verbose=False)

G_motor_pos = Kt / (a4*s**4/Den_a + a3*s**3/Den_a + Num_a2_c*s**2/Den_a) 
G_motor_pos_raw = ctrl.TransferFunction([Kt], [Den_a, Num_a3, Num_a2_c, 0])

sys_est = ctrl.feedback(sys_controlador * G_motor_pos_raw)
sys_est = ctrl.minreal(sys_est, verbose=False)


sys_voltage = sys_controlador * (1 - sys_est)
sys_voltage = ctrl.minreal(sys_voltage, verbose=False) 

sys_current = (sys_voltage - Kb * s * sys_est) / (La * s + Ra)
sys_current = ctrl.minreal(sys_current, verbose=False)


T_end = 5
time = np.linspace(0, T_end, 500)

T_pos, Y_pos = ctrl.step_response(sys_est, time)
T_volt, Y_volt = ctrl.step_response(sys_voltage, time)
T_curr, Y_curr = ctrl.step_response(sys_current, time)

Y_pos *= pos_des
Y_volt *= pos_des
Y_curr *= pos_des

polos_estables = ctrl.poles(sys_est)
print("\nPolos del Sistema (Estable):")
print(polos_estables)
plt.figure(figsize=(10, 8))
plt.suptitle('Respuesta del Sistema de Control PID (Estable)', fontsize=16)

plt.subplot(3, 1, 1)
plt.plot(T_pos, Y_pos, label='Posición Theta_M(t)')
plt.plot(T_pos, np.full_like(Y_pos, pos_des), 'r--', label='Referencia')
plt.title('Posición Angular')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (rad)')
plt.grid()
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(T_volt, Y_volt, label='Voltaje $V_a(t)$')
plt.title('Voltaje de Armadura')
plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.grid()
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(T_curr, Y_curr, label='Corriente $I_a(t)$')
plt.title('Corriente de Armadura')
plt.xlabel('Tiempo (s)')
plt.ylabel('Corriente (A)')
plt.grid()
plt.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
