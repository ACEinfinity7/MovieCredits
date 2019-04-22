from movie_details import *
from movie_credits import *
from movie_ids import *
import os
import csv
import random
from unidecode import unidecode
MY_DIR = os.path.dirname(os.path.realpath(__file__))

SPIDERVERSE_MOVIE_ID = 324857
INFINITY_WAR_MOVIE_ID = 299536
LOGAN_MOVIE_ID = 263115
BLADE_RUNNER_2049_MOVIE_ID = 335984
LEGO_MOVIE_ID = 137106

id_list = [SPIDERVERSE_MOVIE_ID, \
           INFINITY_WAR_MOVIE_ID, \
           LOGAN_MOVIE_ID, \
           BLADE_RUNNER_2049_MOVIE_ID, \
           LEGO_MOVIE_ID]


#A.1 Output title, id, release date, budget, runtime, and revenue
def basic_output(filename):
    """
    this is a def that reads the whole movie_details file and spits back
    out generic data from each movie.
    """
    #opens output file
    with open(filename, 'w') as out_file:
        #writes headings
        out_file.write('Original Title, \
                        Movie Id, \
                        Release Date, \
                        Budget, \
                        Runtime, \
                        Revenue')
        #goes through each movie, writing the details for it
        for id_base in id_list:
            movie = movie_details(id_base)
            out_file.write('\n')
            out_file.write(f'{movie["title"]},\
                             {movie["id"]},\
                             {movie["release_date"]},\
                             ${movie["budget"]},\
                             {movie["runtime"]} min,\
                             ${movie["revenue"]}')




filename = MY_DIR + '/' + 'movie_data.csv'
basic_output(filename)





#A.2 make a csv with the movies genres, not repea ting
def genres_output(filename):
    """
    This def takes the genres for each movie and outputs them to a csv
    if the genre is found twice, only one instance of the genre is outputted
    """
    output_set = set()
    #pulls the genre data for each movie into a set, preventing repeats
    for movie_data_orig in id_list:
        movie_data = movie_details(movie_data_orig)
        for genre_active in movie_data['genres']:
            output_set.add(genre_active['name'])

    #writes the genre data to a csv, with a heading
    with open(filename, 'w') as genre_output:
        genre_output.write('Genres:')
        for item in output_set:
                genre_output.write('\n')
                genre_output.write(item)




filename = MY_DIR + '/' + 'genre_data.csv'
genres_output(filename)




#A.3 output name, id, movie id, character
def pick_actors(filename, num_of_actors):
    """
    takes the cast list from each movie and randomly picks an inputted amount
    of actors to output to a csv.
    """
    output_list = list()
    #goes through each movie, picking out actors (num of actors in inputted)
    for current_movie_credit_orig in id_list:
        current_movie_credit = movie_credits(current_movie_credit_orig)
        act_sample = random.sample(current_movie_credit["cast"], num_of_actors)
        #saves the actors data to a dictionary for later output
        for curr in range(len(act_sample)):
            curr_name = unidecode(act_sample[curr]["name"])
            curr_id = act_sample[curr]["id"]
            curr_movie_id = current_movie_credit["id"]
            curr_character = unidecode(act_sample[curr]["character"])
            output_list.append([curr_name, \
                                curr_id, \
                                curr_movie_id, \
                                curr_character])

    #creates a file and writes the actor data to it
    with open(filename, 'w') as actor_out:
        actor_out.write('Name, Id, Movie Id, Character')
        for item in output_list:
            actor_out.write('\n')
            actor_out.write(f'{item[0]}, {item[1]}, {item[2]}, {item[3]}')




filename = MY_DIR + '/' + 'actor_data.csv'
num_of_actors = 3
pick_actors(filename, num_of_actors)





#B.1 out put directors: name, id, movie id: with an & between them
def output_directors(filename):
    """
    this def outputs directors and corresponding data about them, it repeats
    movie ids if a director has directed multiple movies from the sampled
    movies
    """
    counter = 0
    output_dict = dict()
    #goes through the movies, pulling the director data
    for movie_orig in id_list:
        movie = movie_credits(movie_orig)
        for curr in range(len(movie['crew'])):
            #checks to see if the crew entry is a director
            if movie['crew'][curr]['job'] == 'Director':
                curr_name = unidecode(movie['crew'][curr]['name'])
                #if the director is in the dictionary, append to his/her entry
                if curr_name in output_dict:
                    output_dict[curr_name][2].append(movie_orig)
                #if not, create a new entry for the director, with data
                else:
                    output_dict[curr_name] = (curr_name, \
                                             movie['crew'][curr]['id'], \
                                             [movie_orig])

    #creates a file, and writes the director data to it
    with open(filename, 'w') as f:
        f.write('Director Name, Director Id, Movie Id')
        for key in output_dict:
            f.write('\n')
            f.write(f'{output_dict[key][0]}, {output_dict[key][1]}, ')
            #calcualtes if an '&' is needed
            #it is needed if there are multiple movies for the director
            for i in output_dict[key][2]:
                f.write(f'{i}')
                counter += 1
                if counter < len(output_dict[key][2]) and counter > 0:
                    f.write(" & ")
            counter = 0




filename = MY_DIR + '/' + 'directors_output.csv'
output_directors(filename)




#C.1 Actor Name, Actor Id, list of movie names
def output_actors(filename, num_of_movies):
    """
    this def picks out actors from the sampled movies that have occured in
    a specified amount of movies or more
    """
    counter = 0
    output_dict = dict()
    #goes through the movies, pulling actor data
    for movie_orig in id_list:
        movie = movie_credits(movie_orig)
        for curr in range(len(movie['cast'])):
            curr_name = unidecode(movie['cast'][curr]['name'])
            cast_id = movie['cast'][curr]['id']
            movie_name = movie_details(movie_orig)['original_title']
            #if the actor is in the dictionary, then append to the entry
            if curr_name in output_dict:
                output_dict[curr_name][2].append(movie_name)
            #if the actor is not in the dictionary, create an entry
            else:
                output_dict[curr_name] = [curr_name, cast_id, [movie_name]]

    #create a file and write the data to it
    with open(filename, 'w') as f:
        f.write('Actor Name, Actor Id, Movie Name')
        for key in output_dict:
            #only writes if the actor has been in more than the supplied cap
            if len(output_dict[key][2]) > (num_of_movies - 1):
                f.write('\n')
                f.write(f'{output_dict[key][0]}, {output_dict[key][1]}, ')
                #writes '&' when needed
                for i in output_dict[key][2]:
                    f.write(f'{i}')
                    counter += 1
                    if counter < len(output_dict[key][2]) and counter > 0:
                        f.write(" & ")
                counter = 0




filename = MY_DIR + '/' + 'actors_output.csv'
num_of_movies = 2
output_actors(filename, num_of_movies)
