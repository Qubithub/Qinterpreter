import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np

def draw_bloch_sphere():
    # Establecer el estilo de la gráfica
    plt.style.use('seaborn-dark-palette')

    # Crear figura y eje 3D
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Esfera de Bloch Mejorada')

    # Dibujar la esfera de Bloch con sombreado
    u, v = np.mgrid[0:2*np.pi:200j, 0:np.pi:100j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, rstride=10, cstride=10, color='white', edgecolor='k', alpha=0.5, shade=True)

    # Añadir los vectores de estado
    ax.quiver(0, 0, 0, 0, 0, 1, color='blue', linewidth=2, arrow_length_ratio=0.1)

    # Etiquetas y estilo del gráfico
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_box_aspect([1,1,1])  # Aspect ratio is 1:1:1

    # Añadir anotaciones de los ejes
    ax.text(0, 0, 1.1, r'$|0\rangle$', color='black', fontsize=18, ha='center')
    ax.text(0, 0, -1.1, r'$|1\rangle$', color='black', fontsize=18, ha='center')
    ax.text(1.1, 0, 0, r'$|+\rangle$', color='black', fontsize=18, ha='center')
    ax.text(-1.1, 0, 0, r'$|-\rangle$', color='black', fontsize=18, ha='center')
    ax.text(0, 1.1, 0, r'$|i+\rangle$', color='black', fontsize=18, ha='center')
    ax.text(0, -1.1, 0, r'$|i-\rangle$', color='black', fontsize=18, ha='center')

    # Añadir la circunferencia ecuatorial
    p = Circle((0, 0), 1, edgecolor='k', facecolor='none')
    ax.add_patch(p)
    art3d.pathpatch_2d_to_3d(p, z=0, zdir="z")

    # Añadir líneas de longitud y latitud como guías
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 15)
    for ui in u:  # líneas de longitud
        x = np.cos(ui) * np.sin(v)
        y = np.sin(ui) * np.sin(v)
        z = np.cos(v)
        ax.plot(x, y, z, color='k', linestyle='dotted', alpha=0.5)
    for vi in v:  # líneas de latitud
        x = np.cos(u) * np.sin(vi)
        y = np.sin(u) * np.sin(vi)
        z = np.cos(vi)
        ax.plot(x, y, z, color='k', linestyle='dotted', alpha=0.5)

    # Mostrar la figura
    plt.show()

draw_bloch_sphere()
