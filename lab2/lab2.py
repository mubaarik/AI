# MIT 6.034 Lab 2: Search
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs

all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']


#### PART 1: Helper Functions ##################################################

def path_length(graph, path):
    """Returns the total length (sum of edge weights) of a path defined by a
    list of nodes coercing an edge-linked traversal through a graph.
    (That is, the list of nodes defines a path through the graph.)
    A path with fewer than 2 nodes should have length of 0.
    You can assume that all edges along the path have a valid numeric weight."""
    return sum([graph.get_edge(path[i], path[i+1]).length for i in range(len(path)-1) ])
    


def has_loops(path):
    """Returns True if this path has a loop in it, i.e. if it
    visits a node more than once. Returns False otherwise."""
    return len(path)>len(set(path));


def extensions(graph, path):
    """Returns a list of paths. Each path in the list should be a one-node
    extension of the input path, where an extension is defined as a path formed
    by adding a neighbor node (of the final node in the path) to the path.
    Returned paths should not have loops, i.e. should not visit the same node
    twice. The returned paths should be sorted in lexicographic order."""
    paths=[]
    #print path
    for neighbor in graph.get_neighbors(path[-1]):
        copyPath=path[0:]
        #Sprint paths
        if len(path)>1:
            if neighbor!=path[-2]:
                copyPath.append(neighbor)
                paths.append(copyPath)
        else: 
            copyPath.append(neighbor)
            paths.append(copyPath)
    if len(paths)==1 and has_loops(paths[0]):
        return []


    
    return paths
   # raise NotImplementedError


def sort_by_heuristic(graph, goalNode, nodes):
    """Given a list of nodes, sorts them best-to-worst based on the heuristic
    from each node to the goal node. Here, and in general for this lab, we
    consider a lower heuristic to be "better" because it represents a shorter
    potential path to the goal. Break ties lexicographically by node name."""
    
    return [x[0] for x in sorted([(node, graph.get_heuristic_value(node, goalNode)) for node in sorted(nodes)], key=lambda x: x[-1])]
    
    #raise NotImplementedError


# You can ignore the following line.  It allows generic_search (PART 2) to
# access the extensions and has_loops functions that you just defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE


#### PART 2: Generic Search ####################################################

# Note: If you would prefer to get some practice with implementing search
# algorithms before working on Generic Search, you are welcome to do PART 3
# before PART 2.

# Define your custom path-sorting functions here.
# Each path-sorting function should be in this form:

def hc_new_sort(graph, goalNode, paths):
    sorted_paths=sorted(paths, key = lambda x: graph.get_heuristic_value(x[-1], goalNode))
    return sorted_paths
def basic_bb_agenda_sort(graph, goalNode, paths):
    return sorted(paths, key=lambda x: path_length(graph, x))

def basic_bbh_agenda_sort(graph, goalNode, paths):
    return sorted(paths, key=lambda x: path_length(graph, x)+graph.get_heuristic_value(x[-1], goalNode))




generic_dfs = [do_nothing_fn, True, do_nothing_fn, False]

generic_bfs = [do_nothing_fn, False, do_nothing_fn, False]

generic_hill_climbing = [hc_new_sort, True, do_nothing_fn, False]

generic_best_first = [do_nothing_fn, False, hc_new_sort, False]

generic_branch_and_bound = [do_nothing_fn,False , basic_bb_agenda_sort, False]

generic_branch_and_bound_with_heuristic = [do_nothing_fn, False, basic_bbh_agenda_sort, False]

generic_branch_and_bound_with_extended_set = [do_nothing_fn,False , basic_bb_agenda_sort, True]

generic_a_star = [do_nothing_fn, False, basic_bbh_agenda_sort, True]#[None, None, None, None]

# Here is an example of how to call generic_search (uncomment to run):
#my_dfs_fn = generic_search(*generic_dfs)
#my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
#print my_dfs_path

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
    path_dict={}
    final_paths=[]
    for path in paths:
        if len(path) not in path_dict:
            path_dict[len(path)]=[path]
        else:
            path_dict[len(path)].append(path)


    for key in path_dict.keys():
        path_dict[key]=sorted(path_dict[key], key = lambda x: graph.get_heuristic_value(x[-1], goalNode))
        if not final_paths:
            if len(path_dict[key])>beam_width:
                final_paths=path_dict[key][0:beam_width]
            else:
                final_paths=path_dict[key]
        else:
            if len(path_dict[key])>beam_width:
                final_paths=final_paths+path_dict[key][0:beam_width]
            else:
                final_paths=final_paths+path_dict[key]
    return final_paths



