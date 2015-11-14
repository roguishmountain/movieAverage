from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
	
    def handle_starttag(self, tag, attrs):
    	name = False
        if tag == "img":
        	for attr in attrs:
        		if attr[0].lower() == "class" and attr[1].lower() == "poster shadowed":
        			name = True
        		if attr[0].lower() == "title" and name:
        			print "attr:", attr[1]


file=open("movieList","r")
stream=file.read()
parse = MyHTMLParser()
parse.feed(stream)