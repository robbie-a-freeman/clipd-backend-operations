INSERT INTO Clips VALUES(
	DEFAULT,
	'AzeuySdai40',
	(SELECT Id FROM Events WHERE Name = 'PGL Major Krak\xc3\xb3w 2017'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Dosia'),
	(SELECT Id FROM Teams WHERE Alias = 'Gambit Esports'),
	'1',
	'1',
	'1',
	0,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'he')],
	DEFAULT
);


INSERT INTO Clips VALUES(
	DEFAULT,
	'yJifD2IEgx4',
	(SELECT Id FROM Events WHERE Name = 'Europe Minor Championship - Boston 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'BARBARR'),
	(SELECT Id FROM Teams WHERE Alias = 'Epsilon Esports'),
	'0',
	'1',
	'0',
	4,
	4,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'ak')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'1NN1CjhH7rA',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Katowice 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Friberg'),
	(SELECT Id FROM Teams WHERE Alias = 'Ninjas in Pyjamas'),
	'1',
	'1',
	'1',
	2,
	2,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'ak')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'W9Jbo4Dv7vc',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'KRIMZ'),
	(SELECT Id FROM Teams WHERE Alias = 'Fnatic'),
	'1',
	'1',
	'1',
	3,
	3,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'ak')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'W9Jbo4Dv7vc',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'NBK'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Envy'),
	'1',
	'1',
	'1',
	1,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'knife')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'cjOVXdarUTs',
	(SELECT Id FROM Events WHERE Name = 'MLG Major Championship: Columbus 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Coldzera'),
	(SELECT Id FROM Teams WHERE Alias = 'Luminosity Gaming'),
	'0',
	'0',
	'1',
	4,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'kUSN6u5CSRE',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'S1mple'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Liquid'),
	'0',
	'1',
	'1',
	2,
	2,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'PO1G0bmWurc',
	(SELECT Id FROM Events WHERE Name = 'ESL One: New York 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'S1mple'),
	(SELECT Id FROM Teams WHERE Alias = 'Natus Vincere'),
	'0',
	'1',
	'1',
	1,
	1,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp'),(SELECT Id FROM Weapons WHERE Name = 'p250')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'qLVIgyrRk28',
	(SELECT Id FROM Events WHERE Name = 'ESL One: New York 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cbble' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Snax'),
	(SELECT Id FROM Teams WHERE Alias = 'Virtus.pro'),
	'1',
	'1',
	'1',
	4,
	4,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'usp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'dmrIfz1TN00',
	(SELECT Id FROM Events WHERE Name = 'MLG Major Championship: Columbus 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Hiko'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Liquid'),
	'0',
	'1',
	'1',
	4,
	4,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'm4a4')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'4YyNMj7KrVs',
	(SELECT Id FROM Events WHERE Name = 'ELEAGUE Major: Boston 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'GuardiaN'),
	(SELECT Id FROM Teams WHERE Alias = 'FaZe Clan'),
	'1',
	'1',
	'1',
	1,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'jRWLI0W6PLk',
	(SELECT Id FROM Events WHERE Name = 'CEVO Season 7 Professional'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'KennyS'),
	(SELECT Id FROM Teams WHERE Alias = 'Titan'),
	'0',
	'1',
	'0',
	5,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'9WV1-AklbEQ',
	(SELECT Id FROM Events WHERE Name = 'ESL Major Series One Katowice 2014'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Snax'),
	(SELECT Id FROM Teams WHERE Alias = 'Virtus.pro'),
	'1',
	'1',
	'1',
	3,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'm4a1s')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'wHtSorLfAGA',
	(SELECT Id FROM Events WHERE Name = 'CEVO Season 7 Professional'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Sgares'),
	(SELECT Id FROM Teams WHERE Alias = 'Cloud9'),
	'0',
	'1',
	'1',
	4,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'awp')],
	DEFAULT
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'XbKDbOhITSw',
	(SELECT Id FROM Events WHERE Name = 'FACEIT Major: London 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_overpass' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'TiziaN'),
	(SELECT Id FROM Teams WHERE Alias = 'BIG'),
	'0',
	'1',
	'0',
	4,
	0,
	ARRAY[(SELECT Id FROM Weapons WHERE Name = 'usp')],
	DEFAULT
);