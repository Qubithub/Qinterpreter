# main.py

from quantumgateway.quantum_translator.braket_translator import BraketTranslator
from quantumgateway.quantum_translator.cirq_translator import CirqTranslator
from quantumgateway.quantum_translator.qiskit_translator import QiskitTranslator
from quantumgateway.quantum_translator.pennylane_translator import PennyLaneTranslator
from quantumgateway.quantum_translator.pyquil_translator import PyQuilTranslator

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
