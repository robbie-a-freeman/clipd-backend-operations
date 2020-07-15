# script to scrape Teams from Liquipedia
# output is a postgres script to insert entries into preexisting tables
# TODO grab more information ie active/not active, logo, etc.
import bs4
from bs4 import BeautifulSoup
import requests

f = open("scraped commands/insertTeamsIntoDB.pgsql", "w")
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