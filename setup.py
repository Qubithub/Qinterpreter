from setuptools import setup, find_packages

setup(
    name="quantumgateway",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "qiskit",
        "pennylane",
        "cirq",
        "pyquil",
        "amazon-braket-sdk"
    ],
)