#     # YOUR CODE HERE

#     return sorted_beam_agenda

generic_beam = [do_nothing_fn, False, my_beam_sorting_fn, False]

# Uncomment this to test your generic_beam search:
#print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 3: Search Algorithms #################################################

# Note: It's possible to implement the following algorithms by calling
# generic_search with the arguments you defined in PART 2.  But you're also
# welcome to code them without using generic_search if you would prefer to
# implement the algorithms by yourself.
def findPath(parent, node):
    path=[]
    if node!=None:
        path=[node]
        
        while parent[node]!=None:
           
            node=parent[node]
            path.append(node)
            
    return path[::-1]
def dfs(graph, startNode, goalNode):
    # parent={}
    # parent[startNode]=None;
    # stack=[startNode]
    # while stack:
    #     extend=stack.pop()
    #     if extend==goalNode:
    #         return findPath(parent, extend)
    #     for node in graph.get_neighbors(extend):
    #         stack.append(node)
    #         if node not in parent:
    #             parent[node]=extend
                
    # return None
    my_dfs=generic_search(do_nothing_fn, True, do_nothing_fn, False)
    return my_dfs(graph, startNode, goalNode)

    


def bfs(graph, startNode, goalNode):
    # queue=[]
    # parent={}
    # extended={startNode}
    # while queue:
    #     extend=queue.pop(0)
    #     if extend==goalNode:
    #         return findPath(parent, extend)
    #     extended.add(extend)
    #     for neighbor in graph.get_neighbors(extend):
    #         if neighbor not in extended:
    #             queue.add(neighbor)
    # return None;
    my_bfs=generic_search(do_nothing_fn, False, do_nothing_fn, True)
    return my_bfs(graph, startNode, goalNode)


def hill_climbing(graph, startNode, goalNode):
    my_hc=generic_search(hc_new_sort, True, do_nothing_fn, False)
    return my_hc(graph, startNode, goalNode)
    


def best_first(graph, startNode, goalNode):
    my_best=generic_search(hc_new_sort, False, do_nothing_fn, False)
    return my_best(graph, startNode, goalNode)


def beam(graph, startNode, goalNode, beam_width):
    my_beam=generic_search(do_nothing_fn, False, my_beam_sorting_fn, False)
    return my_beam(graph, startNode, goalNode, beam_width)


def branch_and_bound(graph, startNode, goalNode):
    my_bb=generic_search(do_nothing_fn,False , basic_bb_agenda_sort, False)
    return my_bb(graph, startNode, goalNode)
    #raise NotImplementedError


def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    my_bbh=generic_search(do_nothing_fn,False , basic_bbh_agenda_sort, False)
    return my_bbh(graph, startNode, goalNode)
    


def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    
    my_bbe=generic_search(do_nothing_fn,False , basic_bb_agenda_sort, True)
    return my_bbe(graph, startNode, goalNode)


def a_star(graph, startNode, goalNode):
    my_aStar=generic_search(do_nothing_fn,False , basic_bbh_agenda_sort, True)
    return my_aStar(graph, startNode, goalNode)


#### PART 4: Heuristics ########################################################

def is_admissible(graph, goalNode):
    """Returns True if this graph's heuristic is admissible; else False.
    A heuristic is admissible if it is either always exactly correct or overly
    optimistic; it never over-estimates the cost to the goal."""
    for node in graph.nodes:
        shortest_path_len=path_length(graph, bfs(graph, node, goalNode))
        heuristic=graph.get_heuristic_value(node, goalNode)
        

        if shortest_path_len<heuristic:
            return False
    return True

    


def is_consistent(graph, goalNode):
    """Returns True if this graph's heuristic is consistent; else False.
    A consistent heuristic satisfies the following property for all
    nodes v in the graph:
        Suppose v is a node in the graph, and N is a neighbor of v,
        then, heuristic(v) <= heuristic(N) + edge_weight(v, N)
    In other words, moving from one node to a neighboring node never unfairly
    decreases the heuristic.
    This is equivalent to the heuristic satisfying the triangle inequality."""
    for edge in graph.edges:
        h_diff=abs(graph.get_heuristic_value(edge.startNode, goalNode)-graph.get_heuristic_value(edge.endNode, goalNode))
        leng=edge.length;
        if h_diff>leng:
            return False

    return True


### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


##### PART 5: Multiple Choice ##################################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '1'

ANSWER_4 = '3'


#### SURVEY ####################################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 4
WHAT_I_FOUND_INTERESTING = "generic_search"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = "Instructions could have been clearer"


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the online tester. DO NOT CHANGE!

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]