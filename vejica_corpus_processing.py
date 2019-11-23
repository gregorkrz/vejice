import sys


# Select only entries that have some corrections, and are only from corpuses that offer good sentences


def cond(text):
    return text.startswith("Wiki.") or text.startswith("Solar.") or  text.startswith("Lektor.")

def cond1(text):
    return '¤' in text or '÷' in text

for line in sys.stdin:
    if cond(line) and cond1(line):
        sys.stdout.write(line)
