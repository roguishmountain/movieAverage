# average age of actors in movies currently playing. 
Comments:

The Movie class holds the title of the movie (I decided to leave the year in, but that can easily be removed), url of the title of the movie, ages of the actors, and the average age of the actors. The MyHTMLParser class inherits from HTMLParser. It has methods that can be overridden to handle start/ends tags and data. This class doesn't handle nested tags well, so some pattern matching was done when nested tags became an issue. The URLs on IMDB follow a pattern so it was simple to use pattern matching to find if it was a useable URL. After finding the title and URL of the movie, it loops over the movie pages and downloads the actor page source for the movie cast. The HTMLParser is used to find the birthdate of the actor and then the average age is found and added to the class variable. 

It runs kind of slowly. It takes about 2.5 minutes when I run it on my computer. 

real	2m30.350s
user	0m16.411s
sys	0m4.575s

using the time commmand. This is due to the repeated wget calls. If this was scaled up or used over a long period of time a way to solve this could be to create a cache if there is enough memory. Actors that are more popular could have their html page source stored or their age/birthday stored so it wouldn't need to download the souce multiple times. It could also be run on seperate servers or threads to distribute the work. Since each the age caculation is isolated to the movie it would be simple to perform each averge calculation seperately. 

I stuck with using only IMDB instead of another source such as Wikipedia. I found that for some lesser known actors when I tried to create the link to their wikipedia page it didn't appear to be the correct person. It seemed safer to use the link to the actor's page instead of going to another source. Neither had an API or a useful API. 

Some actors don't have a birthday listed, so those are not factored into the average age. Some movies have only actors with no birthdays listed. In this case "Unknown" is printed instead of an age.  

Some actors don't have their full birthday listed. In this case only the year was used. 

Since people say something like "I'm 30 years old" not "I'm 30.72602739726027 years old" the ages are rounded down. 

The ages are not rounded for the average age calculation output. 

Python 3 is needed to run this. There is a known bug in the htmlparser for python 2, so this wil not be able to run in python 2.


To run:
python3 movieAges.py
