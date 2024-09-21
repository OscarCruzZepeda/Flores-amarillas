import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import time
from tqdm import tqdm

# Función para dibujar la primera flor con tamaño y base variables (Flor 1)
def draw_flower_1(ax, x_offset=0, y_offset=0, color='yellow', size=1.0, z_base=0):
    t = np.linspace(0, 1.57, 500)
    z = (0.26 * np.sin(t) + z_base) * size  # Mantener la altura de los pétalos en Flor 1
    y = 0.75 * (np.sin(2 * t)) ** 1.5 * size
    
    v = np.linspace(-1, 1, 10)
    t, v = np.meshgrid(t, v)

    z_surface = (0.26 * np.sin(t) + z_base) * size  # Mantener la altura en z
    y_surface = 0.75 * (np.sin(2 * t)) ** 1.5 * v * size

    num_petals = 6
    for i in range(num_petals):
        angle = i * (2 * np.pi / num_petals)
        x_rotated = t * np.cos(angle) - y_surface * np.sin(angle)
        y_rotated = t * np.sin(angle) + y_surface * np.cos(angle)
        ax.plot_surface(x_rotated + x_offset, y_rotated + y_offset, z_surface, color=color, edgecolor='none', alpha=0.9)
        
        x_rotated = t * np.cos(angle) - (-y_surface) * np.sin(angle)
        y_rotated = t * np.sin(angle) + (-y_surface) * np.cos(angle)
        ax.plot_surface(x_rotated + x_offset, y_rotated + y_offset, z_surface, color=color, edgecolor='none', alpha=0.9)
    
    # Tallo más delgado
    z_stem = np.linspace(-0.325 * size + z_base, z_base, 500)  # Reducir la longitud del tallo
    x_stem = np.zeros(500) + x_offset
    y_stem = np.zeros(500) + y_offset
    ax.plot(x_stem, y_stem, z_stem, color='green', linewidth=0.25)  # Tallo delgado

# Función para dibujar la segunda flor con tamaño y base variables (Flor 2, más alargada)
def draw_flower_2(ax, x_offset=0, y_offset=0, color='orange', size=1.2, z_base=0):
    def f(t, p):
        return np.cos(p * t)
    
    def g(t, k, n):
        return (k ** 3) / ((np.sin(t)) ** (2 * n) + k ** 2)
    
    R = 1.5 * size  # Mantener tamaño de los pétalos en x e y
    Rz = 1.5 * size  # Alargar los pétalos en z
    k = 0.5
    n = 3
    p = 1
    tf = 2 * np.pi

    u = np.linspace(0, tf, 100)
    v = np.linspace(0, 0.6, 10)  # Mantener pétalos más largos
    u, v = np.meshgrid(u, v)

    def petal_surface(u, v, R, k, p, Rz):
        x = R * np.cos(u) * np.cos(p * u) * v
        y = R * np.sin(u) * np.cos(p * u) * v
        z = Rz * g(u, k, n) * v + z_base  # Aumentar altura de los pétalos
        return x, y, z

    def rotate_z(x, y, z, angle):
        rad = np.deg2rad(angle)
        x_rot = x * np.cos(rad) - y * np.sin(rad)
        y_rot = x * np.sin(rad) + y * np.cos(rad)
        return x_rot, y_rot, z

    for i in range(5):
        x, y, z = petal_surface(u, v, R, k, p, Rz)
        x_rot, y_rot, z_rot = rotate_z(x, y, z, i * 72)
        ax.plot_surface(x_rot + x_offset, y_rot + y_offset, z_rot, color=color, edgecolor='none', rstride=5, cstride=5)

    # Tallo más delgado
    z_stem = np.linspace(-1.5 * size + z_base, z_base, 100)  # Ajustar longitud del tallo también
    x_stem = np.zeros_like(z_stem) + x_offset
    y_stem = np.zeros_like(z_stem) + y_offset
    ax.plot(x_stem, y_stem, z_stem, color='g', linewidth=0.25)  # Tallo delgado

