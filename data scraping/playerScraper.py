# script to scrape Players from Liquipedia
# output is a postgres script to insert entries into preexisting tables
import bs4
from bs4 import BeautifulSoup
import requests

# players: Need Alias, Name, Country, IsActive
f = open("scraped commands/insertPlayersIntoDB.pgsql", "w")
links = ['https://liquipedia.net/counterstrike/Portal:Players/Europe',\
         'https://liquipedia.net/counterstrike/Portal:Players/CIS',\
         'https://liquipedia.net/counterstrike/Portal:Players/Americas',\
         'https://liquipedia.net/counterstrike/Portal:Players/Oceania',\
         'https://liquipedia.net/counterstrike/Portal:Players/Eastern_%26_Southern_Asia',\
         'https://liquipedia.net/counterstrike/Portal:Players/Africa_%26_Middle_East']

players = []
for l in links:
    page_link = l
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    myPlayerTables = page_content.find_all("table", {"class": "wikitable collapsible collapsed"})
    for t in myPlayerTables:
        regionalPlayerList = t.find_all("tr")
        for p in regionalPlayerList:
            if p.find("th") == None:
                row = p.find("td")
                elems = row.findAll("a")
                alias = ''
                name = ''
                isActive = ''
                country = ''
                e = elems[0] # get the right element
                country = e['title']
                e = elems[1]
                alias = e['title']
                name = e.next_element.next_element.split('-')[1].strip()
                print(name)
                isActive = '1' # no real way to tell if active
                result = (alias,name,country,isActive)
                if result not in players:
                    players.append(result)
# form the commands and output them
playerInsertCommands = ""
for p in players:
    alias = p[0].replace("\'", "\'\'") # Alias can't be null
    name = p[1].replace("\'", "\'\'") # Name can't be null
    country = p[2]
    if country is '':
        country = 'NULL'
    else:
        country = ''.join(['\'', p[2].replace("\'", "\'\'"),'\''])
    playerInsertCommands = ''.join([playerInsertCommands, "INSERT INTO Players VALUES(DEFAULT,\'", alias, "\',\'", name,"\',", country, ",NULL,\'", p[3], "\');"])
playerInsertCommands = str(playerInsertCommands.encode('utf8'))[2:-1]
f.write(playerInsertCommands)
f.close()