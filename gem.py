import numpy as np
import matplotlib.pyplot as plt

# --- Parâmetros da Simulação ---
dt = 0.1             # Intervalo de tempo entre predições (s)[cite: 10]
T_total = 20.0       # Tempo total da simulação (s)
n_steps = int(T_total / dt)
gps_interval = 10    # Atualização do GPS a cada 10 passos (1 segundo)[cite: 10]

# --- Parâmetros do Filtro e Ruídos ---
Q = 0.05**2          # Covariância do ruído de processo Q[cite: 10]
R = 0.8**2           # Covariância do ruído de medição GPS R[cite: 10]

# Entrada de controle (velocidade constante em m/s)
u = 1.0  

# --- Inicialização ---
x_real = 0.0         # Posição real inicial
x_est = 0.0          # Estado estimado inicial (x_hat)
P_est = 0.1          # Incerteza inicial

# Vetores para armazenar o histórico
t_hist = np.linspace(0, T_total, n_steps)
x_real_hist = []
x_est_hist = []
P_hist = []
z_hist = []
t_gps_hist = []

# --- Loop de Simulação ---
np.random.seed(42)  # Para resultados reproduzíveis

for k in range(n_steps):
    # 1. Mundo Real (Simulação do movimento físico com ruído)
    w_k = np.sqrt(Q) * np.random.randn()  # Ruído no movimento[cite: 10]
    x_real = x_real + u * dt + w_k
    x_real_hist.append(x_real)
    
    # 2. ETAPA DE PREDIÇÃO (Filtro de Kalman)
    A = 1.0
    B = dt
    x_est = A * x_est + B * u
    P_est = A * P_est * A + Q
    
    # 3. ETAPA DE CORREÇÃO (GPS a cada 1 segundo)
    if (k + 1) % gps_interval == 0:
        # Gera medição com ruído do GPS
        v_k = np.sqrt(R) * np.random.randn()
        z = x_real + v_k
        
        # Equações de Correção
        H = 1.0
        K = P_est * H / (H * P_est * H + R)
        x_est = x_est + K * (z - H * x_est)
        P_est = (1.0 - K * H) * P_est
        
        # Guarda dados do GPS para plot
        z_hist.append(z)
        t_gps_hist.append(t_hist[k])
        
    x_est_hist.append(x_est)
    P_hist.append(P_est)

# Converte listas para arrays numpy
x_real_hist = np.array(x_real_hist)
x_est_hist = np.array(x_est_hist)
P_hist = np.array(P_hist)
std_hist = np.sqrt(P_hist)  # Desvio padrão (incerteza sigma)

# --- Gráficos ---
plt.figure(figsize=(12, 8))

# Subplot 1: Posição Real vs Estimada vs Medições GPS
plt.subplot(2, 1, 1)
plt.plot(t_hist, x_real_hist, 'g-', label='Posição Real ($x_{real}$)')[cite: 10]
plt.plot(t_hist, x_est_hist, 'b--', label='Posição Estimada ($\hat{x}$)')
plt.scatter(t_gps_hist, z_hist, color='red', marker='x', label='Medições GPS ($z$)')
plt.ylabel('Posição (m)')
plt.title('Filtro de Kalman 1D: Estimativa de Posição')
plt.legend()
plt.grid(True)

# Subplot 2: Incerteza P(t) em função do tempo
plt.subplot(2, 1, 2)
plt.plot(t_hist, P_hist, 'r-', label='Incerteza/Covariância $P(t)$')
plt.fill_between(t_hist, 0, P_hist, color='red', alpha=0.1)
plt.xlabel('Tempo (s)')
plt.ylabel('Covariância $P_k$')
plt.title('Evolução da Incerteza $P(t)$ (Crescimento na predição e quedas nas correções GPS)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()