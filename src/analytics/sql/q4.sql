SELECT
  "account_id",
  MAX("wait_time") AS "max_wait_time",
  MIN("wait_time") AS "min_wait_time",
  SUM("wait_time") AS "total_wait_time",
  AVG("wait_time") AS "average_wait_time",
  COUNT(*) AS "record_count",
  APPROX_COUNT_DISTINCT_DS_THETA("team_id_sketch") AS "distinct_teams"
FROM "cs-analytics"
GROUP BY 1