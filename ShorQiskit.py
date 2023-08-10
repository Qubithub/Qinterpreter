from math import pi

import math
import numpy as np
from quantumgateway.quantum_circuit import QuantumCircuit, QuantumGate
from quantumgateway.quantum_translator.braket_translator import BraketTranslator
from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator
from quantumgateway.main import translate_to_framework, simulate_circuit

#-----------------------------------------------------------------------------
pi = math.pi
circ = QuantumCircuit(8,8)

# initial Hadamard gates
for i in range(4):
    circ.add_gate(QuantumGate("H", [i]))

# apply the custom _7mod15 gate
circ.add_gate(QuantumGate("X", [4]))
circ.add_gate(QuantumGate("CNOT", [0, 5]))
circ.add_gate(QuantumGate("CNOT", [0, 6]))
circ.add_gate(QuantumGate("CNOT", [1, 4]))
circ.add_gate(QuantumGate("CNOT", [1, 6]))
for i in range(4,8):
    circ.add_gate(QuantumGate("Toffoli", [0, 1, i]))

# measure the auxiliary qubits
for i in range(4,8):
    circ.add_gate(QuantumGate("MEASURE", [i, i]))

# apply the QFT
n=4
for i in range(n-1, -1, -1):
    circ.add_gate(QuantumGate("H", [i]))
    for j in range(i - 1, -1, -1): 
        circ.add_gate(QuantumGate("CPHASE", [j, i], [pi/(2 ** (i - j))]))

for i in range(n // 2):
    circ.add_gate(QuantumGate("SWAP", [i, n - i - 1]))

# measure the control qubits
for i in range(4):
    circ.add_gate(QuantumGate("MEASURE", [i, i+4]))




#-----------------------------------------------------------------------------

# Example usage
selected_framework = 'qiskit'  # Change this to the desired framework
translated_circuit = translate_to_framework(circ, selected_framework)
translated_circuit.print_circuit() 

print("The results of our simulated circuit are: ")
counts = simulate_circuit(circ, selected_framework)

print(counts)
#---------------------------------------------------------
from fractions import Fraction
import math

n_count = 4  # The number of counting qubits used

# Convert binary to decimal
measured_values = [int(k[:n_count], 2) for k in counts.keys()]

# Remove zeros from measured values
measured_values = list(set(m for m in measured_values if m != 0))

print("Measured values: ", measured_values)


factors = set()

# Try different values of a
for a in range(2, 15):
    #print("\nTrying a =", a)

    if math.gcd(a, 15) != 1:
        #print("Skipping", a, "since it shares a factor with N.")
        continue

    estimates = []
    found_period = False

    for m in measured_values:
        # Estimate s/r by m/2^n_count
        estimate = Fraction(m, 2**n_count)

        # The denominator of the fraction should be an estimate of r
        r = estimate.denominator
        #print("The estimated denominator is: ", r, " and the measured value is: ", m)
        estimates.append(r)

        # Check if a^r mod 15 equals 1
        if pow(a, r, 15) == 1:
            #print("The period r is: ", r)

            # Try to find factors of N using r
            factor1 = math.gcd(a**(r//2) + 1, 15)
            factor2 = math.gcd(a**(r//2) - 1, 15)

            if factor1 > 1 and factor1 not in factors:
                #print("Found factor: ", factor1)
                factors.add(factor1)
            if factor2 > 1 and factor2 not in factors:
                #print("Found factor: ", factor2)
                factors.add(factor2)

            found_period = True

    if not found_period:
        print("Did not find a period.")


line = "*" * 70 
print(line)
print("The factors of the number 15, using the Shor Algorithm are: ", factors)
print(line)
