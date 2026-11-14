SELECT
    ranking,
    COUNT(*) AS count
FROM
    conference
GROUP BY
    ranking
ORDER BY
    count DESC;

