import sys
from glob import glob
from subprocess import call

config = {
    'update': True
}

def parse_bool(b):
    if b == "True" or b == "true" or b == "1":
        return True
    return False

if len(sys.argv) > 1:
    args = sys.argv[1:]    
    for arg in args:
        parts = arg.split('=')
        if parts[0] in config:
            config[parts[0]] = parse_bool(parts[1])


if config['update']:
    call('node md_test.js', shell=True)
    call('python md_test.py', shell=True)

MARKDOWNIT_RESULTS = './markdown-py_results'
MARKDOWNPY_RESULTS = './markdown-it_results'

getfname = lambda p: p.split('/')[-1]
results = set(map(getfname, glob(MARKDOWNIT_RESULTS + '/*.html'))).intersection(
    set(map(getfname, glob(MARKDOWNPY_RESULTS + '/*.html')))
)

for result in results:
    call("diff -b {0}/{1} {2}/{1} >> ./diffs/{3}".format(MARKDOWNPY_RESULTS, result, MARKDOWNIT_RESULTS, result.split('.')[0]), shell=True)

diffs = glob('./diffs/*')

minlength = 1000000000
maxlength = -1
acclength = 0
accempty = 0
for diff in diffs:
    content = open(diff, 'r').read()
    length = len(content)
    if length == 0:
        accempty += 1
    if length < minlength:
        minlength = length
    if length > maxlength:
        maxlength = length
    acclength += length

avglength = acclength / len(diffs)

print "-"*30
print "Docs compared: {0}".format(len(diffs))
print "Empty diffs: {0}".format(accempty)
print "Non-empty diffs: {0}".format(len(diffs) - accempty)
print "Min diff size: {0} chars".format(minlength)
print "Max diff size: {0} chars".format(maxlength)
print "Avg diff size: {0} chars".format(avglength)
print "-"*30

    
