# CKY and PCKY algorithms for sentence parsing
Using CKY and PCKY algorithm to obtain grammatical sentence parses.

## CKY

The **Cocke–Kasami–Younger(CKY)** algorithm uses *Context Free Grammar(CFG)* rules and lexicon to obtain a legal parse of a given sentence.
If a sentence has no legal parse, either the sentence is ungrammatical or set of CFG rules is not adequate. Below is an array
of tuples containing CFG rules and a dictionary of lexicon.
```
Grammar rules in tuple form:
[('S', ('NP', 'VP')),
 ('NP', ('Det', 'Noun')),
 ('VP', ('Verb', 'NP')),
 ('PP', ('Prep', 'NP')),
 ('NP', ('NP', 'PP')),
 ('VP', ('VP', 'PP'))]
 
 lexicon:
 {
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'NounP': set(['cats', 'dogs']),
    'Verb': set(['attacked', 'saw', 'loved', 'hated', 'attacks']),
    'VerbP':set(['attacked', 'saw', 'loved', 'hated', 'attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the','a']),
}
 
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
The function will return **None** for an ungrammatical sentence like *"the cat with the food on a dog attack the dog"*.

***NOTE:*** To obtain legal parses over a larger lexicon of words, look at the code in *cky.py* and update variables **grammar_text** & **lexicon** accordingly.

## PCKY

**Probabilistic CKY** (PCKY for short) uses *CFG* and its probability distribution to obtain the most probable legal parse. The **pcfg_grammar_modified** file contains tab-separated *CFG* rules and their probability distributions. In the script **weighted_cky.py**, *PCKY* is implemented using **pcky_parse** function. 

### Running the function:

Just like the *cky_parse* function, use **bash** to *cd* into the repository directory. From there, run the following line to obtain a legal parse of the phrase *"book the flight through Houston"*:

```
python -c "from weighted_cky import pcky_parse; from pprint import pprint; pprint( pcky_parse(['book','the','flight','through','Houston']))"

```
