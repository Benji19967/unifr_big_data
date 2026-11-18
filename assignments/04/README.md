# Neo4j


Start server in console
```
neo4j console
```

In browser:

```
http://localhost:7474
```
| Protocol  | Connection URL |
| :-------- | :------------- |
| bolt://   | localhost:7687 |

- Database user: neo4j
- Password: w...

## Load data

```
neo4j-admin database import full neo4j \
--nodes=data/movies_actors_roles/movies.csv \
--nodes=data/movies_actors_roles/actors.csv \
--relationships=data/movies_actors_roles/roles.csv --overwrite-destination
```

```
IMPORT DONE in 559ms.
Imported:
  6 nodes
  9 relationships
  24 properties
Peak memory usage: 68.47MiB
```

## Commands

Count the number of nodes:
```cypher
MATCH (n)
RETURN count(n) as nodes;
```

List all nodes:
```cypher
MATCH (n)
RETURN n as nodes;
```

Get the names of all actors:
```cypher
MATCH (n:Actor)
RETURN n.name as nodes;
```
