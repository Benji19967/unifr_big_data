SELECT
    LEFT (paper.abstract,
        50),
    author.authorid,
    writes.paperid,
    author.name
FROM
    author
    INNER JOIN writes ON author.authorid = writes.authorid
    INNER JOIN paper ON paper.paperid = writes.paperid
WHERE
    author.name LIKE 'Victor%';

