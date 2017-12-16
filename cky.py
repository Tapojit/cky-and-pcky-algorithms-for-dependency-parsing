from pprint import pprint

# The productions rules have to be binarized.

grammar_text = """
S -> NP VP
S -> NPP VPP
NP -> Det Noun
NPP -> Det NounP
VP -> Verb NP
VPP -> VerbP NP
VPP -> VerbP NPP
NPP -> NPP VPP
PP -> Prep NP
NP -> NP PP
VP -> VP PP


"""

lexicon = {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'NounP': set(['cats', 'dogs']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated', 'attacks']),
    'VerbP':set(['attacked', 'saw', 'loved', 'hated', 'attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the','a']),
}

# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

# print "Grammar rules in tuple form:"
# pprint(grammar_rules)
# print "Rule parents indexed by children:"
# pprint(possible_parents_for_children)


def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon, possible_parents_for_children
    

    # Set up the cells data structure.
    # It is intended that the cell indexed by (i,j)
    # refers to the span, in python notation, sentence[i:j],
    # which is start-inclusive, end-exclusive, which means it includes tokens
    # at indexes i, i+1, ... j-1.
    # So sentence[3:4] is the 3rd word, and sentence[3:6] is a 3-length phrase,
    # at indexes 3, 4, and 5.
    # Each cell would then contain a list of possible nonterminal symbols for that span.
    # If you want, feel free to use a totally different data structure.
    N = len(sentence)
    cells = {}
    for i in range(N):
        a=0
        for j in range(i + 1, N + 1):
            cells[(a, j)] = []
            if(abs(a-j)==1):
                for key in lexicon:
                    if(sentence[a] in lexicon[key]):
                        cells[(a, j)].append(key)
                a+=1
            elif(abs(a-j)>1):
                for idx in range(abs(a-j)-1):
                    
                    ind1=cells[(a,j-1-idx)]
                    ind2=cells[(j-1-idx,j)]
                    if(not ind1 or not ind2):
                        pass
                    else:
                        for k1 in ind1:
                            for k2 in ind2:
                                if((k1,k2) in possible_parents_for_children):
                                    cells[(a,j)].append(possible_parents_for_children[(k1,k2)][0])
                a+=1
            
            
                

    # TODO replace the below with an implementation
    pprint(cells)
    res=False
    if(len(cells[(0,N)])!=0):
        if(cells[(0,N)][0]=='S'):
            res=True
    return res


def cky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon, possible_parents_for_children

    N = len(sentence)
    cells = {}
    for i in range(N):
        a=0
        for j in range(i + 1, N + 1):
            cells[(a, j)] = []
            if(abs(a-j)==1):
                for key in lexicon:
                    if(sentence[a] in lexicon[key]):
                        cells[(a, j)].append((key,0,sentence[a],sentence[a]))
                a+=1
            elif(abs(a-j)>1):
                for idx in range(abs(a-j)-1):
                    
                    ind1=cells[(a,j-1-idx)]
                    ind2=cells[(j-1-idx,j)]
                    if(not ind1 or not ind2):
                        pass
                    else:
                        for k1 in ind1:
                            for k2 in ind2:
                                if((k1[0],k2[0]) in possible_parents_for_children):
                                    cells[(a,j)].append((possible_parents_for_children[(k1[0],k2[0])][0], j-1-idx,k1[0],k2[0]))
                a+=1
    
    res=backpointer(cells, [], (0,N))
    if(len(res)==0):
        return None
    # TODO replace the below with an implementation
    return res
def backpointer(dict,list,tuple):
    if(len(dict[tuple])==0):
        return []
    if(dict[tuple][0][1]==0):
        return [dict[tuple][0][0], dict[tuple][0][2]]
    
    list.append(dict[tuple][0][0])
    list2=[]
    list2.append(backpointer(dict, [], (tuple[0],dict[tuple][0][1])))
    list2.append(backpointer(dict, [], (dict[tuple][0][1],tuple[1])))
    list.append(list2)
    
    return list
## some examples of calling these things...
## you probably want to call only one sentence at a time to help debug more easily.

# print cky_parse(['a', 'cats', 'attack', 'the', 'dog'])
# pprint( cky_parse(['the','cat','attacked','the','food']))
# pprint( cky_acceptance(["the", "table", "attacked", "a", "dog"]))
# pprint( cky_parse(['the','the']))
# print cky_acceptance(['the','cat','attacked','the','food','with','a','dog'])
# pprint( cky_parse(['the','cat','attacked','the','food','with','a','dog']) )
# pprint( cky_parse(['the','cat','with','a','table','attacked','the','food']) )
#
