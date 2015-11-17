from html.parser import HTMLParser
from datetime import date
import os

# holds list of Movies
listOfMovies = []
# holds actor's ages for current movie
actor_age = []

################################################################

# class Movie holds information on each movie
# the constructors takes the title of the movie
class Movie():
    # init takes the title of the movie
    # sets movie attributes to empty/0
    def __init__(self, title):
        # title of movie
        self.title = title
        # url to movie page
        self.url = ""
        # list of ages of actors
        self.ages = []
        # average age of actors
        self.avg_age = 0


################################################################

# class MyHTMLParser inherits from HTMLParser
# handles the html tag parsing
# the constructor takes a boolean that indicates
# if the parser if being used on the actor's bio page or not
class MyHTMLParser(HTMLParser):
    def __init__(self, actor_page):
        HTMLParser.__init__(self)
        # actor_page is passed since the time tag is not needed
        # on the movie or now playing page
        self.actor_page = actor_page

    # takes tag and attributes
    # parses tags differently depending on name
    def handle_starttag(self, tag, attrs):
        name = False

        # if the tag is "img" then it can extract the movie title and add to array
        if tag == "img":
            for attr in attrs:
                if attr[0].lower() == "class" and attr[1].lower() == "poster shadowed":
                    name = True
                if attr[0].lower() == "title" and name:
                    listOfMovies.append(Movie(attr[1]))

        # if the tag is an "a href" then it can get the link to the movie page
        # title links follow a pattern so pattern matching is also done to
        # check that it is a movie link
        if tag == "a":
            for attr in attrs:
                if attr[0].lower() == "href" and attr[1].startswith("/title") and attr[1].endswith("tt"):
                    listOfMovies[len(listOfMovies)-1].url = attr[1]

        # only does this when on actor page
        # a tag that contains the birth date of actor
        if tag == "time" and self.actor_page:
            for attr in attrs:
                # attribute of the birth date
                if attr[0].lower() == "datetime":
                    # get the current date to subtract from actors birthday
                    dt = date.today()
                    actor_bday_arr = attr[1].split("-")
                    # if the day or month is not specified
                    # use the year
                    if int(actor_bday_arr[1]) == 0 or int(actor_bday_arr[2]) == 0:
                        actor_age.append(dt.year - int(actor_bday_arr[0]))
                    # if the page listed the full birthday
                    # subtract to find how many days old they are
                    # divide by the number of days in a year and round down
                    else:
                        actor_bday_date = date(int(actor_bday_arr[0]), int(actor_bday_arr[1]), int(actor_bday_arr[2]))
                        actor_age.append(int((dt - actor_bday_date).days/365))

################################################################

# download a list of movies
os.system("wget -q -O movieList http://www.imdb.com/movies-in-theaters/?ref_=inth_inth")

# send html file to parser
f = open("movieList", "r")
stream = f.read()
parse = MyHTMLParser(False)
parse.feed(stream)
f.close()

################################################################

url_base = "http://www.imdb.com"
# loop over list of movie
for movie in listOfMovies:
    movie_page = url_base + movie.url
    # create wget command and call wget
    wget = "wget -q -O moviePage " + movie_page
    os.system(wget)

    for line in open("moviePage", "r"):
        # use pattern matching since htmlparser seems
        # to have issues with certain nested tags
        if "/name/nm" in line and "?ref_=tt_cl_t" in line:
            # get rid of a href
            line = line.replace("<a href=", "")
            line = line.replace('"', "")
            # remove new line at end of line
            line = line.rstrip()
            actor_page = url_base + line

            # download page of actor
            wget = "wget -q -O actorPage " + actor_page
            os.system(wget)

            # parse actor page
            f = open("actorPage", "r")
            stream = f.read()
            parse = MyHTMLParser(True)
            parse.feed(stream)
            f.close()
    # set movie's list of actor ages to the current list for that movie
    movie.ages = actor_age
    # reset to empty for the next movie
    actor_age = []

    # calculate average age
    sum = 0
    for age in movie.ages:
        sum += age
    if len(movie.ages) > 0:
        movie.avg_age = sum/len(movie.ages)
    else:
        movie.avg_age = "Unknown"

################################################################

# remove source pages
os.system("rm actorPage")
os.system("rm moviePage")
os.system("rm movieList")

################################################################

# print results
for movie in listOfMovies:
    try:
        print('Movie: {0:30s} Average Age: {1:2f}'.format(movie.title, movie.avg_age))
    except:
        print('Movie: {0:30s} Average Age: {1:2s}'.format(movie.title, movie.avg_age))

