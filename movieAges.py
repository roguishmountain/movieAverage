from HTMLParser import HTMLParser

# add file download and name

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.d = False
        self.end = False

    def handle_starttag(self, tag, attrs):
        name = False

        if tag == "img":
            for attr in attrs:
                print attr

        if tag == "a":
            for attr in attrs:
                if attr[0].lower() == "href" and attr[1].lower() == "poster shadowed":
                    print "attr:", attr

        if tag == "a":
            for name, value in attrs:
                if name == "itemprop" and value == "url":
                    self.d = True
                    print name, value

    def handle_data(self, data):
        if self.d:
            data = data.rstrip().lstrip()
            if len(data) == 0:
                self.end = False
                self.d = True

            elif not self.end:
                print data
                self.d = False



file = open("listofmovies", "r")
stream = file.read()
parse = MyHTMLParser()
parse.feed(stream)
