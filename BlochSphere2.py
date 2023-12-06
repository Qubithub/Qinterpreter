import plotly.graph_objects as go
import numpy as np

# Define los puntos de la esfera de Bloch
theta = np.linspace(0, np.pi, 30)
phi = np.linspace(0, 2 * np.pi, 30)
theta, phi = np.meshgrid(theta, phi)
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

# Inicializa la figura
fig = go.Figure()

# Agrega la superficie de la esfera de Bloch
fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.2))

# Define los estados cuánticos y sus coordenadas
quantum_states = {
    '|0⟩': {'coords': [0, 0, 1], 'color': 'blue'},
    '|1⟩': {'coords': [0, 0, -1], 'color': 'red'},
    '|+⟩': {'coords': [1, 0, 0], 'color': 'green'},
    '|-⟩': {'coords': [0, 1, 0], 'color': 'orange'}
}

# Agrega los vectores de estado y sus etiquetas
for label, state_info in quantum_states.items():
    end_coords = state_info['coords']
    fig.add_trace(go.Scatter3d(
        x=[0, end_coords[0]], y=[0, end_coords[1]], z=[0, end_coords[2]],
        mode='lines',
        line=dict(color=state_info['color'], width=6),
        name=label
    ))
    fig.add_trace(go.Scatter3d(
        x=[end_coords[0]], y=[end_coords[1]], z=[end_coords[2]],
        mode='markers+text',
        text=label,
        textfont=dict(color=state_info['color'], size=18),
        marker=dict(color=state_info['color'], size=10),
        showlegend=False
    ))

# Configura la apariencia de la gráfica
fig.update_layout(
    title='Esfera de Bloch con Estados Cuánticos',
    scene=dict(
        xaxis=dict(showticklabels=False, zeroline=False),
        yaxis=dict(showticklabels=False, zeroline=False),
        zaxis=dict(showticklabels=False, zeroline=False),
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

# Muestra la figura
fig.show()
