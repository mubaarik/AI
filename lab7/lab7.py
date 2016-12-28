# MIT 6.034 Lab 7: Support Vector Machines
# Written by Jessica Noss (jmn) and 6.034 staff

from svm_data import *
import math
# Vector math
def dot_product(u, v):
    """Computes dot product of two vectors u and v, each represented as a tuple
    or list of coordinates.  Assume the two vectors are the same length."""
    return sum([u[i]*v[i] for i in range(len(u))])

def norm(v):
    "Computes length of a vector v, represented as a tuple or list of coords."
    return math.sqrt(sum([i**2 for i in v]))

# Equation 1
def positiveness(svm, point):
    "Computes the expression (w dot x + b) for the given point"
    return dot_product(svm.w, point.coords)+svm.b

def classify(svm, point):
    """Uses given SVM to classify a Point.  Assumes that point's true
    classification is unknown.  Returns +1 or -1, or 0 if point is on boundary"""
    y = positiveness(svm, point)
    if y>0:
    	return 1
    elif y<0:
    	return -1
    return 0

# Equation 2
def margin_width(svm):
    "Calculate margin width based on current boundary."
    return 2.0/norm(svm.w)

# Equation 3
def check_gutter_constraint(svm):
    """Returns the set of training points that violate one or both conditions:
        * gutter constraint (positiveness == classification for support vectors)
        * training points must not be between the gutters
    Assumes that the SVM has support vectors assigned."""
    #print "support vectors: ", svm.support_vectors
    gutter_points = set()
    for point in svm.support_vectors:
    	pos = abs(positiveness(svm, point))

    	if pos != 1 or int(point.classification)!=int(positiveness(svm, point)):
    		gutter_points.add(point)


    for point in svm.training_points:
    	pos = abs(positiveness(svm, point))
    	if pos<1:#margin_width(svm):
            gutter_points.add(point)
    return gutter_points
    

# Equations 4, 5
def check_alpha_signs(svm):
    """Returns the set of training points that violate either condition:
        * all non-support-vector training points have alpha = 0
        * all support vectors have alpha > 0
    Assumes that the SVM has support vectors assigned, and that all training
    points have alpha values assigned."""
    alphs = set()
    for point in svm.training_points:

    	if point.alpha!= 0 and not point in svm.support_vectors:
    		alphs.add(point)
    	elif point.alpha<=0 and point in svm.support_vectors:
    		alphs.add(point)
    return alphs


def multiply_con(cont, vect):
	new_vect = []
	for i in vect:
		new_vect.append(cont*i)
	return new_vect
def add_arr(arr,arr2):
	return [arr[i]+arr2[i] for i in range(len(arr))]
def suming_fun(arr):
	new_arr =arr[0]
	for ar in arr[1:]:
		new_arr=add_arr(new_arr, ar) 
	return new_arr
def check_alpha_equations(svm):
    """Returns True if both Lagrange-multiplier equations are satisfied,
    otherwise False.  Assumes that the SVM has support vectors assigned, and
    that all training points have alpha values assigned."""
    eq4 = sum([point.classification*point.alpha for point in svm.training_points])
    eq5 = suming_fun([multiply_con(point.alpha*point.classification, point.coords) for point in svm.training_points])
    return (eq5 == svm.w and eq4==0)

# Classification accuracy
def misclassified_training_points(svm):
    """Returns the set of training points that are classified incorrectly
    using the current decision boundary."""
    miscl = set()
    for point in svm.training_points:
    	if point.classification!=classify(svm, point):
    		miscl.add(point)
    return miscl

# Training
def update_svm_from_alphas(svm):
    """Given an SVM with training data and alpha values, use alpha values to
    update the SVM's support vectors, w, and b.  Return the updated SVM."""
    min_gut = 100
    max_gut =  -100

    mult = len(svm.training_points[0].coords)
    w=[0]*mult
    svs = []
    for point in svm.training_points:
        scal = point.classification*point.alpha
        y = point.classification
        w  = add_arr(multiply_con(scal, point.coords), w)
        if point.alpha>0:
            svs.append(point)

    for point in svs:
        y = point.classification
        b = y - dot_product(point.coords, w)
        if b>max_gut and y>0:
            max_gut = b 
        elif b<min_gut and y<0:
            min_gut = b

    b = (max_gut+min_gut)/2.0
    svm.w = w;
    svm.b = b;
    svm.support_vectors = svs;
    return svm; 

   

# Multiple choice
ANSWER_1 = 11
ANSWER_2 = 6
ANSWER_3 = 3
ANSWER_4 = 2

ANSWER_5 = ["A", "D"]
ANSWER_6 = ["A", "B", "D"]
ANSWER_7 = ["A","B", "D"]
ANSWER_8 = []
ANSWER_9 = ["A","B", "D"]
ANSWER_10 = ["A","B", "D"]

ANSWER_11 = False
ANSWER_12 = True
ANSWER_13 = False
ANSWER_14 = False
ANSWER_15 = False
ANSWER_16 = True

ANSWER_17 = [1,3,6,8]
ANSWER_18 = [1,2,4,5,6,7,8]
ANSWER_19 = [1,2,4,5,6,7,8]

ANSWER_20 = 6


#### SURVEY ####################################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 5
WHAT_I_FOUND_INTERESTING = "Training"
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""
