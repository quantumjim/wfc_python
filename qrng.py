from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, execute, compile, IBMQ
from qiskit import Aer
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error

import numpy as np

def get_backend(device):
    """Returns backend object for device specified by input string."""
    try:
        backend = Aer.get_backend(device)
    except:
        print("You are using an IBMQ backend. The results for this are provided in accordance with the IBM Q Experience EULA.\nhttps://quantumexperience.ng.bluemix.net/qx/terms") # Legal stuff! Yay!
        backend = IBMQ.get_backend(device)
    return backend

def get_noise(noisy):
    """Returns a noise model when input is not False or None.
    A string will be interpreted as the name of a backend, and the noise model of this will be extracted.
    A float will be interpreted as an error probability for a depolarizing+measurement error model.
    Anything else (such as True) will give the depolarizing+measurement error model with default error probabilities."""
    if noisy:
        
        if type(noisy) is str: # get noise information from a real device (via the IBM Q Experience)
            device = get_backend(noisy)
            noise_model = noise.device.basic_device_noise_model( device.properties() )
        else: # make a simple noise model for a given noise strength
            if type(noisy) is float:
                p_meas = noisy
                p_gate1 = noisy
            else: # default values
                p_meas = 0.08
                p_gate1 = 0.04

            error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)]) # bit flip error with prob p_meas
            error_gate1 = depolarizing_error(p_gate1, 1) # replaces qubit state with nonsense with prob p_gate1
            error_gate2 = error_gate1.kron(error_gate1) # as above, but independently on two qubits

            noise_model = NoiseModel()
            noise_model.add_all_qubit_quantum_error(error_meas, "measure") # add bit flip noise to measurement
            noise_model.add_all_qubit_quantum_error(error_gate1, ["u1", "u2", "u3"]) # add depolarising to single qubit gates
            noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"]) # add two qubit depolarising to two qubit gates
            
    else:
        noise_model = None
    return noise_model

class qrng ():
    """This object generations `num` strings, each of `precision=8192/num` bits. These are then dispensed one-by-one as random integers, floats, etc, depending on the method called. Once all `num` strings are used, it'll loop back around."""
    def __init__( self, precision=None, num = 1280, sim=True, noisy=False, noise_only=False, verbose=True ):

        if precision:
            self.precision = precision
            self.num = int(np.floor( 5*8192/self.precision ))
        else:
            self.num = num
            self.precision = int(np.floor( 5*8192/self.num ))
        
        q = QuantumRegister(5)
        c = ClassicalRegister(5)
        qc = QuantumCircuit(q,c)
        if not noise_only:
            qc.h(q)
        qc.measure(q,c)
        
        if sim:
            backend=Aer.get_backend('qasm_simulator')
        else:
            IBMQ.load_accounts()
            backend=IBMQ.get_backend('ibmq_5_tenerife')
        
        if verbose and not sim:
            print('Sending job to quantum device')
        try:
            job = execute(qc,backend,shots=8192,noise_model=get_noise(noisy),memory=True)
        except:
            job = execute(qc,backend,shots=8192,memory=True)
        data = job.result().get_memory()
        if verbose and not sim:
            print('Results from device received')
        
        full_data = []
        for datum in data:
            full_data += list(datum)
        
        self.int_list = []
        self.bit_list = []
        n = 0
        for _ in range(num):
            bitstring = ''
            for b in range(self.precision):
                bitstring += full_data[n]
                n += 1
            self.bit_list.append(bitstring)
            self.int_list.append( int(bitstring,2) )
            
        self.n = 0
    
    def _iterate(self):
        
        self.n = self.n+1 % self.num
    
    def rand_int(self):
        
        rand_int = self.int_list[self.n]
        
        self._iterate()
        
        return rand_int
    
    def rand(self):
        
        rand_float = self.int_list[self.n] / 2**self.precision
        
        self._iterate()
        
        return rand_float