import lemmagen
from lemmagen.lemmatizer import Lemmatizer
from nltk import word_tokenize

dataset = 'data/preprocessed/vejica_filtered.txt'
print('Lemmatizing')

l = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
commas = {'¤': ' MISSINGCOMMA ', '÷': ' TOOMUCHCOMMA ', ',': ' FIXEDCOMMA '}
file1 = open(dataset, 'r').read()
for comma_type in commas:
    file1 = file1.replace(comma_type, commas[comma_type])
file1 = file1.split('\n')
sentences = {}
for row in range(len(file1)):
    s = file1[row].split('\t')
    if len(s) == 2:
        sentences[s[0]] = s[1]

for key in sentences:
    sent = word_tokenize(sentences[key])
    sent = [l.lemmatize(word) for word in sent]
    sent = [word.upper() for word in sent]
    sentences[key] = sent


# export to file for word2vec
print('Exporing tokenized lemmatized sentences')
f = open("data/preprocessed/vejica_lemmatized_raw.txt", "w")
f1 = open("data/preprocessed/vejica_lemmatized_with_ids.txt", "w")

for key in sentences:
    f1.write(key)
    f1.write('\t')
    f.write(' '.join(sentences[key]))
    f.write('\n')
    f1.write(' '.join(sentences[key]))
    f1.write('\n')
f.close()
print('Files written.')