CREATE DATABASE IF NOT EXISTS mystl;

USE mystl;

CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(100) NOT NULL PRIMARY KEY,
    email VARCHAR(200) NOT NULL,
    password VARCHAR(200) NOT NULL DEFAULT '',
    salt VARCHAR(100) NOT NULL,
    confirmed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS ConfirmationTokens (
    username VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL,
    exp INT DEFAULT 0,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ResetPasswordTokens (
    username VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL,
    exp INT DEFAULT 0,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Objects (
    name VARCHAR(400) NOT NULL PRIMARY KEY,
    hash VARCHAR(200) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    FOREIGN KEY (owner) REFERENCES Users(username)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Permissions (
    permission VARCHAR(10) NOT NULL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Shares (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    permission VARCHAR(10),
    PRIMARY KEY(object, username),
    FOREIGN KEY (permission) REFERENCES Permissions(permission) ON DELETE CASCADE,
    FOREIGN KEY (object) REFERENCES Objects(name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Comments (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    comment TEXT,
    PRIMARY KEY (object, username),
    FOREIGN KEY (object) REFERENCES Objects(name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PointAnnotations (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    annotation VARCHAR(1000) NOT NULL,
    PRIMARY KEY (object, username, name),
    FOREIGN KEY (object) REFERENCES Objects(name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DistanceAnnnotations (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    start_position_x FLOAT NOT NULL,
    start_position_y FLOAT NOT NULL,
    start_position_z FLOAT NOT NULL,
    end_position_x FLOAT NOT NULL,
    end_position_y FLOAT NOT NULL,
    end_position_z FLOAT NOT NULL,
    annotation VARCHAR(1000) NOT NULL,
    PRIMARY KEY (object, username, name),
    FOREIGN KEY (object) REFERENCES Objects(name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AngleAnnnotations (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    start_position_x FLOAT NOT NULL,
    start_position_y FLOAT NOT NULL,
    start_position_z FLOAT NOT NULL,
    end_position_x FLOAT NOT NULL,
    end_position_y FLOAT NOT NULL,
    end_position_z FLOAT NOT NULL,
    center_position_x FLOAT NOT NULL,
    center_position_y FLOAT NOT NULL,
    center_position_z FLOAT NOT NULL,
    annotation VARCHAR(1000) NOT NULL,
    PRIMARY KEY (object, username, name),
    FOREIGN KEY (object) REFERENCES Objects(name) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);