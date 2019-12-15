-- Table to hold all the unique Players
CREATE TABLE Players (
	Id SERIAL PRIMARY KEY,
	Alias VARCHAR(64) NOT NULL,
	Name VARCHAR NOT NULL,
	Country VARCHAR(64) NULL,
	AlternateAliases VARCHAR(64) ARRAY NULL,
	IsActive BOOLEAN NOT NULL DEFAULT '1'
);

-- Table to hold all the unique Teams
CREATE TABLE Teams (
	Id SERIAL PRIMARY KEY,
	Alias VARCHAR(64) NOT NULL,
	AlternateAliases VARCHAR(64) ARRAY NULL,
	IsActive BOOLEAN NOT NULL DEFAULT '1'
);

-- Table to hold all unique Tournament Organizers
CREATE TABLE Organizers (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	EventSeries VARCHAR ARRAY NULL
);

-- Table to hold all the unique Events
-- PrizePool is Varchar to maintain currency and precision
CREATE TABLE Events (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	Organizer INT REFERENCES Organizers NULL,
	Location VARCHAR NULL,
	PrizePool VARCHAR NULL,
	StartDate DATE NULL,
	EndDate DATE NULL
);

INSERT INTO Organizers VALUES(DEFAULT, 'EPICENTER');
INSERT INTO Organizers VALUES(DEFAULT, 'BLAST', '{"Pro", "Premier"}');
INSERT INTO Organizers VALUES(DEFAULT, 'ESL', '{"One", "Pro League", "Intel Extreme Masters"}');
INSERT INTO Organizers VALUES(DEFAULT, 'Faceit', '{"Esports Championship Series"}');
INSERT INTO Organizers VALUES(DEFAULT, 'Perfect World');
INSERT INTO Organizers VALUES(DEFAULT, 'Intel Extreme Masters');
INSERT INTO Organizers VALUES(DEFAULT, 'Starladder', '{"StarSeries", "iLeague"}');
INSERT INTO Organizers VALUES(DEFAULT, 'DreamHack', '{"Masters", "Open"}');
INSERT INTO Organizers VALUES(DEFAULT, 'World Electronic Sports Games');
INSERT INTO Organizers VALUES(DEFAULT, 'EPICENTER');
INSERT INTO Organizers VALUES(DEFAULT, 'ELEAGUE', '{"Premier"}');
INSERT INTO Organizers VALUES(DEFAULT, 'ESG Tour');
INSERT INTO Organizers VALUES(DEFAULT, 'PGL');
INSERT INTO Organizers VALUES(DEFAULT, 'MLG');
INSERT INTO Organizers VALUES(DEFAULT, 'Fragbite Masters');
INSERT INTO Organizers VALUES(DEFAULT, 'CEVO');
INSERT INTO Organizers VALUES(DEFAULT, 'Gfinity', '{"Masters"}');
INSERT INTO Organizers VALUES(DEFAULT, 'ESWC', '{"World Cup"}');
INSERT INTO Organizers VALUES(DEFAULT, 'ESEA');
INSERT INTO Organizers VALUES(DEFAULT, 'cs_summit');
INSERT INTO Organizers VALUES(DEFAULT, 'V4', '{"Future Sports Festival"}');
INSERT INTO Organizers VALUES(DEFAULT, 'iBUYPOWER', '{"Masters"}');
INSERT INTO Organizers VALUES(DEFAULT, 'Power League Gaming');
INSERT INTO Organizers VALUES(DEFAULT, 'ROG');
INSERT INTO Organizers VALUES(DEFAULT, 'World Cyber Arena');
INSERT INTO Organizers VALUES(DEFAULT, 'Acer', '{"Predator Masters"}');
INSERT INTO Organizers VALUES(DEFAULT, 'ZOTAC');
INSERT INTO Organizers VALUES(DEFAULT, 'Copenhagen Games');
INSERT INTO Organizers VALUES(DEFAULT, 'Counter Pit');
INSERT INTO Organizers VALUES(DEFAULT, 'Pantamera');


-- Table to hold all the unique Maps
CREATE TABLE Maps (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	IsActiveDuty BOOLEAN NOT NULL DEFAULT '1',
	CurrentBigVersion BOOLEAN NOT NULL DEFAULT '1'
);

