MATCH (n:Actor)-[a:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Director)
WHERE n.name = "Tom Hanks"
RETURN m.title, m.year, d.name;
