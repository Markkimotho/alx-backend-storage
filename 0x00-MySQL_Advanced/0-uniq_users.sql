-- script that creates a table users with id, email, name
CREATE TABLE IF NOT EXISTS holberton.users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255));
