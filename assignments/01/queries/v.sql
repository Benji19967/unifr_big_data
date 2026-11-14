SELECT
    title
FROM
    paper
    INNER JOIN writes ON paper.paperid = writes.paperid
    INNER JOIN author ON writes.authorid = author.authorid
WHERE
    paper.paperid IN (
        SELECT
            paper.paperid
        FROM
            paper
            INNER JOIN writes ON paper.paperid = writes.paperid
            INNER JOIN author ON writes.authorid = author.authorid
        WHERE
            author.name LIKE 'Victor%')
GROUP BY
    paper.paperid
HAVING
    COUNT(author.name) > 1
