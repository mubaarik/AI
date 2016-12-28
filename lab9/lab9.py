# MIT 6.034 Lab 9: Boosting (Adaboost)
# Written by Jessica Noss (jmn), Dylan Holmes (dxh), and 6.034 staff

from math import log as ln
from utils import *


#### BOOSTING (ADABOOST) #######################################################

def initialize_weights(training_points):
    """Assigns every training point a weight equal to 1/N, where N is the number
    of training points.  Returns a dictionary mapping points to weights."""
    n=len(training_points)
    weight=make_fraction(1,n)
    weights = {}
    for point in training_points:
    	weights[point]=weight
    return weights
def calculate_error_rates(point_to_weight, classifier_to_misclassified):
    """Given a dictionary mapping training points to their weights, and another
    dictionary mapping classifiers to the training points they misclassify,
    returns a dictionary mapping classifiers to their error rates."""
    classifiers = classifier_to_misclassified.keys()
    error_rates = {}
    for classifier in classifiers:
    	error_rates[classifier]=0
    	for point in classifier_to_misclassified[classifier]:
    		#if classifier in error_rates:
    		error_rates[classifier]+=point_to_weight[point]
    		#else:
    			#error_rates[classifier]=point_to_weight[point]
    return error_rates


def pick_best_classifier(classifier_to_error_rate, use_smallest_error=True):
    """Given a dictionary mapping classifiers to their error rates, returns the
    best* classifier, or raises NoGoodClassifiersError if best* classifier has
    error rate 1/2.  best* means 'smallest error rate' if use_smallest_error
    is True, otherwise 'error rate furthest from 1/2'."""
    smallest = 1000
    best = None
    keys = classifier_to_error_rate.keys()
    if use_smallest_error:
    	
    	for key in keys:
    		key_error = classifier_to_error_rate[key]
    		if key_error<smallest:
    			best = key 
    			smallest = key_error
    		if key_error == smallest and best>key:
    			best = key 
    	if smallest == .5:
    		raise NoGoodClassifiersError
    	return best
    else:
    	smallest = -1000
    	for key in keys:
    		key_error = make_fraction(abs(abs(classifier_to_error_rate[key])-.5))
    		if key_error>smallest:
    			best = key
    			smallest = key_error
    		if key_error == smallest and best>key:
    			best = key 
    	if smallest == 0.0:
    		raise NoGoodClassifiersError
    	return best 




def calculate_voting_power(error_rate):
    """Given a classifier's error rate (a number), returns the voting power
    (aka alpha, or coefficient) for that classifier."""
    if error_rate == 1.0:
    	return -INF
    if error_rate == 0:
    	return INF
    return .5*ln((1-error_rate)/error_rate)

def get_overall_misclassifications(H, training_points, classifier_to_misclassified):
    """Given an overall classifier H, a list of all training points, and a
    dictionary mapping classifiers to the training points they misclassify,
    returns a set containing the training points that H misclassifies.
    H is represented as a list of (classifier, voting_power) tuples."""
    classify_dict = {}
    for classifier in H:
    	for point in training_points:
    		if point in classify_dict:
    			if point in classifier_to_misclassified[classifier[0]]:
    				classify_dict[point]+=-1*classifier[1]
    			else:
    				classify_dict[point]+=1*classifier[1]
    		else:
    			if point in classifier_to_misclassified[classifier[0]]:
    				classify_dict[point]=-1*classifier[1]
    			else:
    				classify_dict[point]=1*classifier[1]
    misclass = set()
    points = classify_dict.keys()
   
    for point in points:
    	if classify_dict[point]<=0.0:
    		misclass.add(point)
    return misclass



def is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance=0):
    """Given an overall classifier H, a list of all training points, a
    dictionary mapping classifiers to the training points they misclassify, and
    a mistake tolerance (the maximum number of allowed misclassifications),
    returns False if H misclassifies more points than the tolerance allows,
    otherwise True.  H is represented as a list of (classifier, voting_power)
    tuples."""
    misclass = get_overall_misclassifications(H, training_points, classifier_to_misclassified)
    return len(misclass)<=mistake_tolerance

def update_weights(point_to_weight, misclassified_points, error_rate):
    """Given a dictionary mapping training points to their old weights, a list
    of training points misclassified by the current weak classifier, and the
    error rate of the current weak classifier, returns a dictionary mapping
    training points to their new weights.  This function is allowed (but not
    required) to modify the input dictionary point_to_weight."""
    point_weight = {}
    points = point_to_weight.keys()
    zero = (error_rate ==0.0)
    one = (error_rate==1.0)
    for point in points:
    	current_weight = point_to_weight[point]
    	if point in misclassified_points:
    		if zero:
    			point_weight[point] = make_fraction(make_fraction(.5)*INF*current_weight)
    		else:
    			point_weight[point] = make_fraction(make_fraction(.5)*make_fraction(1/error_rate)*current_weight)
    	else:
    		if one:
    			point_weight[point] = make_fraction(.5*INF*current_weight)
    		else:
    			point_weight[point] = make_fraction(make_fraction(.5)*make_fraction(1/(1-error_rate))*current_weight)
    return point_weight


def adaboost(training_points, classifier_to_misclassified,
             use_smallest_error=True, mistake_tolerance=0, max_rounds=INF):
    """Performs the Adaboost algorithm for up to max_rounds rounds.
    Returns the resulting overall classifier H, represented as a list of
    (classifier, voting_power) tuples."""
    weights = initialize_weights(training_points)
    exit = False
    H = []
    iterations = 0
    while not exit:
    	iterations+=1
    	error_rates = calculate_error_rates(weights, classifier_to_misclassified)

    	try:
    		best_class = pick_best_classifier(error_rates, use_smallest_error)
    	except NoGoodClassifiersError:
    		#print "no good"
    		exit = True
    		continue 
    	error_rate = error_rates[best_class]
    	voting_p = calculate_voting_power(error_rate)
    	H.append((best_class, voting_p))
    	if is_good_enough(H, training_points, classifier_to_misclassified, mistake_tolerance):
    		#print "good enough"
    		exit = True
    		continue
    	misclassified_points = classifier_to_misclassified[best_class]
    	weights = update_weights(weights, misclassified_points, error_rate)
    	if iterations==max_rounds:
    		#print "timeOut"
    		exit = True
    return H








#### SURVEY ####################################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 2
WHAT_I_FOUND_INTERESTING = "all"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
