import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definición de las funciones
def f(t, p):
    return np.cos(p * t)

def g(t, k, n):
    return (k ** 3) / ((np.sin(t)) ** (2 * n) + k ** 2)

# Definición del pétalo como superficie
def petal_surface(u, v, R, k, p, Rz, n):
    x = R * np.cos(u) * np.cos(p * u) * v
    y = R * np.sin(u) * np.cos(p * u) * v
    z = Rz * g(u, k, n) * v
    return x, y, z

# Función para generar un tallo curvo estilizado
def generate_stem(ax, num_sections, curvature_intensity):
    z_stem = np.linspace(-num_sections, 0, 200)  # Longitud del tallo
    x_stem = curvature_intensity * np.sin(z_stem)  # Curvatura del tallo en X
    y_stem = curvature_intensity * np.cos(z_stem)  # Curvatura del tallo en Y

    # Dibujar el tallo curvo
    ax.plot(x_stem, y_stem, z_stem, color='g', linewidth=2)

# Función para generar una flor
def generate_flower(ax, R, Rz, k, p, n, num_layers, num_petals_per_layer, inclinacion_max, rotation_angle_z):
    # Generar las capas de pétalos
    for layer in range(num_layers):
        layer_scale = 1 - layer * 0.10  # Reducción más suave en el tamaño de las capas
        inclinacion_x = inclinacion_max * (layer / num_layers)  # Inclinación gradual en X
        inclinacion_y = inclinacion_max * (layer / num_layers)  # Inclinación gradual en Y
        inclinacion_z = inclinacion_max * (layer / num_layers)  # Inclinación gradual en Z
        u = np.linspace(0, 2 * np.pi, 100)  # Redefinición de u y v en cada iteración
        v = np.linspace(0, 1, 10)
        u, v = np.meshgrid(u, v)
        
        for i in range(num_petals_per_layer):  # Pétalos en la capa
            x, y, z = petal_surface(u, v, R * layer_scale, k, p, Rz * layer_scale, n)
            # Rotación inicial en Z para distribuir los pétalos
            x_rot, y_rot, z_rot = rotate_z(x, y, z, i * (360 / num_petals_per_layer))  

            # Aquí ya generamos el pétalo completo y lo movemos, ahora aplicamos la inclinación completa
            # Aplicamos inclinación simétrica en ambos lados y rotamos en los tres ejes
            angle_x = inclinacion_x if (i % 2 == 0) else -inclinacion_x
            angle_y = inclinacion_y if (i % 2 == 0) else -inclinacion_y
            angle_z = inclinacion_z if (i % 2 == 0) else -inclinacion_z
            x_rot, y_rot, z_rot = rotate_complete(x_rot, y_rot, z_rot, angle_x, angle_y, angle_z)
            
            # Rotación adicional de la flor
            x_rot, y_rot, z_rot = rotate_z(x_rot, y_rot, z_rot, rotation_angle_z)

            # Dibujar el pétalo
            ax.plot_surface(x_rot, y_rot, z_rot, color='yellow', edgecolor='black', alpha=0.5, rstride=5, cstride=5)

# Función para rotar alrededor del eje Z
def rotate_z(x, y, z, angle):
    rad = np.deg2rad(angle)
    x_rot = x * np.cos(rad) - y * np.sin(rad)
    y_rot = x * np.sin(rad) + y * np.cos(rad)
    return x_rot, y_rot, z

# Función para rotar alrededor del eje X (para inclinar las capas)
def rotate_x(x, y, z, angle):
    rad = np.deg2rad(angle)
    y_rot = y * np.cos(rad) - z * np.sin(rad)
    z_rot = y * np.sin(rad) + z * np.cos(rad)
    return x, y_rot, z_rot

# Función para rotar alrededor del eje Y (para inclinar las capas)
def rotate_y(x, y, z, angle):
    rad = np.deg2rad(angle)
    z_rot = z * np.cos(rad) - x * np.sin(rad)
    x_rot = z * np.sin(rad) + x * np.cos(rad)
    return x_rot, y, z_rot

# Añadimos una rotación completa en los tres ejes
def rotate_complete(x, y, z, angle_x, angle_y, angle_z):
    x, y, z = rotate_x(x, y, z, angle_x)
    x, y, z = rotate_y(x, y, z, angle_y)
    x, y, z = rotate_z(x, y, z, angle_z)
    return x, y, z

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Parámetros de la flor
R = 2.25  # Radio base para la primera capa
Rz = 5    # Altura del pétalo
k = 0.5   # Parámetro de forma
n = 3     # Parámetro de forma
p = 1     # Parámetro para curvatura
num_layers = 4  # Número de capas de pétalos externos
num_petals_per_layer = 12  # Número de pétalos por capa
inclinacion_max = 30  # Inclinación máxima

# Generar la flor principal
generate_flower(ax, R, Rz, k, p, n, num_layers, num_petals_per_layer, inclinacion_max, rotation_angle_z=0)

# Generar la segunda flor rotada 90 grados
generate_flower(ax, R, Rz, k, p, n, num_layers, num_petals_per_layer, inclinacion_max, rotation_angle_z=90)

# Generar el tallo curvo estilizado
generate_stem(ax, num_sections=4, curvature_intensity=0.2)

# Configuración final
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_box_aspect([1, 1, 1])  # Aspecto igual en todos los ejes
plt.show()
