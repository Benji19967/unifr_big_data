-- migrate:up

-- IDs: INTEGER GENERATED ALWAYS AS IDENTITY is the SQL-standard successor to SERIAL;
--      it blocks accidental manual inserts and 4 bytes (~2.1B rows) is plenty here.
-- Strings: in PostgreSQL TEXT and VARCHAR(n) perform identically, so a length limit
--      is only used where a real-world maximum exists (it then acts as a constraint).

create table if not exists Paper (
  paperID      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title        VARCHAR(300) NOT NULL,  -- titles are short but can be long-ish; cap catches garbage input
  abstract     TEXT NOT NULL           -- free-form prose of unpredictable length, no natural limit
);

create table if not exists Author (
  authorID     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name         VARCHAR(200) NOT NULL,         -- full names incl. multiple given/family names
  email        VARCHAR(254) NOT NULL UNIQUE,  -- 254 = max valid address length (RFC 5321); unique identifies a person
  affiliation  VARCHAR(300)                   -- institution name; nullable for independent researchers
);

create table if not exists Conference (
  confID       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name         VARCHAR(200) NOT NULL UNIQUE,  -- e.g. "VLDB"; unique avoids duplicate conferences
  ranking      VARCHAR(2)                     -- CORE rank (A*, A, B, C): tiny fixed set, so short string + CHECK
               CHECK (ranking IN ('A*', 'A', 'B', 'C'))
);

-- Link tables: FK columns are plain INTEGER to match the referenced identity columns
-- (they must not generate their own values like SERIAL would).

create table if not exists Writes (
  authorID     INTEGER NOT NULL
               REFERENCES Author (authorID) ON DELETE CASCADE,  -- authorship is meaningless without the author
  paperID      INTEGER NOT NULL
               REFERENCES Paper (paperID) ON DELETE CASCADE,    -- ...or without the paper
  PRIMARY KEY (authorID, paperID)  -- an author writes a given paper only once
);

create table if not exists Submits (
  paperID      INTEGER NOT NULL
               REFERENCES Paper (paperID) ON DELETE CASCADE,         -- submission dies with its paper
  confID       INTEGER NOT NULL
               REFERENCES Conference (confID) ON DELETE RESTRICT,    -- don't silently wipe submission history
  isAccepted   BOOLEAN,       -- yes/no decision; NULL = still under review
  date         DATE NOT NULL, -- calendar day only, time of day is irrelevant
  PRIMARY KEY (paperID, confID)
);

create table if not exists Cites (
  paperIDfrom  INTEGER NOT NULL
               REFERENCES Paper (paperID) ON DELETE CASCADE,  -- a citation needs both endpoints to exist
  paperIDto    INTEGER NOT NULL
               REFERENCES Paper (paperID) ON DELETE CASCADE,
  PRIMARY KEY (paperIDfrom, paperIDto),
  CHECK (paperIDfrom <> paperIDto)  -- a paper cannot cite itself
);

-- migrate:down

drop table if exists Cites;
drop table if exists Submits;
drop table if exists Writes;
drop table if exists Conference;
drop table if exists Author;
drop table if exists Paper;
