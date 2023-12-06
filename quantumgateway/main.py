# main.py

from quantumgateway.quantum_translator.braket_translator import BraketTranslator
from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator



from qiskit.quantum_info import Statevector
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector, partial_trace, DensityMatrix
from qiskit.quantum_info.operators import Operator
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def translate_to_framework(circuit, framework):
    if framework.lower() == 'qiskit':
        translator = QiskitTranslator()
    elif framework.lower() == 'cirq':
        translator = CirqTranslator()
    elif framework.lower() == 'pennylane':
        translator = PennyLaneTranslator()
    elif framework.lower() == 'pyquil':
        translator = PyQuilTranslator()
    elif framework.lower() == 'amazonbraket':
        translator = BraketTranslator()
    else:
        raise ValueError("Invalid framework name. Please choose from 'qiskit', 'cirq', 'pennylane', 'pyquil', 'amazonbraket'.")

    translated_circuit = translator.translate(circuit)
    return translated_circuit

def simulate_circuit(circuit, framework):
    if framework.lower() == 'qiskit':
        translator = QiskitTranslator()
    elif framework.lower() == 'cirq':
        translator = CirqTranslator()
    elif framework.lower() == 'pennylane':
        translator = PennyLaneTranslator()
    elif framework.lower() == 'pyquil':
        translator = PyQuilTranslator()
    elif framework.lower() == 'amazonbraket':
        translator = BraketTranslator()
    else:
        raise ValueError("Invalid framework name. Please choose from 'qiskit', 'cirq', 'pennylane', 'pyquil', 'amazonbraket'.")

    translated_circuit = translator.translate(circuit)
    
    # Call simulate on the translated_circuit, not on the translator
    results = translated_circuit.simulate()
    
    return results





def bloch_sphere(circuit):
    # Translate the high-level circuit to a Qiskit circuit
    translator = QiskitTranslator()
    translator.translate(circuit)
    qiskit_circuit = translator.qc

    # Simulate the circuit using the statevector simulator
    backend = Aer.get_backend('statevector_simulator')
    job = execute(qiskit_circuit, backend)
    result = job.result()
    statevector = result.get_statevector()

    # Number of qubits
    num_qubits = qiskit_circuit.num_qubits

    # Initialize the figure for plotting
    fig = make_subplots(rows=1, cols=num_qubits, specs=[[{'type': 'surface'}] * num_qubits],
                        subplot_titles=[f'Qubit {i}' for i in range(num_qubits)])

    # Define markers for |0>, |1>, |+>, and |->
    markers = {
        '|0⟩': [0, 0, 1],
        '|1⟩': [0, 0, -1],
        '|+⟩': [1, 0, 0],
        '|−⟩': [-1, 0, 0]
    }

    # Pauli matrices
    X = Operator.from_label('X')
    Y = Operator.from_label('Y')
    Z = Operator.from_label('Z')

    for qubit_index in range(num_qubits):
        # Calculate the reduced density matrix for each qubit
        rho = partial_trace(Statevector(statevector), [qubit_index])

        # Calculate the Bloch vector components
        x = np.real(np.trace(np.dot(X.to_matrix(), rho)))
        y = np.real(np.trace(np.dot(Y.to_matrix(), rho)))
        z = np.real(np.trace(np.dot(Z.to_matrix(), rho)))

        # Sphere coordinates for the Bloch sphere
        theta = np.linspace(0, np.pi, 30)
        phi = np.linspace(0, 2 * np.pi, 30)
        theta, phi = np.meshgrid(theta, phi)
        sphere_x = np.sin(theta) * np.cos(phi)
        sphere_y = np.sin(theta) * np.sin(phi)
        sphere_z = np.cos(theta)

        # Add sphere surface
        fig.add_trace(go.Surface(x=sphere_x, y=sphere_y, z=sphere_z, colorscale='Blues', opacity=0.2, showscale=False), row=1, col=qubit_index + 1)

        # Add Bloch vector
        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode='lines+markers',
            line=dict(color='black', width=2),
            marker=dict(size=4, color='red'),
            name=f'Qubit {qubit_index}',
            showlegend=False
        ), row=1, col=qubit_index + 1)

        # Add axis markers for |0>, |1>, |+>, and |->
        for label, position in markers.items():
            fig.add_trace(go.Scatter3d(
                x=[position[0]], y=[position[1]], z=[position[2]],
                mode='markers+text',
                marker=dict(size=5, color='blue'),
                text=label,
                textposition='bottom center',
                showlegend=False
            ), row=1, col=qubit_index + 1)

    # Update layout for a better view
    fig.update_layout(
        title='Bloch Spheres for Each Qubit',
        margin=dict(l=0, r=0, b=0, t=50)
    )

    # Show the figure
    fig.show()

# Example usage
# Define your quantum circuit here using the high-level API and then pass it to bloch_sphere
