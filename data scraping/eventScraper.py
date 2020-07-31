# script to scrape Events from Liquipedia
# output is a postgres script to insert entries into preexisting tables
# TODO grab more information ie active/not active, logo, etc.
import bs4
from bs4 import BeautifulSoup
import requests


# takes a page_content obj and fills out the page
""" go into each event link and scrape more detailed information on:
    - Lineups
    - Matches
    - Events
    - Event Stages
"""
def process_event_page(page_content):

    # Lineups
    # id=Participants, then parent element (h2), then go two elements down, then make list of the following divs
    lineups = []
    lineupTeams = []
    lineupLists = page_content.find(id = "Participants").parent.next_sibling.next_sibling.next_sibling.next_sibling.find_all("div", {"class" : "teamcard"})
    # in each div -> center -> b -> a.innerHTML
    for li in lineupLists:
        # for each div, find the only tbody, take its tds, for each td, take its a.innerHTML
        players = [""] * 6
        lineupLinks = li.findChildren("a", recursive=True)
        i = 2
        for p in range(len(players) - 1):
            players[p] = lineupLinks[i].contents[0]
            i = i + 2
        if len(lineupLinks) >= 13 and lineupLinks[12].contents[0] is not "":
            players[5] = lineupLinks[12].contents[0]
        lineups.append(players)
        lineupTeams.append(lineupLinks[0].contents[0])
    print("Lineups: ")
    for li in range(len(lineups)):
        print(lineups[li])
        print(lineupTeams[li])

    # Matches
    

def main():
    event_page_response = requests.get("https://liquipedia.net/counterstrike/Cs_summit/6/Europe", timeout=5)
    event_page_content = BeautifulSoup(event_page_response.content, "html.parser")
    process_event_page(event_page_content)

if __name__ == '__main__':
    main()



'''
f = open("scraped commands/insertEventsIntoDB.pgsql", "w")
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
            print(d.text)
            if d is not None and d.text is not '' and 'Tournament Delayed' not in d.text:
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

    for e in page_content.find_all("div", {"class": "divCell Tournament Header"}):
        partial_link = e.find_all("a")[-1]["href"]
        print(partial_link )
        event_page_link = "https://www.liquipedia.net" + partial_link
        event_page_response = requests.get(event_page_link, timeout=5)
        event_page_content = BeautifulSoup(event_page_response.content, "html.parser")
        process_event_page(event_page_content)
''' '''
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
f.close()'''