from quantumgateway.quantum_translator.quantum_translator import QuantumTranslator
from pyquil import Program
from pyquil.gates import H, CNOT, RX, RY, RZ, CCNOT, X, Y, Z, MEASURE, SWAP, CPHASE
from pyquil.quil import MemoryReference  # Import MemoryReference
from pyquil.api import WavefunctionSimulator
from pyquil import get_qc
from collections import Counter
from pyquil.quilbase import Gate


class PyQuilCircuit:
    def __init__(self, program):
        self.program = program

    def print_circuit(self):
        print(self.program)

    def simulate(self, shots=100):
        from pyquil.api import get_qc
        from pyquil.quilbase import Gate, Declare
        from pyquil.quil import address_qubits
        from collections import Counter

        # Connect to the Quantum Virtual Machine (QVM)
        qc = get_qc('9q-square-qvm')  # Or another QVM type as needed

        # Declare classical register only if not already declared
        ro_exists = any([isinstance(instr, Declare) and instr.name == 'ro' for instr in self.program.instructions])
        if not ro_exists:
            num_qubits = max([gate.qubits[-1].index for gate in self.program.instructions if isinstance(gate, Gate)]) + 1
            ro = self.program.declare('ro', 'BIT', num_qubits)

        # Compile the program
        compiled_program = qc.compile(address_qubits(self.program))

        # Initialize results
        results = []

        # Execute the program on the QVM for the specified number of shots
        for _ in range(shots):
            # Run the program
            result = qc.run(compiled_program)
            # Convert each result to binary string and append to results
            #results.append(''.join(map(str, result.readout_data['ro'][0])))
            # Convert each result to binary string, reverse it to match Qiskit's bit ordering, and append to results
            results.append(''.join(map(str, result.readout_data['ro'][0]))[::-1])

        # Convert the results to a frequency distribution
        counts = Counter(results)
        
        return counts


class PyQuilTranslator(QuantumTranslator):
    def translate(self, hl_circuit):
        program = Program()
        qubits = list(range(hl_circuit.num_qubits))
        ro = program.declare('ro', 'BIT', hl_circuit.num_qubits)  # Declare classical register
        for gate in hl_circuit.gates:
            if gate.name.lower() == "h":
                program += H(qubits[gate.qubits[0]])
            elif gate.name.lower() == "x":
                program += X(qubits[gate.qubits[0]])
            elif gate.name.lower() == "y":
                program += Y(qubits[gate.qubits[0]])
            elif gate.name.lower() == "z":
                program += Z(qubits[gate.qubits[0]])
            elif gate.name.lower() == "cnot":
                program += CNOT(qubits[gate.qubits[0]], qubits[gate.qubits[1]])
            elif gate.name.lower() == "rx":
                program += RX(np.pi, qubits[gate.qubits[0]])
            elif gate.name.lower() == "ry":
                program += RY(gate.params[0], qubits[gate.qubits[0]])
            elif gate.name.lower() == "rx":
                program += RX(gate.params[0], qubits[gate.qubits[0]])
            elif gate.name.lower() == "rz":
                program += RZ(gate.params[0], qubits[gate.qubits[0]])
            elif gate.name.lower() == "toffoli":
                program += CCNOT(qubits[gate.qubits[0]], qubits[gate.qubits[1]], qubits[gate.qubits[2]])
            elif gate.name.lower() == "swap":
                program += SWAP(qubits[gate.qubits[0]], qubits[gate.qubits[1]])
            elif gate.name.lower() == "cphase":
                program += CPHASE(gate.params[0], qubits[gate.qubits[0]], qubits[gate.qubits[1]])
            elif gate.name.lower() == "measure":
                program += MEASURE(qubits[gate.qubits[0]], ro[gate.qubits[1]])  # Use ro instead of qubits
            # Add other gate translations as needed
        return PyQuilCircuit(program)


