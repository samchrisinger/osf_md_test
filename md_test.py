import sys
import markdown 
from markdown.extensions import codehilite, fenced_code, wikilinks
from json import loads
from requests import get as rget
from glob import glob

config = loads(open('./config.json', 'r').read())

API = config['API']
SEARCH = API + config['SEARCH']
LOCAL = config['LOCAL']
LOCAL_PATH = config['LOCAL_PATH']


def build_wiki_url(node, label, base, end):
    return node.web_url_for('project_wiki_page', wname=label)

def build_url(label, base, end):
    import pdb; pdb.set_trace()

def render_and_write(id, md_string):
    result = markdown.markdown(
        md_string,
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
    
    f = open('markdown-py_results/' + id + '.html', 'w')
    f.write(result.encode('ascii', 'ignore'))
    f.close()


cached = (len(sys.argv) > 1 and sys.argv[1] == '--cached')
if cached: 
    md_files = glob('./mdcache/*.md')
    for f in md_files:
        with open(f, 'r') as mdfile:
            id = f.split('/')[-1].rstrip('.md')
            render_and_write(id, mdfile.read())
else: 
    queries = []
    if LOCAL:
        queries = loads(open(LOCAL_PATH, 'r').read())
    else:
        resp = rget(SEARCH)
        results = resp.json().get('results')
        queries = map(lambda r: dict(id=r.get('url').replace('/', ''), url=("{0}project{1}wiki/home/content/".format(API, r.get('url')))), results)

    for q in queries:
        resp = rget(q['url'])
        # Always cache the markdown
        md_string = resp.json().get('wiki_content')
        f = open('./mdcache/' + q['id'] + '.md', 'w')
        f.write((md_string or '').encode('ascii', 'ignore'))
        f.close()
        render_and_write(q['id'], md_string)




