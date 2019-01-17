import json
import os
import sys
import re
from collections import OrderedDict

files = []
def find_files(rootdir, result):
    for m in os.walk(rootdir):
        for n in m[2]:
            files.append(os.path.join(m[0], n))


if len(sys.argv) != 2:
    print("find-lexis.py <path>")
    exit(1)

if os.path.isfile(sys.argv[1]):
    files.append(sys.argv[1])

find_files(sys.argv[1], files)

words = {}
ignored = []
pattern = re.compile(r'^[a-z\-]+$')
punctus = """!@#$%^&*()_+=[]{}:";'<>?,./"""

for file in files:
    with open(file) as fr:
        while True:
            line = fr.readline()
            if not line: break

            line = line.strip().lower()
            for p in punctus:
                line = line.replace(p, ' ')

            ws = line.split(' ')
            for w in ws:
                if w in ignored:
                    continue
                
                if not pattern.match(w):
                    ignored.append(w)
                    continue
                
                if not w in words:
                    words[w] = {
                        'varies': [], # lie -> lies, lied, lying
                        'relates': [], # ease -> easy
                        'count': 0
                    }
                
                words[w]['count'] += 1

sorted_words = OrderedDict(sorted(words.items(), key=lambda t: -t[1]['count']))

print(sorted_words)
print(ignored)


'''
post article
query?
put acknowledged words to right.
link relates

sentence example

'''
