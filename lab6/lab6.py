# MIT 6.034 Lab 6: Neural Nets
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), Jake Barnwell (jb16), and 6.034 staff

from nn_problems import *
from math import e
INF = float('inf')

#### NEURAL NETS ###############################################################

# Wiring a neural net

nn_half = [1]

nn_angle = [2,1]

nn_cross = [2,2,1]

nn_stripe = [3,1]

nn_hexagon = [6,1]

nn_grid = [4,2,1]

# Threshold functions
def stairstep(x, threshold=0):
    "Computes stairstep(x) using the given threshold (T)"
    return 1*(x>=threshold)

def sigmoid(x, steepness=1, midpoint=0):
    "Computes sigmoid(x) using the given steepness (S) and midpoint (M)"
    return 1.0/(1+e**(-steepness*(x-midpoint)))

def ReLU(x):
    "Computes the threshold of an input using a rectified linear unit."
    return max(0,x)

# Accuracy function
def accuracy(desired_output, actual_output):
    "Computes accuracy. If output is binary, accuracy ranges from -0.5 to 0."
    
    return -.5*(desired_output-actual_output)**2

# Forward propagation

def node_value(node, input_values, neuron_outputs):  # STAFF PROVIDED
    """Given a node, a dictionary mapping input names to their values, and a
    dictionary mapping neuron names to their outputs, returns the output value
    of the node."""
    if isinstance(node, basestring):
        return input_values[node] if node in input_values else neuron_outputs[node]
    return node  # constant input, such as -1

def forward_prop(net, input_values, threshold_fn=stairstep):
    """Given a neural net and dictionary of input values, performs forward
    propagation with the given threshold function to compute binary output.
    This function should not modify the input net.  Returns a tuple containing:
    (1) the final output of the neural net
    (2) a dictionary mapping neurons to their immediate outputs"""
    _queue=net.topological_sort()
    _map={}
    while _queue:

        fix = _queue.pop(0)
        init_value = sum([node_value(node, input_values, _map)*net.get_wires(node, fix)[0].get_weight() for node in net.get_incoming_neighbors(fix)])
        output = threshold_fn(init_value)
        _map[fix]=output
        if net.is_output_neuron(fix):
            return output, _map
    return None, {}


# Backward propagation warm-up
def neib(inputs, original, neighbors, step_size):
    copy= inputs[:]
    for i in [-step_size,step_size]:
        for j in range(len(copy)):
            new_copy=copy[:]
            new_copy[j]=new_copy[j]+i 
            if abs((abs(new_copy[j])-abs(original[j])))<=(step_size+step_size*.01) and new_copy not in neighbors:
                neighbors.append(new_copy)
    return neighbors
def neib_recall(inputs, step_size):
    neighbors = neib(inputs, inputs, [], step_size)
    for i in range(len(inputs)-1):
        for neighbor in neighbors:
            #print "sub_neighbors: ", neighbors
            neighbors = neib(neighbor, inputs, neighbors, step_size)
    return neighbors


def add_cons(arr, cont):
    out =[]
    for i in arr:
        out.append(i+cont)
    return out 
def combine(arr1,arr2):
    out = []
    for i in arr1:
        for j in arr2:
            if isinstance(j, list) and isinstance(i, list):
                new = i[:];
                new.extend(j)
                out.append(new)
            elif isinstance(j, list):
                new = j[:];
                new.append(i)
                out.append(new)
            elif isinstance(i, list):
                new = i[:];
                new.append(j)
                out.append(new)
            else:
                out.append([i,j])
    return out



def gradient_ascent_step(func, inputs, step_size):
    """Given an unknown function of three variables and a list of three values
    representing the current inputs into the function, increments each variable
    by +/- step_size or 0, with the goal of maximizing the function output.
    After trying all possible variable assignments, returns a tuple containing:
    (1) the maximum function output found, and
    (2) the list of inputs that yielded the highest function output."""
    deltas = [-step_size, 0, step_size]
    comb0 = add_cons(deltas, inputs[0])
    comb1 = add_cons(deltas, inputs[1])
    comb2 = add_cons(deltas, inputs[2])
    comb3 = combine(comb0,comb1)
    comb4 = combine(comb3,comb2)
    best = max(comb4, key = lambda x: func(x[0],x[1],x[2]))
    return func(best[0],best[1],best[2]), best
