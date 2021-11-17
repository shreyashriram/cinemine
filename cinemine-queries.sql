-- Michele Campbell and Shreya Shriram CineMine Mini

--Drop Tables
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS entertainer;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS principles;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS watchlist;
DROP TABLE IF EXISTS credentials;
DROP TABLE IF EXISTS comments;

--Table Creation
CREATE TABLE movies (
    movie_id decimal(4,0) not null,
    movie_title char(50) not null,
    movie_year decimal(4,0) not null,
    movie_genre char(25) not null
);

CREATE TABLE entertainer (
    ent_id decimal(4,0) not null,
    ent_name char(25) not null,
    ent_prof char(25) not null
);

CREATE TABLE ratings (
    movie_id decimal(4,0) not null,
    avg_rating decimal(2,1) not null,
    num_ratings decimal(15,0) not null
);

CREATE TABLE principles (
    movie_id decimal(4,0) not null,
    ent_id decimal(4,0) not null,
    job_role char(25) not null
);

CREATE TABLE user (
    user_id decimal(4,0) not null,
    user_name char(25) not null
);

CREATE TABLE watchlist (
    movie_id decimal(4,0) not null,
    user_id decimal(4,0) not null,
    user_rating decimal(2,0) not null,
    user_comment varchar(199) not null,
    comment_id decimal(4,0) not null
);

CREATE TABLE credentials (
    user_id decimal(4,0) not null,
    user_email char(25) not null,
    user_password char(25) not null
);

CREATE TABLE comments (
    movie_id decimal(4,0) not null,
    user_id decimal(4,0) not null,
    user_comment varchar(199) not null,
    comment_id decimal(4,0) not null
);

--Populating tables with movie information
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (1, 'The Dark Knight', 2008, 'Action');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (1, 'The Dark Knight', 2008, 'Action');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (2, 'Inception', 2010, 'Action');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (2, 'Inception', 2010, 'Action');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (3, 'Django Unchained', 2012, 'Drama');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (3, 'Django Unchained', 2012, 'Drama');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (3, 'Django Unchained', 2012, 'Drama');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (4, 'Joker', 2019, 'Crime');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (4, 'Joker', 2019, 'Crime');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (5, 'Spirited Away', 2001, 'Adventure');
INSERT INTO movies(movie_id, movie_title, movie_year, movie_genre) VALUES (5, 'Spirited Away', 2001, 'Adventure');

INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (1, 'Christian Bale', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (2, 'Christopher Nolan', 'Director');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (2, 'Christopher Nolan', 'Director');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (3, 'Leonardo Dicaprio', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (3, 'Leonardo Dicaprio', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (4, 'Quentin Tarantino', 'Director');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (5, 'Jamie Foxx', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (6, 'Todd Phillips', 'Director');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (7, 'Joaquin Phoenix', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (8, 'Hayao Miyazaki', 'Director');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (9, 'Daveign Chase', 'Actor');
INSERT INTO entertainer(ent_id, ent_name, ent_prof) VALUES (9, 'Daveign Chase', 'Director');

INSERT INTO ratings(movie_id, avg_rating, num_ratings) VALUES (1, 9.0, 5);
INSERT INTO ratings(movie_id, avg_rating, num_ratings) VALUES (2, 8.7, 6);
INSERT INTO ratings(movie_id, avg_rating, num_ratings) VALUES (3, 8.4, 10);
INSERT INTO ratings(movie_id, avg_rating, num_ratings) VALUES (4, 9.0, 4);
INSERT INTO ratings(movie_id, avg_rating, num_ratings) VALUES (5, 9.5, 9);

INSERT INTO principles(movie_id, ent_id, job_role) VALUES (1, 1, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (1, 2, 'Director');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (2, 2, 'Director');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (2, 3, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (3, 4, 'Director');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (3, 3, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (3, 5, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (4, 6, 'Director');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (4, 7, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (5, 8, 'Director');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (5, 9, 'Actor');
INSERT INTO principles(movie_id, ent_id, job_role) VALUES (5, 9, 'Director');

--1. Create an account

INSERT INTO credentials(user_id, user_email, user_password) VALUES (1, 'mcampbell24@ucmerced.edu', '12345');
INSERT INTO credentials(user_id, user_email, user_password) VALUES (2, 'sshriram@ucmerced.edu', '678910');
INSERT INTO user(user_id, user_name) VALUES (1, 'Michele');
INSERT INTO user(user_id, user_name) VALUES (2, 'Shreya');

--2. Retreive user input credentials for account login
.headers ON
SELECT user.user_id, user_name as num2
    FROM user
    JOIN credentials ON user.user_id = credentials.user_id
    WHERE credentials.user_email = 'mcampbell24@ucmerced.edu' AND 
        credentials.user_password = '12345'; 

--3. Add a movie to your watchlist

INSERT INTO watchlist(movie_id, user_id, user_rating, user_comment, comment_id) --comment_id should be an incrementing variable
    SELECT movies.movie_id, user.user_id, 5.0, 'it was ok', 1
    FROM movies, user
    WHERE movies.movie_title = 'The Dark Knight' AND user.user_id = 1;
INSERT INTO watchlist(movie_id, user_id, user_rating, user_comment, comment_id) --comment_id should be an incrementing variable
    SELECT movies.movie_id, user.user_id, 5.0, 'great movie', 2
    FROM movies, user
    WHERE movies.movie_title = 'Inception' AND user.user_id = 1;
    --we need to update comments database as well
INSERT INTO comments(movie_id, user_id, user_comment, comment_id)
    SELECT movies.movie_id, user.user_id, 'it was ok', 1
    FROM movies, user
    WHERE movies.movie_title = 'The Dark Knight' AND user.user_id = 1;
INSERT INTO comments(movie_id, user_id, user_comment, comment_id)
    SELECT movies.movie_id, user.user_id, 'great movie', 2
    FROM movies, user
    WHERE movies.movie_title = 'Inception' AND user.user_id = 1;

--4. Leave a rating

UPDATE ratings
    SET avg_rating = round(((avg_rating*num_ratings) + 5) / (num_ratings + 1),1), num_ratings = num_ratings + 1
    WHERE movie_id = (select movie_id from movies where movie_title = 'The Dark Knight');

--5. Leave an additional comment for a movie

INSERT INTO comments(movie_id, user_id, user_comment, comment_id)
    SELECT movies.movie_id, user.user_id, 'another comment', 2
    FROM movies, user
    WHERE movies.movie_title = 'The Dark Knight' AND user.user_id = 1;

--6. View the average rating or comments for a movie
.headers on
SELECT DISTINCT movies.movie_title, avg_rating, user_comment as num6
    FROM ratings
        JOIN comments ON ratings.movie_id = comments.movie_id
        JOIN movies ON comments.movie_id = movies.movie_id
        WHERE movies.movie_title = 'The Dark Knight';

--7. View your rating for a movie
.headers on
SELECT user_rating as num7
    FROM watchlist
    WHERE user_id = (select user_id from user where user_name = 'Michele')
    AND movie_id = (select movie_id from movies where movie_title = 'The Dark Knight')
    LIMIT 1; 

--8. Edit your comment to a movie

UPDATE watchlist
    SET user_comment = 'updating user comment'
    WHERE user_id = (select user_id from user where user_name = 'Michele') 
    AND movie_id = (select movie_id from movies where movie_title = 'The Dark Knight')
    AND comment_id = 1;

UPDATE comments
    SET user_comment = 'updating user comment'
    WHERE user_id = (select user_id from user where user_name = 'Michele') 
    AND movie_id = (select movie_id from movies where movie_title = 'The Dark Knight')
    AND comment_id = 1;  

--9. Update your rating for a movie

UPDATE watchlist
    SET user_rating = 3.5
    WHERE user_id = (select user_id from user where user_name = 'Michele')
    AND movie_id = (select movie_id from movies where movie_title = 'The Dark Knight');
    --also updating avg_rating with new rating from user
    --WE NEED TO STORE OLD RATING IN PYTHON TO SUBTRACT FROM AVG_RATING
UPDATE ratings
    SET avg_rating = round(((avg_rating*num_ratings) + 3.5) / num_ratings,1)
    WHERE movie_id = (select movie_id from movies where movie_title = 'The Dark Knight');

--10. View your watchlist 
.headers on
SELECT movie_title, user_rating, user_comment as num10
    FROM watchlist
    JOIN movies ON movies.movie_id = watchlist.movie_id
    WHERE user_id = (select user_id from user where user_name = 'Michele')
    GROUP BY watchlist.movie_id;

--11. Display/sort watchlist alphabetically 
.headers on
SELECT movie_title, user_rating, user_comment as num11
    FROM watchlist
    JOIN movies ON movies.movie_id = watchlist.movie_id
    WHERE user_id = (select user_id from user where user_name = 'Michele')
    GROUP BY movie_title; 

--12. Remove a movie from your watchlist

DELETE FROM watchlist 
    WHERE EXISTS 
    (select *
        from movies
        where watchlist.movie_id = movies.movie_id and movie_title = 'The Dark Knight');

--13. Remove your comment

DELETE FROM comments
    WHERE user_id = (select user_id from user where user_name = 'Michele') 
    AND movie_id = (select movie_id from movies where movie_title = 'The Dark Knight')
    AND comment_id = 2;

--14. Find movies of the same genre 
.headers on
SELECT DISTINCT movie_title as num14
    FROM movies 
    WHERE movie_genre = 'Action';

--15. Find all movies by actor
.headers on
SELECT DISTINCT movies.movie_title as num15
    FROM movies
    JOIN principles ON movies.movie_id = principles.movie_id
    JOIN entertainer ON principles.ent_id = entertainer.ent_id 
    WHERE entertainer.ent_name = 'Christian Bale';

--16. Find all movies by person's profession
.headers on
SELECT DISTINCT movie_title as num16
    FROM movies
    JOIN principles ON movies.movie_id = principles.movie_id
    JOIN entertainer ON principles.ent_id = entertainer.ent_id
    WHERE ent_prof = 'Director' AND ent_name = 'Christopher Nolan';

--17. Movies released within a range of years
.headers on
SELECT DISTINCT movie_title as num17
    FROM movies
    WHERE movie_year BETWEEN 2000 AND 2002;

--18. All movies above a certain rating threshhold
.headers on
SELECT DISTINCT movie_title, avg_rating as num18
    FROM movies, ratings
    WHERE movies.movie_id = ratings.movie_id 
    AND avg_rating > 8.9;

--19. Display stats on a movie
.headers on
SELECT DISTINCT movie_title, movie_year, movie_genre, avg_rating, num_ratings, ent_name as actor
    FROM movies, ratings, entertainer, principles
    WHERE movies.movie_id = ratings.movie_id AND 
    movies.movie_id = principles.movie_id AND
    principles.ent_id = entertainer.ent_id AND
    ent_prof = 'Actor' AND movie_title = 'The Dark Knight';
    
--20. Movies where a person was both an actor and a director
.headers on
SELECT DISTINCT ent_name, movie_title as num20
    FROM movies
    JOIN principles ON movies.movie_id = principles.movie_id
    JOIN entertainer ON principles.ent_id = entertainer.ent_id
    WHERE job_role = 'Actor' 
INTERSECT
SELECT DISTINCT ent_name, movie_title
    FROM movies
    JOIN principles ON movies.movie_id = principles.movie_id
    JOIN entertainer ON principles.ent_id = entertainer.ent_id
    WHERE job_role = 'Director';
