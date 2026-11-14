SELECT
    *
FROM
    cites
    INNER JOIN writes ON cites.paperidfrom = writes.paperid
    INNER JOIN writes AS writes2 ON cites.paperidto = writes2.paperid
WHERE
    writes.authorid = writes2.authorid
