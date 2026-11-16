-- Part C
EXPLAIN
SELECT
    COUNT(*)
FROM
    payment
    NATURAL JOIN staff
WHERE
    staff.first_name = 'Mike';

