MATCH
  (a:Actor)-[:ACTED_IN]->
  (m1:Movie)<-[:ACTED_IN]-
  (b:Actor)-[:ACTED_IN]->
  (m2:Movie)<-[:ACTED_IN]-
  (c:Actor)
WHERE a.name = "Tom Hanks" AND c.name = "Tom Cruise"
RETURN b.name, m1.title, m2.title;
