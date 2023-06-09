SELECT
  "account_id",
  MAX("wait_time") AS "max_wait_time",
  MIN("wait_time") AS "min_wait_time",
  AVG("wait_time") AS "average_wait_time",
  COUNT(*) AS "record_count"
FROM "cs-analytics"
GROUP BY "account_id"
ORDER BY 2 DESC