# MIT 6.034 Lab 5: k-Nearest Neighbors and Identification Trees
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and Jake Barnwell (jb16)

from api import *
from data import *
import math
log2 = lambda x: math.log(x, 2)
INF = float('inf')

################################################################################
############################# IDENTIFICATION TREES #############################
################################################################################

def id_tree_classify_point(point, id_tree):
    """Uses the input ID tree (an IdentificationTreeNode) to classify the point.
    Returns the point's classification."""
    #print id_tree
    # classify = id_tree.apply_classifier(point)
    # if id_tree.is_leaf():
    #     return classify
    # return [id_tree_classify_point(point, node) for node in id_tree.get_branches()]
    if id_tree.is_leaf():
        return id_tree.get_node_classification()
    child = id_tree.apply_classifier(point)
    return id_tree_classify_point(point, child)

def split_on_classifier(data, classifier):
    """Given a set of data (as a list of points) and a Classifier object, uses
    the classifier to partition the data.  Returns a dict mapping each feature
    values to a list of points that have that value."""
    class_dict={}
    for point in data:
        classif = classifier.classify(point)
        if not classif in class_dict:
            class_dict[classif]=[point]
        else:
            class_dict[classif].append(point)

    return class_dict


#### CALCULATING DISORDER

def branch_disorder(data, target_classifier):
    """Given a list of points representing a single branch and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the branch."""
    cla = split_on_classifier(data, target_classifier)
    total=sum([len(cla[classification])  for classification in cla.keys()])

    disorder=sum([-len(cla[x])/float(total)*log2(len(cla[x])/float(total)) for x in cla.keys()])
    return disorder

def average_test_disorder(data, test_classifier, target_classifier):
    """Given a list of points, a feature-test Classifier, and a Classifier
    for determining the true classification of each point, computes and returns
    the disorder of the feature-test stump."""
    test_split = split_on_classifier(data, test_classifier)
    total = float(len(data))
    aver=sum([branch_disorder(test_split[cla], target_classifier)*(len(test_split[cla])/total) for cla in test_split.keys()])
    return aver 

## To use your functions to solve part A2 of the "Identification of Trees"
## problem from 2014 Q2, uncomment the lines below and run lab5.py:
#for classifier in tree_classifiers:
#    print classifier.name, average_test_disorder(tree_data, classifier, feature_test("tree_type"))


#### CONSTRUCTING AN ID TREE

def find_best_classifier(data, possible_classifiers, target_classifier):
    """Given a list of points, a list of possible Classifiers to use as tests,
    and a Classifier for determining the true classification of each point,
    finds and returns the classifier with the lowest disorder.  Breaks ties by
    preferring classifiers that appear earlier in the list.  If the best
    classifier has only one branch, raises NoGoodClassifiersError."""
    best_cla = None 
    best_cla_disorder = INF
    for test_cla in possible_classifiers:
        disorder = average_test_disorder(data, test_cla, target_classifier)
        if disorder<best_cla_disorder:
            best_cla=test_cla
            best_cla_disorder = disorder
    branches = split_on_classifier(data, best_cla)
    if len(branches.keys())==1:
        raise NoGoodClassifiersError
    else:
        return best_cla

## To find the best classifier from 2014 Q2, Part A, uncomment:
#print find_best_classifier(tree_data, tree_classifiers, feature_test("tree_type"))

def construct(data, possible_classifiers, target_classifier, id_tree_node):
    #print "run"


    #
    if branch_disorder(data, target_classifier)==0.0:
        id_tree_node.set_node_classification(target_classifier.classify(data[-1]))
    else:
        try:
            best_classifier = find_best_classifier(data, possible_classifiers, target_classifier)
        except NoGoodClassifiersError:
            best_classifier=False 
        if best_classifier==False:
            pass
        else:
            split = split_on_classifier(data, best_classifier)
            next_class=possible_classifiers[:]
            next_class.remove(best_classifier)
            features = split.keys()
            id_tree_node.set_classifier_and_expand(best_classifier, features)
            branches = id_tree_node.get_branches()
            for name in branches.keys():
                construct(split[name], next_class, target_classifier, branches[name])
    
def construct_greedy_id_tree(data, possible_classifiers, target_classifier, id_tree_node=None):
    """Given a list of points, a list of possible Classifiers to use as tests,
    a Classifier for determining the true classification of each point, and
    optionally a partially completed ID tree, returns a completed ID tree by
    adding classifiers and classifications until either perfect classification
    has been achieved, or there are no good classifiers left."""
    if id_tree_node==None:
        id_tree_node=IdentificationTreeNode(target_classifier)
    construct(data, possible_classifiers, target_classifier, id_tree_node)
    return id_tree_node
    #construct_greedy_id_tree(data, next_class, target_classifier, id_tree_node=None)


## To construct an ID tree for 2014 Q2, Part A:
#print construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))

## To use your ID tree to identify a mystery tree (2014 Q2, Part A4):
#tree_tree = construct_greedy_id_tree(tree_data, tree_classifiers, feature_test("tree_type"))
#print id_tree_classify_point(tree_test_point, tree_tree)

## To construct an ID tree for 2012 Q2 (Angels) or 2013 Q3 (numeric ID trees):
#print construct_greedy_id_tree(angel_data, angel_classifiers, feature_test("Classification"))
#print construct_greedy_id_tree(numeric_data, numeric_classifiers, feature_test("class"))


#### MULTIPLE CHOICE

