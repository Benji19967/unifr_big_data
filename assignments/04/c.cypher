MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(b:Actor)
WHERE a.name = "Tom Hanks"
RETURN b.name, m.title;
