# clipd-backend
Backend scripts and extras for clipd

Below are some short tutorials for editing the backend of clipd

Steps to backup the clipd Heroku PostgreSQL DB and restore it locally:
Somewhat helpful reference: https://devcenter.heroku.com/articles/heroku-postgres-import-export

0. Ideally take site down for maintanence
1. open up a bash shell with the heroku command functioning locally
2. enter w/o quotes: "heroku pg:backups:capture -a clipd"
3. enter w/o quotes: "heroku pg:backups:download -a clipd"
4. Make sure you're in the directory of latest.dump. Store it somewhere if appropriate.
5. enter w/o quotes: "PGPASSWORD=rorodog pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d csgo_highlights latest.dump"
6. Start server if previously shut down for maintanence

Steps to restore an instance to the Heroku instance from local instance:

0. Ideally take site down for maintanence
1. open up a windows cmd window
2. in pgadmin, right click on DB and click Backup...
3. Don't change any settings except filename, to the form "csgo_highlights_backup_MM_DD_YY.backup"
4. Upload backup to AWS S3 Bucket
5. Right click on file, click Make Public
6. Make sure the S3 profile is public itself
7. Click on the item and copy the URL looking like "https://csgo-highlights-db.s3.us-east-2.amazonaws.com/name.backup"
8. enter w/o outer quotes in cmd: "pg:backups:restore "step7link" postgresql-convex-91631 -a clipd"
9. enter w/o quotes to check if running properly: "heroku pg -a clipd"
10. Start server if previously shut down for maintanence

Details for Reddit account:
email - robbie.a.freeman@gmail.com
username - clipd-official
password - 72ED865568032

Details for Twitch account:
email - robbie.a.freeman@gmail.com
username - clipdofficial
password - f;PB2p:kHG&L

Repo for downloading twitch clips:
https://github.com/ihabunek/twitch-dl

