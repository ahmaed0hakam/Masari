
-- CREATE TABLE Users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     username TEXT NOT NULL UNIQUE,
--     password TEXT NOT NULL,
--     name TEXT,
--     age INTEGER,
-- );
-- SELECT * FROM users;

-- ALTER TABLE Users RENAME COLUMN age TO birthdate;

-- INSERT INTO UserLearningPaths (user_id, path_id)
-- VALUES (2, 1);

-- ALTER TABLE LearningPaths RENAME TO learning_paths;
UPDATE lessons
SET content = NULL
WHERE course_id = 16;

-- INSERT INTO learning_paths (title, description, user_id)
-- VALUES ('Path1', 'Learn Python programming basics', 3),
--        ('Path2', 'Introductory course on web development', 2),
--        ('Database Path', 'Learn about databases and SQL queries', 3),
--        ('Machine Learning Path', 'Introduction to machine learning concepts', 3);


-- UPDATE Users
-- SET birthdate = '2001-03-24'  -- Replace new_user_id with the desired new user_id
-- WHERE id = 2;

-- ALTER TABLE learning_paths
-- DROP COLUMN course_id;

-- -- Update user_id for LearningPaths with id = 2
-- UPDATE Users
-- SET birthdate = '2001-03-24'  -- Replace new_user_id with the desired new user_id
-- WHERE id = 1;


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
