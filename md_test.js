var MarkdownIt = require('markdown-it');
var fs = require('fs');
var request = require('request');

var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
var API = config.API;
var SEARCH = API + config.SEARCH;


var md = new MarkdownIt();

request.get(SEARCH, function(err, res, body){
    var results = JSON.parse(body).results;
    
    var queries = results.map(function(r){
	return {id: r.url.replace(/\//g, ''), url: API + 'project' + r.url + 'wiki/home/content/'};
    });

    queries.map(function(q){
	request.get(q.url, function(err, res, body){
	    var content = JSON.parse(body).wiki_content;
	    var result = md.render(content);    
	    
	   fs.writeFile('markdown-it_results/' + q.id + '.html', result, function(err){
		if (err){
		    console.log(err);
		}
		return;
	    });
	});
    });
});

