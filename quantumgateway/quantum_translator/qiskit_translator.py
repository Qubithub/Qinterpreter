
from qiskit import Aer, execute
from quantumgateway.quantum_translator.quantum_translator import QuantumTranslator
import matplotlib as mpl
class QiskitTranslator(QuantumTranslator):
    def __init__(self):
        self.qc = None
        self.translated_circuit = None  # Add this

    def translate(self, hl_circuit):
        from qiskit import QuantumCircuit as QiskitQuantumCircuit

        self.qc = QiskitQuantumCircuit(hl_circuit.num_qubits, hl_circuit.num_classical_bits)
        
        for gate in hl_circuit.gates:
            if gate.name.lower() == "h":
                self.qc.h(gate.qubits[0])
            elif gate.name.lower() == "cnot":
                self.qc.cx(gate.qubits[0], gate.qubits[1])
            elif gate.name.lower() == "x":
                self.qc.x(gate.qubits[0])
            elif gate.name.lower() == "y":
                self.qc.y(gate.qubits[0])
            elif gate.name.lower() == "z":
                self.qc.z(gate.qubits[0])
            elif gate.name.lower() == "ry":
                self.qc.ry(gate.params[0], gate.qubits[0])
            elif gate.name.lower() == "rx":
                self.qc.rx(gate.params[0], gate.qubits[0])
            elif gate.name.lower() == "rz":
                self.qc.rz(gate.params[0], gate.qubits[0])
            elif gate.name.lower() == "toffoli":
                self.qc.ccx(gate.qubits[0], gate.qubits[1], gate.qubits[2])
            elif gate.name.lower() == "swap":
                self.qc.swap(gate.qubits[0], gate.qubits[1])
            elif gate.name.lower() == "cphase":
                self.qc.cp(gate.params[0], gate.qubits[0], gate.qubits[1])
            elif gate.name.lower() == "measure":
                self.qc.measure(gate.qubits[0], gate.qubits[1])
        self.translated_circuit = self.qc  
        return self  # And return self instead of self.qc

    def simulate(self, shots=1000):
        simulator = Aer.get_backend('qasm_simulator')
        job = execute(self.qc, simulator, shots=shots)
        result = job.result()
        counts = result.get_counts(self.qc)
        # Convert keys to big-endian format
        big_endian_counts = {k[::-1]: v for k, v in counts.items()}
        return counts
    
    def print_circuit(self):
        print(self.translated_circuit.draw())

#--------------------------------------------------------------
