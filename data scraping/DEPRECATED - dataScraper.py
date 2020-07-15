# script to scrape Teams, Players, and Events from Liquipedia
# output is a postgres script to insert entries into preexisting tables
# TODO grab more information ie active/not active, logo, etc.
import bs4
from bs4 import BeautifulSoup
import requests

f = open("insertTeamsIntoDB.pgsql", "w")
# teams: need Name, IsActive (1 default)
page_link = 'https://liquipedia.net/counterstrike/Portal:Teams'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
teams = []
# get active teams
header = page_content.find("span", {"id": "Notable_Active_Counter-Strike_Teams"})
wrapper = header.parent.next_sibling.next_sibling
myActiveTitleWrappers = wrapper.find_all("span", {"class": "team-template-text"}, recursive=True)
for i in myActiveTitleWrappers:
    child = i.find("a", recursive=False)
    teamName = child.text
    teams.append((teamName, 1))
# get inactive teams
header = page_content.find("span", {"id": "Notable_Disbanded_Counter-Strike_Teams"})
wrapper = header.parent.next_sibling.next_sibling
myInactiveTitleWrappers = wrapper.find_all("span", {"class": "team-template-text"}, recursive=True)
for i in myInactiveTitleWrappers:
    child = i.find("a", recursive=False)
    teamName = child.text
    teams.append((teamName, 0))
# write the commands to file
teamInsertCommands = ""
for t in teams:
    name = t[0].replace('\'', '\'\'')
    teamInsertCommands = ''.join([teamInsertCommands, "INSERT INTO Teams VALUES(DEFAULT,\'", name, "\',NULL,\'", str(t[1]), "\');"])
teamInsertCommands = str(teamInsertCommands.encode('utf8'))[2:-1]
f.write(teamInsertCommands)
f.close()


# write the commands to file
eventInsertCommands = ""
for e in events:
    name = e[0].replace("\'", "\'\'") # Name can't be null
    if e[2] is not 'NULL':
        location = ''.join(['\'',e[2].replace("\'", "\'\'"),'\'']) 
    else:
        location = 'NULL'
    if e[4] is 'NULL':
        start = e[4]
    else:
        start = ''.join(['\'',e[4].replace("\'", "\'\'"),'\''])
    if e[5] is 'NULL':
        end = e[5]
    else:
        end = ''.join(['\'',e[5].replace("\'", "\'\'"),'\''])
    eventInsertCommands = ''.join([eventInsertCommands, "INSERT INTO Events VALUES(DEFAULT,\'", name, "\',", str(e[1]),",", location, ",\'", e[3], "\',", start, ",",  end, ");"])
eventInsertCommands = str(eventInsertCommands.encode('utf8'))[2:-1]
f.write(eventInsertCommands)
f.close()

# players: Need Alias, Name, Country, IsActive
f = open("insertPlayersIntoDB.pgsql", "w")
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