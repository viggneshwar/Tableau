--List All Subscriptions

SELECT 
    sub.id AS subscription_id,
    sub.subject AS subscription_name,
    u.name AS subscriber_name,
    u.email AS subscriber_email,
    v.name AS view_name,
    w.name AS workbook_name,
    sch.name AS schedule_name,
    sch.next_run_at
FROM subscriptions sub
JOIN users u ON sub.user_id = u.id
JOIN views v ON sub.view_id = v.id
JOIN workbooks w ON v.workbook_id = w.id
JOIN schedules sch ON sub.schedule_id = sch.id
ORDER BY sub.subject;

--Subscriptions by User
SELECT 
    u.name AS subscriber_name,
    COUNT(sub.id) AS subscription_count
FROM subscriptions sub
JOIN users u ON sub.user_id = u.id
GROUP BY u.name
ORDER BY subscription_count DESC;


--Subscriptions by Workbook

SELECT 
    w.name AS workbook_name,
    COUNT(sub.id) AS subscription_count
FROM subscriptions sub
JOIN views v ON sub.view_id = v.id
JOIN workbooks w ON v.workbook_id = w.id
GROUP BY w.name
ORDER BY subscription_count DESC;

Subscriptions by Schedule
SELECT 
    sch.name AS schedule_name,
    COUNT(sub.id) AS subscription_count
FROM subscriptions sub
JOIN schedules sch ON sub.schedule_id = sch.id
GROUP BY sch.name
ORDER BY subscription_count DESC;




--Subscriptions by Schedule

SELECT 
    sch.name AS schedule_name,
    COUNT(sub.id) AS subscription_count
FROM subscriptions sub
JOIN schedules sch ON sub.schedule_id = sch.id
GROUP BY sch.name
ORDER BY subscription_count DESC;

--Failed Subscription Deliveries (Audit)
SELECT 
    sub.subject AS subscription_name,
    u.name AS subscriber_name,
    bj.completed_at,
    bj.status,
    bj.notes
FROM background_jobs bj
JOIN subscriptions sub ON bj.subscription_id = sub.id
JOIN users u ON sub.user_id = u.id
WHERE bj.job_type = 'SubscriptionNotify'
  AND bj.status = 'Failed'
ORDER BY bj.completed_at DESC;

--Consolidated Query: Workbooks + Datasources + Refresh + Subscriptions

SELECT 
    -- Workbook details
    w.id AS workbook_id,
    w.name AS workbook_name,
    wu.name AS workbook_owner,
    p.name AS project_name,
    s.name AS site_name,

    -- Datasource details
    ds.id AS datasource_id,
    ds.name AS datasource_name,
    du.name AS datasource_owner,

    -- Refresh schedule details
    sch.id AS schedule_id,
    sch.name AS schedule_name,
    sch.schedule_type,
    sch.next_run_at,

    -- Refresh job details
    bj.id AS job_id,
    bj.job_type,
    bj.status AS last_refresh_status,
    bj.completed_at AS last_refresh_time,
    bj.notes AS refresh_notes,

    -- Subscription details
    sub.id AS subscription_id,
    sub.subject AS subscription_name,
    su.name AS subscriber_name,
    su.email AS subscriber_email

FROM workbooks w
JOIN users wu ON w.owner_id = wu.id
JOIN projects p ON w.project_id = p.id
JOIN sites s ON w.site_id = s.id

JOIN workbook_datasources wds ON w.id = wds.workbook_id
JOIN datasources ds ON wds.datasource_id = ds.id
JOIN users du ON ds.owner_id = du.id

LEFT JOIN background_jobs bj ON ds.id = bj.datasource_id
LEFT JOIN schedules sch ON bj.schedule_id = sch.id

LEFT JOIN subscriptions sub ON w.id = sub.workbook_id
LEFT JOIN users su ON sub.user_id = su.id

WHERE (bj.job_type = 'RefreshExtracts' OR bj.job_type = 'SubscriptionNotify')
ORDER BY w.name, ds.name, bj.completed_at DESC;
