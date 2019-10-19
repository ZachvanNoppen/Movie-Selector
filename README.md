# Movie-Selector
A webcrawlder that makes questions based on different movies. 

## MOVIE SELECTION WEBCRALER 
The following program uses a webcrawler to get the data based on the movies.The program generates questions based on the description, actors and directors in the films. For this reason, I can't outline exactly what will be asked, only that it will be based on the first 10 movies from IMDB list pages
You can base your answers of the data found there:
1. Cop Action - https://www.imdb.com/list/ls063275666/
2. Superhero - https://www.imdb.com/list/ls032971261/
Questions are personalized based on good input from the user. I didn't spend any time developing a way to interpret the movie descriptions so it just matches keywords. If no keywords match, the questions will only be about directors and actors. For this reason, every movie NOT being searched for will have very generic questions.
## INSTALLATION INSTRUCTIONS 
run the following commands in terminal:
These install requests and BeautifulSoup4, allowing pagecrawling

- sudo apt python-pip install
- pip install requests
- sudo apt-get install python3-bs4
