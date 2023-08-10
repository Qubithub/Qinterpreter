from math import pi

import math
import numpy as np
from quantumgateway.quantum_circuit import QuantumCircuit, QuantumGate
from quantumgateway.quantum_translator import QiskitTranslator
from quantumgateway.quantum_translator import CirqTranslator
from quantumgateway.quantum_translator import PennyLaneTranslator
from quantumgateway.quantum_translator import PyQuilTranslator
from quantumgateway.quantum_translator import BraketTranslator
from quantumgateway.main import translate_to_framework, simulate_circuit

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
pi = math.pi

# Part 1: function evaluation (f(x) = 7^x mod 15)
circ1 = QuantumCircuit(8,8)

# initial Hadamard gates
for i in range(4):
    circ1.add_gate(QuantumGate("H", [i]))

# apply the custom _7mod15 gate
circ1.add_gate(QuantumGate("X", [4]))
circ1.add_gate(QuantumGate("CNOT", [0, 5]))
circ1.add_gate(QuantumGate("CNOT", [0, 6]))
circ1.add_gate(QuantumGate("CNOT", [1, 4]))
circ1.add_gate(QuantumGate("CNOT", [1, 6]))
for i in range(4,8):
    circ1.add_gate(QuantumGate("Toffoli", [0, 1, i]))

# measure the auxiliary qubits
for i in range(4,8):
    circ1.add_gate(QuantumGate("MEASURE", [i, i]))

# Example usage
selected_framework = 'qiskit'  # Change this to the desired framework
translated_circuit1 = translate_to_framework(circ1, selected_framework)
translated_circuit1.print_circuit() 

print("The results of the first part of our simulated circuit are: ")
counts1 = simulate_circuit(circ1, selected_framework)

print(counts1)

# Extract the measurement results from the first part
measured_values1 = [int(k[4:], 2) for k in counts1.keys()] 

print("Measured values from the first part: ", measured_values1)


# Part 2: inverse Quantum Fourier Transform (QFT)
circ2 = QuantumCircuit(8,8)

# Initialize the control qubits of the second part with the measurement results from the first part
# You may need to modify this part depending on the measurement results and the specific behavior of your simulator
for i in range(4):
    if measured_values1[i] == 1:
        circ2.add_gate(QuantumGate("X", [i]))

# apply the QFT
n=4
for i in range(n-1, -1, -1):
    circ2.add_gate(QuantumGate("H", [i]))
    for j in range(i - 1, -1, -1): 
        circ2.add_gate(QuantumGate("CPHASE", [j, i], [pi/(2 ** (i - j))]))

for i in range(n // 2):
    circ2.add_gate(QuantumGate("SWAP", [i, n - i - 1]))

# measure the control qubits
for i in range(4):
    circ2.add_gate(QuantumGate("MEASURE", [i, i]))

translated_circuit2 = translate_to_framework(circ2, selected_framework)
translated_circuit2.print_circuit() 

print("The results of the second part of our simulated circuit are: ")
counts2 = simulate_circuit(circ2, selected_framework)

print(counts2)

# Extract the measurement results from the second part
measured_values2 = [int(k[:4], 2) for k in counts2.keys()]

print("Measured values from the second part: ", measured_values2)

#The period r is the greatest common divisor of the measured values
r = math.gcd(*measured_values2)

print("The period r is: ", r)

#Check if the period is suitable
#A suitable period is an even number and 7^(r/2) should not be equal to -1 or 1 modulo 15
if r % 2 == 0 and pow(7, r // 2, 15) not in [1, -1 % 15]:
    # Compute the factors of 15
    factor1 = math.gcd(pow(7, r // 2) - 1, 15)
    factor2 = math.gcd(pow(7, r // 2) + 1, 15)

    print("The factors of 15 are: ", factor1, " and ", factor2)
else:
    print("The period found is not suitable. Run the algorithm again.")