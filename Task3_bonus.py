"""

Chris Um Task 3 Bonus (Variational Quantum Algorithm)

"""


import numpy as np
import math
import random
from scipy.optimize import minimize


I = np.array([[1,0],[0,1]])

def get_ground_state(num_qubits):
    # getting a column vector representing our quantum state
    return np.array([[1]+[0]*(2**num_qubits-1)]).T

def get_operator(total_qubits, gate_unitary, param1, param2, param3, target_qubits):
    
    # get_operator for parametrized gates (U3)
    # we return an unitary operator in which U3 is appropriately
    # applied to the desired target qubit.
    # param1 : theta | param2: phi | param3: lambda
    
    
    if(gate_unitary == "u3"):
        u3 = [[complex(math.cos(param1/2),0),-complex(math.cos(param3),math.sin(param3))*complex(math.sin(param1/2),0)],[complex(math.cos(param2),math.sin(param2))*complex(math.sin(param1/2),0), complex(math.cos(param3+param2),math.sin(param3+param2))*complex(math.cos(param1/2),0)]]
        if(target_qubits[0] == 0):
            init_operator = u3
        else: 
            init_operator = I
        for x in range(1, int(total_qubits)):
            if(target_qubits[0] == x):
                init_operator = np.kron(init_operator, fff)
            else:
                init_operator = np.kron(init_operator, I)
        return init_operator
    
def decimalToBinary(n):
    #since our quantum states are tensor products of qubits only,
    #the states will be in binary
    
    return bin(n).replace("0b", "")
def complexx(final_state):
    #converts amplitudes to probabilities
    
    for x in range(len(final_state)):
        final_state[x] = abs(final_state[x])**2
def run_program(my_qpu, program, parram):
    # since the desired unitary operator is calculated from
    # get _operator, run_program just multiplies the calculated operator
    # with the desired parameters in the defined program ("my_circuit")
    
    answer = my_qpu
    totalq = np.log2(len(my_qpu))
    for dict in program:
        answer = np.dot(get_operator(totalq, dict["gate"], parram["global_1"],parram["global_2"], dict["params"]["lambda"], dict["target"]),answer)
    return answer  
def get_counts(final_state, itr):
    
    # Different from get_counts in the main task,
    # we convert the string output into a
    # dictionary "emptyD" to be later converted
    # into "counts". This is necessary because now we
    # have to actually count the frequency of how many times
    # the quantum state collapsed to each classical state by
    # measurement.
    
    statee = []
    final = []
    emptyD = {}
    complexx(final_state)
    for x in range(len(final_state)):
        statee.append(decimalToBinary(x))
    
    result = random.choices(statee, weights = final_state, k=1000)
    for x in range(len(final_state)):
        final.append(result.count(statee[x]))
        emptyD[str(statee[x])] =  final[x]
    return emptyD

def objective_function(params):
    
    # Since the task has not defined what the
    # objective (cost) of our function be,
    # I decided that I would define cost
    # as the frequency of a certain classical
    # state when the final_state is measured
    # 1000 times.
    # This is a simplified example of a quantum annealing, where our goal is
    # to find the global minimum of an objective function.
    
    final_state = run_program(initial_state, my_circuit, {"global_1": params[0], "global_2": params[1] })
    
    counts = get_counts(final_state, 1000)
    
    cost = 0
    
    # We increase our cost by the number of "100"s
    # in emptyD (the set of 1000 classical states)
    
    
    if "100" in counts:
        cost += counts["100"]
        
    return cost

params = np.array([3.1415, 1.5708])
initial_state = get_ground_state(3)
my_circuit = [{"gate": "u3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda":-3.1415 }, "target": [0]}]

minimum = minimize(objective_function, params, method="Powell", tol=1e-6)

# Powell's method finds the optimal set of parameters that
# results in the objective function to output the lowest
# possible cost.

print(minimum)
    