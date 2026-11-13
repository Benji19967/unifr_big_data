# Assignment 1

A. Create a new database.

Solution:
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

Solution:
```
dbmate new create_table
```