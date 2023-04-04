SELECT
  "account_id",
  AVG("wait_time") AS avg_wait_time,
  MAX("wait_time") AS max_wait_time,
  MIN("wait_time") AS min_wait_time,
  COUNT(*) AS total_interactions,
  APPROX_COUNT_DISTINCT_DS_THETA("team_id_sketch") AS approx_distinct_teams,
  APPROX_QUANTILE("wait_time", 0.5) AS median_wait_time
FROM "cs-analytics"
GROUP BY
  "account_id"