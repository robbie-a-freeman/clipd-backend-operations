# Script that generates Dummy entry Insert commands in postgres.
# Output found in insertDummyEntriesIntoDB.pgsql.
# Dummy data in DB:
# 1000 clips
# 1000 Users
# Each User rates each Category in each Clip (clustered randomness)
# 1000 + 1000 + 1000*6*1000 =~ 6,002,000 <- worst case
# 1000 + 1000 + 1000*6*100 =~ 602,000 <- far more likely case
import numpy as np
NUMBER_OF_CLIPS = 1000
NUMBER_OF_USERS = 1000
FILENAME = "insertDummyEntriesIntoDB.pgsql"
f = open(FILENAME, "w")

# 1. Generate and insert Clips individually

# Cluster some clips with events
import psycopg2
conn = psycopg2.connect('dbname=csgo_highlights user=postgres password=rorodog', sslmode='disable')
cur = conn.cursor()
cur.execute("SELECT Id FROM events WHERE Organizer IS NOT NULL")
events = cur.fetchall()
cur.execute("SELECT Id FROM maps")
maps = cur.fetchall()
cur.execute("SELECT Id FROM weapons")
weapons = cur.fetchall()
cur.execute("SELECT Id FROM players")
players = cur.fetchall()
cur.execute("SELECT Id FROM teams")
teams = cur.fetchall()
cur.execute("SELECT * FROM Users")
users = cur.fetchall()
cur.close()
conn.close()

import sys
sys.path.insert(0, '../clipd/srv')
from database import DB
db = DB('dbname=csgo_highlights user=postgres password=rorodog', 'disable')
cats = db.getCategories()

import random as rd
estimatedRatings = []
newUserIds = []
'''
for i in range(NUMBER_OF_CLIPS):
    code = 'ScMzIvxBSi4'
    t = rd.betavariate(10.0, 4.0)
    eventId = events[int(t * float(len(events)))][0]
    mapId = maps[int(np.random.sample() * float(len(maps)))][0]
    playerId = players[int(rd.betavariate(10.0, 4.0) * float(len(players)))][0]
    teamId = teams[int(rd.betavariate(10.0, 4.0) * float(len(teams)))][0]
    grandFinal = '0'
    if np.random.sample() > 0.97:
        grandFinal = '1'
    armor = '0'
    if np.random.sample() > 0.1:
        armor = '1'
    crowd = '0'
    if np.random.sample() > 0.4:
        crowd = '1'
    kills = int(np.random.sample() * 6.0)
    clutchKills = 0
    if np.random.sample() > 0.5:
        clutchKills = int(np.random.sample() * kills)
    weaponId = str(weapons[int(np.random.sample() * float(len(weapons)))][0])
    if np.random.sample() > 0.9:
        weaponId = weaponId + ',' + str(weapons[int(np.random.sample() * float(len(weapons)))][0])
    insertClipCommand = ''.join(["INSERT INTO Clips VALUES(DEFAULT,\'",\
                                code, "\',", str(eventId),",", str(mapId),\
                                ",", str(playerId), ",", str(teamId), ",\'", grandFinal,\
                                "\',\'", armor, "\',\'", crowd, "\',", str(kills), ",",\
                                str(clutchKills), ",ARRAY[", str(weaponId), "]);"])
    f.write(insertClipCommand)
    f.write('\n')

print('clip commands written')

# 3. Generate and insert Users individually, and their activeness factor
names = []
for i in range(NUMBER_OF_USERS):
    name = 'dummy_' + str(i)
    email = 'dummy_' + str(i) + '@dummy.com'
    pw = '$2a$06$LaIHXEH76zjFzNdnmJVFT.VcT7VHpXIxxEztEaQB5qDhFhje7y9p6'
    weaponId = str(weapons[int(np.random.sample() * float(len(weapons)))][0])
    insertUserCommand = ''.join(["INSERT INTO Users VALUES(DEFAULT,\'",\
                                name, "\',\'", email,"\',\'", pw,\
                                "\', DEFAULT, NULL,", weaponId, ");"])
    f.write(insertUserCommand)
    f.write('\n')
    names.append(name)
print('user commands written')
# 5. Close the file
f.close()

conn = psycopg2.connect('dbname=csgo_highlights user=postgres password=rorodog', sslmode='disable')
cur = conn.cursor()
with open(FILENAME) as f:
    for line in f:
        cur.execute(line)
conn.commit()
cur.close()
conn.close()
print('clip and user commands committed')
'''
userActivenessRatings = []
for i in range(NUMBER_OF_USERS):
    userActivenessRatings.append(np.random.sample())
    newId = users[
    newUserIds.append(newId)

for i in range(NUMBER_OF_CLIPS):
    # generate reception
    estimatedRatings.append([np.random.sample() * 5.0, np.random.sample() * 5.0, np.random.sample() * 5.0,\
                             np.random.sample() * 5.0, np.random.sample() * 5.0, np.random.sample() * 5.0])

conn = psycopg2.connect('dbname=csgo_highlights user=postgres password=rorodog', sslmode='disable')
cur = conn.cursor()
cur.execute("SELECT Id FROM clips")
clipIds = cur.fetchall()
cur.close()
conn.close()

print('fetched ids')

# AFTER ABOVE OPS ARE COMMITTED
# 4. For each User:
#   a. Add a rating for some videos for some categories from clustered randomness
#   b. Based on Clip (clustered) popularity and User activeness

for i in range(NUMBER_OF_USERS):
    activeness = userActivenessRatings[i]
    baseClipNumber = NUMBER_OF_CLIPS / 10
    if activeness < 0.5:
        baseClipNumber = baseClipNumber / 5 # half of users aren't power users
    if activeness < 0.9:
        baseClipNumber = baseClipNumber / 5 # most users aren't obssessors
    userId = newUserIds[i][0]
    print('user: ', i)
    for j in range(1 + int(activeness * float(baseClipNumber))): # for each clip to review
        clipId = clipIds[int(rd.betavariate(10.0, 4.0) * float(len(clipIds)))][0] # cluster a bit for popularity
        print('clip: ', j, 'out of', 1 + int(activeness * float(baseClipNumber)))
        for k in range(1 + int(activeness * float(len(cats)))): # for up to each category
            categoryId = cats[int(np.random.sample() * float(len(cats)))][0]
            rating = estimatedRatings[j][k] + 3 * np.random.sample() - 1.5
            if rating < 0.0:
                rating = 0.0
            elif rating > 5.0:
                rating = 5.0
            db.updateRating(clipId, userId, categoryId, rating)