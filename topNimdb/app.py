from bs4 import BeautifulSoup
import requests
from collections import defaultdict as df

n = int(input("Enter the number of movies to Fetch: "))

# Downloading imdb top 250 movie's data
url = "http://www.imdb.com/chart/top"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
individualURL = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]


# create a empty list for storing
# movie information
movie_names = []
cast_to_movies = df(lambda: [])


# Iterating over movies to extract
# each movie's details
for index in range(n):

    # Separating movie into: 'place', 'title'
    movie_string = movies[index].get_text()
    # print(movie_string)

    movie = (' '.join(movie_string.split()).replace('.', ''))
    # print(movie)

    movie_title = movie[len(str(index))+1:-7]

    place = movie[:len(str(index))-(len(movie))]

    data = {
        "movie_title": movie_title,
        "place": place
    }
    movie_names.append(data)

    # actors data
    movieURL = "http://www.imdb.com"
    movieURL += individualURL[index]
    print(movieURL)

    responseForCurrentMovie = requests.get(movieURL)
    soupCurrentMovie = BeautifulSoup(responseForCurrentMovie.text, 'lxml')

    cast_names = soupCurrentMovie.select(
        'a.StyledComponents__ActorName-y9ygcu-1')

    for actor in range(len(cast_names)):
        theActor = cast_names[actor].get_text()
        # print(theActor)

        cast_to_movies[theActor.strip().lower()].append(index)


def topNMovies(Actor, N):
    global movie_names, cast_to_movies
    movieList = [movie_names[i]["movie_title"]
                 for i in cast_to_movies[Actor.strip().lower()][:N]]
    return movieList


while True:
    actorName = input("\nEnter the Actor name: ")
    M = int(input("Enter the number of movies he/she acted in: "))

    print(topNMovies(actorName, M))

    queryMore = input("\nDo you want to query more? [y/n] ")
    if(queryMore == "y"):
        continue
    else:
        break
