MATCH ()-[r:RATED]->(m:Movie)<-[:DIRECTED]-(d:Director)
WHERE d.name = "James Cameron" AND m.title = "Titanic"
RETURN AVG(r.rating);
