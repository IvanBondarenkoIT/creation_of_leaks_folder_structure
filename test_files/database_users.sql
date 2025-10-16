-- Test Database Dump
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255)
);

INSERT INTO users VALUES (1, 'admin', 'admin@test.com', 'hash123');
INSERT INTO users VALUES (2, 'user', 'user@test.com', 'hash456');

