DROP DATABASE IF EXISTS mystl;

CREATE DATABASE IF NOT EXISTS mystl;

USE mystl;

CREATE TABLE IF NOT EXISTS Countries (
    country_code VARCHAR(3),
    country VARCHAR(200),
    PRIMARY KEY (country_code)
);

INSERT INTO Countries VALUES('UZ', 'Узбекистан');

CREATE TABLE IF NOT EXISTS Cities (
    city_code VARCHAR(10),
    city VARCHAR(200),
    country_code VARCHAR(3),
    PRIMARY KEY (country_code, city_code),
    FOREIGN KEY (country_code) REFERENCES Countries(country_code) ON DELETE CASCADE
);

INSERT INTO Cities VALUES('TASH', 'Ташкент', 'UZ');
INSERT INTO Cities VALUES('SAM', 'Самарканд', 'UZ');

CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(100) NOT NULL PRIMARY KEY,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(100),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    street_address VARCHAR(200),
    postal_code VARCHAR(100),
    city_code VARCHAR(10),
    country_code VARCHAR(3),
    password VARCHAR(200) NOT NULL DEFAULT '',
    salt VARCHAR(100) NOT NULL,
    confirmed BOOLEAN DEFAULT FALSE,
    enable_two_factor_auth BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (country_code, city_code) REFERENCES Cities(country_code, city_code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TwoFactorAuthentication (
    username VARCHAR(200) NOT NULL,
    code VARCHAR(6) NOT NULL,
    exp INT DEFAULT 0,
    PRIMARY KEY (username, code),
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ConfirmationTokens (
    username VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL,
    exp INT DEFAULT 0,
    PRIMARY KEY(username, token),
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ResetPasswordTokens (
    username VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL,
    exp INT DEFAULT 0,
    PRIMARY KEY(username, token),
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Objects (
    object VARCHAR(400) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    description VARCHAR(4000) NOT NULL,
    creation_time DATETIME NOT NULL,
    PRIMARY KEY (object, owner),
    FOREIGN KEY (owner) REFERENCES Users(username)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ObjectVersions (
    object VARCHAR(400) NOT NULL,
    version INT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    hash VARCHAR(200) NOT NULL,
    date_uploaded DATETIME NOT NULL,
    surface_area FLOAT DEFAULT 0.0,
    volume FLOAT DEFAULT 0.0,
    cog_x FLOAT DEFAULT 0.0,
    cog_y FLOAT DEFAULT 0.0,
    cog_z FLOAT DEFAULT 0.0,
    bb_x_l FLOAT DEFAULT 0.0,
    bb_y_l FLOAT DEFAULT 0.0,
    bb_z_l FLOAT DEFAULT 0.0,
    bb_x_h FLOAT DEFAULT 0.0,
    bb_y_h FLOAT DEFAULT 0.0,
    bb_z_h FLOAT DEFAULT 0.0,
    is_water_tight BOOLEAN DEFAULT TRUE,
    number_of_facets INT DEFAULT 0,
    number_of_unique_verticies INT DEFAULT 0,
    number_of_unique_edges INT DEFAULT 0,
    has_zero_area_triangles BOOLEAN DEFAULT FALSE,
    is_edge_manifold BOOLEAN DEFAULT FALSE,
    is_vertex_manifold BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(object, version, owner),
    FOREIGN KEY (object, owner) REFERENCES Objects(object, owner)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Colors (
    color VARCHAR(100) NOT NULL PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    description VARCHAR(100)
);

INSERT INTO Colors(description, color, code) VALUES('Белый', 'white', '#ffffff');
INSERT INTO Colors(description, color, code) VALUES('Черный', 'black', '#000000');

CREATE TABLE IF NOT EXISTS Materials (
    material VARCHAR(100) NOT NULL,
    type_code VARCHAR(20) NOT NULL,
    color VARCHAR(100) NOT NULL,
    price_per_cubic_cm FLOAT,
    PRIMARY KEY(material, color),
    FOREIGN KEY (color) REFERENCES Colors(color)
    ON DELETE CASCADE
);

INSERT INTO Materials(material, type_code, color, price_per_cubic_cm) VALUES('Standard Resin', 'SR_W', 'white', 1000);
INSERT INTO Materials(material, type_code, color, price_per_cubic_cm) VALUES('Standard Resin', 'SR_B', 'black', 1000);

CREATE TABLE IF NOT EXISTS Machinery (
    machine VARCHAR(100) NOT NULL,
    dimension_x FLOAT,
    dimension_y FLOAT,
    dimension_z FLOAT,
    material VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    PRIMARY KEY(machine, material, color),
    FOREIGN KEY (material, color) REFERENCES Materials(material, color)
    ON DELETE CASCADE
);

INSERT INTO Machinery(machine, dimension_x, dimension_y, dimension_z, material, color) VALUES('Formlabs Form 4', 30, 30, 30, 'Standard Resin', 'white');
INSERT INTO Machinery(machine, dimension_x, dimension_y, dimension_z, material, color) VALUES('Formlabs Form 4', 30, 30, 30, 'Standard Resin', 'black');

CREATE TABLE IF NOT EXISTS Providers (
    provider VARCHAR(400) NOT NULL PRIMARY KEY,
    is_local BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS ProvidersMachinery (
    provider VARCHAR(400) NOT NULL,
    machine VARCHAR(100) NOT NULL,
    material VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    PRIMARY KEY(provider, machine, material, color),
    FOREIGN KEY (machine, material, color) REFERENCES Machinery(machine, material, color)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS OrderStatus (
    status VARCHAR(100) NOT NULL PRIMARY KEY
);

INSERT INTO OrderStatus VALUES('В ожидании');
INSERT INTO OrderStatus VALUES('В печати');
INSERT INTO OrderStatus VALUES('Готов');
INSERT INTO OrderStatus VALUES('Доставлен');

CREATE TABLE IF NOT EXISTS Orders (
    order_number VARCHAR(100) NOT NULL PRIMARY KEY,
    version INT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    status VARCHAR(100) NOT NULL,
    paid BOOLEAN DEFAULT FALSE,
    cost FLOAT,
    object VARCHAR(100) NOT NULL,
    machine VARCHAR(100) NOT NULL,
    material VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    order_date DATETIME NOT NULL,
    FOREIGN KEY (status) REFERENCES OrderStatus(status)
    ON DELETE CASCADE,
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(object, version, owner)
    ON DELETE CASCADE,
    FOREIGN KEY (machine, material, color) REFERENCES Machinery(machine, material, color)
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Permissions (
    permission VARCHAR(10) NOT NULL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Shares (
    object VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    permission VARCHAR(10),
    PRIMARY KEY(object, username, owner),
    FOREIGN KEY (permission) REFERENCES Permissions(permission) ON DELETE CASCADE,
    FOREIGN KEY (object, owner) REFERENCES Objects(object, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Comments (
    object VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    comment TEXT,
    date_of_comment DATETIME,
    PRIMARY KEY (object, username, owner),
    FOREIGN KEY (object, owner) REFERENCES Objects(object, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PointAnnotations (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    version INT NOT NULL,
    position_x FLOAT NOT NULL,
    position_y FLOAT NOT NULL,
    position_z FLOAT NOT NULL,
    annotation VARCHAR(1000) NOT NULL,
    PRIMARY KEY (object, username, name, version, owner),
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(object, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DistanceAnnnotations (
    object VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    version INT NOT NULL,
    start_position_x FLOAT NOT NULL,
    start_position_y FLOAT NOT NULL,
    start_position_z FLOAT NOT NULL,
    end_position_x FLOAT NOT NULL,
    end_position_y FLOAT NOT NULL,
    end_position_z FLOAT NOT NULL,
    annotation VARCHAR(1000) NOT NULL,
    PRIMARY KEY (object, username, name, version, owner),
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(object, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AngleAnnnotations (
    object VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    version INT NOT NULL,
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
    PRIMARY KEY (object, username, name, version, owner),
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(object, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);
