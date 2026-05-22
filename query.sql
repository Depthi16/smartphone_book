SELECT * FROM phonebook.users;

use phonebook;

DROP TABLE users;

CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL

);


DROP TABLE contacts;

DROP TABLE users;

CREATE TABLE users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL

);

CREATE TABLE contacts (

    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    phone VARCHAR(15) UNIQUE,

    email VARCHAR(100),

    company VARCHAR(100),

    address TEXT,

    category VARCHAR(50),

    favorite BOOLEAN DEFAULT FALSE,

    user_id INT,

    FOREIGN KEY (user_id)
    REFERENCES users(id)

);