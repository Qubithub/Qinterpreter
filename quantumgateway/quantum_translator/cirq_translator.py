
from quantumgateway.quantum_translator.quantum_translator import QuantumTranslator

import cirq
import numpy as np

class CirqCircuit:
    def __init__(self, circuit):
        self.circuit = circuit

    def print_circuit(self):
        print(self.circuit)

    def simulate(self, shots=1000):
        simulator = cirq.Simulator()
        result = simulator.run(self.circuit, repetitions=shots)
        # Combine the results into a binary string
        combined_results = {}
        num_qubits = len(list(self.circuit.all_qubits()))
        for i in range(shots):
            result_string = ''
            for j in range(num_qubits):
                key = 'result' + str(j)
                result_string += str(result.measurements[key][i][0])
            # Reverse the string to match Qiskit's bit ordering
            result_string = result_string[::-1]
            if result_string not in combined_results:
                combined_results[result_string] = 0
            combined_results[result_string] += 1
        return combined_results

    
class CirqTranslator(QuantumTranslator):
    def translate(self, hl_circuit):
        import cirq
        qubits = [cirq.LineQubit(i) for i in range(hl_circuit.num_qubits)]
        circuit = cirq.Circuit()
        for gate in hl_circuit.gates:
            if gate.name.lower() == "h":
                circuit.append(cirq.H(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "cnot":
                circuit.append(cirq.CNOT(qubits[gate.qubits[0]], qubits[gate.qubits[1]]))
            elif gate.name.lower() == "x":
                circuit.append(cirq.X(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "y":
                circuit.append(cirq.Y(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "z":
                circuit.append(cirq.Z(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "ry":
                circuit.append(cirq.ry(gate.params[0])(qubits[gate.qubits[0]]))
            # Add other gate translations as needed
            elif gate.name.lower() == "rx":
                circuit.append(cirq.rx(gate.params[0])(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "rz":
                circuit.append(cirq.rz(gate.params[0])(qubits[gate.qubits[0]]))
            elif gate.name.lower() == "toffoli":
                circuit.append(cirq.TOFFOLI(qubits[gate.qubits[0]], qubits[gate.qubits[1]], qubits[gate.qubits[2]]))
            elif gate.name.lower() == "swap":
                circuit.append(cirq.SWAP(qubits[gate.qubits[0]], qubits[gate.qubits[1]]))
            elif gate.name.lower() == "cphase":
                circuit.append(cirq.CZPowGate(exponent=gate.params[0]/np.pi)(qubits[gate.qubits[0]], qubits[gate.qubits[1]]))
            elif gate.name.lower() == "cz":
                circuit.append(cirq.CZ(cirq.LineQubit(gate.qubits[0]), cirq.LineQubit(gate.qubits[1])))
            elif gate.name.lower() == "cy":
                circuit.append(cirq.ControlledGate(cirq.Y).on(cirq.LineQubit(gate.qubits[0]), cirq.LineQubit(gate.qubits[1])))
            elif gate.name.lower() == "measure":
                meas_qubit = qubits[gate.qubits[0]]
                #print(f"Measuring qubit: {gate.qubits[0]}")  # Add this line for debugging
                key = 'result' + str(gate.qubits[0])
                circuit.append(cirq.measure(meas_qubit, key=key))

        return CirqCircuit(circuit)  # Here, return a CirqCircuit object

