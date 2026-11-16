CREATE INDEX country_idx ON country (country);

EXPLAIN
SELECT
    *
FROM
    country
WHERE
    country = 'Switzerland';