ANSWER_1 = 'bark_texture'
ANSWER_2 =  'leaf_shape'
ANSWER_3 = 'orange_foliage'

ANSWER_4 = [2,3]
ANSWER_5 = [3]
ANSWER_6 = [2]
ANSWER_7 = 2

ANSWER_8 = 'No'
ANSWER_9 = 'No'


################################################################################
############################# k-NEAREST NEIGHBORS ##############################
################################################################################

#### MULTIPLE CHOICE: DRAWING BOUNDARIES

BOUNDARY_ANS_1 = 3
BOUNDARY_ANS_2 = 4

BOUNDARY_ANS_3 = 1
BOUNDARY_ANS_4 = 2

BOUNDARY_ANS_5 = 2
BOUNDARY_ANS_6 = 4
BOUNDARY_ANS_7 = 1
BOUNDARY_ANS_8 = 4
BOUNDARY_ANS_9 = 4

BOUNDARY_ANS_10 = 4
BOUNDARY_ANS_11 = 2
BOUNDARY_ANS_12 = 1
BOUNDARY_ANS_13 = 4
BOUNDARY_ANS_14 = 4


#### WARM-UP: DISTANCE METRICS

def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    return sum([v[i]*u[i] for i in range(len(u))])

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return math.sqrt(sum([i**2 for i in v]))

def euclidean_distance(point1, point2):
    "Given two Points, computes and returns the Euclidean distance between them."
    #print "point: ",point1, "point2: ", point2
    return math.sqrt(sum([(point1.coords[i] - point2.coords[i])**2 for i in range(len(point1.coords))]))

def manhattan_distance(point1, point2):
    "Given two Points, computes and returns the Manhattan distance between them."
    return sum([abs(point1.coords[i]-point2.coords[i]) for i in range(len(point1.coords))])

def hamming_distance(point1, point2):
    "Given two Points, computes and returns the Hamming distance between them."
    return sum([(point1.coords[i]!=point2.coords[i]) for i in range(len(point2.coords))])

def cosine_distance(point1, point2):
    """Given two Points, computes and returns the cosine distance between them,
    where cosine distance is defined as 1-cos(angle_between(point1, point2))."""
    cos_ang = dot_product(point1.coords, point2.coords)/(norm(point1.coords)*norm(point2.coords))
    dist = 1-math.cos(math.acos(cos_ang))
    return dist


#### CLASSIFYING POINTS

def get_k_closest_points(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns a list containing the k points
    from the data that are closest to the test point, according to the distance
    metric.  Breaks ties lexicographically by coordinates."""
    #print "point: ", point, "data[0]: ", data[0], "distance: ", distance_metric(point, data[0])
    _data = sorted(data, key = lambda x: x.coords)
    point_dist=sorted([(_point, distance_metric(point, _point)) for _point in _data], key = lambda x: x[1])
    return [point_dist[i][0] for i in range(k)]

    raise NotImplementedError

def knn_classify_point(point, data, k, distance_metric):
    """Given a test point, a list of points (the data), an int 0 < k <= len(data),
    and a distance metric (a function), returns the classification of the test
    point based on its k nearest neighbors, as determined by the distance metric.
    Assumes there are no ties."""
    point_lst = get_k_closest_points(point, data, k, distance_metric)
    mar = [x.classification for x in  point_lst]

    return max(mar, key = mar.count)

## To run your classify function on the k-nearest neighbors problem from 2014 Q2
## part B2, uncomment the line below and try different values of k:
#print knn_classify_point(knn_tree_test_point, knn_tree_data, 5, euclidean_distance)


#### CHOOSING k

def cross_validate(data, k, distance_metric):
    """Given a list of points (the data), an int 0 < k <= len(data), and a
    distance metric (a function), performs leave-one-out cross-validation.
    Return the fraction of points classified correctly, as a float."""
    correct = []
    for i in range(len(data)):
        point = data[i]
        _data = data[:]
        _data.pop(i)
        cl = knn_classify_point(point, _data, k, distance_metric)
        if point.classification==cl:
            correct.append(point)

    return len(correct)/float(len(data))

def find_best_k_and_metric(data):
    """Given a list of points (the data), uses leave-one-out cross-validation to
    determine the best value of k and distance_metric, choosing from among the
    four distance metrics defined above.  Returns a tuple (k, distance_metric),
    where k is an int and distance_metric is a function."""
    
    best_cros_val = 0
    dist_m = euclidean_distance
    k_best = 0
    for distance_metric in [euclidean_distance, manhattan_distance, hamming_distance, cosine_distance]:
        for k in range(1, len(data)):
            fr = cross_validate(data, k, distance_metric)
            if fr>=best_cros_val:
                best_cros_val = fr 
                dist_m = distance_metric
                best_k=k
    return best_k, dist_m

## To find the best k and distance metric for 2014 Q2, part B, uncomment:
#print find_best_k_and_metric(knn_tree_data)


#### MORE MULTIPLE CHOICE

kNN_ANSWER_1 = 'Overfitting'
kNN_ANSWER_2 = 'Underfitting'
kNN_ANSWER_3 = 4

kNN_ANSWER_4 = 4
kNN_ANSWER_5 = 1
kNN_ANSWER_6 = 3
kNN_ANSWER_7 = 3

#### SURVEY ###################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "id trees"
WHAT_I_FOUND_BORING = "nearest neighbors"
SUGGESTIONS = ""
