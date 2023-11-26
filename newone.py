from pyquil import Program
from pyquil.gates import H, CNOT
from pyquil.api import WavefunctionSimulator

from pyquil import Program
from pyquil.gates import H, CNOT
from pyquil.api import WavefunctionSimulator
import matplotlib.pyplot as plt
import numpy as np


# Crea un programa cuántico
p = Program()

# Asume que los qubits 0 y 1 son los qubits en los que quieres preparar el estado de Bell
q0 = 0
q1 = 1

# Aplica una puerta de Hadamard a q0 para crear una superposición
p += H(q0)

# Aplica una puerta CNOT con q0 como control y q1 como objetivo para entrelazar los qubits
p += CNOT(q0, q1)

# Ahora, el estado de los qubits q0 y q1 es un estado de Bell.

# Crea un simulador de función de onda
wavefunction_simulator = WavefunctionSimulator()

# Simula el programa
wavefunction = wavefunction_simulator.wavefunction(p)

# Imprime la función de onda resultante (que representa el estado cuántico de los qubits)
print(wavefunction)

probabilities = np.abs(wavefunction.amplitudes)**2

# Etiquetas para los estados basales
labels = ['00', '01', '10', '11']

# Crea un "histograma" de las probabilidades
plt.bar(labels, probabilities)
plt.xlabel('Estados')
plt.ylabel('Probabilidad')
plt.show()