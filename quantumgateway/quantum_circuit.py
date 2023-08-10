# quantum_circuit.py
class QuantumCircuit:
    def __init__(self, num_qubits, num_classical_bits=0):
        self.num_qubits = num_qubits
        self.num_classical_bits = num_classical_bits
        self.gates = []

    def add_gate(self, gate):
        self.gates.append(gate)

class QuantumGate:
    def __init__(self, name, qubits, params=None):
        self.name = name
        self.qubits = qubits
        self.params = params if params else []
