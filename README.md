# CKY and PCKY algorithms for sentence parsing
Using CKY and PCKY algorithm to obtain grammatical sentence parses.

## CKY

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
The **cky.py** script contains the function *cky_parse* which returns a legal parse of a given sentence. The function takes an array of words as an argument, hence the sentence needs to be converted into an array of words. If the given sentence has no legal parse, **None** is returned.

### Running the function:

After downloading this repository, use **bash** to *cd* into its directory. Once there, run the following line in bash to obtain a legal parse of the sentence *"the cat saw a dog in a table"*:
```
python -c "import cky; from pprint import pprint; pprint(cky.cky_parse(['the', 'cat', 'saw', 'a', 'dog', 'in', 'a', 'table']))"

```
According to the grammar rules and the lexicon provided in the *cky* script, the sentence above is grammatical, whose legal parse is:

```
['S',
 [['NP', [['Det', 'the'], ['Noun', 'cat']]],
  ['VP',
   [['VP', [['Verb', 'saw'], ['NP', [['Det', 'a'], ['Noun', 'dog']]]]],
    ['PP', [['Prep', 'in'], ['NP', [['Det', 'a'], ['Noun', 'table']]]]]]]]]

```
