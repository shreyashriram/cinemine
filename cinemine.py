import sqlite3
from sqlite3 import Error

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def checkcredentials(_conn, _user_email, _user_password):
    print("++++++++++++++++++++++++++++++++++")
    print("Verifying credentials...")
    
    cur = _conn.cursor()
    try:
        sql = """SELECT user.user_id, user_name as num2
                    FROM user
                    JOIN credentials ON user.user_id = credentials.user_id
                    WHERE credentials.user_email = ? AND credentials.user_password = ?; """
        args = [_user_email,_user_password]
        cur.execute(sql, args)  
        
        _conn.commit()      
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def createaccount(_conn, _user_name, _user_email, _user_password, _user_id):
    print("++++++++++++++++++++++++++++++++++")
    print("Creating account...")
    
    cur = _conn.cursor()
    try:
        sql = "INSERT INTO credentials(user_id, user_email, user_password) VALUES (?, ?, ?);"
        args = [_user_id,_user_email,_user_password]
        cur.execute(sql, args)
        
        sql = "INSERT INTO user(user_id, user_name) VALUES (?, ?);"
        args = [_user_id,_user_name]
        cur.execute(sql, args)
                 
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertmovie(_conn, _movie_title, _movie_id, _user_id, _user_rating, _user_comment, _comment_id):
    print("++++++++++++++++++++++++++++++++++")
    print("Adding" + _movie_title + "to your watchlist")

    cur = _conn.cursor()
    try:
        sql = """INSERT INTO watchlist(movie_id, user_id, user_rating, user_comment, comment_id)--comment_id should be an incrementing variable
                    SELECT movies.?, user.?, ?, ?, ?
                    FROM movies, user
                    WHERE movies.movie_title = ? AND user.user_id = ?;"""
        args = [_movie_id, _user_id, _user_rating, _user_comment, _comment_id, _movie_title, _user_id]
        cur.execute(sql, args)        
                    #we need to update comments database as well
        sql = """INSERT INTO comments(movie_id, user_id, user_comment, comment_id)
                    SELECT movies.?, user.?, ?, ?
                    FROM movies, user
                    WHERE movies.movie_title = ? AND user.user_id = ?;"""
        args = [_movie_id, _user_id, _user_comment, _comment_id, _movie_title, _user_id]
        cur.execute(sql)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")

def leaverating(_conn, newnum, _avg_rating, _numratings, _movie_title):
    print("++++++++++++++++++++++++++++++++++")
    print("Adding" + newnum + "to the ratings")

    cur = _conn.cursor()
    try:
        sql = """UPDATE ratings
                    SET avg_rating = round(((?*?) + ?) / (? + 1),1), num_ratings = ? + 1
                    WHERE movie_id = (select movie_id from movies where movie_title = ?);"""
        args = [_avg_rating, _numratings, newnum, _numratings, _numratings, _movie_title]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")

def leavecomment(_conn, _user_id, _comment_id, word, _movie_title):

    print("++++++++++++++++++++++++++++++++++")
    print("Adding" + word + "to the comments")

    cur = _conn.cursor()
    try:
        sql = """INSERT INTO comments(movie_id, user_id, user_comment, comment_id)
                    SELECT movies.movie_id, user.user_id, ?, ?
                    FROM movies, user
                    WHERE movies.movie_title = ? AND user.user_id = ?;"""
        args = [word, _comment_id, _movie_title, _user_id]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def viewavg(_conn, _movie_title):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Viewing average rating for" + _movie_title)

    cur = _conn.cursor()
    try:
        sql = """SELECT DISTINCT movies.movie_title, avg_rating, user_comment
                    FROM ratings
                        JOIN comments ON ratings.movie_id = comments.movie_id
                        JOIN movies ON comments.movie_id = movies.movie_id
                        WHERE movies.movie_title = ?;"""
        args = [_movie_title]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def viewrat(_conn, _movie_title, _user_name):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Viewing user rating for" + _movie_title)

    cur = _conn.cursor()
    try:
        sql = """SELECT user_rating
                    FROM watchlist
                    WHERE user_id = (select user_id from user where user_name = ?)
                    AND movie_id = (select movie_id from movies where movie_title = ?)
                    LIMIT 1;"""
        args = [_user_name, _movie_title]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def editcomment(_conn, _movie_title, _user_comment, _comment_id, _user_name):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Editing comment for " + _movie_title)

    cur = _conn.cursor()
    try:
        sql = """UPDATE watchlist
                    SET user_comment = ?
                    WHERE user_id = (select user_id from user where user_name = ?) 
                    AND movie_id = (select movie_id from movies where movie_title = ?)
                    AND comment_id = ?;"""
        args = [_user_comment, _user_name, _movie_title, _comment_id]
        cur.execute(sql, args)
        sql = """UPDATE comments
                    SET user_comment = ?
                    WHERE user_id = (select user_id from user where user_name = ?) 
                    AND movie_id = (select movie_id from movies where movie_title = ?)
                    AND comment_id = ?;"""  
        args = [_user_comment, _user_name, _movie_title, _comment_id]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def viewwatchlist(_conn, _user_name):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Viewing personal watchlist of user" + _user_name)

    cur = _conn.cursor()
    try:
        sql = """SELECT movie_title, user_rating, user_comment
                    FROM watchlist
                    JOIN movies ON movies.movie_id = watchlist.movie_id
                    WHERE user_id = (select user_id from user where user_name = ?)
                    GROUP BY watchlist.movie_id;"""
        args = [_user_name]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def sortwatchlist(_conn, _user_name):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Viewing sorted personal watchlist of user" + _user_name)

    cur = _conn.cursor()
    try:
        sql = """SELECT movie_title, user_rating, user_comment as num11
                    FROM watchlist
                    JOIN movies ON movies.movie_id = watchlist.movie_id
                    WHERE user_id = (select user_id from user where user_name = ?)
                    GROUP BY movie_title;"""
        args = [_user_name]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def removemovie(_conn, _movie_title):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Removing " + _movie_title + " from watchlist")

    cur = _conn.cursor()
    try:
        sql = """DELETE FROM watchlist 
                    WHERE EXISTS 
                    (select *
                        from movies
                        where watchlist.movie_id = movies.movie_id and movie_title = ?);"""
        args = [_movie_title]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")
    
