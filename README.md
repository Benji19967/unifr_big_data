# Big Data at Uni Fribourg

Repo for resources for course Big Data Infrastructures at the University of Fribourg


## Docker Compose

- Launch a `postgres` DB instance and `pgadmin` in containers, see: `docker-compose.yaml`.

### PgAdmin

Open on `localhost:5050`

In `General` tab:

- Name: Tutorial Server (random name for server)

In `Connection` tab:
- Host name/adress: (in this example we run postgres in a docker container)
  - If docker container: `postgres` (name of container, defined in `docker-compose.yaml`) 
  - If server: `<IP address>`
  - If local: `localhost`
- Port: `5432`
- Maintenance database: `dvdrental`
- Username: `postgres`
- Password: `postgres`

==> Starts a connection with `Tutorial Server`.

## PSQL

```
createdb dvdrental
cd data/dvdrental
psql -d dvdrental < restore.sql
```

## [dbmate](https://github.com/amacneil/dbmate) -- DB migration tool

```
dbmate --help         # print usage help
dbmate new            # generate a new migration file
dbmate up             # create the database (if it does not already exist) and run any pending migrations
dbmate create         # create the database
dbmate drop           # drop the database
dbmate migrate        # run any pending migrations
dbmate rollback       # roll back the most recent migration
dbmate down           # alias for rollback
dbmate status         # show the status of all migrations (supports --exit-code and --quiet)
dbmate dump           # write the database schema.sql file
dbmate dump -- [...]  # optionally pass additional arguments directly to mysqldump or pg_dump
dbmate load           # load schema.sql file to the database
dbmate wait           # wait for the database server to become available
```
