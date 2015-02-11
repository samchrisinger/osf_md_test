# Getting started

- Setup your virtualenv, and ```pip install -r requirements.txt```
- Run ```npm install```

# Running

- With your virtualenv active, run ```python run.py [|update=True]```

# What to expect

This script fetches some markdown documents from the OSF, renders them as html using both the python markdown module and the javascript library markdown-it. The rendered html is then compared using diff, like ``` diff -b [python-rendered-file] [js-rendered-file] ```. Some results of the diffing are printed to the console, and diffs are stored in the diffs directory.

