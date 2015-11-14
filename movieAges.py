from HTMLParser import HTMLParser
import os

# add file download and name
listOfMovies = []

class Movie():
    def __init__(self, title):
        self.title = title
        self.url = ""
        self.actorNameURL = []

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.d = False
        self.end = False

    def handle_starttag(self, tag, attrs):
        name = False

        if tag == "img":
            for attr in attrs:
                if attr[0].lower() == "class" and attr[1].lower() == "poster shadowed":
                    name = True
                if attr[0].lower() == "title" and name:
                    #print "Title:", attr[1]
                    listOfMovies.append(Movie(attr[1]))

        if tag == "a":
            for attr in attrs:
                if attr[0].lower() == "href" and attr[1].lower() == "poster shadowed":
                    print "attr:", attr
                elif attr[0].lower() == "href" and attr[1].startswith("/title") and attr[1].endswith("tt"):
                    listOfMovies[len(listOfMovies)-1].url = attr[1]


        if tag == "a":
            for name, value in attrs:
                if name == "itemprop" and value == "url":
                    self.d = True

os.system("wget -q -O movieList http://www.imdb.com/movies-in-theaters/?ref_=inth_inth")

file = open("movieList", "r")
stream = file.read()
parse = MyHTMLParser()
parse.feed(stream)
file.close()

url_base = "http://www.imdb.com"
for item in listOfMovies:
    print item.title, url_base + item.url
    actors = url_base + item.url
    wget = "wget -q -O moviePage " + actors
    os.system(wget)

    for line in open("moviePage", "r"):
        if "/name/nm" in line and "?ref_=tt_cl_t" in line:
            # get rid of a href
            item.actorNameURL.append(line)
    for link in item.actorNameURL:
        print link