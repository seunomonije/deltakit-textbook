from math import floor, comb
import numpy as np
import matplotlib.pyplot as plotter; plotter.rcParams['font.family'] = 'Monospace'
import cirq
from myMWPM import MWPMDecoder1D
from tqdm import tqdm

def create_repetition_code_encoder(n_qubits):

    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    # The first qubit holds the quantum state
    for i in range(1, n_qubits):
        circuit.append(cirq.CNOT(qubits[0], qubits[i]))

    return circuit

def get_syndrome_measurement(qubits, ancilla_qubits, repcode_type = 'Z'):

    syndrome_measurement = []

    if repcode_type == 'Z': # bit-flip rep codes using ZZ stabilizers
        for i in range(len(qubits) - 1):
            # Extract the parity of qubits i and i+1 onto ancillary qubit i
            syndrome_measurement.append(cirq.CNOT(qubits[i], ancilla_qubits[i]))
            syndrome_measurement.append(cirq.CNOT(qubits[i+1], ancilla_qubits[i]))
    elif repcode_type == 'X': # phase-flip rep codes -- detected by turning phase flips to bit flips
        for i in range(len(qubits) - 1):
            # Extract the parity of qubits i and i+1 onto ancillary qubit i
            syndrome_measurement.append(cirq.CNOT(qubits[i], ancilla_qubits[i]))
            syndrome_measurement.append(cirq.CNOT(qubits[i+1], ancilla_qubits[i]))
        
    # Measure the ancilla qubits to extract the syndrome
    syndrome_measurement.append(cirq.measure(*ancilla_qubits, key='syndrome'))
    
    return syndrome_measurement

def create_full_repetition_code_circuit(n_qubits, error_gate = cirq.X, logical_state = '0', 
                                        repcode_type = 'Z'):

    # Create qubits: data qubits for encoding, ancillary qubits for syndrome measurement
    data_qubits = cirq.LineQubit.range(n_qubits)
    ancilla_qubits = cirq.LineQubit.range(n_qubits, 2*n_qubits - 1)
    
    circuit = cirq.Circuit()

    # Step 0: Decide what quantum state we are protecting. It's either 0 or 1. Then encode it
    encoding_circuit = create_repetition_code_encoder(n_qubits)

    # logical state |0>_L = |0000...>
    # do nothing, since all data qubits start reset at |0>.
    if logical_state == '0':
        pass
        
    # logical state |1>_L = |1111...>
    # apply X gate on all data qubits since they all start reset at |0>
    if logical_state == '1':
        circuit.append(
            cirq.Moment(cirq.X(data_qubits[0]))
                       )
        circuit += encoding_circuit        

    # logical state |+>_L = 1/sqrt(2) * (|0>_L + |1>_L) = 1/sqrt(2) * (|0000...> + |1111...>)
    if logical_state == '+':
        circuit.append(
            cirq.Moment(cirq.H(data_qubits[0]))
                       )
        circuit += encoding_circuit

    # logical state |->_L = 1/sqrt(2) * (|0>_L - |1>_L) = 1/sqrt(2) * (|0000...> - |1111...>)
    if logical_state == '-':
        circuit.append(
            cirq.Moment(cirq.H(data_qubits[0]))
                       )
        circuit += encoding_circuit
        circuit.append(
            cirq.Moment(cirq.Z(data_qubits[0]))
                       )
    
    # Step 1: Hadamard sandwich where phase flips will be inserted
    
    circuit.append(
        cirq.Moment(cirq.H.on_each(*data_qubits))
    )
    
    ## errors go here
    
    circuit.append(
        cirq.Moment(cirq.H.on_each(*data_qubits))
    )
            
    # Step 2: Measure error syndrome
    circuit += get_syndrome_measurement(data_qubits, ancilla_qubits, repcode_type = repcode_type)

    # Step 3: Measure data qubits
    circuit.append(cirq.measure(*data_qubits, key='data_qubits'))
            
    return circuit

def get_logical_error_probability_analytical(distances, physical_errors):
    
    # method 1: small p approximation
    # all_analytical_errors = []
    # for distance in distances:
    #     t = floor((distance - 1) / 2)
    #     analytical_errors = comb(distance, t+1) * physical_errors**(t+1)
    #     all_analytical_errors.append(analytical_errors)

    # method 2: full expression
    all_analytical_errors = []
    for distance in distances:
        analytical_success = 0
        for i in range(floor(distance/2.)+1):
            analytical_success += comb(distance, i) * physical_errors**i * (1-physical_errors)**(distance-i)
        analytical_errors = 1-analytical_success
        all_analytical_errors.append(analytical_errors)

    return all_analytical_errors

