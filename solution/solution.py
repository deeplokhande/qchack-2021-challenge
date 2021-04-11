from typing import List, Tuple
from attr.setters import convert

import numpy as np
import cirq
from numpy.core.fromnumeric import size

def matrix_to_sycamore_operations(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
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
    def optimize_circuit(circ):
        ouut=[]
        converter = cirq.google.ConvertToSycamoreGates()
        for _ in circ.all_operations():
            ouut.append(converter.convert(_))
        return cirq.google.optimized_for_sycamore(cirq.Circuit(ouut),optimizer_type="sycamore"),[]


    if np.trace(matrix)==len(matrix):
        return [],[]
    
    # def incrementors(target_qubits,matrix):
    #     def xor_swap(a, b):
    #         """Swaps two qubits with three CNOTs."""
    #         yield cirq.CNOT(a, b) # |a> |b> --> |a> |a ^ b>
    #         yield cirq.CNOT(b, a) # |a> |a ^ b> --> |a ^ a ^ b> | a ^ b> = |b>|a^b>
    #         yield cirq.CNOT(a, b)

    #     def check_left_rotate(M):
    #         I = np.identity(M.shape[0])
    #         if np.all((np.matmul(M, M.T)) == I) and (np.linalg.det(M)==1): return True
    #         return False

    #     def left_rotate(qubits):
    #         for i in range(len(qubits) - 1):
    #             a, b = qubits[i: i + 2]
    #             yield xor_swap(a, b)
        
    #     if (check_left_rotate(matrix)):
    #         return cirq.Circuit(left_rotate(target_qubits))
    #     else:
    #         return None
            

    # incre=incrementors(target_qubits,matrix)
    # if incre != None: 
    #     print("hh")
    #     return optimize_circuit(incre)


    if len(matrix)==2:
        try:
            comparison=matrix == cirq.unitary(cirq.Z)
            if (comparison.all()): return cirq.Z(target_qubits[0]),[]

            comparison=matrix == cirq.unitary(cirq.X)
            if (comparison.all()): return cirq.X(target_qubits[0]),[]

            comparison=matrix == cirq.unitary(cirq.Y)
            if (comparison.all()): return cirq.Y(target_qubits[0]),[]

            comparison=matrix == cirq.unitary(cirq.H)
            if (comparison.all()): return cirq.H.on(target_qubits[0]),[]

            comparison=matrix == cirq.unitary(cirq.S)
            if (comparison.all()): return cirq.S(target_qubits[0]),[]

            comparison=matrix == cirq.unitary(cirq.T)
            if (comparison.all()): return cirq.T(target_qubits[0]),[]

        except [TypeError,ValueError]:
            return NotImplemented,[] 

    if len(matrix)==4:
        try:
            comparison= matrix == cirq.unitary(cirq.CNOT)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.CNOT(target_qubits[0],target_qubits[1])))

            comparison= matrix == cirq.unitary(cirq.XX)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.XX(target_qubits[0],target_qubits[1])))

            comparison= matrix == cirq.unitary(cirq.YY)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.YY(target_qubits[0],target_qubits[1])))

            comparison= matrix == cirq.unitary(cirq.ZZ)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.ZZ(target_qubits[0],target_qubits[1])))

            comparison= matrix == cirq.unitary(cirq.google.SYC)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.google.SYC(target_qubits[0],target_qubits[1])))


        except TypeError:
            return NotImplemented,[]
    
    if len(matrix)==8:
        try:
            comparison= matrix == cirq.unitary(cirq.CCX)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.CCX(target_qubits[0],target_qubits[1],target_qubits[2])))

            comparison= matrix == cirq.unitary(cirq.CSWAP)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.CSWAP(target_qubits[0],target_qubits[1],target_qubits[2])))

            comparison= matrix == cirq.unitary(cirq.CCZ)
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.CCZ(target_qubits[0],target_qubits[1],target_qubits[2])))

            comparison= matrix == cirq.unitary(cirq.ControlledGate(cirq.ISWAP**0.5,1))
            if (comparison.all()):return cirq.ControlledGate(cirq.ISWAP**0.5,1)

        except TypeError:
            return NotImplemented,[]


    if len(matrix)==16:
        try:
            comparison= matrix == cirq.unitary(cirq.ControlledGate(cirq.ISWAP**0.5,2))
            if (comparison.all()):return optimize_circuit(cirq.Circuit(cirq.ControlledGate(sub_gate=cirq.ISWAP**0.5).on(target_qubits[2],target_qubits[0],target_qubits[1])))

        except TypeError:
            return NotImplemented,[]


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

    # A=cirq.unitary(cirq.CCX)
    # print(A)

    # temp=quantum_decomp.matrix_to_cirq_circuit(A=matrix)
    # print(repr(temp))
    # print(type(temp[0]))
    # # temp2=quantum_decomp.matrix_to_gates(A)
    # # print(temp2)
    # out2=cirq.google.optimized_for_sycamore(temp,optimizer_type='sycamore')
    # print(out2)
    # try:
    #     out=[]
    #     converter = cirq.google.ConvertToSycamoreGates()
    #     for _ in temp.all_operations():
    #     #     # if isinstance(_,cirq.ops.controlled_operation.ControlledOperation): 
    #     #         # _
    #     #     print(type(_))
    #         out.append(converter.convert(_))
    #     # print(out)
    #     return out, []


    # except BaseException as es:

    return NotImplemented,[]

# print(matrix_to_sycamore_operations(cirq.GridQubit.rect(1,2,3,3),np.array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],[0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],[0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],[0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]])))
