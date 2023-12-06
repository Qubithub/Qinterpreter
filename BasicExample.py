

from quantumgateway.quantum_circuit import QuantumCircuit, QuantumGate

from quantumgateway.quantum_translator.braket_translator import BraketTranslator
from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator

from quantumgateway.main import translate_to_framework, simulate_circuit, bloch_sphere

import math
circuit = QuantumCircuit(2,2)  

circuit.add_gate(QuantumGate("x", [0]))
circuit.add_gate(QuantumGate("x", [1]))
circuit.add_gate(QuantumGate("h", [1]))
circuit.add_gate(QuantumGate("cphase", [0, 1], [math.pi/4]))

bloch_sphere(circuit)



circuit.add_gate(QuantumGate("MEASURE", [0,0]))
circuit.add_gate(QuantumGate("MEASURE", [1,1]))


selected_framework = 'pennylane'  # Change this to the desired framework
translated_circuit = translate_to_framework(circuit, selected_framework)

translated_circuit.print_circuit() 


#Simulate the circuit and print the result
print("The results of our simulated circuit are: ")

print(simulate_circuit(circuit, selected_framework))