INSERT INTO Maps VALUES(
	DEFAULT, 'de_dust2', DEFAULT, DEFAULT
);
-- old cache
INSERT INTO Maps VALUES(
	DEFAULT, 'de_cache', '0', '0'
);
-- new cache
INSERT INTO Maps VALUES(
	DEFAULT, 'de_cache', '0', '1'
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_inferno', DEFAULT, '0'
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_inferno', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_train', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_dust2', DEFAULT, '0'
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_vertigo', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_nuke', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_overpass', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_mirage', DEFAULT, DEFAULT
);
INSERT INTO Maps VALUES(
	DEFAULT, 'de_cbble', '0', DEFAULT
);

CREATE TYPE WEAPON AS ENUM('cz','desert_eagle','dual_berettas','five_seven','glock','p2000','p250','r8','tec9','usp','mag7','nova','sawed_off','xm','mac10','mp5','mp7','mp9','p90','pp_bizon','ump','ak','aug','famas','galil','m4a1s','m4a4','sg','awp','g3sg1','scar','ssg','m249','negev','knife','zeus','he','fire','flash','smoke');
CREATE TABLE Clips(
	Id SERIAL PRIMARY KEY,
	Code VARCHAR(512) NOT NULL,
	Event INT REFERENCES Events NULL,
	Map SERIAL REFERENCES Maps,
	Player SERIAL REFERENCES Players,
	Team SERIAL REFERENCES Teams,
	GrandFinal BOOLEAN NOT NULL,
	Armor BOOLEAN NOT NULL,
	Crowd BOOLEAN NOT NULL,
	Kills INT CHECK (kills >= 0 AND kills <= 5),
	ClutchKills INT CHECK (clutchkills >= 0 AND clutchkills <= 5),
	Weapon WEAPON ARRAY NOT NULL
);

-- Enable the crypto for passwords
CREATE EXTENSION pgcrypto;

CREATE TABLE Users (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR(64) NOT NULL,
  	Email TEXT NOT NULL UNIQUE,
	Password TEXT NOT NULL,
	SignUpDate DATE NOT NULL DEFAULT CURRENT_DATE,
	SignInDate DATE NULL,
	FavoriteWeapon WEAPON NULL
);

CREATE TYPE STORY_TYPE AS ENUM('Player', 'Team', 'Event');
CREATE TYPE STORY_SCOPE AS ENUM('Map', 'Series', 'Event', 'Epoch');
-- Note that the relationships with primary keys in ClipIds are not maintained
CREATE TABLE Stories (
	Id SERIAL PRIMARY KEY,
	CreationDate DATE NULL,
	Title VARCHAR NOT NULL,
	ClipIds INT ARRAY NOT NULL,
	Type STORY_TYPE NOT NULL,
	Scope STORY_SCOPE NOT NULL
);

INSERT INTO Users VALUES(
	DEFAULT,
	'clipd',
	'robbie.a.freeman@gmail.com',
	crypt('pass', gen_salt('bf')),
	DEFAULT,
	NULL,
	'mag7'
);

-- 6 cats: Casting, Significance, Intelligence, Atmosphere, Aim, Luck
-- meant to range from 0-5
CREATE TABLE RatingCategories (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL
);

INSERT INTO RatingCategories VALUES(DEFAULT, 'Casting');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Significance');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Intelligence');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Atmosphere');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Aim');
INSERT INTO RatingCategories VALUES(DEFAULT, 'Luck');

CREATE TABLE Ratings (
	Id SERIAL PRIMARY KEY,
	ClipId SERIAL REFERENCES Clips,
	UserId SERIAL REFERENCES Users,
	RatingCategoryId SERIAL REFERENCES RatingCategories,
	UNIQUE (ClipId, UserId, RatingCategoryId),
	Rating FLOAT CHECK (rating >= 0.0 AND rating <= 5.0),
	CreationDate DATE NOT NULL DEFAULT now()
);

-- Table to track the average aggregate ratings, per cat, per clip
CREATE TABLE RatingAvgs (
	Id SERIAL PRIMARY KEY,
	ClipId SERIAL REFERENCES Clips,
	RatingCategoryId SERIAL REFERENCES RatingCategories,
	UNIQUE (ClipId, RatingCategoryId),
	Total INT NOT NULL DEFAULT 1,
	Average FLOAT NOT NULL CHECK (average >= 0.0 AND average <= 5.0)
);