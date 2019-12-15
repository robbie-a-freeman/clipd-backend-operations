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

f = open("insertEventsIntoDB.pgsql", "w")
# events: need Name, Organizer, Location, Prize Pool, Start Date, End Date
links = ['https://liquipedia.net/counterstrike/S-Tier_Tournaments',\
         'https://liquipedia.net/counterstrike/A-Tier_Tournaments',\
         'https://liquipedia.net/counterstrike/B-Tier_Tournaments',\
         'https://liquipedia.net/counterstrike/C-Tier_Tournaments',\
         'https://liquipedia.net/counterstrike/Qualifier_Tournaments']
# scrape organizers from db
import psycopg2
conn = psycopg2.connect('dbname=csgo_highlights user=postgres password=rorodog', sslmode='disable')
cur = conn.cursor()
cur.execute("SELECT Id, Name FROM organizers")
organizers = cur.fetchall()
cur.close()
conn.close()
events = []
for l in links:
    print("link processing")
    page_link = l
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    myEventYears = page_content.find_all("div", {"class": "divTable table-full-width tournament-card"})
    for y in myEventYears:
        eventsInAYear = y.find_all("div", {"class": "divRow"})
        for e in eventsInAYear:
            d = e.select("div[class*='divCell Tournament']")[0]
            b = d.find("b")
            a = b.find("a")
            name = a.text

            organizer = 'NULL'
            for o in organizers:
                if o[1] in name:
                    organizer = o[0]
                    break

            location = 'NULL'
            d = e.select("div[class*='divCell EventDetails Location']")[0]
            if d is not None:
                s = d.findChildren("span")
                if s[1].text is not 'TBA' and s[1].text is not 'TBD':
                    location = s[1].text

            prize = 'NULL'
            d = e.select("div[class*='divCell EventDetails Prize']")[0]
            if d is not None and d.text.strip() is not '':
                prize = d.text.strip()

            d = e.select("div[class*='divCell EventDetails Date']")[0]
            # how many months are there listed?
            if d is not None and d.text is not '':
                firstM = "-1"
                firstMIndex = -1
                secondM = "-1"
                secondMIndex = -1
                dates = d.text
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                # get the months
                for i, m in enumerate(months):
                    if m in dates:
                        if firstM is "-1":
                            firstMIndex = dates.index(m)
                            firstM = str(i + 1)
                        elif secondM is "-1":
                            secondMIndex = dates.index(m)
                            secondM = str(i + 1)
                        else:
                            print("3 or more months listed in date!!!")
                # enforce first month
                if firstMIndex > secondMIndex and secondMIndex is not -1:
                    tempM = firstM
                    tempMIndex = firstMIndex
                    firstM = secondM
                    firstMIndex = secondMIndex
                    secondM = tempM
                    secondMIndex = tempMIndex
                # get the year: assume event starts and ends in the same year
                import re
                regex = re.compile("[0-9][0-9][0-9][0-9]")
                year = regex.search(dates).group(0)
                # get the days 
                regex = re.compile("[0-9]+( - )([a-zA-Z]+\s)*[0-9]+")
                result = regex.search(dates)
                if result is not None:
                    days = result.group(0)
                    firstDay = days.split("-")[0][:-1]
                    if len(firstDay) is 1: # 1-9
                        firstDay = ''.join(["0", firstDay])
                    secondDay = days.split('-')[1]
                    regex = re.compile("[0-9]+")
                    secondDay = regex.search(secondDay).group(0)
                    if len(secondDay) is 1: # 1-9
                        secondDay = ''.join(['0', secondDay])
                else:
                    firstDay = "none"
                    secondDay = "found"
                # combine the date pieces, yyyy-mm-dd (postgres format)
                start = '-'.join([year, firstM, firstDay])
                if secondM is '-1':
                    secondM = firstM
                end = '-'.join([year, secondM, secondDay])
                regex = re.compile("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
                if not regex.match(start):
                    start = 'NULL'
                if not regex.match(end):
                    end = 'NULL'
            else:
                start = 'NULL'
                end = 'NULL'

            result = (name, organizer, location, prize, start, end)
            if result not in events: 
                events.append(result)
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