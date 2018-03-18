# CKY and PCKY algorithms for sentence parsing
Using CKY and PCKY algorithm to obtain grammatical sentence parses.

The **Cocke–Kasami–Younger(CKY)** algorithm uses *Context Free Grammar(CFG)* rules to obtain a legal parse of a given sentence.
If a sentence has no legal parse, either the sentence is ungrammatical or set of CFG rules is not adequate. Below is an array
of tuples containing CFG rules.
```
Grammar rules in tuple form:
[('S', ('NP', 'VP')),
 ('NP', ('Det', 'Noun')),
 ('VP', ('Verb', 'NP')),
 ('PP', ('Prep', 'NP')),
 ('NP', ('NP', 'PP')),
 ('VP', ('VP', 'PP'))]
 
 ```
 
