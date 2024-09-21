import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de las funciones
def f(t, p):
    return np.cos(p * t)

def g(t, k, n):
    return (k ** 3) / ((np.sin(t)) ** (2 * n) + k ** 2)

# Parámetros de la flor
R = 2.25
Rz = 5
k = 0.5
n = 3
p = 1
tf = 2 * np.pi

# Definición del pétalo como superficie
def petal_surface(u, v, R, k, p, Rz):
    x = R * np.cos(u) * np.cos(p * u) * v
    y = R * np.sin(u) * np.cos(p * u) * v
    z = Rz * g(u, k, n) * v
    return x, y, z

# Función para rotar alrededor del eje Z
def rotate_z(x, y, z, angle):
    rad = np.deg2rad(angle)
    x_rot = x * np.cos(rad) - y * np.sin(rad)
    y_rot = x * np.sin(rad) + y * np.cos(rad)
    return x_rot, y_rot, z

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generar los pétalos como superficies
u = np.linspace(0, tf, 100)
v = np.linspace(0, 1, 10)
u, v = np.meshgrid(u, v)

for i in range(5):  # 5 pétalos rotados
    x, y, z = petal_surface(u, v, R, k, p, Rz)
    x_rot, y_rot, z_rot = rotate_z(x, y, z, i * 72)  # Rotación de 72° (360°/5)
    ax.plot_surface(x_rot, y_rot, z_rot, color='white', edgecolor='black', rstride=5, cstride=5)

# Añadir el tallo
z_stem = np.linspace(-3, 0, 100)  # Longitud del tallo
x_stem = np.zeros_like(z_stem)
y_stem = np.zeros_like(z_stem)
ax.plot(x_stem, y_stem, z_stem, color='g', linewidth=2)

# Añadir estambres
for i in range(5):
    x_stamen = np.zeros(2)
    y_stamen = np.zeros(2)
    z_stamen = np.linspace(0, 1, 2)  # Estambres de altura 1
    x_rot, y_rot, z_rot = rotate_z(x_stamen, y_stamen, z_stamen, i * 72 + 36)  # Rotar estambres
    ax.plot(x_rot, y_rot, z_rot, color='yellow', linewidth=2)

# Configuración final
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])  # Aspecto igual en todos los ejes
plt.show()
