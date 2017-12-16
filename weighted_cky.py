from pprint import pprint
import operator
grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}
file=open("pcfg_grammar_modified",'r')
rules=file.read()
a=2
def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    for line in rules.strip().split("\n"):
        if not line.strip(): continue
        left, right = line.split("->")
        left = left.strip()
        children = right.split()
        if(len(children)>2):
            rule = (left, tuple(children[:2]))
            grammar_rules.append(rule)
            probabilities[rule]=float(children[-1])
        elif(left in lexicon):
            lexicon[left].add(children[0])
            probabilities[left,children[0]]=float(children[-1])
        else:
            lexicon[left]=set()
            lexicon[left].add(children[0])
            probabilities[left,children[0]]=float(children[-1])
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
  
#     print "Grammar rules in tuple form:"
#     pprint(grammar_rules)
#     print "Rule parents indexed by children:"
#     pprint(possible_parents_for_children)
#     print "probabilities"
#     pprint(probabilities)
#     print "Lexicon"
#     pprint(lexicon)


def pcky_parse(sentence):
    # Return one of the legal parses for the sentence.
    # If nothing is legal, return None.
    # This will be similar to cky_acceptance(), except with backpointers.
    global grammar_rules, lexicon, possible_parents_for_children, probabilities

    N = len(sentence)
    cells = {}
    backward={}
    for i in range(N):
        a=0
        for j in range(i + 1, N + 1):
            cells[(a, j)] = []
            if(abs(a-j)==1):
                for key in lexicon:
                    if(sentence[a] in lexicon[key]):
                        cells[(a, j)].append((key,sentence[a], probabilities[key,sentence[a]]))
                a+=1
            elif(abs(a-j)>1):
                for idx in range(abs(a-j)-1):
                    
                    ind1=cells[(a,j-1-idx)]
                    ind2=cells[(j-1-idx,j)]
                    back={}
                    if(not ind1 or not ind2):
                        pass
                    else:
                        for k1 in ind1:
                            for k2 in ind2:
                                if((k1[0],k2[0]) in possible_parents_for_children):
                                    prob_top=probabilities[possible_parents_for_children[(k1[0],k2[0])][0],(k1[0],k2[0])]
                                    prob_calc=prob_top*k1[-1]*k2[-1]
                                    appender_sh=(possible_parents_for_children[(k1[0],k2[0])][0], j-1-idx,k1[0],k2[0])
                                    back[appender_sh]=prob_calc
                                    appender=(possible_parents_for_children[(k1[0],k2[0])][0], j-1-idx,k1[0],k2[0], probabilities[possible_parents_for_children[(k1[0],k2[0])][0],(k1[0],k2[0])])
                                    cells[(a,j)].append(appender)
                        if(bool(back)):
                            backward[(a,j)]=max(back.iteritems(), key=operator.itemgetter(1))[0]
                a+=1
    
    res=backpointer(cells,backward, [], (0,N))
    if(len(res)==0):
        return None
    # TODO replace the below with an implementation
    return res
def backpointer(dict,back,list,tuple):
    if(not tuple in back):
        return []
    left=(tuple[0],back[tuple][1])
    right=(back[tuple][1], tuple[1])
    if(left in back):
        node_tar_l=backpointer(dict, back, [], left)
    else:
        li_node=dict[left]
        node_tar_l=0
        for node in li_node:
            if(node[0]==back[tuple][2]):
                node_tar_l=[node[0],node[1]]
    if(right in back):
        node_tar_r=backpointer(dict, back, [], right)
    else:
        li_node=dict[right]
        node_tar_r=0
        for node in li_node:
            if(node[0]==back[tuple][3]):
                node_tar_r=[node[0],node[1]]
    
    
    list.append(back[tuple][0])
    list2=[]
    list2.append(node_tar_l)
    list2.append(node_tar_r)
    list.append(list2)
    return list

populate_grammar_rules()
# pprint(cky_parse(['book','this','flight','through','Houston']))
