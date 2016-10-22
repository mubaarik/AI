# MIT 6.034 Lab 1: Rule-Based Systems
# Written by 6.034 staff

from production import IF, AND, OR, NOT, THEN, DELETE, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = '4'

ANSWER_3 = '2'

ANSWER_4 = '0'

ANSWER_5 = '3'

ANSWER_6 = '1'

ANSWER_7 = '0'

#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?z) beats (?x)'), THEN('(?z) beats (?y)') )

# You can test your rule by uncommenting these print statements:
print forward_chain([transitive_rule], abc_data)
print forward_chain([transitive_rule], poker_data)
print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:
rulex=IF("person (?x)", THEN("self (?x) (?x)"))
rule1=IF("parent (?x) (?y)", THEN("child (?y) (?x)"))
#

rule2=IF(AND("parent (?x) (?y)", "parent (?x) (?z)", NOT("self (?y) (?z)")), THEN("sibling (?y) (?z)"))
rule3=IF(AND(OR("sibling (?x) (?y)","sibling (?y) (?x)"), "parent (?x) (?z)", "parent (?y) (?w)"), THEN("cousin (?z) (?w)"))
rule4=IF(AND("parent (?x) (?y)", "parent (?y) (?z)"),THEN("grandparent (?x) (?z)"))
rule5=IF("grandparent (?x) (?y)",THEN("grandchild (?y) (?x)"))



# Add your rules to this list:
family_rules = [rulex, rule1,rule2, rule3, rule4, rule5]

# Uncomment this to test your data on the Simpsons family:=
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [
    relation for relation in
    forward_chain(family_rules, black_data, verbose=False)
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def putHypos(hypos, anteced):
    for sttment in anteced:
        if isinstance(sttment, str):
            hypos.append(sttment)
        else:
            hypos.append(putHypos(hypos, sttment))
    return hypos
def hasMatch(hypothesis, rules):
    matched = False
    for rule in rules:
        for stmnt in rule.consequent():
            mymatch=match(stmnt,hypothesis)
            if mymatch!=None:
                return True
    return matched



#com=0
def backchain_to_goal_tree(rules, hypothesis):
    """
    Takes a hypothesis (string) and a list of rules (list
    of IF objects), returning an AND/OR tree representing the
    backchain of possible statements we may need to test
    to determine if this hypothesis is reachable or not.

    This method should return an AND/OR tree, that is, an
    AND or OR object, whose constituents are the subgoals that
    need to be tested. The leaves of this tree should be strings
    (possibly with unbound variables), *not* AND or OR objects.
    Make sure to use simplify(...) to flatten trees where appropriate.

    """
    
   # print "Random matching", match('h (?y) j', 'h i j')
    tree=(OR(hypothesis))
    if not hasMatch(hypothesis, rules):
    
        return simplify(OR(hypothesis));


    else:

        for rule in rules:
            for stmnt in rule.consequent():
                mymatch=match(stmnt, hypothesis)

                if mymatch!=None:# and mymatch!={}:
                    anteced = simplify(populate(rule.antecedent(), mymatch))

                    sub=[]
                    if isinstance(anteced, str):
                        sub=backchain_to_goal_tree(rules, anteced)
                        tree.append(sub)
                        #return simplify(OR(hypothesis, sub))
                    elif isinstance(anteced, AND):
                        sub=AND()
                        for st in anteced:
                            sub.append(backchain_to_goal_tree(rules, st))
                            #sub.append(AND(backchain_to_goal_tree(rules, st) for st in anteced))

                        tree.append(sub)
                        
                        #return simplify(OR(hypothesis, sub))
                    elif isinstance(anteced, OR):
                        sub=OR()
                        for st in anteced:
                            sub.append(backchain_to_goal_tree(rules, st))
                        tree.append(sub)
                       # return simplify(OR(hypothesis, sub))
    return simplify(tree)
    

# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = ""
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = "BackChaining"
WHAT_I_FOUND_BORING = "Family rules"
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
