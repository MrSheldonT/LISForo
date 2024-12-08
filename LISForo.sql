CREATE DATABASE LISForo;
USE LISForo;

CREATE TABLE roles (
    id_role INT AUTO_INCREMENT PRIMARY KEY,
    name ENUM('admin', 'user') NOT NULL UNIQUE --role_name
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