def removecomment(_conn, _movie_title, _comment_id, _user_name):
    
    print("++++++++++++++++++++++++++++++++++")
    print("Removing comment number " + _comment_id + " from " + _movie_title + " ")

    cur = _conn.cursor()
    try:
        sql = """DELETE FROM comments
                    WHERE user_id = (select user_id from user where user_name = ?) 
                    AND movie_id = (select movie_id from movies where movie_title = ?)
                    AND comment_id = ?;"""
        args = [_user_name, _movie_title, _comment_id]
        cur.execute(sql, args)
        
        _conn.commit()
    
    except Error as e:
            _conn.rollback()
            print(e)

    print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"newfiltered.sqlite"

    # create a database connection
    conn = openConnection(database)
    id = 32
    with conn:
        print("Welcome to Cinemine!\n")
        check = 0
        while(check != 1):
            print("1. Sign In\n2. Sign Up\n3. Exit program\nWhat would you like to do?")
            val = input()
            val = int(val)
            if (val == 1):
                email = input("Input your email to sign in ")
                password = input("Input your password to sign in ")
                checkcredentials(conn, email, password)
            if (val == 2):
                name = input("What's your name? ")
                email = input("Input your new username ")
                password = input("Input your new password ")
                id = id + 1
                createaccount(conn, name, email, password, id)
            if (val == 3):
                print("Closing Cinemine...")
                quit();
        val = 0
        print("""Input the corresponding digit to run the command:
              1. Add a movie to your watchlist
              2. Update a rating
              3. Leave an additional comment for a movie
              4. View the average rating or comments for a movie
              5. View your rating for a movie
              6. Edit your comment to a movie
              7. View your watchlist
              8. Display/sort watchlist alphabetically
              9. Remove a movie from your watchlist
              10. Remove your comment
              11. Log out
              """)
        
        while(val != 0):
            val = int(input("What would you like to do? "))
            if val == 1:
                title = input("What movie did you watch? ")
                rating = input("What rating out of 10 do you give this movie? ")
                comment = input("What comment do you give this movie? ")
                insertmovie(conn, title, 1, 1, rating, comment, 1)
            if val == 2:
                num = input("What rating would you give " + title)
                leaverating(conn, num, 8.6, 6, title )
            if val == 3:
                word = input("What do you have to say about " + title)
                leavecomment(conn, 1, 2, word, title)
            if val == 4:
                title2 = input("For which movie would you like to see average ratings or comments? ")
                viewavg(conn, title2)
            if val == 5:
                user = input("What is your user name? ")
                title3 = input("For which movie would you like to see your rating? ")
                viewrat(conn, title3, user)
            if val == 6:
                user = input("What is your user name? ")
                title4 = input("For which movie would you like to edit your comment? ")
                word2 = input("What would you like your new comment to be? ")
                editcomment(conn, title4, word2, 1, user)
            if val == 7:
                user = input("What is your user name? ")
                viewwatchlist(conn, user)
            if val == 8:
                user = input("What is your user name? ")
                sortwatchlist(conn, user)
            if val == 9:
                title6 = input("What movie would you like to remove? ")
                removemovie(conn, title6)
            if val == 10:
                user = input("What is your user name? ")
                title7 = input("From what movie would you like to remove a comment? ")
                com = input("What number comment would you like to remove? ")
                removecomment(conn, title7, com, user)
            if val == 11:
                print("Closing cinemine...")
                quit();

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
