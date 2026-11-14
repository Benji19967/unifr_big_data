CREATE VIEW PublishesIn AS
SELECT
    writes.authorid,
    submits.confid
FROM
    submits
    INNER JOIN writes ON submits.paperid = writes.paperid
WHERE
    isaccepted = TRUE;
