

from quantumgateway.quantum_circuit import QuantumCircuit, QuantumGate

from quantumgateway.quantum_translator.braket_translator import BraketTranslator
from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator

from quantumgateway.main import translate_to_framework, simulate_circuit

import math

# Inicialización del circuito cuántico
circuit = QuantumCircuit(4, 4)

# Aplicación de puertas Hadamard para la inicialización
for i in range(4):
    circuit.add_gate(QuantumGate("h", [i]))

# Función para añadir el Oracle de |1111|
def apply_oracle(circuit):
    pi = math.pi
    # Secuencia de puertas para el Oracle
    circuit.add_gate(QuantumGate("cphase", [0, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 1]))
    circuit.add_gate(QuantumGate("cphase", [1, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 1]))
    circuit.add_gate(QuantumGate("cphase", [1, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [1, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [1, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [pi/4]))

# Función para añadir el operador de amplificación
def apply_amplification(circuit):
    # Aplicar puertas Hadamard y X
    for i in range(4):
        circuit.add_gate(QuantumGate("h", [i]))
        circuit.add_gate(QuantumGate("x", [i]))

    # Secuencia de puertas para el operador de amplificación
    pi = math.pi
    circuit.add_gate(QuantumGate("cphase", [0, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 1]))
    circuit.add_gate(QuantumGate("cphase", [1, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 1]))
    circuit.add_gate(QuantumGate("cphase", [1, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [1, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [pi/4]))
    circuit.add_gate(QuantumGate("cnot", [1, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [-pi/4]))
    circuit.add_gate(QuantumGate("cnot", [0, 2]))
    circuit.add_gate(QuantumGate("cphase", [2, 3], [pi/4]))

    # Aplicar de nuevo puertas X y Hadamard
    for i in range(4):
        circuit.add_gate(QuantumGate("x", [i]))
        circuit.add_gate(QuantumGate("h", [i]))

# Aplicar Oracle y operador de amplificación
apply_oracle(circuit)
apply_amplification(circuit)

# Medición de los qubits
for i in range(4):
    circuit.add_gate(QuantumGate("measure", [i, i]))

# Aquí se añadirían las líneas para ejecutar la simulación y obtener los resultados
# utilizando las funciones proporcionadas por tu librería.
selected_framework = 'amazonbraket'  # Change this to the desired framework
translated_circuit = translate_to_framework(circuit, selected_framework)

translated_circuit.print_circuit() 


#Simulate the circuit and print the result
print("The results of our simulated circuit are: ")

print(simulate_circuit(circuit, selected_framework))
