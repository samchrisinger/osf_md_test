import markdown 
from markdown.extensions import codehilite, fenced_code, wikilinks
import json
from requests import get as rget

config = json.loads(open('config.json', 'r').read())

API = config['API']
SEARCH = API + config['SEARCH']

resp = rget(SEARCH)
results = resp.json().get('results')

queries = map(lambda r: dict(id=r.get('url').replace('/', ''), url=("{0}project{1}wiki/home/content/".format(API, r.get('url')))), results)

'''
        extensions=[
            wikilinks.WikiLinkExtension(
                configs=[
                    ('base_url', ''),
             1       ('end_url', ''),
                    ('build_url', functools.partial(build_wiki_url, node))
                ]
            ),
            fenced_code.FencedCodeExtension(),
            codehilite.CodeHiliteExtension(
                [('css_class', 'highlight')]
            )
         ]
'''

for q in queries:
    resp = rget(q['url'])
    result = markdown.markdown(
        resp.json().get('wiki_content'),
    )    
    
    f = open('markdown-py_results/' + q['id'] + '.html', 'w')
    f.write(result.encode('ascii', 'ignore'))
    f.close()






