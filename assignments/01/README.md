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

D. With reference to the schema just introduced, write SQL code to complete the following
tasks. Don’t use the CONTAINS operator, avoid returning duplicate results, try to use the
DISTINCT clause only when you really need it, and try to use aggregate operators only
when they are really needed.

- i. Select the number of conference belonging to each ranking.
  - `psql -d unifr_big_data < assignments/01/queries/i.sql` 
- ii. Select all the abstracts of the papers written (or co-written) by the author whose
name is ‘Alex’ or ‘Alexander’.
- iii. Select the names of all the authors that cited themselves.
- iv. Create a view PublishesIn(authorID, confID) containing all the pairs (authorID,
confID) such that there is at least one publication by authorID accepted at confID.
- v. Select the title of all the papers co-authored by the author ‘Alex’ (the papers where
‘Alex’ is the only author should not be part of the result).
