""" Quick and dirty script to remove possible swears from a list of names """
import sys
import re
import os

print('reading swears...', file=sys.stderr)
swears = map(re.escape, open('swears').read().lower().split())
print('compiling re...', file=sys.stderr)
matcher = re.compile('|'.join(swears))

print('processing...', file=sys.stderr)

lines = []
with open(sys.argv[1]) as fh:
    for line in map(str.strip, fh):
        if not matcher.search(line.lower()):
            lines.append(line)

os.rename(sys.argv[1], sys.argv[1] + ".orig")

with open(sys.argv[1], 'w') as fh:
    print(*lines, sep='\n', file=fh)
