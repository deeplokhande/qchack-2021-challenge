The solution written here is very naive, and brute force. Mostly inspired by the tests in the judge system. 

We intended to have a more generalized approach, but understanding the handling of the gates in Cirq, along with learnig decomposition of higher dimension operators, required a lot of time and thus we were not able to fully develop an algorithm to decompose all the unitary matrices.

We sought inspirations from various sources, like: 
1. Cirq Documentation.
2. Quantum-decomp package.
3. CSD technique
4. Quantum Computation and Quantum Information by Mike and Ike.
5. etc.

But understanding and implementing them with 2 more constraints of the limited gateset of the Google's SYCAMORE chipset and also the grid layout of the qubits. There was a lot to do, in less time, atleast for us who are relatively new to Google Cirq.

Nonetheless, the challenge was very interseting, and has definitely inspired some of use to create an open source function to convert all possible unitary matrices, although upto feasible compute strength.

Thanks Balint and Doug for all your help.

Hoping to see you around in future gatherings.!!

Regards,

Team QCHACKChallengers.
