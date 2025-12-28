--List Extract Refresh Schedules

SELECT 
    s.id AS schedule_id,
    s.name AS schedule_name,
    s.schedule_type,
    s.priority,
    s.next_run_at,
    s.created_at,
    s.updated_at
FROM schedules s
WHERE s.schedule_type = 'Extract'
ORDER BY s.next_run_at;

--Workbooks with Extract Refresh Schedules
SELECT 
    w.name AS workbook_name,
    ds.name AS datasource_name,
    sch.name AS schedule_name,
    sch.next_run_at,
    sch.priority
FROM workbooks w
JOIN workbook_datasources wds ON w.id = wds.workbook_id
JOIN datasources ds ON wds.datasource_id = ds.id
JOIN background_jobs bj ON ds.id = bj.datasource_id
JOIN schedules sch ON bj.schedule_id = sch.id
ORDER BY sch.next_run_at;

--Last Extract Refresh Status
SELECT 
    ds.name AS datasource_name,
    w.name AS workbook_name,
    bj.completed_at,
    bj.status,
    bj.notes
FROM background_jobs bj
JOIN datasources ds ON bj.datasource_id = ds.id
JOIN workbook_datasources wds ON ds.id = wds.datasource_id
JOIN workbooks w ON wds.workbook_id = w.id
WHERE bj.job_type = 'RefreshExtracts'
ORDER BY bj.completed_at DESC;


--Failed Extract Refreshes (Audit)

SELECT 
    ds.name AS datasource_name,
    w.name AS workbook_name,
    bj.completed_at,
    bj.status,
    bj.notes
FROM background_jobs bj
JOIN datasources ds ON bj.datasource_id = ds.id
JOIN workbook_datasources wds ON ds.id = wds.datasource_id
JOIN workbooks w ON wds.workbook_id = w.id
WHERE bj.job_type = 'RefreshExtracts'
  AND bj.status = 'Failed'
ORDER BY bj.completed_at DESC;

--Datasource Extracts with Last Refresh
SELECT 
    ds.name AS datasource_name,
    u.name AS owner_name,
    MAX(bj.completed_at) AS last_refresh,
    MIN(bj.completed_at) AS first_refresh
FROM datasources ds
JOIN users u ON ds.owner_id = u.id
JOIN background_jobs bj ON ds.id = bj.datasource_id
WHERE bj.job_type = 'RefreshExtracts'
GROUP BY ds.name, u.name
ORDER BY last_refresh DESC;

#Consolidated query/view that ties together workbooks, datasources, schedules, and refresh jobs

SELECT 
    w.id AS workbook_id,
    w.name AS workbook_name,
    wu.name AS workbook_owner,
    p.name AS project_name,
    s.name AS site_name,

    ds.id AS datasource_id,
    ds.name AS datasource_name,
    du.name AS datasource_owner,

    sch.id AS schedule_id,
    sch.name AS schedule_name,
    sch.schedule_type,
    sch.next_run_at,

    bj.id AS job_id,
    bj.job_type,
    bj.status AS last_refresh_status,
    bj.completed_at AS last_refresh_time,
    bj.notes AS refresh_notes

FROM workbooks w
JOIN users wu ON w.owner_id = wu.id
JOIN projects p ON w.project_id = p.id
JOIN sites s ON w.site_id = s.id

JOIN workbook_datasources wds ON w.id = wds.workbook_id
JOIN datasources ds ON wds.datasource_id = ds.id
JOIN users du ON ds.owner_id = du.id

LEFT JOIN background_jobs bj ON ds.id = bj.datasource_id
LEFT JOIN schedules sch ON bj.schedule_id = sch.id

WHERE bj.job_type = 'RefreshExtracts'
ORDER BY w.name, ds.name, bj.completed_at DESC;
