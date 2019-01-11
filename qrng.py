from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit, Aer, execute
from qiskit import IBMQ, providers

class qrng ():
    
    def __init__( self, precision=16, num = 512, sim=True, verbose=True ):
        
        self.precision = precision
        self.num = num
        
        q = QuantumRegister(1)
        c = ClassicalRegister(1)
        qc = QuantumCircuit(q,c)
        qc.h(q)
        qc.measure(q,c)
        
        if sim:
            backend=Aer.get_backend('qasm_simulator')
        else:
            IBMQ.load_accounts()
            backend=IBMQ.get_backend('ibmq_5_tenerife')
        
        if verbose and not sim:
            print('Sending job to quantum device')
        job = execute(qc,backend,shots=precision*num,memory=True)
        data = job.result().get_memory()
        if verbose and not sim:
            print('Results from device received')
        
        self.int_list = []
        n = 0
        for _ in range(num):
            bitstring = ''
            for b in range(precision):
                bitstring += data[n]
                n += 1
            self.int_list.append( int(bitstring,2) )
            
        self.n = 0
        
    def rand_int(self):
        
        rand_int = self.int_list[self.n]
        
        self.n = self.n+1 % self.num
        
        return rand_int
    
    def rand(self):
        
        rand_float = self.int_list[self.n] / 2**self.precision
        
        self.n = (self.n+1) % self.num
        
        return rand_float