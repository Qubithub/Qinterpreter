import pennylane as qml
import numpy as np
from quantumgateway.quantum_translator.quantum_translator import QuantumTranslator

class PennyLaneTranslator:
    def __init__(self):
        self.gates = []
        self.measurements = []  # keep track of measurements
    
    def quantum_function(self, params=None):
        if params is None:
            params = []
        for gate in self.gates:
            target = gate.qubits[0]
            if gate.name.lower() == "x":
                qml.PauliX(wires=target)
            elif gate.name.lower() == "y":
                qml.PauliY(wires=target)
            elif gate.name.lower() == "z":
                qml.PauliZ(wires=target)
            elif gate.name.lower() == "h":
                qml.Hadamard(wires=target)
            elif gate.name.lower() == "ry":
                qml.RY(gate.params[0], wires=target)
            elif gate.name.lower() == "rx":
                qml.RX(gate.params[0], wires=target)
            elif gate.name.lower() == "rz":
                qml.RZ(gate.params[0], wires=target)
            elif gate.name.lower() == "t":
                qml.T(wires=target)
            elif gate.name.lower() == "t_inv":
                qml.adjoint(qml.T)(wires=target)
            elif gate.name.lower() == "cnot":
                control, target = gate.qubits
                qml.CNOT(wires=[control, target])
            elif gate.name.lower() == "toffoli":
                control1, control2, target = gate.qubits
                qml.Toffoli(wires=[control1, control2, target])
            elif gate.name.lower() == "u3":
                theta, phi, lam = gate.params
                qml.U3(theta, phi, lam, wires=target)
            elif gate.name.lower() == "swap":
                qml.SWAP(wires=gate.qubits)
            elif gate.name.lower() == "cphase":
                qml.CRot(gate.params[0], 0, 0, wires=gate.qubits)
            elif gate.name.lower() == "measure":
                self.measurements.append(target)
            # Perform measurements if specified
    
        measurement_results = None

        if self.measurements:
            measurement_results = [qml.sample(qml.PauliZ(wires=i)) for i in self.measurements]
        else:
            measurement_results = qml.state()  # return the quantum state if no measurements are specified
        
        return measurement_results

    def translate(self, circuit):
        self.circuit = circuit
        self._translate_gates()
        self.num_qubits = circuit.num_qubits
        return self

    def simulate(self, shots=1000):
        #Plotting the result in the big-indian notation
        dev = qml.device('default.qubit', wires=self.num_qubits, shots=shots)
        qnode = qml.QNode(self.quantum_function, dev)
        measurement_results = qnode([])

        if self.measurements:
            #binary_results = [''.join('1' if bit == -1 else '0' for bit in result) for result in measurement_results.T]
            binary_results = [''.join('1' if bit == -1 else '0' for bit in result)[::-1] for result in measurement_results.T]

            #binary_results = [''.join('1' if bit == 1 else '0' for bit in result) for result in measurement_results.T]

            unique, counts = np.unique(binary_results, return_counts=True)
            result = dict(zip(unique, counts))
        else:
            result = measurement_results

        return result
    def _translate_gates(self):
        self.gates = self.circuit.gates

    def print_circuit(self):
        dev = qml.device('default.qubit', wires=self.num_qubits)

        # Apply the qml.draw transform to your quantum function
        drawn_quantum_function = qml.draw(self.quantum_function)

        # The drawn function now returns the string representation of the circuit
        print(drawn_quantum_function())

