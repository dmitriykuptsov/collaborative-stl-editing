DROP DATABASE mystl;

CREATE DATABASE IF NOT EXISTS mystl;

USE mystl;

CREATE TABLE IF NOT EXISTS Countries (
    country_code VARCHAR(3),
    country VARCHAR(200),
    PRIMARY KEY (country_code)
);

CREATE TABLE IF NOT EXISTS Cities (
    city_code VARCHAR(10),
    city VARCHAR(200),
    country_code VARCHAR(3),
    PRIMARY KEY (country_code, city_code),
    FOREIGN KEY (country_code) REFERENCES Countries(country_code) ON DELETE CASCADE
);

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
    enable_two_factor_auth DEFAULT FALSE,
    FOREIGN KEY (country_code, city_code) REFERENCES Cities(country_code, city_code) ON DELETE CASCADE,
    FOREIGN KEY (country_code) REFERENCES Countries(country_code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TwoFactorAuthentication (
    username VARCHAR(200) NOT NULL,
    code VARCHAR(6) NOT NULL,
    exp INT DEFAULT 0,
    PRIMARY KEY (username, code),
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ConfirmationTokens (
    username VARCHAR(100) NOT NULL PRIMARY KEY,
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
    name VARCHAR(400) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    description VARCHAR(4000) NOT NULL,
    creation_time DATETIME NOT NULL,
    PRIMARY KEY (name, owner),
    FOREIGN KEY (owner) REFERENCES Users(username)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ObjectVersions (
    name VARCHAR(400) NOT NULL,
    version INT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    hash VARCHAR(200) NOT NULL,
    date_uploaded DATETIME NOT NULL,
    surface_area FLOAT DEFAULT 0.0,
    volume FLOAT DEFAULT 0.0,
    cog_x FLOAT DEFAULT 0.0,
    cog_y FLOAT DEFAULT 0.0,
    cog_z FLOAT DEFAULT 0.0,
    is_water_tight BOOLEAN DEFAULT TRUE,
    number_of_facets INT DEFAULT 0,
    number_of_unique_verticies INT DEFAULT 0,
    has_zero_area_triangles BOOLEAN DEFAULT FALSE,
    is_edge_manifold BOOLEAN DEFAULT FALSE,
    is_vertex_manifold BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(name, version, owner),
    FOREIGN KEY (name, owner) REFERENCES Objects(name, owner)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Colors (
    color VARCHAR(400) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Materials (
    material VARCHAR(400) NOT NULL,
    type_code INT,
    color VARCHAR(400) NOT NULL,
    price_per_cubic_cm FLOAT,
    PRIMARY KEY(material, color),
    FOREIGN KEY (color) REFERENCES Colors(color)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Machinery (
    machine VARCHAR(400) NOT NULL,
    dimension_x FLOAT,
    dimension_y FLOAT,
    dimension_z FLOAT,
    material VARCHAR(400) NOT NULL,
    PRIMARY KEY(name, material),
    FOREIGN KEY (material) REFERENCES Materials(name, owner)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Providers (
    provider VARCHAR(400) NOT NULL PRIMARY KEY,
    is_local BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS ProvidersMachinery (
    provider VARCHAR(400) NOT NULL,
    machine VARCHAR(400) NOT NULL,
    material VARCHAR(400) NOT NULL,
    PRIMARY KEY(provider, machine),
    FOREIGN KEY (machine, material) REFERENCES Machinery(machine, material)
    ON DELETE CASCADE
)

CREATE TABLE IF NOT EXISTS OrderStatus (
    name VARCHAR(400) NOT NULL,
    status INT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Orders (
    name VARCHAR(400) NOT NULL,
    version INT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    status INT NOT NULL DEFAULT 0,
    paid BOOLEAN DEFAULT FALSE,
    cost FLOAT,
    machine VARCHAR(400) NOT NULL,
    material VARCHAR(400) NOT NULL,
    order_date DATETIME NOT NULL,
    PRIMARY KEY(name, version, owner),
    FOREIGN KEY (name, version, owner) REFERENCES ObjectVersions(name, version, owner)
    ON DELETE CASCADE,
    FOREIGN KEY (machine, material) REFERENCES Machinery(machine, material)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Permissions (
    permission VARCHAR(10) NOT NULL PRIMARY KEY,
    description VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Shares (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    permission VARCHAR(10),
    PRIMARY KEY(object, username, owner),
    FOREIGN KEY (permission) REFERENCES Permissions(permission) ON DELETE CASCADE,
    FOREIGN KEY (object, owner) REFERENCES Objects(name, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Comments (
    object VARCHAR(400) NOT NULL,
    username VARCHAR(100) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    comment TEXT,
    date_of_comment DATETIME,
    PRIMARY KEY (object, username, owner),
    FOREIGN KEY (object, owner) REFERENCES Objects(name, owner) ON DELETE CASCADE,
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
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(name, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DistanceAnnnotations (
    object VARCHAR(400) NOT NULL,
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
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(name, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AngleAnnnotations (
    object VARCHAR(400) NOT NULL,
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
    FOREIGN KEY (object, version, owner) REFERENCES ObjectVersions(name, version, owner) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
);