def plot_logical_error_probabilities(distances, physical_errors, all_logical_errors, all_analytical_errors):
    
    plotter.figure(figsize=(10, 8))
    if distances is not None:
        colors = plotter.cm.viridis(np.linspace(0, 0.8, len(distances)))
    else:
        colors = plotter.cm.viridis(np.linspace(0, 0.8, 1))
    
    plotter.loglog(physical_errors, physical_errors, label = 'Unprotected qubit',
                      linewidth=2, linestyle = '--', color='gray',
                      )

    if all_analytical_errors and distances:
        for distance, logical_errors, analytical_errors, color in zip(distances, all_logical_errors, all_analytical_errors, colors):
            plotter.loglog(physical_errors, logical_errors, label = f'd = {distance} simulated',
                          marker='o', linewidth=2, markersize=8,
                          color=color,
                          )
            plotter.loglog(physical_errors, analytical_errors, label = f'd = {distance} analytical',
                          linewidth=2, linestyle = '--', color=color,
                          )
    else:
        for logical_errors, color in zip(all_logical_errors, colors):
            plotter.loglog(physical_errors, logical_errors,
                          marker='o', linewidth=2, markersize=8,
                          color=color,
                          )
    
    plotter.legend()
    plotter.xlim([physical_errors.min(), physical_errors.max()])
    plotter.ylim([1e-10, 1.1])
    plotter.grid(visible=True, which='major', axis='both')
    plotter.xlabel('Physical error probability')
    plotter.ylabel('Logical error probability')
    plotter.tight_layout()
    plotter.show()

def get_binary_representation(index, n_qubits):
    # Binary representation of index in n_qubits bits, LSB first
    # This trick avoids having to do string manipulations with Python's generic bin() function
    # TLDR: >> is a right-shift, & 1 picks out the LSBs
    return (index >> np.arange(n_qubits)) & 1

def get_logical_error_probability_for_rep_code(n_qubits, error_probability, 
                                               logical_state = '0', error_gate = cirq.X, 
                                               n_shots = 100, 
                                               simulator = cirq.Simulator(),
                                               repcode_type = 'Z',
                                               ):

    if n_qubits == 1:
        return error_probability
    
    # step 1: build the repetition code circuit without errors
    base_circuit = create_full_repetition_code_circuit(n_qubits, logical_state = logical_state, 
                                                       error_gate = error_gate, repcode_type = repcode_type)

    # step 2: generate all errors
    # first, create independent errors in a n_shots x n_qubits matrix
    # then, for each shot, the errors can be taken sliced out of this matrix and applied to the data qubits
    actual_errors_all_shots = []
    error_mask = np.random.random((n_shots, n_qubits)) < error_probability
    for shot in range(n_shots):
        actual_errors_all_shots.append(np.where(error_mask[shot])[0].tolist())

    # step 3: insert all errors into copies of the base_circuit
    circuits = []
    if logical_state == '+':
        insert_index = (1 +                     # initial H gate
                       (n_qubits - 1) +         # CNOT gates to create logical +
                       + 1)                     # H gates to turn phase flips into bit flips
    elif logical_state == '-':
        insert_index = (1 +                     # initial H gate
                        (n_qubits - 1) +        # CNOT gates to create logical +
                        1 +                     # Z gate to turn logical + into logical -
                        1)                      # H gates to turn phase flips into bit flips
    data_qubits = cirq.LineQubit.range(n_qubits)
    for shot_errors in actual_errors_all_shots:
        circuit = base_circuit.copy()
        error_moment = []
        for i in range(n_qubits):
            if i in shot_errors:
                error_moment.append(error_gate(data_qubits[i]))
        if error_moment:
            circuit.insert(insert_index, cirq.Moment(error_moment)) # insert a moment with all errors
        circuits.append(circuit)

    # step 4: run all noise instances (circuits) in one batch
    results = simulator.run_batch(circuits, repetitions=1)

    # step 5: decode the syndrome information
    syndromes = [results[i][0].measurements['syndrome'].tolist()[0] for i in range(n_shots)]
    decoder = MWPMDecoder1D(num_qubits=n_qubits)
    decoded_syndromes = [decoder.decode(syndrome) for syndrome in syndromes]

    # step 6: count logical errors
    datas = [results[i][0].measurements['data_qubits'].tolist()[0] for i in range(n_shots)]

    logical_errors = 0
    if repcode_type == 'Z': # bit-flip rep code using ZZ parity checks
        # correct the data qubits using the syndrome measurements and compare with known initial state
        initial_state = [int(logical_state)]*n_qubits
        for data, error_locations in zip(datas, decoded_syndromes):
            final_state = data.copy()
            for error_location in error_locations:
                final_state[error_location] = 1-final_state[error_location] # flip the bit at error_location
            if not np.array_equal(initial_state, final_state):
                logical_errors += 1

    elif repcode_type == 'X': # phase-flip rep code, detecting phase flips by turning them into bit flips
        for actual_error_locations, decoded_error_locations, in zip(actual_errors_all_shots, decoded_syndromes):
            # compare decoder with knowledge of actual error locations
            if not np.array_equal(actual_error_locations, decoded_error_locations):
                logical_errors += 1
            
    return logical_errors * 1. / n_shots

def get_logical_error_probability_simulated(distances, physical_errors, n_shots = 1000000, 
                                            logical_state = '0', error_gate = cirq.X,
                                            simulator = cirq.Simulator(),
                                            repcode_type = 'Z'
                                           ):

    all_logical_errors = []
    for distance in distances:
        print(f"Simulating distance-{distance} repetition code circuits")
        thisdistance_logicalerrors = []
        for physical_error in physical_errors:
            logical_error = get_logical_error_probability_for_rep_code(
                                         n_qubits = distance,
                                         error_probability = physical_error,
                                         logical_state = logical_state,
                                         error_gate = error_gate,
                                         n_shots = n_shots,
                                         repcode_type = repcode_type,
                                         simulator = simulator)
            thisdistance_logicalerrors.append(logical_error)
        all_logical_errors.append(thisdistance_logicalerrors)

    return all_logical_errors