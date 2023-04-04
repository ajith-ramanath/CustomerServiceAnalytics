SELECT 
  COUNT(*) as all_rows, 
  COUNT(DISTINCT "account_id") as distinct_acc_ids, 
  COUNT(DISTINCT "site_id") as distinct_site_ids, 
  COUNT(DISTINCT "queue_id") as distinct_queue_ids,
  APPROX_COUNT_DISTINCT_DS_THETA("team_id_sketch") AS "distinct_teams"
FROM "cs-analytics"