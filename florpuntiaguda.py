import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear figura y ejes 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Parámetros
t = np.linspace(0, 1.57, 500)  # Rango de t
z = 2 * np.sin(t)  # Ecuación para z
y = 0.75 * (np.sin(2 * t)) ** 1.5  # Ecuación del pétalo

# Generar malla para el pétalo
v = np.linspace(-1, 1, 10)  # Para expandir en el plano y rellenar
t, v = np.meshgrid(t, v)

z_surface = 2 * np.sin(t)
y_surface = 0.75 * (np.sin(2 * t)) ** 1.5 * v

# Dibujar los pétalos como superficies rellenas
num_petals = 6  # Número de pétalos
for i in range(num_petals):
    angle = i * (2 * np.pi / num_petals)  # Ángulo de rotación para cada pétalo
    
    # Rotar y dibujar el pétalo
    x_rotated = t * np.cos(angle) - y_surface * np.sin(angle)
    y_rotated = t * np.sin(angle) + y_surface * np.cos(angle)
    
    ax.plot_surface(x_rotated, y_rotated, z_surface, color='purple', edgecolor='black', alpha=0.6)

    # Dibuja el pétalo en la dirección opuesta para completar el círculo
    x_rotated = t * np.cos(angle) - (-y_surface) * np.sin(angle)
    y_rotated = t * np.sin(angle) + (-y_surface) * np.cos(angle)
    
    ax.plot_surface(x_rotated, y_rotated, z_surface, color='purple', edgecolor='black', alpha=0.6)

# Dibujar el tallo
z_stem = np.linspace(-2, 0, 500)
x_stem = np.zeros(500)
y_stem = np.zeros(500)
ax.plot(x_stem, y_stem, z_stem, color='green', linewidth=3)

# Configurar la visualización y mostrar
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-2, 2])
ax.view_init(elev=30, azim=45)
ax.grid(True)
plt.show()