# Iniciar cronómetro para medir el tiempo total
start_time = time()

# Crear el campo de flores en vista 2D
fig = plt.figure()

# Gráfico en 2D
ax2 = fig.add_subplot(111, projection='3d')

# Texto para generar la distribución (usaremos los valores ASCII de las letras)
texto = '''Él la estaba esperando con una flor amarilla
Ella lo estaba soñando con la luz en su pupila
Y el amarillo del sol iluminaba la esquina (la esquina)
Lo sentía tan cercano, lo sentía desde niña

Ella sabía que él sabía, que algún día pasaría
Que vendría a buscarla, con sus flores amarillas

No te apures no detengas, el instante del encuentro
Está dicho que es un hecho, no la pierdas no hay derecho

No te olvides, que la vida
Casi nunca está dormida

En ese bar tan desierto los esperaba el encuentro (el encuentro)
Ella llegó en limosina amarilla por supuesto
Él se acercó de repente y la miró tan de frente (de frente)
Toda una vida soñada y no pudo decir nada

Ella sabía que él sabía, que algún día pasaría
Que vendría a buscarla, con sus flores amarillas

No te apures no detengas, el instante del encuentro
Está dicho que es un hecho, no la pierdas no hay derecho

No te olvides, que la vida
Casi nunca está dormida

(Flores amarillas)

Ella sabía que él sabía, que algún día pasaría
Que vendría a buscarla, con sus flores amarillas

No te apures no detengas, el instante del encuentro
Está dicho que es un hecho, no la pierdas no hay derecho

No te olvides, que la vida
Casi nunca está dormida

Ella sabía que él sabía
Él sabía, ella sabia
Él sabía, ella sabía y se olvidaron, de sus flores amarillas'''

# Generar posiciones basadas en el valor ASCII de las letras
letras = [ord(letra) for letra in texto if letra.isalpha()]  # Solo considerar letras

# Generar 800 flores con mezcla de distribución aleatoria y texto
colors = ['yellow', 'orange']
num_flores = 800
mezcla_factor = 0.5  # Factor de mezcla entre la distribución del texto y valores aleatorios

for i in tqdm(range(num_flores)):
    # Mezclar posiciones ASCII con una distribución aleatoria
    x_text = letras[i % len(letras)] % 50 - 25
    y_text = letras[(i + 1) % len(letras)] % 50 - 25
    x_random = np.random.uniform(-25, 25)
    y_random = np.random.uniform(-25, 25)
    
    # Aplicar el factor de mezcla
    x_pos = mezcla_factor * x_text + (1 - mezcla_factor) * x_random
    y_pos = mezcla_factor * y_text + (1 - mezcla_factor) * y_random
    
    flower_type = np.random.choice([1, 2])
    color = np.random.choice(colors)
    
    if flower_type == 1:
        size = np.random.uniform(0.7, 1.0)  # Tamaño de las flores 1
        draw_flower_1(ax2, x_pos, y_pos, color=color, size=size)
    else:
        size = np.random.uniform(1.0, 1.2)  # Tamaño de las flores 2
        draw_flower_2(ax2, x_pos, y_pos, color=color, size=size)

# Configurar la visualización 2D desde arriba (elevación a 90 grados, ángulo azimutal de 45)
ax2.set_xlim([-25, 25])  # Ajustar para el terreno de 50x50
ax2.set_ylim([-25, 25])
ax2.set_zlim([-3, 3])

# Ajustar la proporción para que no se vean alargadas
ax2.set_box_aspect([1, 1, 0.3])  # Proporción ajustada de los ejes x, y y z

ax2.view_init(elev=45, azim=45)  # Vista 2D desde arriba, con ángulo de 45° en azimut

# Mostrar gráfico
plt.show()

# Mostrar tiempo total de ejecución
end_time = time()
print(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")
