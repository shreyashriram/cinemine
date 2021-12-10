import sqlite3
import os
import getpass
import random

sqldirectory = '/mnt/c/Users/miche/Downloads/CSE111/cinemine/cinemine.sqlite'

welcomeTitle = '''
-----------------------
| WELCOME TO CINEMINE |
-----------------------'''

exitTitle = '''--------------------------
| SEE YOU LATER ~CINEMINE |
--------------------------'''

signInTitle = '''----------------------
| SIGN INTO CINEMINE |
----------------------'''

createAccountTitle = '''---------------------------
| CREATE CINEMINE ACCOUNT |
---------------------------'''

homeMenuOptions = '''Choose an option: 
(1) Sign In
(2) Create an Account
(3) Leave CINEMINE
'''

userMenuOptions = '''
USER MENU
---------------------
Choose an option: 
(1) Watchlist
(2) Search for Movie
(3) Logout of CINEMINE
'''

searchMovieOptions = '''
SEARCH OPTIONS
---------------------
Choose an option: 
(1) Browse by Title
(2) Browse by Ratings
(3) Browse by Year
(4) Return to User Menu
'''

watchListOptions = '''
WATCHLIST OPTIONS
---------------------
Choose an option: 
(1) Browse WatchList
(2) Add Movie to Watchlist
(3) Delete Movie from Watchlist
(4) Return to User Menu
'''

runCinemine = True
userLoggedIn = False
user_id = 0

def quitCinemine():
    global runCinemine
    runCinemine = False
    
    print(exitTitle)
    quit()

def signIn():
    print(signInTitle)
    email = input("Email: ")
    password = getpass.getpass('Password: ')
    # password = input("Password: ")

    accountAuthenticated, list = authenticateUser(email, password)

    if (accountAuthenticated):
        return list[0][0]

    else: return (0)

def authenticateUser(email, password):
    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()

    query = '''SELECT user.user_id, user_name as num2
               FROM user
               JOIN credentials ON user.user_id = credentials.user_id
               WHERE credentials.user_email = "{em}" AND credentials.user_password = "{pw}"; 
    '''.format(em = email, pw = password)

    users = cur.execute(query)
    users = users.fetchall()

    if (len(users) == 1):
        return True, users
    else: 
        return False, users

def create_Account():
    print(createAccountTitle)
    name = input("Your Name: ")
    email = input("Email: ")
    password = input("Password: ")

    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()

    query = '''INSERT INTO credentials(user_email, user_password) VALUES ("{em}", "{pw}");'''.format(em = email, pw = password)
    query1 = '''INSERT INTO user(user_name) VALUES ("{nm}");'''.format(nm = name)
    query2 = '''SELECT user_id
                FROM credentials
                WHERE user_email = "{em}" AND user_password = "{pw}";'''.format(em = email, pw = password)

    cur.execute(query)
    conn.commit()
    cur.execute(query1)
    conn.commit()

    users = cur.execute(query2)
    users = users.fetchall()

    return users[0][0]


def logOut():
    global userLoggedIn
    global user_id

    user_id = 0
    userLoggedIn = False

    print('''You have been logged out.
''')

def mainMenu():
    global userLoggedIn;
    global user_id;
    print(homeMenuOptions)
    choice = int(input("I choose choice: "))

    if (choice == 1):
        u_id = signIn()
        if (u_id > 0):
            print("You have been signed in. ")
            userLoggedIn = True
            return u_id;
        else:
            print('''Login Failed, try another option.
---------------------------------''')
            mainMenu()

    elif (choice == 2):
        u_id = create_Account()
        if (u_id > 0):
            print("Yay! You have created an account. ")
            userLoggedIn = True
            return u_id;
        else:
            print('''Account Creation Failed, try another option.
---------------------------------''')
            mainMenu()
    else: 
        quitCinemine()

def userMenu():
    global userLoggedIn
    global user_id

    print(userMenuOptions)
    choice = int(input("I choose choice: "))

    if (choice == 1):
        watchList()

    elif (choice == 2):
        searchMovie()

    else:
        logOut()


