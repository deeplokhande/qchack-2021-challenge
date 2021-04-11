from typing import List, Tuple

import numpy as np
import cirq
import quantum_decomp

def matrix_to_sycamore_operations():
    # target_qubits: List[cirq.GridQubit], matrix: np.ndarray
# ) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    """A method to convert a unitary matrix to a list of Sycamore operations.

    This method will return a list of `cirq.Operation`s using the qubits and (optionally) ancilla
    qubits to implement the unitary matrix `matrix` on the target qubits `qubits`.
    The operations are also supported by `cirq.google.gate_sets.SYC_GATESET`.

    Args:
        target_qubits: list of qubits the returned operations will act on. The qubit order defined by the list
            is assumed to be used by the operations to implement `matrix`.
        matrix: a matrix that is guaranteed to be unitary and of size (2**len(qs), 2**len(qs)).
    Returns:
        A tuple of operations and ancilla qubits allocated.
            Operations: In case the matrix is supported, a list of operations `ops` is returned.
                `ops` acts on `qs` qubits and for which `cirq.unitary(ops)` is equal to `matrix` up
                to certain tolerance. In case the matrix is not supported, it might return NotImplemented to
                reduce the noise in the judge output.
            Ancilla qubits: In case ancilla qubits are allocated a list of ancilla qubits. Otherwise
                an empty list.
        .
    """
    # def T(n,a,b,x) :
    #     m = 2**(n-a)+2**(n-b)
    #     d = lambda i : 2**(n-x) if (2**(n-x)) & i == 0 else -(2**(n-x))
    #     T = np.array([([0] * 2**n)] * 2**n)
    #     for i in range(2**n) :
    #         for j in range(2**n) :
    #             T[i][j] = 1 if (i & m == m and j == d(i) + i) or (i & m != m and j == i) else 0
    #     return T
    
    
    # A=np.array([[1,1],[1,-1]])*(1/np.sqrt(2))
    # A=T(3,1,2,3)
    # A=np.identity(8)
    # A[7][7]=-1
    # print(type(A))

    A=cirq.unitary(cirq.CCX)
    print(A)

    temp=quantum_decomp.matrix_to_cirq_circuit(A=A)
    print(repr(temp))
    print(type(temp[0]))
    # temp2=quantum_decomp.matrix_to_gates(A)
    # print(temp2)
    out2=cirq.google.optimized_for_sycamore(temp,optimizer_type='sycamore')
    print(out2)
    out=[]
    converter = cirq.google.ConvertToSycamoreGates()
    for _ in out2.all_operations():
        # if isinstance(_,cirq.ops.controlled_operation.ControlledOperation): 
            # _
        print(type(_))
        out.append(converter.convert(_))
    print(out)
    return NotImplemented, []


matrix_to_sycamore_operations()
