DROP DATABASE IF EXISTS LISForo;
CREATE DATABASE LISForo;
USE LISForo;

CREATE TABLE roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    name ENUM('admin', 'user') NOT NULL UNIQUE
);

CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY
    , username VARCHAR(50) NOT NULL UNIQUE
    , email VARCHAR(100) NOT NULL UNIQUE
    , password VARCHAR(60) NOT NULL
    , id_role INT NOT NULL
    , FOREIGN KEY (id_role) REFERENCES roles(id_role) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE posts (
    id_post INT AUTO_INCREMENT PRIMARY KEY
    , id_user INT NOT NULL
    , title VARCHAR(50) NOT NULL
    , content TEXT NOT NULL
    , created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    , FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE comments (
    id_comment INT AUTO_INCREMENT PRIMARY KEY
    , id_post INT NOT NULL
    , id_user INT NOT NULL
    , content VARCHAR(255) NOT NULL
    , created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    , updated_at DATETIME NULL
    , is_edited BOOLEAN DEFAULT FALSE
    , FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE ON UPDATE CASCADE
    , FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE comment_likes (
    id_comment_like INT AUTO_INCREMENT PRIMARY KEY
    , id_comment INT NOT NULL
    , id_user INT NOT NULL
    , created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    , FOREIGN KEY (id_comment) REFERENCES comments(id_comment) ON DELETE CASCADE ON UPDATE CASCADE
    , FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE post_likes (
    id_post_like INT AUTO_INCREMENT PRIMARY KEY
    , id_post INT NOT NULL
    , id_user INT NOT NULL
    , created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    , FOREIGN KEY (id_post) REFERENCES posts(id_post) ON DELETE CASCADE ON UPDATE CASCADE
    , FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO roles(name) VALUES 
    ("admin")
    , ("user")
;

DELIMITER //

CREATE TRIGGER update_comment
BEFORE UPDATE ON comments
FOR EACH ROW
BEGIN
    SET NEW.is_edited = TRUE;
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END //

DELIMITER ;

CREATE TABLE logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY
    , table_name VARCHAR(50) NOT NULL
    , action VARCHAR(50) NOT NULL
    , performed_by INT
    , details TEXT NOT NULL
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


DELIMITER //
CREATE TRIGGER after_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'users'
        , 'INSERT'
        , NEW.id_user
        , CONCAT('New user created with ID ', NEW.id_user, ', username: "', NEW.username, '"')
    );
END //

CREATE TRIGGER after_user_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'users'
        , 'UPDATE'
        , NEW.id_user
        , CONCAT('User ID ', NEW.id_user, ' was updated. New username: "', NEW.username, '", New email: "', NEW.email, '"')
    );
END //

CREATE TRIGGER after_user_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'users'
        , 'DELETE'
        , OLD.id_user
        , CONCAT('User ID ', OLD.id_user, ', username: "', OLD.username, '" was deleted')
    );
END //

CREATE TRIGGER after_post_insert
AFTER INSERT ON posts
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'posts'
        , 'INSERT'
        , NEW.id_user
        , CONCAT('New post created with ID ', NEW.id_post, ', title: "', NEW.title, '" by user ID ', NEW.id_user)
    );
END //

CREATE TRIGGER after_post_update
AFTER UPDATE ON posts
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'posts'
        , 'UPDATE'
        , NEW.id_user
        , CONCAT('Post ID ', NEW.id_post, ' updated. New title: "', NEW.title, '", New content: "', NEW.content, '"')
    );
END //

CREATE TRIGGER after_post_delete
AFTER DELETE ON posts
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'posts'
        , 'DELETE'
        , OLD.id_user
        , CONCAT('Post ID ', OLD.id_post, ', title: "', OLD.title, '" deleted')
    );
END //

CREATE TRIGGER after_comment_insert
AFTER INSERT ON comments
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'comments'
        , 'INSERT'
        , NEW.id_user
        , CONCAT('New comment created with ID ', NEW.id_comment, ' on post ID ', NEW.id_post)
    );
END //

CREATE TRIGGER after_comment_update
AFTER UPDATE ON comments
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'comments'
        , 'UPDATE'
        , NEW.id_user
        , CONCAT('Comment ID ', NEW.id_comment, ' was updated. Edited flag: ', NEW.is_edited,
               '. New content: "', NEW.content, '"')
    );
END //

CREATE TRIGGER after_comment_delete
AFTER DELETE ON comments
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'comments'
        , 'DELETE'
        , OLD.id_user
        , CONCAT('Comment ID ', OLD.id_comment, ' deleted from post ID ', OLD.id_post)
    );
END //

CREATE TRIGGER after_comment_like_insert
AFTER INSERT ON comment_likes
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'comment_likes'
        , 'INSERT'
        , NEW.id_user
        , CONCAT('User ID ', NEW.id_user, ' liked comment ID ', NEW.id_comment)
    );
END //

CREATE TRIGGER after_comment_like_delete
AFTER DELETE ON comment_likes
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'comment_likes'
        , 'DELETE'
        , OLD.id_user
        , CONCAT('User ID ', OLD.id_user, ' unliked comment ID ', OLD.id_comment)
    );
END //

CREATE TRIGGER after_post_like_insert
AFTER INSERT ON post_likes
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'post_likes'
        , 'INSERT'
        , NEW.id_user
        , CONCAT('User ID ', NEW.id_user, ' liked post ID ', NEW.id_post)
    );
END //

CREATE TRIGGER after_post_like_delete
AFTER DELETE ON post_likes
FOR EACH ROW
BEGIN
    INSERT INTO logs (table_name, action, performed_by, details)
    VALUES (
        'post_likes'
        , 'DELETE'
        , OLD.id_user
        , CONCAT('User ID ', OLD.id_user, ' unliked post ID ', OLD.id_post)
    );
END //
DELIMITER ;