import numpy as np
import matplotlib.pyplot as plt 

dt = 0.1 
T_total = 20 
n_steps = int(T_total / dt) 
un_seconde = 10

# Modèle de prédiction 
X = np.array([[0.0], [0.0]]) 
A = np.array([[1.0, dt], [0.0, 0.0]])
B = np.array([[0.0], [1.0]])

# Incertitude et correction
P = np.array([[0.1, 0.0], [0.0, 0.1]]) 
H = np.array([1, 0])

# les matrices de covariances 
Q = np.array([[0.01, 0.0], [0.0, 0.01]])
R = np.array([[0.01, 0.0], [0.0, 0.01]])

u = 1.0 

t_hist = []
x_hist = []
p_hist = []


for k in range(n_steps):
    t = k * dt
    
    # l'expression de prédition
    X = A @ X + B * u
    P = A @ P @ A.T + Q

    if t % 1 == 0 : # chaque seconde, réduit l'incertitude.
        # l'expression de correction
        K = P @ H.T @ np.linalg.inv(H @ P @ H.T + R)
        P = (np.eye(2) - K @ H) @ P
    
    t_hist.append(round(t, 1))
    x_hist.append(X[0, 0].item())
    p_hist.append(P[0, 0].item())

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
ax1.plot(t_hist, x_hist, 'b-o', markersize=2, label='Position reel')
ax1.set_ylabel('position')
ax1.grid(True)
ax2.plot(t_hist, p_hist, 'r-o', markersize=2, label='Propagation d incertitude')
ax2.set_ylabel('variance')
ax2.grid(True)
plt.show()