def searchTitles():
    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()
    title = input("Movie Name: ")
    print('''
Search Results for: {title}
-----------------------------------------------'''.format(title = title))
    query = '''SELECT movie_title, movie_year, movie_genre, avg_rating, num_ratings 
               FROM movies, ratings
               WHERE movies.movie_id = ratings.movie_id AND 
               movie_title LIKE "%{name}%";'''.format(name = title)

    movie = cur.execute(query)
    movie = movie.fetchall()
  
    for i in range(len(movie)):
        output = '''    {title} ({year}, {genre})
        Ratings: {rating}/10 with {num_votes} votes
        
        '''.format(title= movie[i][0], year = movie[i][1], genre = movie[i][2], rating = movie[i][3], num_votes = movie[i][4])

        print(output)


def searchRatings():
    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()
    rating = float(input("Movies with Minimum Rating: "))
    print('''
Search Results for Minimum Rating of : {rating}
-----------------------------------------------'''.format(rating = rating))
    query = '''SELECT movie_title, movie_year, movie_genre, avg_rating, num_ratings
               FROM movies, ratings 
               WHERE movies.movie_id = ratings.movie_id AND 
               avg_rating >= {rating};'''.format(rating = rating)

    movie = cur.execute(query)
    movie = movie.fetchall()
    low = random.randint(0, len(movie)-10)
    
    if(len(movie) >= 10):
        low = random.randint(0, len(movie)-10)      
    else: 
        low = 0

    for i in range(low, low+10):
        output = '''    {title} ({year}, {genre})
        Ratings: {rating}/10 with {num_votes} votes
        
        '''.format(title= movie[i][0], year = movie[i][1], genre = movie[i][2], rating = movie[i][3], num_votes = movie[i][4])

        print(output)

def searchYear():
    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()
    year = int(input("Movies from year: "))
    print('''
    Search Results for Movies from year: {year}
-----------------------------------------------'''.format(year = year))
    query = '''SELECT movie_title, movie_year, movie_genre, avg_rating, num_ratings
               FROM movies, ratings 
               WHERE movies.movie_id = ratings.movie_id AND 
               movie_year = {year};'''.format(year = year)

    movie = cur.execute(query)
    movie = movie.fetchall()

    if(len(movie) >= 10):
        low = random.randint(0, len(movie)-10)      
    else: 
        low = 0
  
    for i in range(low, low+10):
        output = '''    {title} ({year}, {genre})
        Ratings: {rating}/10 with {num_votes} votes
        
        '''.format(title= movie[i][0], year = movie[i][1], genre = movie[i][2], rating = movie[i][3], num_votes = movie[i][4])

        print(output)

def searchMovie():
    keepSearching = True

    while(keepSearching):
        print(searchMovieOptions)
        choice = int(input("I choose choice: "))

        if (choice == 1):
            searchTitles()
        
        elif (choice == 2):
            searchRatings()
        
        elif (choice == 3):
            searchYear()
        else:
            keepSearching = False
            userMenu()

def viewWatchlist():
    global user_id

    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()

    query = '''SELECT movies.movie_title, movies.movie_year, movies.movie_genre, watchlist.user_rating, watchlist.user_comment
               FROM movies, ratings, watchlist
               WHERE watchlist.user_id = {id} AND 
                    watchlist.movie_id = movies.movie_id AND
                    movies.movie_id = ratings.movie_id;'''.format(id = user_id)

    movie = cur.execute(query)
    movie = movie.fetchall()

    # print(movie)
    if(len(movie) > 0):
        print('''
            MOVIES YOU'VE WATCHED
-----------------------------------------------''')
        for i in range(len(movie)):
            output = '''    {num}. {title} ({year}, {genre})
        Your Rating: {rating}/10 
        {comment}

            '''.format(num = i+1, title= movie[i][0], year = movie[i][1], genre = movie[i][2], rating = movie[i][3], comment = movie[i][4])

            print(output)
    else:
        print("Your watchlist is empty, choose (2) to add a movie.")
        
