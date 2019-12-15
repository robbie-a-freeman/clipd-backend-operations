INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/AzeuySdai40" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'PGL Major Krak\xc3\xb3w 2017'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Dosia'),
	(SELECT Id FROM Teams WHERE Alias = 'Gambit Esports'),
	'1',
	'1',
	'1',
	0,
	0,
	'{"he"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/yJifD2IEgx4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'Europe Minor Championship - Boston 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'BARBARR'),
	(SELECT Id FROM Teams WHERE Alias = 'Epsilon Esports'),
	'0',
	'1',
	'0',
	4,
	4,
	'{"ak"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/1NN1CjhH7rA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Katowice 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Friberg'),
	(SELECT Id FROM Teams WHERE Alias = 'Ninjas in Pyjamas'),
	'1',
	'1',
	'1',
	2,
	2,
	'{"ak"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'KRIMZ'),
	(SELECT Id FROM Teams WHERE Alias = 'Fnatic'),
	'1',
	'1',
	'1',
	3,
	3,
	'{"ak"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2015'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'NBK'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Envy'),
	'1',
	'1',
	'1',
	1,
	0,
	'{"knife"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/cjOVXdarUTs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'MLG Major Championship: Columbus 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Coldzera'),
	(SELECT Id FROM Teams WHERE Alias = 'Luminosity Gaming'),
	'0',
	'0',
	'1',
	4,
	0,
	'{"awp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/kUSN6u5CSRE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: Cologne 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'S1mple'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Liquid'),
	'0',
	'1',
	'1',
	2,
	2,
	'{"awp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/PO1G0bmWurc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: New York 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_dust2' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'S1mple'),
	(SELECT Id FROM Teams WHERE Alias = 'Natus Vincere'),
	'0',
	'1',
	'1',
	1,
	1,
	'{"awp","p250"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/qLVIgyrRk28" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL One: New York 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cbble' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Snax'),
	(SELECT Id FROM Teams WHERE Alias = 'Virtus.pro'),
	'1',
	'1',
	'1',
	4,
	4,
	'{"usp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/dmrIfz1TN00" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'MLG Major Championship: Columbus 2016'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Hiko'),
	(SELECT Id FROM Teams WHERE Alias = 'Team Liquid'),
	'0',
	'1',
	'1',
	4,
	4,
	'{"m4a4"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/4YyNMj7KrVs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ELEAGUE Major: Boston 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'GuardiaN'),
	(SELECT Id FROM Teams WHERE Alias = 'FaZe Clan'),
	'1',
	'1',
	'1',
	1,
	0,
	'{"awp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/jRWLI0W6PLk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'CEVO Season 7 Professional'),
	(SELECT Id FROM Maps WHERE Name = 'de_inferno' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'KennyS'),
	(SELECT Id FROM Teams WHERE Alias = 'Titan'),
	'0',
	'1',
	'0',
	5,
	0,
	'{"awp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/9WV1-AklbEQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'ESL Major Series One Katowice 2014'),
	(SELECT Id FROM Maps WHERE Name = 'de_mirage' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'Snax'),
	(SELECT Id FROM Teams WHERE Alias = 'Virtus.pro'),
	'1',
	'1',
	'1',
	3,
	0,
	'{"m4a1s"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/wHtSorLfAGA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'CEVO Season 7 Professional'),
	(SELECT Id FROM Maps WHERE Name = 'de_cache' AND CurrentBigVersion = '0'),
	(SELECT Id FROM Players WHERE Alias = 'Sgares'),
	(SELECT Id FROM Teams WHERE Alias = 'Cloud9'),
	'0',
	'1',
	'1',
	4,
	0,
	'{"awp"}'
);

INSERT INTO Clips VALUES(
	DEFAULT,
	'<iframe width="560" height="315" src="https://www.youtube.com/embed/XbKDbOhITSw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
	(SELECT Id FROM Events WHERE Name = 'FACEIT Major: London 2018'),
	(SELECT Id FROM Maps WHERE Name = 'de_overpass' AND CurrentBigVersion = '1'),
	(SELECT Id FROM Players WHERE Alias = 'TiziaN'),
	(SELECT Id FROM Teams WHERE Alias = 'BIG'),
	'0',
	'1',
	'0',
	4,
	0,
	'{"usp"}'
);