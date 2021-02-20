# QOSF Assessment Task 3
<p>Download <a href = "https://github.com/jrrhuang/QOSF_Application/blob/main/HuangJ_package.zip?raw=true">here</a></p>

## Summary
In this task, we are introduced to implement a simple quantum circuit with single-qubit and Controlled-NOT gates, demonstrating our underestanding of basic principles of
quantum computing and unitary operators. Programming quantum circuits allows one to generalize their gates and target qubits, which is crucial in desiging and implementing actual 
quantum algorithms. We include a parametrized single-qubit gate, which in principle can transform our initial state to any point on the Bloch sphere. Using parameters to alter the entries in the matrix rather than changing the matrices itself as a whole 
gives us more efficiency when trying to find for most optimal operators in a given problem. We even perform a simple case of a variational quantum algorithm that finds the optimal set of parameters that results in 
the objective function to reach its mininum. The measurement steps included in the task
conveys an interesting insight as one uses a random sampling method to statistically infer the amplitude of the desired quantum state. Since measurement of a quantum state immediately results in its collapse
to a classical state, the amplitudes can not be directly computed out.  Overall, this task gives one a solid understanding of how one can build quantum algorithms. 

## Techniques
- Measurement<br/>
- Adapting global parameters in implementing the variational quantum algorithm<br/>
- Efficiently converting unitary operators depending on control and target qubits. 
