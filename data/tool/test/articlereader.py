# Usage: >>> python articlereader.py [file path]

import sys, json, codecs, webbrowser

f = codecs.open(sys.argv[1], 'r', 'utf-8')
doc = json.loads(f.read())
f.close()

fname = 'article.html'
f = codecs.open(fname, 'w', 'utf-8')
f.write('<h4>%s</h4>' % doc['headline']['main'])
f.write('<p><a href="%s">Link</a></p>' % doc['web_url'])
f.write(doc['article'])
f.close()

path = sys.path[0].replace('\\', '/')
url = 'file:///' + path + '/' + fname
webbrowser.open_new_tab(url)