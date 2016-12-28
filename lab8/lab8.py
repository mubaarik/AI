# MIT 6.034 Lab 8: Bayesian Inference
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from nets import *


#### ANCESTORS, DESCENDANTS, AND NON-DESCENDANTS ###############################

def get_ancestors(net, var):
    "Return a set containing the ancestors of var"
    queue = [var]
    _set=set()
    while queue:
        extend = queue.pop(0)
        for _var in net.get_parents(extend):
            if _var not in _set:
                _set.add(_var)
                queue.append(_var)
    return _set

def get_descendants(net, var):
    "Returns a set containing the descendants of var"
    queue = [var]
    _set=set()
    while queue:
        extend = queue.pop(0)
        for _var in net.get_children(extend):
            if _var not in _set:
                _set.add(_var)
                queue.append(_var)
    return _set

def get_nondescendants(net, var):
    "Returns a set containing the non-descendants of var"
    queue = []
    _set = set()
    descend = get_descendants(net, var)
    _vars = net.variables
    for _var in _vars:
        if _var not in descend and _var!= var:
            _set.add(_var)
    return _set

def simplify_givens(net, var, givens):
    """If givens include every parent of var and no descendants, returns a
    simplified list of givens, keeping only parents.  Does not modify original
    givens.  Otherwise, if not all parents are given, or if a descendant is
    given, returns original givens."""
    prnts = net.get_parents(var)
    descends = get_descendants(net, var)
    _parents = {}
    for _var in prnts:

        if _var not in givens:
            return givens
        else:
            _parents[_var] = givens[_var]
    for _var in descends:
        if _var in givens:
            return givens
    return _parents


#### PROBABILITY ###############################################################

def probability_lookup(net, hypothesis, givens=None):
    "Looks up a probability in the Bayes net, or raises LookupError"
    var = hypothesis.keys()[0]
    if var!=None and givens!=None:
        givens = simplify_givens(net, var, givens)
    try: 
        prob = net.get_probability(hypothesis, parents_vals=givens, infer_missing=True)
    except ValueError:
        raise LookupError
    return prob
def get_givens(hypothesis, keys):
    givens  = {}
    for key in keys:
        givens[key] = hypothesis[key]
    return givens
def probability_joint(net, hypothesis):
    "Uses the chain rule to compute a joint probability"
    keys = net.topological_sort()[::-1]
    n = len(keys)
    prob = 1
    for i in range(n):
        _keys = net.get_parents(keys[i])
        givens = get_givens(hypothesis, _keys)
        _hypothesis={keys[i]:hypothesis[keys[i]]}
        prob*=probability_lookup(net, _hypothesis, givens)

    return prob


def probability_marginal(net, hypothesis):
    "Computes a marginal probability as a sum of joint probabilities"
    combos = net.combinations(net.variables, constant_bindings=hypothesis)
    prob = 0
    for combo in combos:
        prob+=probability_joint(net, combo)
    return prob

def probability_conditional(net, hypothesis, givens=None):
    "Computes a conditional probability as a ratio of marginal probabilities"
    if givens == None:
        return probability_marginal(net, hypothesis)
    l_givens = givens.keys()
    l_hypo = hypothesis.keys()
    for key in l_hypo:
        if key in givens:
            if givens[key] == hypothesis[key]:
                return 1.0;
            else:
                return 0

    num  = probability_marginal(net, dict(givens, **hypothesis))
    deno = probability_marginal(net, givens)
    return num/deno

def probability(net, hypothesis, givens=None):
    "Calls previous functions to compute any probability"
    return probability_conditional(net, hypothesis, givens)


#### PARAMETER-COUNTING AND INDEPENDENCE #######################################

def number_of_parameters(net):
    "Computes minimum number of parameters required for net"
    num = 0
    for var in net.variables:
        parent_prod =1
        for node in net.get_parents(var):
            parent_prod*=len(net.get_domain(node))
        dom_len = len(net.get_domain(var))-1
        num+=dom_len*parent_prod
    return num



def is_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    otherwise False.  Uses numerical independence."""
    binding_1 = net.combinations(var1, constant_bindings=None)
    binding_2 = net.combinations(var2, constant_bindings=None)
    for binding1 in binding_1:
        for binding2 in binding_2:

            prob1 = probability(net, binding1, givens)
            prob2 = probability(net, binding2, givens)
            prob3 = probability(net, dict(binding1, **binding2), givens)
    
            if not  approx_equal(prob1*prob2, prob3, epsilon=0.00000000001):
                return False
    return True

    #raise NotImplementedError
###Classics D-Seperation


def is_structurally_independent(net, var1, var2, givens=None):
    """Return True if var1, var2 are conditionally independent given givens,
    based on the structure of the Bayes net, otherwise False.
    Uses structural independence only (not numerical independence)."""
    
    ###Create the mentioned set
    involved = [var1, var2]
    gvns = []
    if givens!=None:
        gvns = givens.keys()
        involved.extend(gvns)
    involved_set = set(involved)

    ##Create the ancestral graph
    for node in involved:
        node_ances = get_ancestors(net, node)
        involved_set.update(node_ances)

    _net = net.subnet(involved_set)

    #Moralize
    for node in _net.variables:
        parents = net.get_parents(node)
        for parent in parents:
            for other in parents:
                if not _net.is_neighbor(parent, other) and parent!=other:
                    _net.link(parent, other)
    ##disorient 
    disoriented_net = _net.make_bidirectional()
    
    ##remove the givens 
    for node in gvns:
        disoriented_net = disoriented_net.remove_variable(node)

    #check whether a path exists between var1 and var2
    return disoriented_net.find_path(var1, var2)==None 


    



#### SURVEY ####################################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = "D-separation"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
