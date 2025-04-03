import spacy
from spacy.cli import download

##TASK 1
# Loading the small English model
nlp = spacy.load("en_core_web_sm")

# Coding the text to tokenize
text = "The quick brown fox doesn't jump over the lazy dog. Natural Language Processing is fascinating!"

# Processing the text
doc = nlp(text)

# Printing each token
print("Tokens:")
for token in doc:
    print(token.text)
##RESPONDING TO QUESTIONS: 

##SpaCy processes the tokens taking the text and converting it to a doc object. Later, each word or symbol becomes a Token object. That allows users to then go thorugh each token.
##Each punctuation mark is its own token. 
##Contractions are split up. Won't would be separated by the verb and the negation particle (will, n't)

##TASK 2
# Printing token details including POS and tag factors
print("Token\t\tPOS\t\tTAG")
print("-" * 40)
for token in doc:
    print(f"{token.text:<15}{token.pos_:<10}{token.tag_}")

##RESPONDING TO QUESTIONS:
##The POS tag for quick is JJ
##The POS tag for jumps is VB
##The POS tag for is is VBZ
##Could be useful when the combination of words used isn't grammatically correct. The tags tell the system if the use is correct, and which is most accurate when there could be two possible. 


#TASK 3
# Changing text
text = "Barack Obama was the 44th President of the United States. He was born in Hawaii."
# Re-processing the new text
doc = nlp(text)
# Extracting and displaying named entities
print("\nNamed Entities:")
for ent in doc.ents:
    print(f"{ent.text:<25} {ent.label_}")

##RESPONDING TO QUESTIONS:
    ##spaCy recognized Barack Obama, 44th, the United States, and Hawaii. 
    ##Barack Obama as a person (which is impressive to me). 
    ##44th as Ordinal
    ##the United Sates and Hawaii as GPE, which is geopolitical entity. 


##TASK 4
text= "Studying in Hesburgh Library on south bend is a convenient yet stressful place."
doc = nlp(text)
print("\nNamed Entities in Custom Text:")
for ent in doc.ents:
    print(f"{ent.text:<25} {ent.label_}")

##RESPONDING TO QUESTIONS:
##South Bend is recognized as a Location, and Hesburgh Libaray as an ORG.
##When I change the text to south bend, without capitals it is not recognized as a location. 
#putting on south bend instead of in south bend is not recognized as an error. 