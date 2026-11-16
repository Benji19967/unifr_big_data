CREATE INDEX customer_idx ON rental (customer_id);

EXPLAIN
SELECT
    *
FROM
    rental
WHERE
    customer_id = 459;
