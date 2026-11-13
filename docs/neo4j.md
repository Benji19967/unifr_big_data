# neo4j

## Installation

https://neo4j.com/docs/operations-manual/current/installation/osx/

```
brew install neo4j
```

```
brew services start neo4j
```

## Query examples

```
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre {name:'Comedy'}) WHERE m.imdbRating IS NOT NULL RETURN m.title, m.imdbRating ORDER BY m.imdbRating DESC LIMIT 3;
```
