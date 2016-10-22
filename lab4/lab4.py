# MIT 6.034 Lab 4: Constraint Satisfaction Problems
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    #raise NotImplementedError
    for var in csp.get_all_variables():
        if csp.get_domain(var)==[]:
            return True
    return False


def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""
    for var in csp.get_all_variables():
        val = csp.get_assigned_value(var)
        for nei in csp.get_neighbors(var):
            nei_val = csp.get_assigned_value(nei)
            if val!=None and nei_val!=None:
                for cons in csp.constraints_between(var, nei):
                    if not cons.check(val, nei_val):
                        return False
    return True


def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""

    
    num_extensions=0
    problem_list = [problem]

    while problem_list:
        num_extensions+=1
        toExpand = problem_list.pop()
        if has_empty_domains(toExpand):
            continue
        elif check_all_constraints(toExpand):
            
            if toExpand.unassigned_vars==[]:
                return toExpand.assigned_values, num_extensions
            else:
                var = toExpand.pop_next_unassigned_var()
                new_problems = []
                for val in toExpand.get_domain(var):
                    _problem=toExpand.copy().set_assigned_value(var, val)
                    new_problems.append(_problem)

                problem_list.extend(new_problems[::-1])
                
                    
    return None, num_extensions
    

        




#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    cSp=csp.copy()
    reduced = set()
    for n in cSp.get_neighbors(var):
        var_n_cons = cSp.constraints_between(var, n)
        for constr in var_n_cons:
            for nval in cSp.get_domain(n):
                remove = True
                for val in cSp.get_domain(var):
                    if constr.check(val, nval):
                        remove = False
                        for cons in var_n_cons:
                            if not cons.check(val, nval):
                                remove=True
                        if not remove:
                            break
                if remove:
                    csp.eliminate(n, nval)
                    reduced.add(n)
                    if not csp.get_domain(n):
                        return None
    return sorted(list(reduced))




            

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    my_queue = csp.get_all_variables()
    dequeued=[]
    if queue!=None:
        my_queue=queue
    while my_queue:
        extend = my_queue.pop(0)
        dequeued.append(extend)
        reduced=eliminate_from_neighbors(csp, extend)
        if reduced==None:
            return None
        for var in reduced:
            if var not in my_queue:
                my_queue.append(var)
    return dequeued


    #raise NotImplementedError

# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.

ANSWER_1 = 20;#solve_constraint_dfs(get_pokemon_problem())

# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?
my_poke = get_pokemon_problem()
#domain_reduction(my_poke)
ANSWER_2 = 6;#solve_constraint_dfs(my_poke)


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    #domain_reduction(problem)
    num_extensions=0
    problem_list = [problem]

    while problem_list:
        num_extensions+=1
        toExpand = problem_list.pop()
        if has_empty_domains(toExpand):
            continue
        elif check_all_constraints(toExpand):
            
            if toExpand.unassigned_vars==[]:
                return toExpand.assigned_values, num_extensions
            else:
                var = toExpand.pop_next_unassigned_var()
                new_problems = []
                for val in toExpand.get_domain(var):
                    _problem=toExpand.copy().set_assigned_value(var, val)
                    domain_reduction(_problem, [var])
                    
                    new_problems.append(_problem)

                problem_list.extend(new_problems[::-1])
                
                    
    return None, num_extensions


    
   

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)
#my_poke = 
ANSWER_3 = solve_constraint_propagate_reduced_domains(my_poke)[1]


#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    my_queue = csp.get_all_variables()
    dequeued=[]
    if queue!=None:
        my_queue=queue
    while my_queue:
        extend = my_queue.pop(0)
        dequeued.append(extend)
        reduced=eliminate_from_neighbors(csp, extend)
        if reduced==None:
            return None
        for var in reduced:
            if len(csp.get_domain(var))==1:
                if var not in my_queue:
                    my_queue.append(var)
    return dequeued

    #raise NotImplementedError

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    num_extensions=0
    problem_list = [problem]

    while problem_list:
        num_extensions+=1
        toExpand = problem_list.pop()
        if has_empty_domains(toExpand):
            continue
        elif check_all_constraints(toExpand):
            
            if toExpand.unassigned_vars==[]:
                return toExpand.assigned_values, num_extensions
            else:
                var = toExpand.pop_next_unassigned_var()
                new_problems = []
                for val in toExpand.get_domain(var):
                    _problem=toExpand.copy().set_assigned_value(var, val)
                    domain_reduction_singleton_domains(_problem, [var])
                    
                    new_problems.append(_problem)

                problem_list.extend(new_problems[::-1])
                
                    
    return None, num_extensions

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)
#poke = get_pokemon_problem

ANSWER_4 = solve_constraint_propagate_singleton_domains(get_pokemon_problem())[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    my_queue = csp.get_all_variables()
    dequeued=[]
    if queue!=None:
        my_queue=queue
    while my_queue:
        extend = my_queue.pop(0)
        dequeued.append(extend)
        reduced=eliminate_from_neighbors(csp, extend)
        if reduced==None:
            return None
        for var in reduced:
            if enqueue_condition_fn(csp, var):
                if var not in my_queue:
                    my_queue.append(var)
    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var))==1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    num_extensions=0
    problem_list = [problem]

    while problem_list:
        num_extensions+=1
        toExpand = problem_list.pop()
        if has_empty_domains(toExpand):
            continue
        elif check_all_constraints(toExpand):
            
            if toExpand.unassigned_vars==[]:
                return toExpand.assigned_values, num_extensions
            else:
                var = toExpand.pop_next_unassigned_var()
                new_problems = []
                for val in toExpand.get_domain(var):
                    _problem=toExpand.copy().set_assigned_value(var, val)
                    if enqueue_condition!=None:
                        propagate(enqueue_condition, _problem, [var])
                    
                    new_problems.append(_problem)

                problem_list.extend(new_problems[::-1])
                
                    
    return None, num_extensions

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)

ANSWER_5 = solve_constraint_generic(get_pokemon_problem(), enqueue_condition=condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m-n)==1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    #raise NotImplementedError
    return abs(m-n)!=1

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraint_list = []
    for i in range(len(variables)-1):
        for j in range(i+1, len(variables)):
            constr = Constraint(variables[i], variables[j],constraint_different)
            constraint_list.append(constr)
    return constraint_list


#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ''
HOW_MANY_HOURS_THIS_LAB_TOOK = 8
WHAT_I_FOUND_INTERESTING = 'reduction problems'
WHAT_I_FOUND_BORING = "Too many dfs could just put all of them on one problem"
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