def get_back_prop_dependencies(net, wire):
    """Given a wire in a neural network, returns a set of inputs, neurons, and
    Wires whose outputs/values are required to update this wire's weight."""
    _queue=[wire.endNode]
    _effective_set={wire.startNode, wire}
    while _queue:
        extend=_queue.pop(0)
        _effective_set.add(extend)
        if net.is_output_neuron(extend):
            return _effective_set
        for node in net.get_outgoing_neighbors(extend):
            _effective_set.add(net.get_wires(extend, node)[0])
            _queue.append(node)
    return _effective_set

# Backward propagation
def calculate_deltas(net, desired_output, neuron_outputs):
    """Given a neural net and a dictionary of neuron outputs from forward-
    propagation, computes the update coefficient (delta_B) for each
    neuron in the net. Uses the sigmoid function to compute neuron output.
    Returns a dictionary mapping neuron names to update coefficient (the
    delta_B values). """
    _map={}
    _queue=[net.get_output_neuron()]
    inputs = net.inputs
    while _queue:
        extend=_queue.pop(0)
        if net.is_output_neuron(extend):
            out_b=neuron_outputs[extend]
            out_d = desired_output
            _map[extend]=out_b*(1.0-out_b)*(out_d - out_b)
        elif extend in inputs:
            pass
        else:
            out_b = neuron_outputs[extend]
            out_d = sum([net.get_wires(extend, node)[0].get_weight()*_map[node] for node in net.get_outgoing_neighbors(extend)])
            _map[extend]=out_b*(1.0-out_b)*out_d
        _in = net.get_incoming_neighbors(extend)
        if _in!=None:
            for node in _in:
                _queue.append(node)
    return _map


def update_weights(net, input_values, desired_output, neuron_outputs, r=1):
    """Performs a single step of back-propagation.  Computes delta_B values and
    weight updates for entire neural net, then updates all weights.  Uses the
    sigmoid function to compute neuron output.  Returns the modified neural net,
    with the updated weights."""
    deltas = calculate_deltas(net, desired_output, neuron_outputs)
    _queue=[net.get_output_neuron()]
    inputs = net.inputs
    while _queue:
        #print "trying: ", net.neurons, inputs
        extend = _queue.pop(0)

        for node in net.get_incoming_neighbors(extend):
            out_a = node_value(node, input_values, neuron_outputs)
            if node not in inputs and node not in _queue:
                _queue.append(node)
            wire = net.get_wires(node, extend)[0]
            weight = wire.get_weight()+r*out_a*deltas[extend]
            #print "wire1: ", wire

            wire.set_weight(weight)
            #print "wire2: ", wire 
    return net 


def back_prop(net, input_values, desired_output, r=1, minimum_accuracy=-0.001):
    """Updates weights until accuracy surpasses minimum_accuracy.  Uses the
    sigmoid function to compute neuron output.  Returns a tuple containing:
    (1) the modified neural net, with trained weights
    (2) the number of iterations (that is, the number of weight updates)"""
    iterations=0
    difference = 8
    output, neuron_outputs=forward_prop(net, input_values, threshold_fn=sigmoid)
    #print "output: ", output, "desired_output: ", desired_output, "minimum_accuracy: ", minimum_accuracy
    while accuracy(desired_output, output)<minimum_accuracy:
        #print "output: ", output, "desired_output: ", desired_output
        iterations+=1
        net = update_weights(net, input_values, desired_output, neuron_outputs, r)
        output, neuron_outputs=forward_prop(net, input_values, threshold_fn=sigmoid)
    return net, iterations

# Training a neural net

ANSWER_1 = 11
ANSWER_2 = 18
ANSWER_3 = 6
ANSWER_4 = 200
ANSWER_5 = 60

ANSWER_6 = 1
ANSWER_7 = "checkerboard"
ANSWER_8 = ["small","medium", "large"]
ANSWER_9 = "B"

ANSWER_10 = "D"
ANSWER_11 = ["A","C"]
ANSWER_12 = ["A", "E"]


#### SURVEY ####################################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = "training.py"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
