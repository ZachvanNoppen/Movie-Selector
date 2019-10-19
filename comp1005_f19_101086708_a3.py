#D. Zachary van Noppen
#101086708

'''
MOVIE SELECTION WEBCRALER -----------------

The following program uses a webcrawler to get the data based on the movies.
The program generates questions based on the description, actors and directors in the films
For this reason, I can't outline exactly what will be asked, only that it will be based on the
    first 10 movies from IMDB list pages
You can base your answers of the data found there:
1. Cop Action - https://www.imdb.com/list/ls063275666/
2. Superhero - https://www.imdb.com/list/ls032971261/

NOTE: questions are personalized based on good input from the user. I didn't spend any time developing a way
to interpret the movie descriptions so it just matches keywords. If no keywords match, the questions will only
be about directors and actors.
For this reason, every movie NOT being searched for will have very generic questions.

INSTALLATION INSTRUCTIONS ------------------

run the following commands in terminal
These install requests, allowing querying of webpages
and BeautifulSoup4, allowing pagecrawling
---------------------------
sudo apt python-pip install
pip install requests
sudo apt-get install python3-bs4
--------------------------

'''

import requests
from bs4 import BeautifulSoup as crawler
from copy import copy, deepcopy

def crawlPage(link):
    #Creating a Translator
    #translator = Translator()
    #defining arrays to hold the names and titles
    randomNums = []
    titles = []
    descriptions =[]
    directors = []
    actors = []
    #Getting the raw html page
    url = requests.get(link)

    #Parsing html into soup object
    soup = crawler(url.text, 'html.parser')

    #Getting the titles
    titles_raw = soup.find_all('h3', attrs={'class': 'lister-item-header'})
    for title in titles_raw:
        #translated_word = translator.translate(title.find('a').text, dest = "en")
        #itles.append(translated_word.text)
        titles.append(title.find('a').text)

    #Getting the descriptions
    desc_raw = soup.find_all('div', attrs={'class': 'lister-item-content'})
    for desc in desc_raw:
        descriptions.append(desc.find_all('p')[1].text)

    #Finding the directors
    #Not all movies have directors
    cast_raw = soup.find_all('p', attrs={'class': ['text-muted','text-small']})
    #print(soup.find('p', attrs={'class': ['text-muted','text-small']}).text)
    for field in cast_raw:
        if(field.find('a') is not None):
            bool_check = 'Director' in field.text
            if(bool_check):
                #adding director
                directors.append(field.find('a').text)
                actors_temp = []
                #Adding the actors
                for entry in field.find_all('a')[1:]: #searches after the first index
                    actors_temp.append(entry.text)
                actors.append(actors_temp)

            else:
                directors.append('')
                actors_temp = []
                #Adding the actors
                for entry in field.find_all('a'):
                    actors_temp.append(entry.text)
                actors.append(actors_temp)

    final_titles = []
    final_desc = []
    final_dir = []
    final_actors = []
    for number in range(10):
        final_titles.append(titles[number])
        final_desc.append(descriptions[number])
        final_dir.append(directors[number])
        final_actors.append(actors[number])

    return list(zip(final_titles,final_desc,final_dir,final_actors))

def createStatements(text, movie_information):
#Get the input and generate keywords
#Look through all abstracts and generate questions based on them for each of the 10 movies
#get keywords and generate categories based on them
#ie. home would translate to {home, hometown, village, town, city, rural, ect...}

    replacement_text = {' is ', ' and ',' the ',' or ',' to ',' be ',' if ',' but ',' a ',' about ',' who ',' goes ',' in ',' on ',' go ',' when ', ' him ', ' until ', ' so ', ' she ',' her ' ' he ', ' his ',' that ', ' won\'t ', ' can ', ' by ', ' at ', ' they ', ' were ', ' are ',' now ', ' this ', ' film ', ' of ',' with ', ' an ', ' them ', ' for '}

    questions = []
    keywords_all = ''
    movie_abstract = movie_information[1].lower()
    movie_director = movie_information[2].lower()
    movie_actors = movie_information[3]

    #extract only keywords
    for word in replacement_text:
            #getting keywords in user input
            keywords_all = text.replace(word, " ")
            #getting keywords in abstract
            movie_abstract = movie_abstract.replace(word, " ")

    keywords_all = keywords_all.lower()

    #check for similar keywords in description of the movie
    if(len(questions) < 3):
        for word in keywords_all.split():
            #adding spaces to the words so that partial words are not accepted
            word = ' ' + word + ' '
            match = int(movie_abstract.find(word))
            if(match != -1):
                #If we find a match,add this to list of questions being asked about this movies
                questions.append("Does your movie invole \""+word+"\" ? (Y/N): ")

    #Check for directors
    if(len(questions) < 3):
        #always ask about who directed
        if(movie_director != ''):
            questions.append("Did "+movie_director+" direct your film? (Y/N): ")

    #check for actors
    #if keywords match from the description they will aleady be added.
    for actor in movie_actors:
        if(len(questions) >= 3):
            break
        #checking for a match
        questions.append("Does "+actor+" star in your movie? (Y/N): ")

    return (movie_information[0],questions)

def main():
    while True:
        print("\nWelcome to the film selector! ")

        while True:
            genre = input("Choose a genre from the list below OR paste in the URL to your own IMDB list.\nIf you pase in your own link, make sure it follows the URL format \"www.imdb.com/list/xxxxxxxx/\". \n\n1. Cop Action \n2. Super-hero\n\nEnter your selection:")
            if(genre == '1'):
                #Getting the data from COP movies
                print("Getting your movies...")
                films = crawlPage("https://www.imdb.com/list/ls063275666/")
                break
            elif(genre == '2'):
                #Superhero
                print("Getting your movies...")
                films = crawlPage("https://www.imdb.com/list/ls032971261/")
                break
            elif("https://www.imdb.com/list" in genre):
                #custom input
                print("Getting your movies...")
                films = crawlPage(genre)
                break
            else:
                print("Please Enter a valid input")
        # specify user input is to generate questions that the user might find useful
        user_def = input("\nDescribe your movie (type keywords for better results): ")

        #Creating questions based on user input
        titles_questions = []
        for movie in films:
            titles_questions.append(createStatements(user_def, movie ))

        #the tuple with movie data is in the format (title, [q1,q2,q3...])
        for movie in titles_questions:
            yes_counter = 0
            #Ask all questions
            for question in movie[1]:
                response = input(question)
                if(response.lower() == 'y'):
                    yes_counter = yes_counter + 1
                else:
                    break
            #check if all are correct
            if(yes_counter == 3):
                print("\n\n\nYour movie is: " +  str(movie[0]) + "\n\n\n")
                break

        end = input("Press Q to quit. Press any other key to continue: ")
        if(end.lower() == 'q'):
            break

#RUN PROGRAM
main()
