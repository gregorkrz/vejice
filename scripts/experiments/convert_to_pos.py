# convert sentences to sequences of parts of speech only
import classla
from time import time

classla.download('sl', type='nonstandard')
nlp = classla.Pipeline('sl', processors='pos,tokenize', type='nonstandard')
from nltk import word_tokenize

dataset = 'data/preprocessed/vejica_filtered.txt'
print('Replacing words with POS')

commas = {'¤': 'MISSINGCOMMA', '÷': 'TOOMUCHCOMMA', ',': 'FIXEDCOMMA'}
file1 = open(dataset, 'r').read()
for comma_type in commas:
    file1 = file1.replace(comma_type, " {} ".format(commas[comma_type]))
file1 = file1.split('\n')
sentences = {}
lemma_sentences = {}
for row in range(len(file1)):
    s = file1[row].split('\t')
    if len(s) == 2:
        sentences[s[0]] = s[1]

n = 0
t = time()

for key in sentences:
    n += 1
    if n % 100 == 0:
        print("Processed", n, "; took", int(time()-t), "secs")
        t = time()
    doc = nlp(sentences[key])
    pos_list = list()
    lemma_list = list()
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.text in commas.values():
                pos_list.append(word.text)
                #lemma_list.append(word.text)
            else:
                pos_list.append(word.pos)
                #lemma_list.append(word.lemma)
    sentences[key] = pos_list
    #lemma_sentences[key] = lemma_list
    #sent = word_tokenize(sentences[key])
    #sent = [l.lemmatize(word) for word in sent]
    #sent = [word.upper() for word in sent]
    #sentences[key] = sent

# export to file for word2vec
print('Exporing POS sentences')
f = open("data/preprocessed/vejica_POS_raw.txt", "w")
f1 = open("data/preprocessed/vejica_POS_with_keys.txt", "w")
lf = open("data/preprocessed/lemmatized_sentences.txt", "w")

for key in sentences:
    f1.write(key)
    f1.write('\t')
    #lf.write(key)
    #lf.write('\t')
    f.write(' '.join(sentences[key]))
    f.write('\n')
    f1.write(' '.join(sentences[key]))
    f1.write('\n')
    #lf.write(' '.join(lemma_sentences[key]))
    #lf.write('\n')
f.close()
f1.close()
print('Files written.')