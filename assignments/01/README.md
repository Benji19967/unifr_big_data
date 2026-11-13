# Assignment 1

A. Create a new database.

Solution:

Create the database
```
createdb unifr_big_data
```

B. Create the following tables: choose the right type for each field and justify the choice of
referential actions (cascade, restrict, update, set null, set default) for foreign keys.
```
Paper (paperID, title, abstract)
Author (authorID, name, email, affiliation)
Conference (confID, name, ranking)
Writes (authorID, paperID)
Submits (paperID, confID, isAccepted, date)
Cites (paperIDfrom, paperIDto)
```

Solution: in `db/migrations/...`

Create the tables:
```
DATABASE_URL=postgres://localhost/unifr_big_data?sslmode=disable dbmate --no-dump-schema up
```

C. Use your favorite programming language to connect to the database and populate it
with random data. Use a search engine to find PostgreSQL drivers or API for the
language you chose.
For python, you can use psycopg2 module:

Solution:
```
uv run assignments/01/main.py --seed 42
```