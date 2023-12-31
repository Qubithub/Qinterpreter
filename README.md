# quantumgateway
Project: Quantum Interpreter

This project was elaborated by Wilmer Contreras Sepulveda, in the 5th month of the year 2023 at the Wilmer laboratories, you can find him in the linkedin profile: https://www.linkedin.com/in/contreraswilmer/.


This repository contains an implementation of a high-level interpreter for various quantum computing libraries, including Qiskit, Pyquil, Cirq, PennyLane, and Amazon Braket.

Overview
The goal of this project is to simplify the usage of different quantum libraries by providing a unified, high-level interface. This allows developers and researchers to focus on designing quantum algorithms, rather than the specifics of each quantum library.

Features
High-level syntax for defining quantum circuits.
Support for different quantum libraries: Qiskit, Pyquil, Cirq, PennyLane, and Amazon Braket.
Quantum algorithm templates for commonly used quantum algorithms.
Prerequisites
Before starting, make sure to install the quantum libraries supported by the interpreter:

Qiskit
Pyquil
Cirq
PennyLane
Amazon Braket
The installation instructions for each library can be found on their respective websites.

Usage
To use the interpreter, import the main module:


    from quantumgateway.quantum_circuit import QuantumCircuit, QuantumGate
    from quantumgateway.quantum_translator.braket_translator import BraketTranslator
    from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
    from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
    from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
    from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator
    from quantumgateway.main import translate_to_framework, simulate_circuit

Next, create an instance of the interpreter, specifying the target library:


    n=8
    circuit = QuantumCircuit(n,n)  
    circuit.add_gate(QuantumGate("x", [0]))
    circuit.add_gate(QuantumGate("X", [1]))
    circuit.add_gate(QuantumGate("h", [1]))
    circuit.add_gate(QuantumGate("X", [2]))
    circuit.add_gate(QuantumGate("X", [3]))

    #circuit.add_gate(QuantumGate("CPHASE", [0,1],[3*math.pi/4]))


    # measure the auxiliary qubits
    for i in range(8):
        circuit.add_gate(QuantumGate("MEASURE", [i, i]))



Finally, use the interpreter's methods to define and execute quantum circuits:


    # Example usage
    selected_framework = 'amazonbraket'  # Change this to the desired framework
    translated_circuit = translate_to_framework(circuit, selected_framework)

    translated_circuit.print_circuit() 
    # Simulate the circuit and print the result
    print("The results of our simulated circuit are: ")
    print(simulate_circuit(circuit, selected_framework))




Contributing
We welcome contributions to this project. If you're interested in contributing, please see the CONTRIBUTING.md file for guidelines.

License
This project is licensed under the MIT License. See the LICENSE file for more details.#   Q i n t e r p r e t e r 
 
 
