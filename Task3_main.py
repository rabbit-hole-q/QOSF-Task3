"""
Chris Um Task 3

This is the main (required) portion of Task 3.
I believe this task sets an introduction how one
can apply basic quantum gates and simulate a
quantum circuit. I initialized my_circuit as stated in the github
page, and I have initialized the number of qubits to 4.
For single-qubit gates, I included X,Y,Z, and H gates.
I included CNOT only for two-qubit gate.
I have also included the existence of U3, parametrized gates
in this task.
My code has three following values that are generalized:
number of qubits, number of gates in the input program,
and number of total qubits.

"""




import numpy as np
import random 
import math
P0x0 = np.array([[1,0],[0,0]]) # \ket{0}\bra{0} Projection
P1x1 = np.array([[0,0],[0,1]]) # \ket{1}\bra{1} Projection
X = np.array([[0,1],[1,0]]) # X-gate
Y = np.array([[0,complex(0,-1)],
              [complex(0,1),0]]) # Y-gate
Z = np.array([[1,0],[0,1]]) #Z-gate
I = np.array([[1,0],[0,1]]) # size 2 Identity
H = (1/math.sqrt(2))*np.array([[1,1],[1,-1]])
def get_ground_state(num_qubits):
    
    # num_qubits = number of qubits represented
    # generates a column vector (ground state)
    
    return np.array([[1]+[0]*(2**num_qubits-1)]).T

def get_operator1(total_qubits, gate_unitary, target_qubits):
    
    if(len(target_qubits) == 2): # distinguishes (filters) CNOT gates
        if(target_qubits[0] == 0): # if control qubit is 0
            init_operator1 = P0x0 # control projection
            init_operator2 = P1x1 # target projection
          
        if(target_qubits[1] == 0): # if target qubit is 0
            init_operator1 = I # target is not affected 
            init_operator2 = X # target is affected
            
        if(target_qubits[0] != 0 and target_qubits[1] != 0): # if neither
            init_operator1 = I # uninvolved is not affected
            init_operator2 = I # uninvolved is not affected
            
        for x in range(1, int(total_qubits)): # excluding 0 case
            if (target_qubits[0] == x): # if control qubit is x
                init_operator1 = np.kron(init_operator1, P0x0) 
                init_operator2 = np.kron(init_operator2, P1x1)
            if(target_qubits[1] == x): # if target qubit is x
                init_operator1 = np.kron(init_operator1, I)
                init_operator2 = np.kron(init_operator2, X)
            if(target_qubits[0] != x and target_qubits[1] != x): # if neither
                init_operator1 = np.kron(init_operator1, I) 
                init_operator2 = np.kron(init_operator2, I)
        return init_operator1+init_operator2 # CNOT
    
    # We now include single-qubit gate cases
    
    if(len(target_qubits) == 1): 
        if(gate_unitary == "x"):
            gate_unitary = X
        if(gate_unitary == "y"):
            gate_unitary = Y
        if(gate_unitary == "z"):
            gate_unitary = Z
        if(target_qubits[0] == 0):
            init_operator = gate_unitary
        else:
            init_operator = I
        for x in range(1, int(total_qubits)):
            if(target_qubits[0] == x):
                init_operator = np.kron(init_operator, gate_unitary)
            else:
                init_operator = np.kron(init_operator, I)
        return init_operator


def get_operator(total_qubits, gate_unitary, param1, param2, param3, target_qubits):
    
    # get_operator for parametrized gates (U3)
    # we return an unitary operator in which U3 is appropriately
    # applied to the desired target qubit.
    # param1 : theta | param2: phi | param3: lambda
    
    u3 = [[complex(math.cos(param1/2),0),-complex(math.cos(param3),math.sin(param3))*
           complex(math.sin(param1/2),0)],[complex(math.cos(param2),math.sin(param2))*
           complex(math.sin(param1/2),0), complex(math.cos(param3+param2), math.sin(param3+param2))*
           complex(math.cos(param1/2),0)]]
    if(target_qubits[0] == 0):
        init_operator = u3
    else: 
        init_operator = I
    for x in range(1, int(total_qubits)):
         if(target_qubits[0] == x):
            init_operator = np.kron(init_operator, u3)
         else:
            init_operator = np.kron(init_operator, I)
    return init_operator           
        
def run_program(initial_state, program):
    
    # since the desired unitary operator is calculated from
    # get _operator, run_program just multiplies the calculated operator
    # with the desired parameters in the defined program ("my_circuit")
    
    answer = initial_state
    totalq = np.log2(len(initial_state))
    for dict in program:
        if(dict["gate"] == "u3"):
            answer = np.dot(get_operator(totalq, dict["gate"], dict["params"]["theta"],
                    dict["params"]["phi"],dict["params"]["lambda"], dict["target"]),answer)
        else:
            answer = np.dot(get_operator1(totalq, dict["gate"], dict["target"]),answer)
    return answer

def decimalToBinary(n):
    #since our quantum states are tensor products of qubits only,
    #the states will be in binary
    
    return bin(n).replace("0b", "")

def complexx(final_state):
    #converts amplitudes to probabilities
    
    for x in range(len(final_state)):
        final_state[x] = abs(final_state[x])**2
        
def get_counts(final_state, itr):
    # We count the frequency of each classical state outputted from
    # our measurement. We are essentially using a random sampling
    # distribution to infer the true amplitude distribution
    # of our final_state. Since we can not directly "observe"
    # amplitudes as they collapse to a classical state upon
    # measurement, this random sampling method is used instead,
    # meaning that as k increases, the accuracy increases.
    
    statee = []
    final = []
    complexx(final_state)
    for x in range(len(final_state)):
        statee.append(decimalToBinary(x))
    
    result = random.choices(statee, weights = final_state, k=1000) #random sampling
    for x in range(len(final_state)):
        final.append(result.count(statee[x]))
        print(str(statee[x]) + ": " + str(final[x]) +"\n")


my_circuit = [{ "gate": "u3", "params": { "theta":1, "phi": 2, "lambda":-1}, "target":[0] },
              { "gate": "cx", "target": [0,1] }]

final_state = run_program(get_ground_state(4), my_circuit)

get_counts(final_state, 1000)


