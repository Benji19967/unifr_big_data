-- migrate:up
create table if not exists Paper (
  paperID         SERIAL,
  title           VARCHAR(100) NOT NULL, 
  abstract        VARCHAR(500) NOT NULL,
);
create table if not exists Author (
  authorID         SERIAL,
  name             VARCHAR(100) NOT NULL, 
  email            VARCHAR(500) NOT NULL,
  affiliation      VARCHAR(500) NOT NULL,
);
create table if not exists Conference (
  confID         SERIAL,
  name           VARCHAR(100) NOT NULL, 
  ranking        VARCHAR(500) NOT NULL,
);
create table if not exists Writes (
  authorID          SERIAL,
  paperID           VARCHAR(100) NOT NULL, 
);
create table if not exists Submits (
  paperID           SERIAL,
  confID            VARCHAR(100) NOT NULL, 
  isAccepted        VARCHAR(500) NOT NULL,
  date              VARCHAR(500) NOT NULL,
);
create table if not exists Cites (
  paperIDfrom         SERIAL,
  paperIDto           VARCHAR(100) NOT NULL, 
);

-- migrate:down

