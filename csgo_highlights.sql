CREATE database csgo_highlights;

use csgo_highlights;

CREATE TABLE videos(
code VARCHAR(512) NOT NULL,
event VARCHAR(64) NULL,
map VARCHAR(32) NOT NULL,
casting FLOAT CHECK (casting >= 1.0 AND casting <= 5.0),
significance FLOAT CHECK (significance >= 1.0 AND significance <= 5.0),
intelligence FLOAT CHECK (intelligence >= 1.0 AND intelligence <= 5.0),
atmosphere FLOAT CHECK (atmosphere >= 1.0 AND atmosphere <= 5.0),
aim FLOAT CHECK (aim >= 1.0 AND aim <= 5.0),
luck FLOAT CHECK (luck >= 1.0 AND luck <= 5.0),
player VARCHAR(32) NOT NULL,
team VARCHAR(64) NULL,
grand_final ENUM(1,0) NOT NULL,
armor ENUM(1,0) NOT NULL,
crowd ENUM(1,0) NOT NULL,
kills INT CHECK (kills >= 0 AND kills <= 5),
clutch_kills INT CHECK (clutch_kills >= 0 AND clutch_kills <= 5),
-- ENUM('cz','desert_eagle','dual_berettas','five_seven','glock','p2000','p250','r8','tec9','usp','mag7','nova','sawed_off','xm','mac10','mp5','mp7','mp9','p90','pp_bizon','ump','ak','aug','famas','galil','m4a1s','m4a4','sg','awp','g3sg1','scar','ssg','m249','negev','knife','zeus','he','fire','flash','smoke')
weapons VARCHAR(32) NOT NULL
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/AzeuySdai40" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'PGL Major Krakow 2017',
'de_inferno',
3.0,
3.0,
5.0,
4.0,
1.0,
3.0,
'Dosia',
'Gambit Gaming',
1,
1,
1,
0,
0,
'he'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/yJifD2IEgx4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'PGL Regional Minor Championship Europe - ELEAGUE Major 2017',
'de_mirage',
3.0,
2.0,
3.0,
2.0,
4.0,
1.0,
'BARBARR',
'Epsilon',
0,
1,
0,
4,
4,
'ak'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/1NN1CjhH7rA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One Katowice 2015',
'de_inferno',
5.0,
3.0,
2.0,
5.0,
5.0,
1.5,
'friberg',
'Ninjas in Pyjamas',
1,
1,
1,
2,
2,
'ak'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One Cologne 2015',
'de_dust2',
4.5,
5.0,
2.5,
4.5,
5.0,
2.0,
'KRIMZ',
'Fnatic',
1,
1,
1,
3,
3,
'ak'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/W9Jbo4Dv7vc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One Cologne 2015',
'de_dust2',
5.0,
4.0,
3.5,
5.0,
1.0,
2.5,
'NBK',
'Team EnVyUs',
1,
1,
1,
1,
0,
'knife'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/cjOVXdarUTs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'MLG Major Championship: Columbus 2016',
'de_mirage',
5.0,
5.0,
2.0,
4.0,
2.0,
5.0,
'coldzera',
'Luminosity Gaming',
0,
0,
1,
4,
0,
'awp'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/kUSN6u5CSRE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One Cologne 2016',
'de_cache',
5.0,
5.0,
2.0,
5.0,
5.0,
5.0,
's1mple',
'Team Liquid',
0,
1,
1,
2,
2,
'awp'
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/PO1G0bmWurc" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One New York 2016',
'de_dust2',
4.0,
2.5,
3.0,
3.0,
3.0,
1.5,
's1mple',
'Natus Vincere',
0,
1,
1,
1,
1,
('awp,p250')
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/qLVIgyrRk28" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'ESL One New York 2016',
'de_cbble',
5.0,
4.0,
3.5,
5.0,
5.0,
1.5,
'Snax',
'Virtus.pro',
1,
1,
1,
4,
4,
('usp')
);

INSERT INTO videos VALUES(
'<iframe width="560" height="315" src="https://www.youtube.com/embed/dmrIfz1TN00" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
'MLG Major Championship: Columbus 2016',
'de_cache',
5.0,
4.0,
4.5,
5.0,
4.5,
1.0,
'Hiko',
'Team Liquid',
0,
1,
1,
4,
4,
('m4a4')
);
