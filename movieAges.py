from html.parser import HTMLParser
import os

# add file download and name
listOfMovies = []

class Movie():
    def __init__(self, title):
        # title of movie
        self.title = title
        # url to movie page
        self.url = ""
        # list of urls for actor pages
        self.actor_name_url = []
        # list of ages of actors
        self.ages = []
        # average age of actors
        self.avg_age = 0

class MyHTMLParser(HTMLParser):
    def __init__(self, actor_page):
        HTMLParser.__init__(self)
        self.d = False
        self.end = False
        self.actor_page = actor_page

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
                    print("attr: " + attr)
                elif attr[0].lower() == "href" and attr[1].startswith("/title") and attr[1].endswith("tt"):
                    listOfMovies[len(listOfMovies)-1].url = attr[1]

        if tag == "a":
            for name, value in attrs:
                if name == "itemprop" and value == "url":
                    self.d = True

        if tag == "time" and self.actor_page:
            for attr in attrs:
                if attr[0].lower() == "datetime":
                    print(attr)

os.system("wget -q -O movieList http://www.imdb.com/movies-in-theaters/?ref_=inth_inth")

file = open("movieList", "r")
stream = file.read()
parse = MyHTMLParser(False)
parse.feed(stream)
file.close()

url_base = "http://www.imdb.com"
for item in listOfMovies:
    print(item.title)
    movie_page = url_base + item.url
    # reusing file name so there's not a ton of files at the end
    # probably delete downloaded files
    wget = "wget -q -O moviePage " + movie_page
    os.system(wget)

    for line in open("moviePage", "r"):
        if "/name/nm" in line and "?ref_=tt_cl_t" in line:
            # get rid of a href
            line = line.replace("<a href=", "")
            line = line.replace('"', "")
            # remove new line at end of line
            line = line.rstrip()
            actor_page = url_base + line
            item.actor_name_url.append(actor_page)

            wget = "wget -q -O actorPage " + actor_page
            os.system(wget)

            file = open("actorPage", "r")
            stream = file.read()
            parse = MyHTMLParser(True)
            parse.feed(stream)
            file.close()