def existsInWatchlist(title):
    global user_id

    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()
    
    query = '''SELECT movies.movie_id
               FROM movies, watchlist
               WHERE movies.movie_id = watchlist.movie_id AND 
               movies.movie_title = '{title}' AND
               watchlist.user_id = {id};
    '''.format(title = title, id = user_id)
    
    info = cur.execute(query)
    info = info.fetchall()
    
    if (len(info) == 0):
        return False
    else:
        return True
    

def addMovieToWatchlist():
    global user_id

    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()

    name = input("What movie did you watch? ")
    #rating = int(input("What did you think of the movie /10? "))
    #comment = input("What did you think? ")

    if (existsInWatchlist(name)):
        print("This movie is already in your watchlist.")
    else:
        
        rating = int(input("What did you think of the movie /10? "))
        comment = input("What did you think? ")
        query = '''INSERT INTO comments(movie_id, user_id, user_comment)
                SELECT movie_id, {id}, '{comment}'
                FROM movies
                WHERE movie_title = "{name}";
        '''.format(id = user_id, comment = comment, name = name)

        cur.execute(query)
        conn.commit()

        query1 = '''SELECT comments.movie_id, comment_id
                    FROM comments, movies
                    WHERE user_id = {id} AND 
                    comments.movie_id = movies.movie_id AND movie_title = '{name}'
        '''.format(id = user_id, name = name)

        info = cur.execute(query1)
        info = info.fetchall()

        movie_id = info[0][0]
        comment_id = info[0][1]

        query2 = '''INSERT INTO watchlist(movie_id, user_id, user_rating, user_comment, comment_id) VALUES ('{movie_id}', {id}, {user_rating}, '{user_comment}', {comment_id})
        '''.format(movie_id = movie_id, id = user_id, user_rating = rating, user_comment = comment, comment_id = comment_id)

        cur.execute(query2)
        conn.commit()

        query3 = '''SELECT *
                    FROM ratings
                    WHERE movie_id = '{movie_id}'
        '''.format(movie_id = movie_id)

        info = cur.execute(query3)
        info = info.fetchall()
        
        avg_rating = info[0][1]
        total = info[0][2]

        # print('total: ', total)
        # print('avg_rating: ', avg_rating)

        avg_rating = ((avg_rating*total)+rating)/(total+1)
        avg_rating = round(avg_rating, 1)

        # print(avg_rating)
        total = total+1

        query4 = '''UPDATE ratings
                    SET avg_rating = {avg}, num_ratings = {tot}
                    WHERE movie_id = '{movie_id}'
        '''.format(avg = avg_rating, tot = total, movie_id = movie_id)

        cur.execute(query4)
        conn.commit()

        print('{name} has been added to your watchlist!'.format(name = name))

def deleteMovieWatchlist():
    conn = sqlite3.connect(sqldirectory)
    cur = conn.cursor()
    title = input("Movie Name: ")

    if (existsInWatchlist(title)):
        query = '''DELETE FROM watchlist 
                WHERE EXISTS
                (select * 
                from movies
                where watchlist.movie_id = movies.movie_id and movie_title = '{title}')
        '''.format(title = title)
        
        cur.execute(query)
        conn.commit()

        print('{title} has been deleted from your watchlist!'.format(title = title))
    else:
        print('{title} is not in your watchlist!'.format(title = title))
    
    
def watchList():
    keepWatchlist = True
    while (keepWatchlist):

        print(watchListOptions)
        choice = int(input("I choose choice: "))

        if (choice == 1):
            viewWatchlist()
        elif (choice == 2):
            addMovieToWatchlist()
        elif (choice == 3):
            deleteMovieWatchlist()
        else:
            keepWatchlist = False
            userMenu()

def main():
    global user_id

    while (runCinemine):
        print(welcomeTitle)

        # HOME
        while(not userLoggedIn):
            user_id = mainMenu()

        # print(user_id)
        # LOGGED IN
        while(userLoggedIn):
            userMenu()

        # print("hello user", user_id)
        # quitCinemine()

if __name__ == '__main__':
    main()