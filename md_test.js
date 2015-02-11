var md = require('markdown-it')('commonmark');
var fs = require('fs');
var request = require('request');

var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
var API = config.API;
var SEARCH = API + config.SEARCH;
var LOCAL = config.LOCAL;
var LOCAL_PATH = config.LOCAL_PATH;


var renderAndWrite = function(id, md_string) {
    var result = md.render(md_string);

    fs.writeFile('markdown-it_results/' + id + '.html', result, function(err) {
        if (err) {
            console.log(err);
        }
        return;
    });
};

var processQueries = function(queries) {
    queries.forEach(function(q) {
        request.get(q.url, function(err, res, body) {
            var content = JSON.parse(body).wiki_content;
            renderAndWrite(q.id, content);
        });
    });
};


var cached = (process.argv.length > 2 && process.argv[2] == '--cached');
if (cached) {
    var mdFiles = fs.readdirSync('./mdcache/').filter(function(f) {
        return f.indexOf('.') !== 0;
    });
    mdFiles.forEach(function(file) {
        var id = file.split('.')[0];
        var md_string = fs.readFileSync('./mdcache/' + file, 'utf-8');
        renderAndWrite(id, md_string);
    });
} else {
    if (LOCAL) {
        var queries = JSON.parse(fs.readFileSync(LOCAL_PATH, 'utf-8'));
        processQueries(queries);
    } else {
        request.get(SEARCH, function(err, res, body) {
            var results = JSON.parse(body).results;
            var queries = results.map(function(r) {
                return {
                    id: r.url.replace(/\//g, ''),
                    url: API + 'project' + r.url + 'wiki/home/content/'
                };
            });
            processQueries(queries);
        });
    }
}
