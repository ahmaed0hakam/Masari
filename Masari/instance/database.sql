
-- CREATE TABLE Users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL UNIQUE,
--     password TEXT NOT NULL,
--     name TEXT,
--     age INTEGER,
-- );
-- SELECT * FROM users;

-- INSERT INTO UserLearningPaths (user_id, path_id)
-- VALUES (2, 1);

-- INSERT INTO UserLearningPaths (user_id, path_id)
-- VALUES (2, 2);

-- INSERT INTO Users (username, password) VALUES ('admin', 'admin');

-- CREATE TABLE Courses (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     title TEXT NOT NULL,
--     description TEXT
-- );
-- CREATE TABLE Lessons (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     course_id INTEGER,
--     title TEXT NOT NULL,
--     content TEXT,
--     FOREIGN KEY(course_id) REFERENCES Courses(id)
-- );
-- CREATE TABLE LearningPaths (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     title TEXT NOT NULL,
--     description TEXT
-- );
-- CREATE TABLE UserLearningPaths (
--     user_id INTEGER,
--     path_id INTEGER,
--     PRIMARY KEY (user_id, path_id),
--     FOREIGN KEY(user_id) REFERENCES Users(id),
--     FOREIGN KEY(path_id) REFERENCES LearningPaths(id)
-- );
-- CREATE TABLE SessionHistory (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER,
--     interaction TEXT,
--     FOREIGN KEY(user_id) REFERENCES Users(id)
-- );

-- DROP TABLE user;
