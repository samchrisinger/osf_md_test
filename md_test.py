import markdown 
from markdown.extensions import codehilite, fenced_code, wikilinks
from json import loads
from requests import get as rget

config = loads(open('./config.json', 'r').read())

API = config['API']
SEARCH = API + config['SEARCH']
LOCAL = config['LOCAL']
LOCAL_PATH = config['LOCAL_PATH']

queries = []
if LOCAL:
    queries = loads(open(LOCAL_PATH, 'r').read())
else:
    resp = rget(SEARCH)
    results = resp.json().get('results')
    queries = map(lambda r: dict(id=r.get('url').replace('/', ''), url=("{0}project{1}wiki/home/content/".format(API, r.get('url')))), results)

def build_wiki_url(node, label, base, end):
    return node.web_url_for('project_wiki_page', wname=label)

def build_url(label, base, end):
    import pdb; pdb.set_trace()

for q in queries:
    resp = rget(q['url'])
    result = markdown.markdown(
        resp.json().get('wiki_content'),
        extensions=[
            wikilinks.WikiLinkExtension(
                configs=[
                    ('base_url', ''),
                    ('end_url', ''),
                    ('build_url', build_url)
                ]
            ),
            fenced_code.FencedCodeExtension(),
            codehilite.CodeHiliteExtension(
                [('css_class', 'highlight')]
            )
         ]
    )    
    
    f = open('markdown-py_results/' + q['id'] + '.html', 'w')
    f.write(result.encode('ascii', 'ignore'))
    f.close()






