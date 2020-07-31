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
	IsActive BOOLEAN NOT NULL DEFAULT '1',
	LineupIds INT[] NOT NULL
);

-- Table to hold all unique Tournament Organizers
CREATE TABLE Organizers (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	EventSeries VARCHAR ARRAY NULL
);

-- Tables to hold all the unique Events and their information
-- PrizePool is Varchar to maintain currency and precision
CREATE TABLE Events (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	Organizer INT REFERENCES Organizers NULL,
	Location VARCHAR NULL,
	PrizePool INT NULL,
	EventStageIds INT[] NOT NULL,
	StartDate DATE NULL,
	EndDate DATE NULL
);

-- Scoreflow example: [8, 7, 8, 0]
-- even indices are team 1, odd are team 2, pairs represent halves or OT halves
CREATE TABLE Matches (
	Id SERIAL PRIMARY KEY,
	EventId INT REFERENCES EventStages NOT NULL,
	EventStageId INT REFERENCES Events NOT NULL,
	MapIds INT[] NOT NULL,
	Team1 INT REFERENCES Teams NOT NULL,
	Team2 INT REFERENCES Teams NOT NULL,
	Lineup1 SERIAL REFERENCES Lineups NOT NULL,
	Lineup2 SERIAL REFERENCES Lineups NOT NULL,
	ScoreFlow INT[] NOT NULL,
	NextMatchId INT REFERENCES Matches NULL,
	PreviousMatchIds INT[] NULL,
	Date DATE NULL
);

CREATE TABLE Lineups (
	Id SERIAL PRIMARY KEY,
	PlayerIds INT[5] NOT NULL,
	TeamIds INT[] NULL,
	FormalizedStartDate DATE NOT NULL,
	FormalizedEndDate DATE NULL
);

-- basically a contiguous collection of matches. A connected graph
CREATE TABLE EventStages (
	Id SERIAL PRIMARY KEY,
	NominalMatchId SERIAL REFERENCES Matches NULL,
	IsOnline BOOLEAN NULL,
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

CREATE TABLE Weapons (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	DateInserted DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO Weapons VALUES(DEFAULT, 'cz', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'desert_eagle', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'dual_berettas', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'five_seven', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'glock', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'p2000', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'p250', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'r8', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'tec9', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'usp', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'mag7', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'nova', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'sawed_off', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'xm', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'mac10', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'mp5', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'mp7', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'mp9', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'p90', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'ump', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'ak', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'aug', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'famas', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'galil', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'm4a1s', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'm4a4', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'sg', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'awp', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'g3sg1', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'scar', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'ssg', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'negev', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'knife', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'zeus', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'he', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'fire', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'flash', DEFAULT);
INSERT INTO Weapons VALUES(DEFAULT, 'smoke', DEFAULT);

CREATE TABLE Casters (
	Id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	Alias VARCHAR NULL,
	AlternateAliases VARCHAR[] NULL
);

INSERT INTO Casters VALUES(DEFAULT, 'Matthew Trivett', 'Sadokist', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Anders Blume', 'Anders', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Mark Wilson', 'boq', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Rahim Abdullav', 'Babam', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Daniel Kapadia', 'ddk', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Dustin Mouret', 'dusT', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Alex Hawkins', 'Hawka', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Joseph Cunningham', 'heliumbrella', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'James Bardolph', 'James', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Alex Richardson', 'Machine', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Chad Burchill', 'SPUNJ', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Auguste Massonnat', 'Semmler', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Stuart Saw', 'TosspoT', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Henry Greer', 'HenryG', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Jason O''Toole', 'moses', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Tomi Kovanen', 'lurppis', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Sam Marine', 'DaZeD', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Jordan Gilbert', 'n0thing', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Duncan Shields', 'Thorin', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Scott Smith', 'SirScoots', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Sean Gares', 'seang@res', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Richard Lewis', NULL, NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Vince Hill', 'Vince', '{"Metuz"}');
INSERT INTO Casters VALUES(DEFAULT, 'John Mullen', 'Blu', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Leigh Smith', 'Deman', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Cory Gilbert', 'megaman', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'Mohan Govindasamy', 'csboxr', NULL);
INSERT INTO Casters VALUES(DEFAULT, 'UNKNOWN', 'UNKNOWN', NULL);

CREATE TABLE Clips (
	Id SERIAL PRIMARY KEY,
	Code VARCHAR(16) NOT NULL,
	Event INT REFERENCES Events NULL,
	Map SERIAL REFERENCES Maps,
	Player SERIAL REFERENCES Players,
	Team SERIAL REFERENCES Teams,
	GrandFinal BOOLEAN NOT NULL,
	Armor BOOLEAN NOT NULL,
	Crowd BOOLEAN NOT NULL,
	Kills INT CHECK (kills >= 0 AND kills <= 5),
	ClutchKills INT CHECK (clutchkills >= 0 AND clutchkills <= 5),
	Weapon INT[] NOT NULL,
	Casters Caster[] NULL,
	DateInserted DATE NOT NULL DEFAULT CURRENT_DATE
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
	FavoriteWeapon INT REFERENCES Weapons NULL
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
	(SELECT Id FROM Weapons WHERE Name = 'mag7')
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

-- Keeps track of each of the kills tracked in clips
CREATE TABLE Interactions (
	Id SERIAL PRIMARY KEY,
	WinnerId SERIAL REFERENCES Players,
	LoserId SERIAL REFERENCES Players,
	WeaponId SERIAL REFERENCES Weapons,
	Clutch BOOLEAN NOT NULL,
	HealthOfWinner INT NOT NULL,
	Armor INT NOT NULL
);