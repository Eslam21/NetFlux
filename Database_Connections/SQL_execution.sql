USE netflex;
create table IF NOT EXISTS users(
   userid INT NOT NULL AUTO_INCREMENT,
   username VARCHAR (40),
   first_name VARCHAR(40) NOT NULL,
   last_name VARCHAR(40) NOT NULL,
   email VARCHAR(100) NOT NULL,
   password VARCHAR(100) NOT NULL,
   birthday DATE,
   gender ENUM('m''f'),
   PRIMARY KEY ( userid ),
   UNIQUE (username),
   UNIQUE (email)
);

INSERT INTO users(username, first_name, last_name, email, password, birthday)
VALUES('MyriamB', 'Mariam', 'Barakat', 'ma.barakat@nu.edu.eg', '123', '2002-03-06');