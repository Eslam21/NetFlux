USE netflux;
#SET FOREIGN_KEY_CHECKS=0; drop TABLE casting; SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE IF NOT EXISTS persons(
   userid VARCHAR (40),
   first_name VARCHAR(40) NOT NULL,
   last_name VARCHAR(40) NOT NULL,
   email VARCHAR(100) NOT NULL,
   password VARCHAR(100) NOT NULL,
   birthday DATE,
   person_type ENUM('user','admin') DEFAULT 'user',
   gender ENUM('M', 'F'),
   PRIMARY KEY ( userid ),
   UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS favourites(
    userid VARCHAR (40) NOT NULL,
    movieid INTEGER NOT NULL, 
	PRIMARY KEY(userid, movieid)
    , FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
    , FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS watchlist(
	userid VARCHAR (40) NOT NULL,
    movieid INTEGER NOT NULL, 
	PRIMARY KEY(userid, movieid)
	, FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
    , FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS rated(
	userid VARCHAR (40) NOT NULL,
    movieid INTEGER NOT NULL, 
    rating INTEGER NOT NULL,
	PRIMARY KEY(userid, movieid)
	, FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
    , FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Watched(
	userid VARCHAR (40) NOT NULL,
    movieid INTEGER NOT NULL, 
    Total_time INTEGER  NOT NULL,
	PRIMARY KEY(userid, movieid)
	, FOREIGN KEY (movieid) REFERENCES movies(movieid) ON DELETE CASCADE
    , FOREIGN KEY (userid) REFERENCES persons(userid) ON DELETE CASCADE
);