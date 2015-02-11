var fs = require('fs');
var request = require('request');
var md = require('markdown-it')('commonmark');
//var hljs = require('highlight.js')
/*({
    html: true,
    linkify: true,
    highlight: function (str, lang) {
	if (lang && hljs.getLanguage(lang)) {
	    try {
		return hljs.highlight(lang, str).value;
	    } catch (__) {}
	}
	try {
	    return hljs.highlightAuto(str).value;
	} catch (__) {}	
	return ''; // use external default escaping
    }
})*/

var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
var API = config.API;
var SEARCH = API + config.SEARCH;
var LOCAL = config.LOCAL;
var LOCAL_PATH = config.LOCAL_PATH;

var processQueries = function(queries){
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
};

if (LOCAL){
    var queries = JSON.parse(fs.readFileSync(LOCAL_PATH, 'utf-8'));       
    processQueries(queries);
}
else{
    request.get(SEARCH, function(err, res, body){
	var results = JSON.parse(body).results;
	var queries = results.map(function(r){
	    return {id: r.url.replace(/\//g, ''), url: API + 'project' + r.url + 'wiki/home/content/'};
	});
	processQueries(queries);
    });
}

