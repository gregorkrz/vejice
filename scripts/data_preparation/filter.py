

data = open("data/raw/vejica13.txt", "r")

def cond(text):
    # Only specific corpuses are kept.
    return text.startswith("Wiki.") or text.startswith("Solar.") or  text.startswith("Lektor.")

def cond1(text):
    # Keep only the sentences that have at least one correction.
    return '¤' in text or '÷' in text

counts = {}

def renumber(line):
    # Number duplicates.
    id, sentence = line.split("\t")
    if id in counts:
        counts[id] += 1
        id = id + ".{}".format(counts[id])
    else:
        counts[id] = 0
    return "{}\t{}".format(id, sentence)
    
out = open("data/preprocessed/vejica_filtered.txt", "w")

line = True
while line:
    line = data.readline()
    if not cond(line) or not cond1(line):
        continue
    line = renumber(line).replace(",÷", "÷") # this is present in the data, for some reason
    out.write(line)

out.close()
print("Files written")