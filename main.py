import numpy as np
import matplotlib.pyplot as plt 

dt = 0.1 
T_total = 20 
n_steps = int(T_total / dt)
Tgps = 10 # 10 pas = 1 seconde 

# Modèle de prediction
X=np.zeros((2,1)) #2x1
A=np.array([1, dt],[0, 0]) #2x2
B=np.array([0],[1]) #2x1

#Modèle de observation (corretion GPS)
Z=np.zeros((2,1))
H=np.array([1, 0])

Q = np.array([0.001, 0.0], [0.0, 0.1])
R = 0.8 ** 2

u = 1.0 # m/s

x_real = 0.0 
x_est = 0.0   
P_est = 0.1    

t_hist = np.linspace(0, T_total, n_steps)
x_real_hist = []
x_est_hist = []
P_hist = []

for k in range (n_steps):
    wk = 

    if k % Tgps = 0 :
        # One mesure gps (modèl d'oservation)
        zk = Hk @ xk + vk